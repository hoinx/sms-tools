import joe_Opt1_soundAnalysis as sa
import numpy as np
import matplotlib.pyplot as plt

import descriptors_essentia as dscrpt

descriptorMapping = dscrpt.getDescriptorMapping()


numClusters = 2

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

descRange = range(len(descriptorMapping))

errMax = 10000.0
length = 1
retries = 1
inputDir = 'joeDown_Opt0'


print"----------------------------------------------------------"
for i in range(len(descriptorMapping)):
    print i, " : ", descriptorMapping[i]


while True:
    print"----------------------------------------------------------"
    a=[0]*length
    length += 1

    while True:
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
