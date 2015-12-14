import numpy as np
import essentia.standard as ess
import essentia as es
import json
import os

import descriptors_joeOpt2_redux as dscr

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


def appendFeatures(features, pool, namespace):
    for d in dscr.descriptors:
        desc = d[1]
        if not pool.containsKey(desc):
            continue
        num = d[0]
        if num == 1:
            features[namespace + "." + desc] = [float(pool[desc])]
        elif num > 1:
            features[namespace + "." + desc] = [[float(f) for f in pool[desc]]]


def reComputeDescriptors(inputAudioFile, outputJsonFile):

    """
    :param inputAudioFile:
    :param outputJsonFile:
    :return:
    """

    M = 2048
    N = 2048
    H = 1024
    fs = 44100

    W = 'blackmanharris62'


    #spectrum = ess.Spectrum(size=N)
    spectrum = ess.Spectrum()
    #window = ess.Windowing(size=M, type=W)
    window = ess.Windowing(type=W)
    #mfcc = ess.MFCC(numberCoefficients=12, inputSize=N/2+1)
    mfcc = ess.MFCC()

    spectral_peaks = ess.SpectralPeaks(minFrequency=1,
                                       maxFrequency=20000,
                                       maxPeaks=100,
                                       sampleRate=fs,
                                       magnitudeThreshold=0,
                                       orderBy="magnitude")

    dissonance = ess.Dissonance()

    #pitch_detection = ess.PitchYinFFT(frameSize=M, sampleRate=fs)
    pitch_detection = ess.PitchYinFFT()

    harmonic_peaks = ess.HarmonicPeaks()

    inharmonicity = ess.Inharmonicity()

    #spectral_contrast = ess.SpectralContrast(sampleRate=fs)
    spectral_contrast = ess.SpectralContrast()

    centroid = ess.Centroid()

    log_attack_time = ess.LogAttackTime()

    hfc = ess.HFC()

    # magnitudeThreshold = 0.005 is hardcoded for a "blackmanharris62" frame, see lowlevel.py
    spectral_complexity = ess.SpectralComplexity(magnitudeThreshold=0.005)


    energy = ess.Energy()

    x = ess.MonoLoader(filename=inputAudioFile, sampleRate=fs)()
    frames = ess.FrameGenerator(x, frameSize=M, hopSize=H, startFromZero=True)

    E = []
    numFrames = 0
    for frame in frames:
        numFrames += 1
        E_frame = energy(frame)
        E.append(E_frame)

    E_max = np.max(E)

    frames = ess.FrameGenerator(x, frameSize=M, hopSize=H, startFromZero=True)

    pools = [(t, es.Pool()) for t in dscr.threshold]
    for frame in frames:

        eNorm = energy(frame) / E_max

        threshPools = []
        for t, pool in pools:
            if eNorm >= t:
                threshPools.append(pool)

        mX = spectrum(window(frame))
        mfcc_bands, mfcc_coeffs = mfcc(mX)

        [pool.add('lowlevel.mfcc', mfcc_coeffs) for pool in threshPools]
        #[pool.add('lowlevel.mfcc_bands', mfcc_bands) for pool in threshPools]

        pfreq, pmag = spectral_peaks(mX)

        inds = pfreq.argsort()
        pfreq_sorted = pfreq[inds]
        pmag_sorted = pmag[inds]

        diss = dissonance(pfreq_sorted, pmag_sorted)
        [pool.add('lowlevel.dissonance', diss) for pool in threshPools]

        pitch, pitch_confidence = pitch_detection(mX)

        phfreq, phmag = harmonic_peaks(pfreq_sorted, pmag_sorted, pitch)
        if len(phfreq) > 1:
            inharm = inharmonicity(phfreq, phmag)
            [pool.add('sfx.inharmonicity', inharm) for pool in threshPools]

        sc_coeffs, sc_valleys = spectral_contrast(mX)
        [pool.add('lowlevel.spectral_contrast', sc_coeffs) for pool in threshPools]

        c = centroid(mX)
        [pool.add('lowlevel.spectral_centroid', c) for pool in threshPools]

        lat = log_attack_time(frame)
        [pool.add('sfx.logattacktime', lat) for pool in threshPools]

        h = hfc(mX)
        [pool.add('lowlevel.hfc', h) for pool in threshPools]

        spec_complx = spectral_complexity(mX)
        [pool.add('lowlevel.spectral_complexity', spec_complx) for pool in threshPools]


    #calc_Mean_Var = ess.PoolAggregator(defaultStats=['mean', 'var'])
    calc_Mean_Var = ess.PoolAggregator(defaultStats=['mean'])
    aggrPools = [calc_Mean_Var(pool) for t, pool in pools]

    features = {}
    [appendFeatures(features, aggrPools[i], ("ethc"+str(dscr.thresholdSelect[i]))) for i in range(len(aggrPools))]
    json.dump(features, open(outputJsonFile, 'w'))


def updateDescriptorsInFileList(fileList):
    print '-'*70
    print "Start updating %s files" % (len(fileList), )
    print '-'*70
    for ff in fileList:
        audioFile = ff[0]
        jsonFile = ff[1]
        print "Updating descriptors: ", jsonFile
        reComputeDescriptors(audioFile, jsonFile)
    print "Done."


#updateDescriptorsInFileList(getInputFileList('joeDown_Opt1_redux'))


updateDescriptorsInFileList(getInputFileList('joeDown_Opt1/bassoon'))
updateDescriptorsInFileList(getInputFileList('joeDown_Opt1/guitar'))
updateDescriptorsInFileList(getInputFileList('joeDown_Opt1/cello'))
updateDescriptorsInFileList(getInputFileList('joeDown_Opt1/clarinet'))
updateDescriptorsInFileList(getInputFileList('joeDown_Opt1/daluo'))
updateDescriptorsInFileList(getInputFileList('joeDown_Opt1/flute'))
updateDescriptorsInFileList(getInputFileList('joeDown_Opt1/guitar'))
updateDescriptorsInFileList(getInputFileList('joeDown_Opt1/mridangam'))
updateDescriptorsInFileList(getInputFileList('joeDown_Opt1/naobo'))
updateDescriptorsInFileList(getInputFileList('joeDown_Opt1/snare_drum'))
updateDescriptorsInFileList(getInputFileList('joeDown_Opt1/trumpet'))
updateDescriptorsInFileList(getInputFileList('joeDown_Opt1/violin'))
updateDescriptorsInFileList(getInputFileList('joeDown_Opt1/xiaoluo'))

