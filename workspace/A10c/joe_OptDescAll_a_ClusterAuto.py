import joeSoundAnalysis as sa
import numpy as np
import matplotlib.pyplot as plt
import random

import descriptors_all as dscrpt

descriptorMapping = dscrpt.getDescriptorMapping()
sa.setDescriptorMapping(descriptorMapping)

numClusters = 12

def increment(a, base):
    m=len(a)
    a[m-1]+=1
    c=0
    for i in reversed(range(m)):
        a[i]+=c
        if a[i]==base:
            a[i]=0
            c=1
        else:
            c=0
    return c==0

def createArray(a, words):
    s=[]
    for i in range(len(a)):
        s.append(words[a[i]])
    return s

#descRange = range(len(descriptorMapping)) # brute force
descRange_freesound = [1, 3, 7, 11, 13, 14, 15] # freesound
#descRange_essentia = [0, 1, 2, 3, 6, 8, 9, 12, 21, 24, 28, 29, 30, 12, 40, 57, 64] # essentia
descRange_essentia = [1, 2, 6, 8, 12, 40, 57, 64] # essentia
descRange_freesound = [x + dscrpt.idx_freesound for x in descRange_freesound]

descRange = descRange_essentia
descRange.extend(descRange_freesound)

n = len(descRange)

errMax = 10000.0
length = 1
retries = 1
inputDir = 'joeDesc_All'


print"----------------------------------------------------------"
for i in range(len(descriptorMapping)):
    print i, " : ", descriptorMapping[i],
    if i in descRange:
        print " <---- selected"
    else:
        print


while True:
    print"----------------------------------------------------------"
    a = [0]*length
    length += 1

    while True:
        #a = [random.randint(0, n-1) for x in range(length)]

        descriptors = createArray(a, descRange)
        print descriptors,
        errRay = np.array([])
        for i in range(retries):
            print ".",
            err = sa.doClusterSounds(inputDir, numClusters, descriptors)
            errRay = np.append(errRay, err)

        print "\r",
        print "                             \r",

        errVerage = errRay.sum() / len(errRay)
        if errVerage <= errMax:
            print descriptors, "misses: ", errVerage, errRay,
            print "     [ ",
            for d in descriptors:
                print descriptorMapping[d], ", ",
            print " ] "
            errMax = errVerage

        if increment(a, len(descRange)) == False:
            break
