# functions that implement analysis and synthesis of sounds using the Sinusoidal Model
# (for example usage check the examples models_interface)

import numpy as np
from scipy.signal import blackmanharris, triang
from scipy.fftpack import ifft, fftshift
import math
import dftModel as DFT
import utilFunctions as UF


import matplotlib.pyplot as plt


def sineTracking(pfreq, pmag, pphase, tfreq, freqDevOffset=20, freqDevSlope=0.01):
    """
    Tracking sinusoids from one frame to the next
    pfreq, pmag, pphase: frequencies and magnitude of current frame
    tfreq: frequencies of incoming tracks from previous frame
    freqDevOffset: minimum frequency deviation at 0Hz
    freqDevSlope: slope increase of minimum frequency deviation
    returns tfreqn, tmagn, tphasen: frequency, magnitude and phase of tracks
    """

    tfreqn = np.zeros(tfreq.size)                              # initialize array for output frequencies
    tmagn = np.zeros(tfreq.size)                               # initialize array for output magnitudes
    tphasen = np.zeros(tfreq.size)                             # initialize array for output phases
    pindexes = np.array(np.nonzero(pfreq), dtype=np.int)[0]    # indexes of current peaks
    incomingTracks = np.array(np.nonzero(tfreq), dtype=np.int)[0] # indexes of incoming tracks
    newTracks = np.zeros(tfreq.size, dtype=np.int) -1           # initialize to -1 new tracks
    magOrder = np.argsort(-pmag[pindexes])                      # order current peaks by magnitude
    pfreqt = np.copy(pfreq)                                     # copy current peaks to temporary array
    pmagt = np.copy(pmag)                                       # copy current peaks to temporary array
    pphaset = np.copy(pphase)                                   # copy current peaks to temporary array

    # continue incoming tracks
    if incomingTracks.size > 0:                                 # if incoming tracks exist
        for i in magOrder:                                        # iterate over current peaks
            if incomingTracks.size == 0:                            # break when no more incoming tracks
                break
            track = np.argmin(abs(pfreqt[i] - tfreq[incomingTracks]))   # closest incoming track to peak
            freqDistance = abs(pfreq[i] - tfreq[incomingTracks[track]]) # measure freq distance
            if freqDistance < (freqDevOffset + freqDevSlope * pfreq[i]):  # choose track if distance is small
                    newTracks[incomingTracks[track]] = i                      # assign peak index to track index
                    incomingTracks = np.delete(incomingTracks, track)         # delete index of track in incomming tracks
    indext = np.array(np.nonzero(newTracks != -1), dtype=np.int)[0]   # indexes of assigned tracks
    if indext.size > 0:
        indexp = newTracks[indext]                                    # indexes of assigned peaks
        tfreqn[indext] = pfreqt[indexp]                               # output freq tracks
        tmagn[indext] = pmagt[indexp]                                 # output mag tracks
        tphasen[indext] = pphaset[indexp]                             # output phase tracks
        pfreqt= np.delete(pfreqt, indexp)                             # delete used peaks
        pmagt= np.delete(pmagt, indexp)                               # delete used peaks
        pphaset= np.delete(pphaset, indexp)                           # delete used peaks

    # create new tracks from non used peaks
    emptyt = np.array(np.nonzero(tfreq == 0), dtype=np.int)[0]      # indexes of empty incoming tracks
    peaksleft = np.argsort(-pmagt)                                  # sort left peaks by magnitude
    if ((peaksleft.size > 0) & (emptyt.size >= peaksleft.size)):    # fill empty tracks
            tfreqn[emptyt[:peaksleft.size]] = pfreqt[peaksleft]
            tmagn[emptyt[:peaksleft.size]] = pmagt[peaksleft]
            tphasen[emptyt[:peaksleft.size]] = pphaset[peaksleft]
    elif ((peaksleft.size > 0) & (emptyt.size < peaksleft.size)):   # add more tracks if necessary
            tfreqn[emptyt] = pfreqt[peaksleft[:emptyt.size]]
            tmagn[emptyt] = pmagt[peaksleft[:emptyt.size]]
            tphasen[emptyt] = pphaset[peaksleft[:emptyt.size]]
            tfreqn = np.append(tfreqn, pfreqt[peaksleft[emptyt.size:]])
            tmagn = np.append(tmagn, pmagt[peaksleft[emptyt.size:]])
            tphasen = np.append(tphasen, pphaset[peaksleft[emptyt.size:]])
    return tfreqn, tmagn, tphasen

def cleaningSineTracks(tfreq, minTrackLength=3):
    """
    Delete short fragments of a collection of sinusoidal tracks
    tfreq: frequency of tracks
    minTrackLength: minimum duration of tracks in number of frames
    returns tfreqn: output frequency of tracks
    """

    if tfreq.shape[1] == 0:                                 # if no tracks return input
        return tfreq
    nFrames = tfreq[:,0].size                               # number of frames
    nTracks = tfreq[0,:].size                               # number of tracks in a frame
    for t in range(nTracks):                                # iterate over all tracks
        trackFreqs = tfreq[:,t]                               # frequencies of one track
        trackBegs = np.nonzero((trackFreqs[:nFrames-1] <= 0)  # begining of track contours
                                & (trackFreqs[1:]>0))[0] + 1
        if trackFreqs[0]>0:
            trackBegs = np.insert(trackBegs, 0, 0)
        trackEnds = np.nonzero((trackFreqs[:nFrames-1] > 0)   # end of track contours
                                & (trackFreqs[1:] <=0))[0] + 1
        if trackFreqs[nFrames-1]>0:
            trackEnds = np.append(trackEnds, nFrames-1)
        trackLengths = 1 + trackEnds - trackBegs              # lengths of trach contours
        for i,j in zip(trackBegs, trackLengths):              # delete short track contours
            if j <= minTrackLength:
                trackFreqs[i:i+j] = 0
    return tfreq


def sineModelMultiRes_combined(x, fs, multi_w, multi_N, t, multi_B):
    """
    Analysis/synthesis of a sound using the sinusoidal model, without sine tracking
    x: input array sound, w: analysis window, N: size of complex spectrum, t: threshold in negative dB
    returns y: output array sound
    """




    # fallback for original code
    w = multi_w[0]
    N = multi_N[0]

    bands = range(len(multi_B))                                     # to iterate over bands

    #-orig-----------------------------
    hM1 = int(math.floor((w.size+1)/2))                     # half analysis window size by rounding
    hM2 = int(math.floor(w.size/2))                         # half analysis window size by floor
    #-multi----------------------------
    multi_w_size = np.array([multi_w[i].size for i in bands])
    multi_hM1 = np.floor((multi_w_size + 1)/2.0).astype(int)                     # half analysis window size by rounding
    multi_hM2 = np.floor(multi_w_size / 2.0).astype(int)                         # half analysis window size by floor
    #----------------------------------

    Ns = 512                                                # FFT size for synthesis (even)
    H = Ns/4                                                # Hop size used for analysis and synthesis
    hNs = Ns/2                                              # half of synthesis FFT size

    #-orig-----------------------------
    pin = max(hNs, hM1)                                     # init sound pointer in middle of anal window
    pend = x.size - max(hNs, hM1)                           # last sample to start a frame
    #-multi----------------------------
    multi_pin = np.maximum(hNs, multi_hM1)                    # init sound pointer in middle of anal window
    multi_pend = x.size - multi_pin                           # last sample to start a frame
    #----------------------------------


    #-orig-----------------------------
    fftbuffer = np.zeros(N)                                 # initialize buffer for FFT
    #-multi----------------------------
    fftbuffer_combined = np.zeros(N)
    #multi_fftbuffer = [np.array(multi_N[i]) for i in bands]
    #----------------------------------


    yw = np.zeros(Ns)                                       # initialize output sound frame
    y = np.zeros(x.size)                                    # initialize output array

    #-multi----------------------------
    yw_combined = np.zeros(Ns)                                       # initialize output sound frame
    y_combined = np.zeros(x.size)                                    # initialize output array

    #-orig-----------------------------
    w = w / sum(w)                                          # normalize analysis window
    #-multi----------------------------
    multi_w = [multi_w[i] / sum(multi_w[i]) for i in bands]                                          # normalize analysis window
    #----------------------------------


    sw = np.zeros(Ns)                                       # initialize synthesis window
    ow = triang(2*H)                                        # triangular window
    sw[hNs-H:hNs+H] = ow                                    # add triangular window
    bh = blackmanharris(Ns)                                 # blackmanharris window
    bh = bh / sum(bh)                                       # normalized blackmanharris window
    sw[hNs-H:hNs+H] = sw[hNs-H:hNs+H] / bh[hNs-H:hNs+H]     # normalized synthesis window


    while pin<pend and (multi_pin<multi_pend).all():                                         # while input sound pointer is within sound
    #-----analysis-----

        #-orig-----------------------------
        x1 = x[pin-hM1:pin+hM2]                               # select frame
        #-multi----------------------------
        multi_x1 = [x[(multi_pin[i] - multi_hM1[i]) : (multi_pin[i] + multi_hM2[i])] for i in bands]                               # select frame
        #----------------------------------

        #-orig-----------------------------
        mX, pX = DFT.dftAnal(x1, w, N)                        # compute dft
        #-multi----------------------------
        multi_mX = []
        multi_pX = []
        for i in bands:
            mXi, pXi = DFT.dftAnal(multi_x1[i], multi_w[i], multi_N[i])
            multi_mX.append(mXi)
            multi_pX.append(pXi)
        #----------------------------------


        # we could apply the filters for the bands here already ...


        #-orig-----------------------------
        ploc = UF.peakDetection(mX, t)                        # detect locations of peaks
        #pmag = mX[ploc]                                       # get the magnitude of the peaks
        #-multi----------------------------
        multi_ploc = []
        #multi_pmag = []
        for i in bands:
            ploci = UF.peakDetection(multi_mX[i], t)                        # detect locations of peaks
            #pmagi = multi_mX[i][ploci]                                       # get the magnitude of the peaks
            multi_ploc.append(ploci)
            #multi_pmag.append(pmagi)
        #----------------------------------


        #-orig-----------------------------
        iploc, ipmag, ipphase = UF.peakInterp(mX, pX, ploc)   # refine peak values by interpolation
        ipfreq = fs*iploc/float(N)                            # convert peak locations to Hertz
        #-multi----------------------------
        #multi_iploc = []
        multi_ipmag = []
        multi_ipphase = []
        multi_ipfreq = []
        for i in bands:
            iploci, ipmagi, ipphasei = UF.peakInterp(multi_mX[i], multi_pX[i], multi_ploc[i])   # refine peak values by interpolation
            ipfreqi = fs*iploci/float(multi_N[i])                            # convert peak locations to Hertz
            #multi_iploc.append(iploci)
            multi_ipmag.append(ipmagi)
            multi_ipphase.append(ipphasei)
            multi_ipfreq.append(ipfreqi)
        #----------------------------------

        # ... but we shall decide here!

        """
        print "--------------------------------------"
        print ipfreq
        print ipmag
        print ipphase
        """

        """
        ipfreq_combined = []
        ipmag_combined = []
        ipphase_combined = []
        for i in bands:
            for p in range(len(multi_ipfreq[i])):
                f = multi_ipfreq[i][p]
                if (i == 0 or f >= multi_B[i-1]) and f < multi_B[i]:
                    ipfreq_combined.append(f)
                    ipmag_combined.append(multi_ipmag[i][p])
                    ipphase_combined.append(multi_ipphase[i][p])


        #ipfreq = np.array(ipfreq_combined)
        #ipmag = np.array(ipmag_combined)
        #ipphase = np.array(ipphase_combined)
        """

        # count first for array allocation
        num_ip = 0
        for i in bands:
            for p in range(len(multi_ipfreq[i])):
                f = multi_ipfreq[i][p]
                if (i == 0 or f >= multi_B[i-1]) and f < multi_B[i]:
                    num_ip += 1

        ipfreq_combined = np.zeros(num_ip)
        ipmag_combined = np.zeros(num_ip)
        ipphase_combined = np.zeros(num_ip)
        ip = 0
        for i in bands:
            for p in range(len(multi_ipfreq[i])):
                f = multi_ipfreq[i][p]
                if (i == 0 or f >= multi_B[i-1]) and f < multi_B[i]:
                    ipfreq_combined[ip] = f
                    ipmag_combined[ip] = multi_ipmag[i][p]
                    ipphase_combined[ip] = multi_ipphase[i][p]
                    ip += 1






        """
        print "--------------------------------------"
        print ipfreq_combined
        print ipmag_combined
        print ipphase_combined
        """

    #-----synthesis-----
        Y = UF.genSpecSines(ipfreq, ipmag, ipphase, Ns, fs)   # generate sines in the spectrum
        fftbuffer = np.real(ifft(Y))                          # compute inverse FFT
        yw[:hNs-1] = fftbuffer[hNs+1:]                        # undo zero-phase window
        yw[hNs-1:] = fftbuffer[:hNs+1]
        y[pin-hNs:pin+hNs] += sw*yw                           # overlap-add and apply a synthesis window
        #print y[pin-hNs:pin+hNs]
        pin += H                                              # advance sound pointer


        Y_combined = UF.genSpecSines(ipfreq_combined, ipmag_combined, ipphase_combined, Ns, fs)   # generate sines in the spectrum
        fftbuffer_combined = np.real(ifft(Y_combined))                          # compute inverse FFT
        yw_combined[:hNs-1] = fftbuffer_combined[hNs+1:]                        # undo zero-phase window
        yw_combined[hNs-1:] = fftbuffer_combined[:hNs+1]
        y_combined[pin-hNs:pin+hNs] += sw*yw_combined                           # overlap-add and apply a synthesis window
        #print y_combined[pin-hNs:pin+hNs]
        multi_pin += H

        """
        plt.figure(1)
        plt.plot(abs(Y))
        plt.figure(2)
        plt.plot(abs(Y_combined))
        plt.show()
        """

    return y, y_combined




def sineModelMultiRes(x, fs, multi_w, multi_N, t, multi_B):
    """
    Analysis/synthesis of a sound using the sinusoidal model, without sine tracking
    x: input array sound, w: analysis window, N: size of complex spectrum, t: threshold in negative dB
    returns y: output array sound
    """

    bands = range(len(multi_B))                                     # to iterate over bands

    N = max(multi_N)

    multi_w_size = np.array([multi_w[i].size for i in bands])
    multi_hM1 = np.floor((multi_w_size + 1)/2.0).astype(int)                     # half analysis window size by rounding
    multi_hM2 = np.floor(multi_w_size / 2.0).astype(int)                         # half analysis window size by floor

    Ns = 512                                                # FFT size for synthesis (even)
    H = Ns/4                                                # Hop size used for analysis and synthesis
    hNs = Ns/2                                              # half of synthesis FFT size

    multi_pin = np.maximum(hNs, multi_hM1)                    # init sound pointer in middle of anal window
    multi_pend = x.size - multi_pin                           # last sample to start a frame

    fftbuffer_combined = np.zeros(N)

    yw_combined = np.zeros(Ns)                                       # initialize output sound frame
    y_combined = np.zeros(x.size)                                    # initialize output array

    multi_w = [multi_w[i] / sum(multi_w[i]) for i in bands]                                          # normalize analysis window

    sw = np.zeros(Ns)                                       # initialize synthesis window
    ow = triang(2*H)                                        # triangular window
    sw[hNs-H:hNs+H] = ow                                    # add triangular window
    bh = blackmanharris(Ns)                                 # blackmanharris window
    bh = bh / sum(bh)                                       # normalized blackmanharris window
    sw[hNs-H:hNs+H] = sw[hNs-H:hNs+H] / bh[hNs-H:hNs+H]     # normalized synthesis window

    while (multi_pin<multi_pend).all():                                         # while input sound pointer is within sound
    #-----analysis-----

        multi_x1 = [x[(multi_pin[i] - multi_hM1[i]) : (multi_pin[i] + multi_hM2[i])] for i in bands]                               # select frame

        multi_mX = []
        multi_pX = []
        for i in bands:
            mXi, pXi = DFT.dftAnal(multi_x1[i], multi_w[i], multi_N[i])
            multi_mX.append(mXi)
            multi_pX.append(pXi)

        multi_ploc = []
        for i in bands:
            ploci = UF.peakDetection(multi_mX[i], t)                        # detect locations of peaks
            multi_ploc.append(ploci)

        multi_ipmag = []
        multi_ipphase = []
        multi_ipfreq = []
        for i in bands:
            iploci, ipmagi, ipphasei = UF.peakInterp(multi_mX[i], multi_pX[i], multi_ploc[i])   # refine peak values by interpolation
            ipfreqi = fs*iploci/float(multi_N[i])                            # convert peak locations to Hertz
            multi_ipmag.append(ipmagi)
            multi_ipphase.append(ipphasei)
            multi_ipfreq.append(ipfreqi)

        # count first for array allocation
        num_ip = 0
        for i in bands:
            for p in range(len(multi_ipfreq[i])):
                f = multi_ipfreq[i][p]
                if (i == 0 or f >= multi_B[i-1]) and f < multi_B[i]:
                    num_ip += 1

        ipfreq_combined = np.zeros(num_ip)
        ipmag_combined = np.zeros(num_ip)
        ipphase_combined = np.zeros(num_ip)
        ip = 0
        for i in bands:
            for p in range(len(multi_ipfreq[i])):
                f = multi_ipfreq[i][p]
                if (i == 0 or f >= multi_B[i-1]) and f < multi_B[i]:
                    ipfreq_combined[ip] = f
                    ipmag_combined[ip] = multi_ipmag[i][p]
                    ipphase_combined[ip] = multi_ipphase[i][p]
                    ip += 1

    #-----synthesis-----
        Y_combined = UF.genSpecSines(ipfreq_combined, ipmag_combined, ipphase_combined, Ns, fs)   # generate sines in the spectrum
        fftbuffer_combined = np.real(ifft(Y_combined))                          # compute inverse FFT
        yw_combined[:hNs-1] = fftbuffer_combined[hNs+1:]                        # undo zero-phase window
        yw_combined[hNs-1:] = fftbuffer_combined[:hNs+1]
        y_combined[multi_pin[0]-hNs:multi_pin[0]+hNs] += sw*yw_combined                           # overlap-add and apply a synthesis window
        multi_pin += H

    return y_combined





def sineModelAnal(x, fs, w, N, H, t, maxnSines = 100, minSineDur=.01, freqDevOffset=20, freqDevSlope=0.01):
    """
    Analysis of a sound using the sinusoidal model with sine tracking
    x: input array sound, w: analysis window, N: size of complex spectrum, H: hop-size, t: threshold in negative dB
    maxnSines: maximum number of sines per frame, minSineDur: minimum duration of sines in seconds
    freqDevOffset: minimum frequency deviation at 0Hz, freqDevSlope: slope increase of minimum frequency deviation
    returns xtfreq, xtmag, xtphase: frequencies, magnitudes and phases of sinusoidal tracks
    """

    if (minSineDur <0):                          # raise error if minSineDur is smaller than 0
        raise ValueError("Minimum duration of sine tracks smaller than 0")

    hM1 = int(math.floor((w.size+1)/2))                     # half analysis window size by rounding
    hM2 = int(math.floor(w.size/2))                         # half analysis window size by floor
    x = np.append(np.zeros(hM2),x)                          # add zeros at beginning to center first window at sample 0
    x = np.append(x,np.zeros(hM2))                          # add zeros at the end to analyze last sample
    pin = hM1                                               # initialize sound pointer in middle of analysis window
    pend = x.size - hM1                                     # last sample to start a frame
    w = w / sum(w)                                          # normalize analysis window
    tfreq = np.array([])
    while pin<pend:                                         # while input sound pointer is within sound
        x1 = x[pin-hM1:pin+hM2]                               # select frame
        mX, pX = DFT.dftAnal(x1, w, N)                        # compute dft
        ploc = UF.peakDetection(mX, t)                        # detect locations of peaks
        pmag = mX[ploc]                                       # get the magnitude of the peaks
        iploc, ipmag, ipphase = UF.peakInterp(mX, pX, ploc)   # refine peak values by interpolation
        ipfreq = fs*iploc/float(N)                            # convert peak locations to Hertz
        # perform sinusoidal tracking by adding peaks to trajectories
        tfreq, tmag, tphase = sineTracking(ipfreq, ipmag, ipphase, tfreq, freqDevOffset, freqDevSlope)
        tfreq = np.resize(tfreq, min(maxnSines, tfreq.size))  # limit number of tracks to maxnSines
        tmag = np.resize(tmag, min(maxnSines, tmag.size))     # limit number of tracks to maxnSines
        tphase = np.resize(tphase, min(maxnSines, tphase.size)) # limit number of tracks to maxnSines
        jtfreq = np.zeros(maxnSines)                          # temporary output array
        jtmag = np.zeros(maxnSines)                           # temporary output array
        jtphase = np.zeros(maxnSines)                         # temporary output array
        jtfreq[:tfreq.size]=tfreq                             # save track frequencies to temporary array
        jtmag[:tmag.size]=tmag                                # save track magnitudes to temporary array
        jtphase[:tphase.size]=tphase                          # save track magnitudes to temporary array
        if pin == hM1:                                        # if first frame initialize output sine tracks
            xtfreq = jtfreq
            xtmag = jtmag
            xtphase = jtphase
        else:                                                 # rest of frames append values to sine tracks
            xtfreq = np.vstack((xtfreq, jtfreq))
            xtmag = np.vstack((xtmag, jtmag))
            xtphase = np.vstack((xtphase, jtphase))
        pin += H
    # delete sine tracks shorter than minSineDur
    xtfreq = cleaningSineTracks(xtfreq, round(fs*minSineDur/H))
    return xtfreq, xtmag, xtphase

def sineModelSynth(tfreq, tmag, tphase, N, H, fs):
    """
    Synthesis of a sound using the sinusoidal model
    tfreq,tmag,tphase: frequencies, magnitudes and phases of sinusoids
    N: synthesis FFT size, H: hop size, fs: sampling rate
    returns y: output array sound
    """

    hN = N/2                                                # half of FFT size for synthesis
    L = tfreq.shape[0]                                      # number of frames
    pout = 0                                                # initialize output sound pointer
    ysize = H*(L+3)                                         # output sound size
    y = np.zeros(ysize)                                     # initialize output array
    sw = np.zeros(N)                                        # initialize synthesis window
    ow = triang(2*H)                                        # triangular window
    sw[hN-H:hN+H] = ow                                      # add triangular window
    bh = blackmanharris(N)                                  # blackmanharris window
    bh = bh / sum(bh)                                       # normalized blackmanharris window
    sw[hN-H:hN+H] = sw[hN-H:hN+H]/bh[hN-H:hN+H]             # normalized synthesis window
    lastytfreq = tfreq[0,:]                                 # initialize synthesis frequencies
    ytphase = 2*np.pi*np.random.rand(tfreq[0,:].size)       # initialize synthesis phases
    for l in range(L):                                      # iterate over all frames
        if (tphase.size > 0):                                 # if no phases generate them
            ytphase = tphase[l,:]
        else:
            ytphase += (np.pi*(lastytfreq+tfreq[l,:])/fs)*H     # propagate phases
        Y = UF.genSpecSines(tfreq[l,:], tmag[l,:], ytphase, N, fs)  # generate sines in the spectrum
        lastytfreq = tfreq[l,:]                               # save frequency for phase propagation
        ytphase = ytphase % (2*np.pi)                         # make phase inside 2*pi
        yw = np.real(fftshift(ifft(Y)))                       # compute inverse FFT
        y[pout:pout+N] += sw*yw                               # overlap-add and apply a synthesis window
        pout += H                                             # advance sound pointer
    y = np.delete(y, range(hN))                             # delete half of first window
    y = np.delete(y, range(y.size-hN, y.size))              # delete half of the last window
    return y

