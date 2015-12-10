import soundAnalysis as sa
import matplotlib.pyplot as plt


plt.figure(1)
sa.doDescriptorPairScatterPlot('joeDown_Opt1', (3,13))
#sa.clusterSounds('joeDown_Opt1', 2, [3,13])

plt.figure(2)
sa.doDescriptorPairScatterPlot('joeDown_Opt0', (3,13))
#sa.clusterSounds('joeDown_Opt2', 2, [3,13])

plt.show()
