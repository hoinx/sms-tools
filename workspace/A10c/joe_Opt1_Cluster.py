import soundAnalysis as sa
import matplotlib.pyplot as plt



sa.doDescriptorPairScatterPlot('joeDown_Opt1', (3,13))
#sa.clusterSounds('joeDown_Opt1', 2, [3,13])

sa.doDescriptorPairScatterPlot('joeDown_Opt0', (3,13))
#sa.clusterSounds('joeDown_Opt2', 2, [3,13])

plt.show()
