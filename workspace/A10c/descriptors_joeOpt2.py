import numpy as np

descriptors = [
    (1, 'lowlevel.spectral_centroid.mean'),
    (1, 'lowlevel.dissonance.mean'),
    (1, 'lowlevel.hfc.mean'),
    (1, 'sfx.logattacktime.mean'),
    (1, 'sfx.inharmonicity.mean'),
    (6, 'lowlevel.spectral_contrast.mean'),
    (6, 'lowlevel.mfcc.mean'),
    (8, 'lowlevel.mfcc_bands.mean'),

    (1, 'lowlevel.dissonance.var'),
    (1, 'sfx.inharmonicity.var'),
    (6, 'lowlevel.spectral_contrast.var'),
    (1, 'lowlevel.spectral_centroid.var'),
    (6, 'lowlevel.mfcc.var'),
    (1, 'sfx.logattacktime.var'),
    (1, 'lowlevel.hfc.var'),
    (8, 'lowlevel.mfcc_bands.var'),
]


eps = np.finfo(float).eps
threshold = [eps, 0.0001, 0.001, 0.01, 0.05, 0.1, 0.2, 0.5, 0.8, 0.9, 0.95, 0.98, 0.99, 0.999, 0.9999, 1-eps]

def getDescriptors():
    descriptors = []
    for i in range(len(threshold)):
        for n, desc in descriptorsBase:
            descriptors.append((n, "ethc"+str(i) + "." + desc))
    return descriptors



def getExpandedDescriptors():
    expandedDesc = []
    idx = 0
    for d in getDescriptors():
        descriptor = d[1]
        numSub = d[0]
        if numSub == 1:
            expandedDesc.append(descriptor)
            idx += 1
        elif numSub > 1:
            for ii in range(numSub):
                expandedDesc.append(descriptor + "." + str(ii))
                idx += 1
    return expandedDesc



def getDescriptorMapping():
    map = {}
    idx = 0
    for d in getDescriptors():
        descriptor = d[1]
        numSub = d[0]
        if numSub == 1:
            map[idx] = descriptor
            idx += 1
        elif numSub > 1:
            for ii in range(numSub):
                map[idx] = descriptor + "." + str(ii)
                idx += 1
    return map