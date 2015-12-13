

descriptors = [
    (1, 'lowlevel.barkbands_kurtosis.mean'),
    (1, 'lowlevel.barkbands_skewness.mean'),
    (1, 'lowlevel.barkbands_spread.mean'),
    (1, 'lowlevel.dissonance.mean'),
    (1, 'lowlevel.hfc.mean'),
    (1, 'lowlevel.pitch.mean'),
    (1, 'lowlevel.pitch_instantaneous_confidence.mean'),
    (1, 'lowlevel.pitch_salience.mean'),
    (1, 'lowlevel.silence_rate_20dB.mean'),
    (1, 'lowlevel.silence_rate_30dB.mean'),
    (1, 'lowlevel.silence_rate_60dB.mean'),
    (1, 'lowlevel.spectral_centroid.mean'),
    (1, 'lowlevel.spectral_complexity.mean'),
    (1, 'lowlevel.spectral_crest.mean'),
    (1, 'lowlevel.spectral_decrease.mean'),
    (1, 'lowlevel.spectral_energy.mean'),
    (1, 'lowlevel.spectral_energyband_high.mean'),
    (1, 'lowlevel.spectral_energyband_low.mean'),
    (1, 'lowlevel.spectral_energyband_middle_high.mean'),
    (1, 'lowlevel.spectral_energyband_middle_low.mean'),
    (1, 'lowlevel.spectral_flatness_db.mean'),
    (1, 'lowlevel.spectral_kurtosis.mean'),
    (1, 'lowlevel.spectral_pitch_histogram_spread.mean'),
    (1, 'lowlevel.spectral_rolloff.mean'),
    (1, 'lowlevel.spectral_skewness.mean'),
    (1, 'lowlevel.spectral_spread.mean'),
    (1, 'lowlevel.spectral_strongpeak.mean'),
    (1, 'lowlevel.zerocrossingrate.mean'),
    (10, 'lowlevel.barkbands.mean'),
    (12, 'lowlevel.mfcc.mean'),
    (6, 'lowlevel.spectral_contrast.mean'),
    #(10, 'lowlevel.temporal_lpc.mean'),
    (1, 'sfx.der_av_after_max.mean'),
    (1, 'sfx.effective_duration.mean'),
    (1, 'sfx.flatness.mean'),
    (1, 'sfx.inharmonicity.mean'),
    (1, 'sfx.logattacktime.mean'),
    (1, 'sfx.max_der_before_max.mean'),
    (1, 'sfx.max_to_total.mean'),
    #(1, 'sfx.odd2evenharmonicenergyratio.mean'),
    (1, 'sfx.strongdecay.mean'),
    (1, 'sfx.tc_to_total.mean'),
    (1, 'sfx.temporal_centroid.mean'),
    (1, 'sfx.temporal_decrease.mean'),
    (1, 'sfx.temporal_kurtosis.mean'),
    (1, 'sfx.temporal_skewness.mean'),
    (1, 'sfx.temporal_spread.mean'),
    (3, 'sfx.tristimulus.mean'),
]


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