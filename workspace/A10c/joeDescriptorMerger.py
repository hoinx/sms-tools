import numpy as np
import matplotlib.pyplot as plt
import essentia.standard as ess
import essentia as es
import json
import os, sys
from collections import OrderedDict



def getFileList(inputDir, audioType = '.mp3', jsonType = '.json'):
    fileList = []
    for path, dname, fnames  in os.walk(inputDir):
        tuple = [None, None]
        for fname in fnames:
            fullPath = os.path.join(path, fname)
            if audioType in fname.lower():
                tuple[0] = fullPath
            elif jsonType in fname.lower():
                tuple[1] = fullPath
            else:
                print "unknown file type: ", fname
        if not tuple[0] == None or not tuple[1] == None:
            fileList.append(tuple)
    return fileList

def mergeDescriptors(fileList_in_A, namespace_A, fileList_in_B, namespace_B, fileList_out):
    n = len(fileList_out)
    nA = len(fileList_in_A)
    nB = len(fileList_in_B)
    if not (nA == nB == n):
        return

    for i in range(n):
        jsonFile_in_A = fileList_in_A[i][1]
        jsonFile_in_B = fileList_in_B[i][1]
        jsonFile_out = fileList_out[i][1]

        remain_A, fname_A = jsonFile_in_A.split('/')[-2], jsonFile_in_A.split('/')[-1]
        remain_B, fname_B = jsonFile_in_B.split('/')[-2], jsonFile_in_B.split('/')[-1]
        remain_Out, fname_Out = jsonFile_out.split('/')[-2], jsonFile_out.split('/')[-1]

        fDict_A = json.load(open(jsonFile_in_A, 'r'))
        fDict_B = json.load(open(jsonFile_in_B, 'r'))

        if not (fname_A == fname_B == fname_Out):
            print "Error: different structure, abort!"
            return

        fDict_out = {}

        for key, value in fDict_A.iteritems():
            if not namespace_A == None:
                fDict_out[namespace_A + "." + key] = value
            else:
                fDict_out[key] = value


        for key, value in fDict_B.iteritems():
            if not namespace_B == None:
                fDict_out[namespace_B + "." + key] = value
            else:
                fDict_out[key] = value

        json.dump(fDict_out, open(jsonFile_out, 'w'))


a = getFileList('joeDesc_All')
b = getFileList('joeDown_Opt1')
out = getFileList('joeDesc_All2')

mergeDescriptors(a, None, b, None, out)
