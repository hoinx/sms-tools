import soundAnalysis as sa
import numpy as np
import matplotlib.pyplot as plt


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


"""
A9
------------------------------------------------------------
#descRange = [1, 2, 3, 11, 13, 15, 16]
#descRange = [3, 5, 8, 11, 13, 15]
#descRange = [3, 11, 13, 15]

#descRange = [3, 11, 13, 15]


#descRange = [3, 8, 11, 13, 14]
#descRange = [3, 8, 13, 14]
#descRange = [1, 3, 7, 11, 13, 14, 15]

a=[0]*5
------------------------------------
[11, 11, 15, 3, 13]
new min Error of 5
------------------------------------
[13, 3, 11, 11, 15]
new min Error of 5
"""



"""

A10(c)
------------------------------------------------------------
/usr/bin/python2.7 /home/ubuntu/data01/sms-tools-hoinx/workspace/A10c/joeClusterAuto.py
----------------------------------------------------------
descRange = range(17)

[0, 0] try:  0 misses:  856
[0, 1] try:  0 misses:  827
[0, 3] try:  0 misses:  686
[3, 0] try:  0 misses:  645
[3, 13] try:  0 misses:  596
[13, 3] try:  0 misses:  596
----------------------------------------------------------
[2, 3, 13] try:  0 misses:  575
[3, 13, 3] try:  0 misses:  571
[3, 13, 10] try:  0 misses:  545
[3, 13, 14] try:  0 misses:  507
[3, 14, 13] try:  0 misses:  505


----------------------------------------------------------
/usr/bin/python2.7 /home/ubuntu/data01/sms-tools-hoinx/workspace/A10c/joeClusterAuto.py
----------------------------------------------------------
descRange = [2, 3, 10, 13, 14]
retries = 10

[2, 2] misses:  871.3 [ 873.  870.  870.  871.  870.  870.  874.  870.  871.  874.]
[2, 3] misses:  778.3 [ 782.  764.  772.  770.  775.  764.  773.  813.  807.  763.]
[2, 10] misses:  771.1 [ 782.  774.  751.  776.  777.  776.  761.  764.  773.  777.]
[2, 13] misses:  710.6 [ 709.  708.  709.  716.  718.  704.  706.  715.  715.  706.]
[3, 10] misses:  677.8 [ 681.  680.  680.  677.  679.  674.  674.  678.  675.  680.]
[3, 13] misses:  591.8 [ 597.  592.  595.  598.  583.  579.  589.  595.  595.  595.]
----------------------------------------------------------
[3, 3, 13] misses:  577.0 [ 599.  565.  567.  563.  580.  579.  574.  612.  565.  566.]
[3, 10, 13] misses:  562.3 [ 547.  565.  568.  564.  558.  568.  571.  543.  577.  562.]
[3, 13, 14] misses:  510.7 [ 508.  500.  503.  506.  510.  547.  518.  508.  502.  505.]
[13, 3, 14] misses:  506.6 [ 498.  504.  499.  500.  508.  503.  508.  531.  505.  510.]
----------------------------------------------------------
[2, 2, 2, 2] misses:  872.7 [ 873.  873.  876.  874.  870.  874.  876.  871.  870.  870.]
[2, 2, 2, 3] misses:  782.8 [ 776.  782.  788.  757.  795.  782.  777.  795.  789.  787.]
[2, 2, 2, 10] misses:  763.5 [ 762.  764.  764.  764.  764.  768.  757.  766.  762.  764.]
[2, 2, 2, 13] misses:  703.7 [ 758.  700.  690.  690.  698.  702.  695.  695.  705.  704.]
[2, 2, 3, 10] misses:  689.9 [ 685.  695.  691.  684.  699.  697.  682.  699.  666.  701.]
[2, 2, 3, 13] misses:  628.8 [ 646.  594.  593.  647.  637.  646.  643.  646.  592.  644.]
[2, 2, 13, 3] misses:  607.7 [ 586.  606.  593.  645.  646.  589.  589.  590.  641.  592.]
[2, 3, 3, 13] misses:  600.0 [ 605.  595.  595.  589.  602.  605.  623.  596.  601.  589.]
[2, 3, 10, 13] misses:  566.8 [ 593.  573.  556.  568.  555.  588.  562.  558.  559.  556.]
[2, 10, 3, 13] misses:  562.4 [ 555.  554.  551.  584.  592.  555.  555.  559.  563.  556.]
[2, 13, 3, 10] misses:  562.1 [ 544.  561.  554.  555.  555.  592.  556.  554.  557.  593.]
[2, 13, 3, 14] misses:  554.7 [ 551.  602.  552.  539.  555.  550.  550.  542.  553.  553.]
[3, 3, 13, 14] misses:  552.2 [ 553.  546.  558.  545.  548.  539.  563.  556.  559.  555.]
[3, 10, 13, 14] misses:  528.4 [ 542.  515.  519.  522.  523.  554.  507.  542.  510.  550.]
[3, 13, 13, 14] misses:  519.6 [ 519.  517.  524.  524.  520.  499.  525.  526.  519.  523.]
[13, 13, 3, 14] misses:  518.3 [ 524.  518.  491.  520.  524.  520.  524.  517.  523.  522.]
[14, 3, 13, 13] misses:  518.0 [ 521.  519.  521.  516.  513.  506.  523.  521.  522.  518.]
----------------------------------------------------------

best run:
[13, 3, 14] try:  9 misses:  506.6 [ 498.  504.  499.  500.  508.  503.  508.  531.  505.  510.]

"""


#descRange = range(17)
descRange = [2, 3, 10, 13, 14]

errMax = 10000.0
length = 4
retries = 10

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
            err = sa.doClusterSounds('joeDown', numClusters, descriptors)
            errRay = np.append(errRay, err)

        print "\r",
        print "                             \r",

        errVerage = errRay.sum() / len(errRay)
        if errVerage <= errMax:
            print descriptors, "misses: ", errVerage, errRay
            errMax = errVerage

        if increment(a, len(descRange)) == False:
            break
