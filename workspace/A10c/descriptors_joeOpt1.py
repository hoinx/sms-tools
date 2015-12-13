

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

def getExpandedDescriptors():
    expandedDesc = []
    idx = 0
    for d in descriptors:
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
    for d in descriptors:
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