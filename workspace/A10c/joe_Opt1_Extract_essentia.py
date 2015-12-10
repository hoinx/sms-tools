import numpy as np
import matplotlib.pyplot as plt
import essentia.standard as ess
import essentia as es
import json
import os, sys
from collections import OrderedDict

import lowlevel as esx
import sfx

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


def fromPoolOne (pool, desc):
    return desc, [float(pool[desc])]

def fromPoolMany (pool, desc):
    return desc, [[float(f) for f in pool[desc]]]

import descriptors_essentia

def makeFeatures(pool):
    features = {}
    for d in descriptors_essentia.descriptors:
        desc = d[1]
        num = d[0]
        if num == 1:
            features[desc] = [float(pool[desc])]
        elif num > 1:
            features[desc] = [[float(f) for f in pool[desc]]]
    return features


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


    # analysis parameters
    options = {}

    options['sampleRate'] = fs
    options['frameSize'] = M
    options['hopSize'] = H
    options['windowType'] = W
    options['skipSilence'] = True

    audio = ess.MonoLoader(filename=inputAudioFile, sampleRate=fs)()

    pool = es.Pool()

    sfx.compute(audio, pool, options)
    esx.compute(audio, pool, options)

    #output = ess.YamlOutput(filename='joeTestOut/essExtract_Pool.json', format='json')
    #output(pool)

    #calc_Mean_Var = ess.PoolAggregator(defaultStats=['mean', 'var'])
    calc_Mean_Var = ess.PoolAggregator(defaultStats=['mean'])
    aggrPool = calc_Mean_Var(pool)

    #output = ess.YamlOutput(filename='joeTestOut/essExtract_AggrPool.json', format='json')
    #output = ess.YamlOutput(filename=outputJsonFile, format='json')
    #output(aggrPool)

    features = makeFeatures(aggrPool)
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




updateDescriptorsInFileList(getInputFileList('joeDown_Opt0'))

"""
updateDescriptorsInFileList(getInputFileList('joeDown_Opt1/bassoon'))
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
"""

