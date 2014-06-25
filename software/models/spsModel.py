import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hamming, triang, blackmanharris, resample
from scipy.fftpack import fft, ifft, fftshift
import math
import sys, os, functools, time
import utilFunctions as UF
import sineModel as SM
import stochasticModel as STM
  
def spsModel(x, fs, w, N, t, stocf):
  # Analysis/synthesis of a sound using the sinusoidal plus stochastic model
  # x: input sound, fs: sampling rate, w: analysis window, 
  # N: FFT size (minimum 512), t: threshold in negative dB, 
  # stocf: decimation factor of mag spectrum for stochastic analysis
  # returns y: output sound, ys: sinusoidal component, yst: stochastic component

  hN = N/2                                                      # size of positive spectrum
  hM1 = int(math.floor((w.size+1)/2))                           # half analysis window size by rounding
  hM2 = int(math.floor(w.size/2))                               # half analysis window size by floor
  Ns = 512                                                      # FFT size for synthesis (even)
  H = Ns/4                                                      # Hop size used for analysis and synthesis
  hNs = Ns/2      
  pin = max(hNs, hM1)                                           # initialize sound pointer in middle of analysis window          
  pend = x.size - max(hNs, hM1)                                 # last sample to start a frame
  fftbuffer = np.zeros(N)                                       # initialize buffer for FFT
  ysw = np.zeros(Ns)                                            # initialize output sound frame
  ystw = np.zeros(Ns)                                           # initialize output sound frame
  ys = np.zeros(x.size)                                         # initialize output array
  yst = np.zeros(x.size)                                        # initialize output array
  w = w / sum(w)                                                # normalize analysis window
  sw = np.zeros(Ns)     
  ow = triang(2*H)                                              # overlapping window
  sw[hNs-H:hNs+H] = ow      
  bh = blackmanharris(Ns)                                       # synthesis window
  bh = bh / sum(bh)                                             # normalize synthesis window
  wr = bh                                                       # window for residual
  sw[hNs-H:hNs+H] = sw[hNs-H:hNs+H] / bh[hNs-H:hNs+H]

  while pin<pend:  
  #-----analysis-----             
    xw = x[pin-hM1:pin+hM2] * w                                  # window the input sound
    fftbuffer = np.zeros(N)                                      # reset buffer
    fftbuffer[:hM1] = xw[hM2:]                                   # zero-phase window in fftbuffer
    fftbuffer[N-hM2:] = xw[:hM2]                           
    X = fft(fftbuffer)                                           # compute FFT
    mX = 20 * np.log10(abs(X[:hN]))                              # magnitude spectrum of positive frequencies
    ploc = UF.peakDetection(mX, hN, t)                
    pX = np.unwrap(np.angle(X[:hN]))                             # unwrapped phase spect. of positive freq.    
    iploc, ipmag, ipphase = UF.peakInterp(mX, pX, ploc)          # refine peak values
        
    iploc = (iploc!=0) * (iploc*Ns/N)                            # synth. locs
    ri = pin-hNs-1                                               # input sound pointer for residual analysis
    xr = x[ri:ri+Ns]*wr                                          # window the input sound                                       
    fftbuffer = np.zeros(Ns)                                     # reset buffer
    fftbuffer[:hNs] = xr[hNs:]                                   # zero-phase window in fftbuffer
    fftbuffer[hNs:] = xr[:hNs]                           
    Xr = fft(fftbuffer)                                          # compute FFT for residual analysis
  
  #-----synthesis-----
    Ys = UF.genSpecSines(fs*iploc/N, ipmag, ipphase, Ns, fs)     # generate spec of sinusoidal component           
    Yr = Xr-Ys;                                                  # get the residual complex spectrum
    mYr = 20 * np.log10( abs(Yr[:hNs]) )                         # magnitude spectrum of residual
    mYrenv = resample(np.maximum(-200, mYr), mYr.size*stocf)     # decimate the magnitude spectrum and avoid -Inf                     
    mYst = resample(mYrenv, hNs)                                 # interpolate to original size
    mYst = 10**(mYst/20)                                         # dB to linear magnitude  
    fc = 1+round(500.0/fs*Ns)                                    # 500 Hz to bin location
    mYst[:fc] *= (np.arange(0, fc)/(fc-1))**2                    # high pass filter the stochastic component
    pYst = 2*np.pi*np.random.rand(hNs)                           # generate phase random values
    Yst = np.zeros(Ns, dtype = complex)
    Yst[:hNs] = mYst * np.exp(1j*pYst)                           # generate positive freq.
    Yst[hNs+1:] = mYst[:0:-1] * np.exp(-1j*pYst[:0:-1])          # generate negative freq.

    fftbuffer = np.zeros(Ns)
    fftbuffer = np.real(ifft(Ys))                                # inverse FFT of sinusoidal spectrum
    ysw[:hNs-1] = fftbuffer[hNs+1:]                              # undo zero-phase window
    ysw[hNs-1:] = fftbuffer[:hNs+1] 
    
    fftbuffer = np.zeros(Ns)
    fftbuffer = np.real(ifft(Yst))                                # inverse FFT of residual spectrum
    ystw[:hNs-1] = fftbuffer[hNs+1:]                              # undo zero-phase window
    ystw[hNs-1:] = fftbuffer[:hNs+1]
    
    ys[ri:ri+Ns] += sw*ysw                                       # overlap-add for sines
    yst[ri:ri+Ns] += sw*ystw                                       # overlap-add for residual
    pin += H                                                     # advance sound pointer
  
  y = ys+yst                                                      # sum of sinusoidal and residual components
  return y, ys, yst
  
# example of using the sinusoidal plus stochastic model by first doing the whole analysis and then the synthesis
# this permits to apply sinusoidal tracking, which is not possible with the sprModel function
if __name__ == '__main__':
	(fs, x) = UF.wavread(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../sounds/bendir.wav'))
	w = np.hamming(2001)
	N = 2048
	H = 128
	t = -100
	minSineDur = .02
	maxnSines = 200
	freqDevOffset = 10
	freqDevSlope = 0.001
	stocf = 0.2
	# perform sinusoidal analysis
	tfreq, tmag, tphase = SM.sineModelAnal(x, fs, w, N, H, t, maxnSines, minSineDur, freqDevOffset, freqDevSlope)
	# subtract sinusoids from original sound
	Ns = 512
	xr = UF.sineSubtraction(x, Ns, H, tfreq, tmag, tphase, fs)
	# compute stochastic model of residual
	mYst = STM.stochasticModelAnal(xr, H, stocf)
	# synthesize sinusoids
	ys = SM.sineModelSynth(tfreq, tmag, tphase, Ns, H, fs)
	# synthesize stochastic component
	yst = STM.stochasticModelSynth(mYst, H)

	# plot stochastic component
	plt.figure(1, figsize=(9.5, 7)) 
	maxplotfreq = 22500.0
	numFrames = int(mYst[:,0].size)
	sizeEnv = int(mYst[0,:].size)
	frmTime = H*np.arange(numFrames)/float(fs)
	binFreq = (.5*fs)*np.arange(sizeEnv*maxplotfreq/(.5*fs))/sizeEnv                      
	plt.pcolormesh(frmTime, binFreq, np.transpose(mYst[:,:sizeEnv*maxplotfreq/(.5*fs)+1]))
	plt.autoscale(tight=True)

	# plot sinusoidal frequencies on top of stochastic component
	sines = tfreq*np.less(tfreq,maxplotfreq)
	sines[sines==0] = np.nan
	numFrames = int(sines[:,0].size)
	frmTime = H*np.arange(numFrames)/float(fs) 
	plt.plot(frmTime, sines, color='k', ms=3, alpha=1)
	plt.xlabel('Time(s)')
	plt.ylabel('Frequency(Hz)')
	plt.autoscale(tight=True)
	plt.title('sinusoidal + residual components')

	# write sounds files for sinusoidal sound and stochastic sound
	UF.wavwrite(ys, fs, 'bendir-sines.wav')
	UF.wavwrite(yst, fs, 'bendir-stochastic.wav')

	plt.tight_layout()
	plt.show()
