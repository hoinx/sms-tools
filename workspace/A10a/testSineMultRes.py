import os
import sys
import numpy as np
import math
from scipy.signal import get_window
import matplotlib.pyplot as plt

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../software/models/'))
import utilFunctions as UF
import harmonicModel as HM
import sineModelMultiRes as SMMR
import sineModel as SM
import stft


def computeModel(inputFile, B, M, window = 'hanning', t = -90):

    bands = range(len(B))

    fs, x = UF.wavread(inputFile)
    w = [get_window(window, M[i]) for i in bands]
    N = (2**np.ceil(np.log2(B))).astype(int)

    y_combined = SMMR.sineModelMultiRes(x, fs, w, N, t, B)

    #y, y_combined = SMMR.sineModelMultiRes_combined(x, fs, w, N, t, B)

    # output sound file name
    outputFileInputFile = 'output_sounds/' + os.path.basename(inputFile)
    #outputFile = 'output_sounds/' + os.path.basename(inputFile)[:-4] + '_sineModel.wav'
    outputFile_combined = 'output_sounds/' + os.path.basename(inputFile)[:-4] + '_sineModelMultiRes.wav'

    # write the synthesized sound obtained from the sinusoidal synthesis
    UF.wavwrite(x, fs, outputFileInputFile)
    #UF.wavwrite(y, fs, outputFile)
    UF.wavwrite(y_combined, fs, outputFile_combined)

    plt.figure()
    plt.plot(x)
    plt.plot(y_combined)
    plt.show()


B = [1000, 5000, 22050]
M = [1023, 2047, 4095]



#computeModel ('../../sounds/orchestra.wav')
#computeModel ('../../sounds/speech-female.wav')
#computeModel ('../../sounds/impulse-response.wav')

#computeModel ('sounds/64961__experimental-illness_remaster.wav', B, M, 'hanning', -90)
computeModel ('sounds/81200__milton__maria_snippet.wav', B, M, 'hanning', -90)
