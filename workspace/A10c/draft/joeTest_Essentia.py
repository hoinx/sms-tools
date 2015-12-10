import numpy as np
import matplotlib.pyplot as plt
import essentia.standard as ess


def printInfo(algo, indent=0):
    #print '-'*70
    #print algo.getDoc()
    #print '-'*70
    #print algo.getStruct()

    print ' '*indent, '-'*70
    print ' '*indent, algo.name()

    print ' '*indent, '-'*70
    print ' '*indent, "Input: ", [[t, algo.inputType(t)] for t in algo.inputNames()]

    print ' '*indent, '-'*70
    print ' '*indent, "Output: ", algo.outputNames()

    print ' '*indent, '-'*70
    print ' '*indent, "Parameter: ", [[t, algo.paramType(t), algo.paramValue(t)] for t in algo.parameterNames()]

    print ' '*indent, '-'*70



M = 1024
N = 1024
H = 512
fs = 44100



help(ess.MFCC)



spectrum = ess.Spectrum(size=N)
#printInfo(spectrum)

window = ess.Windowing(size=M, type='hann')
#printInfo(window)


mfcc = ess.MFCC(numberCoefficients=12, inputSize=N/2+1)
#printInfo(mfcc)


x = ess.MonoLoader(filename='../../sounds/speech-female.wav', sampleRate=fs)()
frames = ess.FrameGenerator(x, frameSize=M, hopSize=H, startFromZero=True)

print '-'*70

mfccs=[]
frameIndex = 0
for frame in frames:
    mX = spectrum(window(frame))
    mfcc_bands, mfcc_coeffs = mfcc(mX)

    print mfcc_bands
    print '-'*70

    mfccs.append(mfcc_coeffs)
    frameIndex += 1
    if frameIndex >= 2:
        break

"""
mfccs = np.array(mfccs)
plt.pcolormesh(mfccs)
plt.show()
"""
