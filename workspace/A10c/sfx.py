# Copyright (C) 2006-2013  Music Technology Group - Universitat Pompeu Fabra
#
# This file is part of Essentia
#
# Essentia is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation (FSF), either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the Affero GNU General Public License
# version 3 along with this program. If not, see http://www.gnu.org/licenses/

import essentia.standard as ess
import essentia as es
import numpy as np
import sys
from essentia import EssentiaError, INFO
from essentia.progress import Progress

namespace = 'sfx'
dependencies = ['lowlevel', 'onsetdetection']


def compute(audio, pool, options):
    INFO('Computing SFX descriptors...')

    # analysis parameters
    sampleRate = options['sampleRate']
    frameSize = options['frameSize']
    hopSize = options['hopSize']
    windowType = options['windowType']

    # frame algorithms
    frames = ess.FrameGenerator(audio=audio, frameSize=frameSize, hopSize=hopSize)
    window = ess.Windowing(size=frameSize, zeroPadding=0, type=windowType)
    spectrum = ess.Spectrum(size=frameSize)

    # pitch algorithm
    pitch_detection = ess.PitchYinFFT(frameSize=2048, sampleRate=sampleRate)

    # sfx descriptors
    spectral_peaks = ess.SpectralPeaks(sampleRate=sampleRate, orderBy='frequency')
    harmonic_peaks = ess.HarmonicPeaks()
    inharmonicity = ess.Inharmonicity()
    odd2evenharmonicenergyratio = ess.OddToEvenHarmonicEnergyRatio()
    tristimulus = ess.Tristimulus()

    # used for a nice progress display
    total_frames = frames.num_frames()
    n_frames = 0
    start_of_frame = -frameSize * 0.5
    progress = Progress(total=total_frames)

    for frame in frames:

        frameScope = [start_of_frame / sampleRate, (start_of_frame + frameSize) / sampleRate]
        # pool.setCurrentScope(frameScope)

        if options['skipSilence'] and es.isSilent(frame):
            total_frames -= 1
            start_of_frame += hopSize
            continue

        frame_windowed = window(frame)
        frame_spectrum = spectrum(frame_windowed)

        # pitch descriptors
        frame_pitch, frame_pitch_confidence = pitch_detection(frame_spectrum)

        # spectral peaks based descriptors
        frame_frequencies, frame_magnitudes = spectral_peaks(frame_spectrum)

        # ERROR CORRECTION - hoinx 2015-12
        errIdx = np.where(frame_frequencies < 1)
        frame_frequencies = np.delete(frame_frequencies, errIdx)
        frame_magnitudes = np.delete(frame_magnitudes, errIdx)

        (frame_harmonic_frequencies, frame_harmonic_magnitudes) = harmonic_peaks(frame_frequencies, frame_magnitudes,
                                                                                 frame_pitch)
        if len(frame_harmonic_frequencies) > 1:
            frame_inharmonicity = inharmonicity(frame_harmonic_frequencies, frame_harmonic_magnitudes)
            pool.add(namespace + '.' + 'inharmonicity', frame_inharmonicity)
            frame_tristimulus = tristimulus(frame_harmonic_frequencies, frame_harmonic_magnitudes)
            pool.add(namespace + '.' + 'tristimulus', frame_tristimulus)
            frame_odd2evenharmonicenergyratio = odd2evenharmonicenergyratio(frame_harmonic_frequencies,
                                                                            frame_harmonic_magnitudes)
            pool.add(namespace + '.' + 'odd2evenharmonicenergyratio', frame_odd2evenharmonicenergyratio)

        # display of progress report
        progress.update(n_frames)

        n_frames += 1
        start_of_frame += hopSize

    envelope = ess.Envelope()
    file_envelope = envelope(audio)

    # temporal statistics
    decrease = ess.Decrease()
    pool.add(namespace + '.' + 'temporal_decrease', decrease(file_envelope))  # , pool.GlobalScope)

    centralmoments = ess.CentralMoments()
    file_centralmoments = centralmoments(file_envelope)

    distributionshape = ess.DistributionShape()
    (file_spread, file_skewness, file_kurtosis) = distributionshape(file_centralmoments)
    pool.add(namespace + '.' + 'temporal_spread', file_spread)  # , pool.GlobalScope)
    pool.add(namespace + '.' + 'temporal_skewness', file_skewness)  # , pool.GlobalScope)
    pool.add(namespace + '.' + 'temporal_kurtosis', file_kurtosis)  # , pool.GlobalScope)

    centroid = ess.Centroid()
    pool.add(namespace + '.' + 'temporal_centroid', centroid(file_envelope))  # , pool.GlobalScope)

    # effective duration
    effectiveduration = ess.EffectiveDuration()
    pool.add(namespace + '.' + 'effective_duration', effectiveduration(file_envelope))  # , pool.GlobalScope)

    # log attack time
    logattacktime = ess.LogAttackTime()
    pool.add(namespace + '.' + 'logattacktime', logattacktime(audio))  # , pool.GlobalScope)

    # strong decay
    strongdecay = ess.StrongDecay()
    pool.add(namespace + '.' + 'strongdecay', strongdecay(file_envelope))  # , pool.GlobalScope)

    # dynamic profile
    flatness = ess.FlatnessSFX()
    pool.add(namespace + '.' + 'flatness', flatness(file_envelope))  # , pool.GlobalScope)

    """
    # onsets number
    onsets_number = len(pool['rhythm.onset_times'][0])
    pool.add(namespace + '.' + 'onsets_number', onsets_number)  # , pool.GlobalScope)
    """

    # morphological descriptors
    max_to_total = ess.MaxToTotal()
    pool.add(namespace + '.' + 'max_to_total', max_to_total(file_envelope))  # , pool.GlobalScope)

    tc_to_total = ess.TCToTotal()
    pool.add(namespace + '.' + 'tc_to_total', tc_to_total(file_envelope))  # , pool.GlobalScope)

    derivativeSFX = ess.DerivativeSFX()
    (der_av_after_max, max_der_before_max) = derivativeSFX(file_envelope)
    pool.add(namespace + '.' + 'der_av_after_max', der_av_after_max)  # , pool.GlobalScope)
    pool.add(namespace + '.' + 'max_der_before_max', max_der_before_max)  # , pool.GlobalScope)

    # pitch profile
    """
    pitch = pool['lowlevel.pitch']

    if len(pitch) > 1:
        pool.add(namespace + '.' + 'pitch_max_to_total', max_to_total(pitch))  # , pool.GlobalScope)

        min_to_total = ess.MinToTotal()
        pool.add(namespace + '.' + 'pitch_min_to_total', min_to_total(pitch))  # , pool.GlobalScope)

        pitch_centroid = ess.Centroid(range=len(pitch) - 1)
        pool.add(namespace + '.' + 'pitch_centroid', pitch_centroid(pitch))  # , pool.GlobalScope)

        pitch_after_max_to_before_max_energy_ratio = ess.AfterMaxToBeforeMaxEnergyRatio()
        pool.add(namespace + '.' + 'pitch_after_max_to_before_max_energy_ratio',
                 pitch_after_max_to_before_max_energy_ratio(pitch))  # , pool.GlobalScope)

    else:
        pool.add(namespace + '.' + 'pitch_max_to_total', 0.0)  # , pool.GlobalScope)
        pool.add(namespace + '.' + 'pitch_min_to_total', 0.0)  # , pool.GlobalScope)
        pool.add(namespace + '.' + 'pitch_centroid', 0.0)  # , pool.GlobalScope)
        pool.add(namespace + '.' + 'pitch_after_max_to_before_max_energy_ratio', 0.0)  # , pool.GlobalScope)
    """

    progress.finish()
