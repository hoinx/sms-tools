import essentia as es
import essentia.standard as ess
import matplotlib.pyplot as plt
import numpy as np


loader = ess.MonoLoader(filename='./joeDown/bassoon/154275/154275_2626346-lq.mp3')
audio = loader()

w = ess.Windowing(type='hann')
spectrum = ess.Spectrum()  # FFT() would give the complex FFT, here we just want the magnitude spectrum



"""
frame = audio[5*44100 : 5*44100 + 1024]
spec = spectrum(w(frame))
plt.plot(spec)
plt.show()
"""




mfcc = ess.MFCC()


"""
mfccs = []
frameSize = 1024
hopSize = 512
for fstart in range(0, len(audio)-frameSize, hopSize):
    frame = audio[fstart:fstart+frameSize]

    s = spectrum(w(frame))

    #plt.plot(s)

    mfcc_bands, mfcc_coeffs = mfcc(s)
    mfccs.append(mfcc_coeffs)

#plt.show()

#plt.figure()
plt.pcolormesh(np.array(mfccs))
plt.show()
"""



"""
# and let's do it in a more essentia-like way:
mfccs = []
for frame in ess.FrameGenerator(audio, frameSize = 1024, hopSize = 512):
    mfcc_bands, mfcc_coeffs = mfcc(spectrum(w(frame)))
    mfccs.append(mfcc_coeffs)

# transpose to have it in a better shape
mfccs = ess.array(mfccs).T
"""


# So let's redo the previous using a Pool
pool = es.Pool()
for frame in ess.FrameGenerator(audio, frameSize = 1024, hopSize = 512):
    mfcc_bands, mfcc_coeffs = mfcc(spectrum(w(frame)))
    pool.add('lowlevel.mfcc', mfcc_coeffs)
    pool.add('lowlevel.mfcc_bands', mfcc_bands)

"""
plotMfcc = pool['lowlevel.mfcc'].T[1:,:]
plt.pcolormesh(plotMfcc)
plt.show()
"""




#output = es.YamlOutput(filename = 'mfcc.sig')
output = ess.YamlOutput(filename='joeTestOut/mfcc.json', format='json')
output(pool)

# Say we're not interested in all the MFCC frames, but just their mean & variance.
# To this end, we have the PoolAggregator algorithm, that can do all sorts of
# aggregation: mean, variance, min, max, etc...
aggrPool = ess.PoolAggregator(defaultStats=['mean', 'var'])(pool)

print 'Original pool descriptor names:'
print pool.descriptorNames()
print
print 'Aggregated pool descriptor names:'
print aggrPool.descriptorNames()

output = ess.YamlOutput(filename='joeTestOut/mfccaggr.json', format='json')
output(aggrPool)
