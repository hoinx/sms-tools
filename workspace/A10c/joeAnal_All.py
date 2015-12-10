import soundAnalysis as sa
import matplotlib.pyplot as plt
import os

outputDir = 'joePlot'

for a in range (17):
    for b in range(17):
        if a != b:
            figure = sa.doDescriptorPairScatterPlot('joeDown', (a,b))
            plt.savefig(os.path.join(outputDir, ("plot_" + str(a) + "_" + str(b) + ".png")))
            plt.close(figure)
