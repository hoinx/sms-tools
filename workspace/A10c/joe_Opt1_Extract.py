import numpy as np
import matplotlib.pyplot as plt
import essentia.standard as ess
import essentia as es
import json
import os, sys
from collections import OrderedDict


def getInputFileList(inputDir, audioType = '.mp3'):
    fileList = []
    for path, dname, fnames  in os.walk(inputDir):
        tuple = [None, None]
        for fname in fnames:
            fullPath = os.path.join(path, fname)
            if audioType in fname.lower():
                tuple[0] = fullPath
            else:
                tuple[1] = fullPath
        if not tuple[0] == None and not tuple[1] == None:
            fileList.append(tuple)
    return fileList


def reComputeDescriptors(inputAudioFile, outputJsonFile):

    """
    :param inputAudioFile:
    :param outputJsonFile:
    :return:
    """

    """ orig
    M = 1024
    N = 1024
    H = 512
    fs = 44100
    """

    """ freesound
    Real sampleRate = 44100;
    int frameSize =   2048;
    int hopSize =     1024;
    int zeroPadding = 0;
    """

    M = 2048
    N = 2048
    H = 1024
    fs = 44100


    spectrum = ess.Spectrum(size=N)
    window = ess.Windowing(size=M, type='hann')
    mfcc = ess.MFCC(numberCoefficients=12, inputSize=N/2+1)

    spectral_peaks = ess.SpectralPeaks(minFrequency=1,
                                       maxFrequency=20000,
                                       maxPeaks=100,
                                       sampleRate=fs,
                                       magnitudeThreshold=0,
                                       orderBy="magnitude")

    dissonance = ess.Dissonance()

    pitch_detection = ess.PitchYinFFT(frameSize=2048, sampleRate=fs)

    harmonic_peaks = ess.HarmonicPeaks()

    inharmonicity = ess.Inharmonicity()




    x = ess.MonoLoader(filename=inputAudioFile, sampleRate=fs)()
    frames = ess.FrameGenerator(x, frameSize=M, hopSize=H, startFromZero=True)
    pool = es.Pool()
    for frame in frames:
        mX = spectrum(window(frame))
        mfcc_bands, mfcc_coeffs = mfcc(mX)

        pool.add('lowlevel.mfcc', mfcc_coeffs)
        pool.add('lowlevel.mfcc_bands', mfcc_bands)

        pfreq, pmag = spectral_peaks(mX)

        inds = pfreq.argsort()
        pfreq_sorted = pfreq[inds]
        pmag_sorted = pmag[inds]

        diss = dissonance(pfreq_sorted, pmag_sorted)
        pool.add('lowlevel.dissonance', diss)

        pitch, pitch_confidence = pitch_detection(mX)

        phfreq, phmag = harmonic_peaks(pfreq_sorted, pmag_sorted, pitch)
        if len(phfreq) > 1:
            inharm = inharmonicity(phfreq, phmag)
            pool.add('sfx.inharmonicity', inharm)


    calc_Mean_Var = ess.PoolAggregator(defaultStats=['mean', 'var'])
    aggrPool = calc_Mean_Var(pool)

    features = OrderedDict([
        ('lowlevel.dissonance.mean', [float(aggrPool['lowlevel.dissonance.mean'])]),
        ('sfx.inharmonicity.mean', [float(aggrPool['sfx.inharmonicity.mean'])]),
        ('lowlevel.mfcc.mean', [[float(f) for f in aggrPool['lowlevel.mfcc.mean']]]),
        ('lowlevel.mfcc_bands.mean', [[float(f) for f in aggrPool['lowlevel.mfcc_bands.mean']]])
    ])

    json.dump(features, open(outputJsonFile, 'w'))


fileList = getInputFileList('joeDown_Opt1')

audioFile = fileList[0][0]
jsonFile = fileList[0][1]
reComputeDescriptors (audioFile, jsonFile)

