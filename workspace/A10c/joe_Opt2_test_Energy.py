import numpy as np
import matplotlib.pyplot as plt
import essentia.standard as ess
import essentia as es
import json
import os, sys
from collections import OrderedDict

import descriptors_joeOpt1 as dscr

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



def computeEnergyHistogram(inputAudioFile, outputJsonFile, threshold, histograms):

    M = 2048
    H = 1024
    fs = 44100

    energy = ess.Energy()
    x = ess.MonoLoader(filename=inputAudioFile, sampleRate=fs)()
    frames = ess.FrameGenerator(x, frameSize=M, hopSize=H, startFromZero=True)

    E = []
    numFrames = 0
    for frame in frames:
        numFrames += 1
        E_frame = energy(frame)
        E.append(E_frame)

    E = np.array(E)
    E_norm = E / np.max(E)

    for i in range(len(threshold)):
        t = threshold[i]
        histograms[i] = np.append(histograms[i], [0] * (numFrames - len(histograms[i])))
        idx_threshold = np.where(E_norm > t)
        histograms[i][idx_threshold[0]] += 1




eps = np.finfo(float).eps

def computeEnergyInFileList(inputDir, threshold, category):

    fileList = getInputFileList(os.path.join(inputDir, category))

    print '-'*70
    print "Start computing energy histogram %s files" % (len(fileList), )
    print '-'*70

    histograms = [np.array([])] * len(threshold)

    for ff in fileList:
        audioFile = ff[0]
        jsonFile = ff[1]
        print "Updating histogram: ", jsonFile
        computeEnergyHistogram(audioFile, jsonFile, threshold, histograms)
    print "Done."

    h = np.array([[histograms[i][j] for i in range(len(threshold))] for j in range(len(histograms[0]))])

    figure = plt.figure()
    plt.pcolormesh(h.T)
    plt.xlabel(category, fontsize=16)
    plt.savefig(os.path.join('joeHist', ("hist_" + category + ".png")))
    plt.close(figure)

    return histograms


#threshold = [0.01, 0.05, 0.1, 0.2, 0.5, 0.8, 0.9, 0.95, 0.98, 0.99]
threshold = [eps, 0.0001, 0.001, 0.01, 0.05, 0.1, 0.2, 0.5, 0.8, 0.9, 0.95, 0.98, 0.99, 0.999, 0.9999, 1-eps]
inputDir = 'joeDown_Opt1'

categories = ['bassoon', 'cello', 'clarinet', 'daluo', 'flute', 'guitar', 'mridangam', 'naobo', 'snare_drum', 'trumpet', 'violin', 'xiaoluo']

for cat in categories:
    computeEnergyInFileList(inputDir, threshold, cat)



