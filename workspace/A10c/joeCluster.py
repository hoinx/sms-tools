import soundAnalysis as sa
import matplotlib.pyplot as plt


# 'lowlevel.mfcc.mean.2', 'sfx.logattacktime.mean'
#sa.descriptorPairScatterPlot('joeDown', (3,13))


# 'lowlevel.spectral_contrast.mean.3', 'lowlevel.mfcc.mean.2'
#sa.descriptorPairScatterPlot('joeDown', (13,8))



# 'lowlevel.mfcc.mean.3', 'lowlevel.mfcc.mean.2',
#sa.descriptorPairScatterPlot('joeDown', (13,14))

#[3,8,13,14]
#sa.clusterSounds('joeDown', 3, [3,13])
#sa.clusterSounds('joeDown', 3, [8,13])
sa.clusterSounds('joeDown', 12, [13,14])

#sa.clusterSounds('joeDown', 3, [11, 11, 14, 1, 3])

#sa.clusterSounds('joeDown', 3, [11, 15, 3])
#sa.clusterSounds('joeDown', 3, [3, 11, 11])
