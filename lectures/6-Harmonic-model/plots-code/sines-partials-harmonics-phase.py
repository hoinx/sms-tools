import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hamming, triang, blackmanharris
import sys, os, functools, time
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../../software/models/'))
import dftModel as DFT
import utilFunctions as UF

(fs, x) = UF.wavread('../../../sounds/sine-440+490.wav')
w = np.hamming(3529)
N = 16084*2
hN = N/2
t = -20
pin = 4850
x1 = x[pin:pin+w.size]
mX1, pX1 = DFT.dftAnal(x1, w, N)
ploc = UF.peakDetection(mX1, hN, t)
pmag = mX1[ploc] 
iploc, ipmag, ipphase = UF.peakInterp(mX1, pX1, ploc)

plt.figure(1, figsize=(9, 6))
plt.subplot(311)
plt.plot(fs*np.arange(0,N/2)/float(N), pX1, 'c', lw=1.5)
plt.plot(fs * iploc / N, ipphase, marker='x', color='b', alpha=1, linestyle='', markeredgewidth=1.5) 
plt.axis([200, 1000, 50, 180])
plt.title('pX + peaks (sine-440+490.wav)')


(fs, x) = UF.wavread('../../../sounds/vibraphone-C6.wav')
w = np.blackman(401)
N = 1024
hN = N/2
t = -80
pin = 200
x2 = x[pin:pin+w.size]
mX2, pX2 = DFT.dftAnal(x2, w, N)
ploc = UF.peakDetection(mX2, hN, t)
pmag = mX2[ploc] 
iploc, ipmag, ipphase = UF.peakInterp(mX2, pX2, ploc)

plt.subplot(3,1,2)
plt.plot(fs*np.arange(0,N/2)/float(N), pX2, 'c', lw=1.5)
plt.plot(fs * iploc / N, ipphase, marker='x', color='b', alpha=1, linestyle='', markeredgewidth=1.5) 
plt.axis([500,10000,min(pX2), 25])
plt.title('pX + peaks (vibraphone-C6.wav)')

(fs, x) = UF.wavread('../../../sounds/oboe-A4.wav')
w = np.blackman(651)
N = 2048
hN = N/2
t = -80
pin = 10000
x3 = x[pin:pin+w.size]
mX3, pX3 = DFT.dftAnal(x3, w, N)
ploc = UF.peakDetection(mX3, hN, t)
pmag = mX3[ploc] 
iploc, ipmag, ipphase = UF.peakInterp(mX3, pX3, ploc)

plt.subplot(3,1,3)
plt.plot(fs*np.arange(0,N/2)/float(N), pX3, 'c', lw=1.5)
plt.plot(fs * iploc / N, ipphase, marker='x', color='b', alpha=1, linestyle='', markeredgewidth=1.5)
plt.axis([0,6000,2, 24])
plt.title('pX + peaks (oboe-A4.wav)')

plt.tight_layout()
plt.savefig('sines-partials-harmonics-phase.png')
plt.show()
