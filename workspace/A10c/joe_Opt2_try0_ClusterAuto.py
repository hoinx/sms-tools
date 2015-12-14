import joeSoundAnalysis as sa
import numpy as np

import descriptors_joeOpt2_redux as dscrpt
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

descRange = range(len(descriptorMapping))  # brute force
#descRange = [0, 1, 2, 3, 5, 6, 7, 8, 14, 17, 19, 20, 24]
n = len(descRange)

errMax = 10000.0
length = 2
retries = 1
inputDir = 'joeDown_Opt1'

debugInit = False

print"----------------------------------------------------------"
for i in range(len(descriptorMapping)):
    print i, " : ", descriptorMapping[i],
    if i in descRange:
        print " <---- selected"
    else:
        print

accomplished = []

while True:
    print"----------------------------------------------------------"
    a = [0]*length
    length += 1


    done = False
    while not done:
        #a = [random.randint(0, n-1) for x in range(length)]

        if debugInit:
            a = [274]
            #descriptors = [740]
            debugInit = False

        descriptors = createArray(a, descRange)
        if increment(a, len(descRange)) == False:
            done = True

        desc_set = set(descriptors)
        if desc_set in accomplished:
            continue

        accomplished.append(desc_set)

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
