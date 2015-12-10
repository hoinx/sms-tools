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

    #help(ess.SpectralContrast)



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

    pitch_detection = ess.PitchYinFFT(frameSize=M, sampleRate=fs)

    harmonic_peaks = ess.HarmonicPeaks()

    inharmonicity = ess.Inharmonicity()

    spectral_contrast = ess.SpectralContrast(sampleRate=fs)

    centroid = ess.Centroid()

    log_attack_time = ess.LogAttackTime()

    hfc = ess.HFC()

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

        sc_coeffs, sv_mag = spectral_contrast(mX)
        pool.add('lowlevel.spectral_contrast', sc_coeffs)

        c = centroid(mX)
        pool.add('lowlevel.spectral_centroid', c)

        lat = log_attack_time(frame)
        pool.add('sfx.logattacktime', lat)

        h = hfc(mX)
        pool.add('lowlevel.hfc', h)



    calc_Mean_Var = ess.PoolAggregator(defaultStats=['mean', 'var'])
    aggrPool = calc_Mean_Var(pool)

    features = OrderedDict([
        ('lowlevel.dissonance.mean', [float(aggrPool['lowlevel.dissonance.var'])]),
        ('sfx.inharmonicity.mean', [float(aggrPool['sfx.inharmonicity.var'])]),
        ('lowlevel.spectral_contrast.mean', [[float(f) for f in aggrPool['lowlevel.spectral_contrast.var']]]),
        ('lowlevel.spectral_centroid.mean', [float(aggrPool['lowlevel.spectral_centroid.var'])]),
        ('lowlevel.mfcc.mean', [[float(f) for f in aggrPool['lowlevel.mfcc.var']]]),
        ('sfx.logattacktime.mean', [float(aggrPool['sfx.logattacktime.var'])]),
        ('lowlevel.hfc.mean', [float(aggrPool['lowlevel.hfc.var'])]),
        ('lowlevel.mfcc_bands.mean', [[float(f) for f in aggrPool['lowlevel.mfcc_bands.var']]]),

        ('lowlevel.dissonance.var', [float(aggrPool['lowlevel.dissonance.var'])]),
        ('sfx.inharmonicity.var', [float(aggrPool['sfx.inharmonicity.var'])]),
        ('lowlevel.spectral_contrast.var', [[float(f) for f in aggrPool['lowlevel.spectral_contrast.var']]]),
        ('lowlevel.spectral_centroid.var', [float(aggrPool['lowlevel.spectral_centroid.var'])]),
        ('lowlevel.mfcc.var', [[float(f) for f in aggrPool['lowlevel.mfcc.var']]]),
        ('sfx.logattacktime.var', [float(aggrPool['sfx.logattacktime.var'])]),
        ('lowlevel.hfc.var', [float(aggrPool['lowlevel.hfc.var'])]),
        ('lowlevel.mfcc_bands.var', [[float(f) for f in aggrPool['lowlevel.mfcc_bands.var']]]),
    ])

    json.dump(features, open(outputJsonFile, 'w'))



def updateDescriptorsInFileList(fileList):
    for ff in fileList:
        audioFile = ff[0]
        jsonFile = ff[1]
        print "Updating descriptors: ", jsonFile
        reComputeDescriptors(audioFile, jsonFile)




updateDescriptorsInFileList(getInputFileList('joeDown_Opt1'))

#updateDescriptorsInFileList(getInputFileList('joeDown_Opt1/mridangam'))
#updateDescriptorsInFileList(getInputFileList('joeDown_Opt1/cello'))
#updateDescriptorsInFileList(getInputFileList('joeDown_Opt1/daluo'))
#updateDescriptorsInFileList(getInputFileList('joeDown_Opt1/xiaoluo'))


