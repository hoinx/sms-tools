#import soundAnalysis as sa
import joeSoundAnalysis as sa
import matplotlib.pyplot as plt

"""
sa.doDescriptorPairScatterPlot('joeDown_NoNorm', (3,13))
#sa.clusterSounds('joeDown_Opt2', 2, [3,13])

sa.doDescriptorPairScatterPlot('joeDown_Norm', (3,13))
#sa.clusterSounds('joeDown_Opt1', 2, [3,13])
"""
sa.doDescriptorPairScatterPlot('joeDown_Opt0', (0,1))
#sa.clusterSounds('joeDown_Opt2', 2, [3,13])



plt.show()
