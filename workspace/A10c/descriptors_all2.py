

descriptors = [
    (1, 'essentia.lowlevel.barkbands_kurtosis.mean'),
    (1, 'essentia.lowlevel.barkbands_skewness.mean'),
    (1, 'essentia.lowlevel.barkbands_spread.mean'),
    (1, 'essentia.lowlevel.dissonance.mean'),
    (1, 'essentia.lowlevel.hfc.mean'),
    (1, 'essentia.lowlevel.pitch.mean'),
    (1, 'essentia.lowlevel.pitch_instantaneous_confidence.mean'),
    (1, 'essentia.lowlevel.pitch_salience.mean'),
    (1, 'essentia.lowlevel.silence_rate_20dB.mean'),
    (1, 'essentia.lowlevel.silence_rate_30dB.mean'),
    (1, 'essentia.lowlevel.silence_rate_60dB.mean'),
    (1, 'essentia.lowlevel.spectral_centroid.mean'),
    (1, 'essentia.lowlevel.spectral_complexity.mean'),
    (1, 'essentia.lowlevel.spectral_crest.mean'),
    (1, 'essentia.lowlevel.spectral_decrease.mean'),
    (1, 'essentia.lowlevel.spectral_energy.mean'),
    (1, 'essentia.lowlevel.spectral_energyband_high.mean'),
    (1, 'essentia.lowlevel.spectral_energyband_low.mean'),
    (1, 'essentia.lowlevel.spectral_energyband_middle_high.mean'),
    (1, 'essentia.lowlevel.spectral_energyband_middle_low.mean'),
    (1, 'essentia.lowlevel.spectral_flatness_db.mean'),
    (1, 'essentia.lowlevel.spectral_kurtosis.mean'),
    (1, 'essentia.lowlevel.spectral_pitch_histogram_spread.mean'),
    (1, 'essentia.lowlevel.spectral_rolloff.mean'),
    (1, 'essentia.lowlevel.spectral_skewness.mean'),
    (1, 'essentia.lowlevel.spectral_spread.mean'),
    (1, 'essentia.lowlevel.spectral_strongpeak.mean'),
    (1, 'essentia.lowlevel.zerocrossingrate.mean'),
    (10, 'essentia.lowlevel.barkbands.mean'),
    (12, 'essentia.lowlevel.mfcc.mean'),
    (6, 'essentia.lowlevel.spectral_contrast.mean'),
    #(10, 'essentia.lowlevel.temporal_lpc.mean'),
    (1, 'essentia.sfx.der_av_after_max.mean'),
    (1, 'essentia.sfx.effective_duration.mean'),
    (1, 'essentia.sfx.flatness.mean'),
    (1, 'essentia.sfx.inharmonicity.mean'),
    (1, 'essentia.sfx.logattacktime.mean'),
    (1, 'essentia.sfx.max_der_before_max.mean'),
    (1, 'essentia.sfx.max_to_total.mean'),
    #(1, 'essentia.sfx.odd2evenharmonicenergyratio.mean'),
    (1, 'essentia.sfx.strongdecay.mean'),
    (1, 'essentia.sfx.tc_to_total.mean'),
    (1, 'essentia.sfx.temporal_centroid.mean'),
    (1, 'essentia.sfx.temporal_decrease.mean'),
    (1, 'essentia.sfx.temporal_kurtosis.mean'),
    (1, 'essentia.sfx.temporal_skewness.mean'),
    (1, 'essentia.sfx.temporal_spread.mean'),
    (3, 'essentia.sfx.tristimulus.mean'),

    (1, 'freesound.lowlevel.spectral_centroid.mean'),
    (1, 'freesound.lowlevel.dissonance.mean'),
    (1, 'freesound.lowlevel.hfc.mean'),
    (1, 'freesound.sfx.logattacktime.mean'),
    (1, 'freesound.sfx.inharmonicity.mean'),
    (6, 'freesound.lowlevel.spectral_contrast.mean'),
    (6, 'freesound.lowlevel.mfcc.mean'),

    (1, 'ethc1.lowlevel.spectral_centroid.mean'),
    (1, 'ethc1.lowlevel.dissonance.mean'),
    (1, 'ethc1.lowlevel.hfc.mean'),
    (1, 'ethc1.lowlevel.spectral_complexity.mean'),
    (1, 'ethc1.sfx.logattacktime.mean'),
    (1, 'ethc1.sfx.inharmonicity.mean'),
    (4, 'ethc1.lowlevel.mfcc.mean'),

    (1, 'ethc4.lowlevel.spectral_centroid.mean'),
    (1, 'ethc4.lowlevel.dissonance.mean'),
    (1, 'ethc4.lowlevel.hfc.mean'),
    (1, 'ethc4.lowlevel.spectral_complexity.mean'),
    (1, 'ethc4.sfx.logattacktime.mean'),
    (1, 'ethc4.sfx.inharmonicity.mean'),
    (4, 'ethc4.lowlevel.mfcc.mean'),

    (1, 'ethc7.lowlevel.spectral_centroid.mean'),
    (1, 'ethc7.lowlevel.dissonance.mean'),
    (1, 'ethc7.lowlevel.hfc.mean'),
    (1, 'ethc7.lowlevel.spectral_complexity.mean'),
    (1, 'ethc7.sfx.logattacktime.mean'),
    (1, 'ethc7.sfx.inharmonicity.mean'),
    (4, 'ethc7.lowlevel.mfcc.mean'),

]

def getExpandedDescriptors():
    expandedDesc = []
    idx = 0
    for d in descriptors:
        descriptor = d[1]
        numSub = d[0]
        if numSub == 1:
            expandedDesc.append(descriptor)
            idx += 1
        elif numSub > 1:
            for ii in range(numSub):
                expandedDesc.append(descriptor + "." + str(ii))
                idx += 1
    return expandedDesc



descExpanded = getExpandedDescriptors()
idx_essentia = descExpanded.index('essentia.lowlevel.barkbands_kurtosis.mean')
idx_freesound = descExpanded.index('freesound.lowlevel.spectral_centroid.mean')
idx_ethc1 = descExpanded.index('ethc1.lowlevel.spectral_centroid.mean')

def getDescriptorMapping():
    map = {}
    idx = 0
    for d in descriptors:
        descriptor = d[1]
        numSub = d[0]
        if numSub == 1:
            map[idx] = descriptor
            idx += 1
        elif numSub > 1:
            for ii in range(numSub):
                map[idx] = descriptor + "." + str(ii)
                idx += 1
    return map