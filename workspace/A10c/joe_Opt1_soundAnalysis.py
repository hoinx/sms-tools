import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import os, sys
import json
from scipy.cluster.vq import vq, kmeans, whiten
# from scipy.stats import mode

"""
{"lowlevel.dissonance.mean": [0.014288026839494705],
"sfx.inharmonicity.mean": [0.002446323400363326],
"lowlevel.spectral_contrast.mean": [[0.058500517159700394, 0.1047227755188942, 0.06718894094228745, 0.04017995670437813, 0.007832195609807968, 0.005342446733266115]],
"lowlevel.spectral_centroid.mean": [0.006109363399446011],
"lowlevel.mfcc.mean": [[39999.5390625, 7668.8203125, 1028.5701904296875, 2007.390869140625, 1292.0933837890625, 384.57940673828125, 491.9180908203125, 320.84381103515625, 83.44264221191406, 91.61522674560547, 116.17028045654297, 67.18522644042969]],
"sfx.logattacktime.mean": [0.7650894522666931],
"lowlevel.hfc.mean": [4091.340576171875],
"lowlevel.mfcc_bands.mean": [[1.723233304640713e-14, 3.6358033757614115e-15, 4.1392095795345085e-07, 1.2552201269500074e-06, 1.2591675098427846e-11, 1.6592915130786423e-07, 2.0349806106878532e-07, 3.6580488540494116e-06, 0.000331611285218969, 4.600903764639952e-07, 7.681605751486131e-08, 8.276048646393974e-08, 2.3098989458958386e-06, 3.994299788701028e-07, 2.7374551336833974e-07, 3.9588607392282427e-10, 1.255269999056452e-09, 2.2853603731665117e-10, 1.7725515499833477e-10, 2.171128832273439e-10, 4.401178206603351e-12, 8.303709960301789e-14, 4.9570112961193e-14, 2.5132426386331383e-14, 2.6641274974395675e-14, 1.061626372748925e-14, 6.022106099380642e-15, 3.4480625464089953e-15, 1.1425798526168603e-14, 5.786044369727973e-15, 1.5467971887605896e-14, 8.108697755437844e-16, 3.3124426189164516e-15, 2.480404907685631e-15, 8.959054777614526e-16, 3.4659248830798124e-16, 1.9108463749549037e-16, 2.3972707944345487e-16, 2.1555912511081135e-16, 7.052224265271894e-17]],

"lowlevel.dissonance.var": [0.014288026839494705],
"sfx.inharmonicity.var": [0.002446323400363326],
"lowlevel.spectral_contrast.var": [[0.058500517159700394, 0.1047227755188942, 0.06718894094228745, 0.04017995670437813, 0.007832195609807968, 0.005342446733266115]],
"lowlevel.spectral_centroid.var": [0.006109363399446011],
"lowlevel.mfcc.var": [[39999.5390625, 7668.8203125, 1028.5701904296875, 2007.390869140625, 1292.0933837890625, 384.57940673828125, 491.9180908203125, 320.84381103515625, 83.44264221191406, 91.61522674560547, 116.17028045654297, 67.18522644042969]],
"sfx.logattacktime.var": [0.7650894522666931],
"lowlevel.hfc.var": [4091.340576171875],
"lowlevel.mfcc_bands.var": [[1.723233304640713e-14, 3.6358033757614115e-15, 4.1392095795345085e-07, 1.2552201269500074e-06, 1.2591675098427846e-11, 1.6592915130786423e-07, 2.0349806106878532e-07, 3.6580488540494116e-06, 0.000331611285218969, 4.600903764639952e-07, 7.681605751486131e-08, 8.276048646393974e-08, 2.3098989458958386e-06, 3.994299788701028e-07, 2.7374551336833974e-07, 3.9588607392282427e-10, 1.255269999056452e-09, 2.2853603731665117e-10, 1.7725515499833477e-10, 2.171128832273439e-10, 4.401178206603351e-12, 8.303709960301789e-14, 4.9570112961193e-14, 2.5132426386331383e-14, 2.6641274974395675e-14, 1.061626372748925e-14, 6.022106099380642e-15, 3.4480625464089953e-15, 1.1425798526168603e-14, 5.786044369727973e-15, 1.5467971887605896e-14, 8.108697755437844e-16, 3.3124426189164516e-15, 2.480404907685631e-15, 8.959054777614526e-16, 3.4659248830798124e-16, 1.9108463749549037e-16, 2.3972707944345487e-16, 2.1555912511081135e-16, 7.052224265271894e-17]]}
"""


# Mapping of descriptors
descriptorMapping = { 0: 'lowlevel.spectral_centroid.mean',
                      1: 'lowlevel.dissonance.mean',
                      2: 'lowlevel.hfc.mean',
                      3: 'sfx.logattacktime.mean',
                      4: 'sfx.inharmonicity.mean',
                      5: 'lowlevel.spectral_contrast.mean.0',
                      6: 'lowlevel.spectral_contrast.mean.1',
                      7: 'lowlevel.spectral_contrast.mean.2',
                      8: 'lowlevel.spectral_contrast.mean.3',
                      9: 'lowlevel.spectral_contrast.mean.4',
                      10: 'lowlevel.spectral_contrast.mean.5',
                      11: 'lowlevel.mfcc.mean.0',
                      12: 'lowlevel.mfcc.mean.1',
                      13: 'lowlevel.mfcc.mean.2',
                      14: 'lowlevel.mfcc.mean.3',
                      15: 'lowlevel.mfcc.mean.4',
                      16: 'lowlevel.mfcc.mean.5',
                      17: 'lowlevel.mfcc.mean.6',
                      18: 'lowlevel.mfcc.mean.7',
                      19: 'lowlevel.mfcc.mean.8',
                      20: 'lowlevel.mfcc.mean.9',
                      21: 'lowlevel.mfcc.mean.10',
                      22: 'lowlevel.mfcc.mean.11',
                    }

def showDescriptorMapping():
  """
  This function prints the mapping of integers to sound descriptors.
  """
  for key in descriptorMapping.keys():
    print "Number %d is for %s"%(key, descriptorMapping[key])

def descriptorPairScatterPlot(inputDir, descInput = (0,0), anotOn = 0):
  """
  This function does a scatter plot of the chosen feature pairs for all the sounds in the 
  directory inputDir. The chosen features are specified in descInput as a tuple. 
  Additionally, you can annotate the sound id on the scatter plot by setting anotOn = 1

  Input:
    inputDir (string): path to the directory where the sound samples and descriptors are present
    descInput (tuple): pair of descriptor indices (see descriptorMapping for mapping between 
                       indices and descriptor names)
    anotOn (int): Set this flag to 1 to annotate the scatter points with the sound id. (Default = 0)
    
  Output:
    scatter plot of the chosen pair of descriptors for all the sounds in the directory inputDir
  """
  doDescriptorPairScatterPlot (inputDir, descInput, anotOn)

  plt.show()
  



def doDescriptorPairScatterPlot(inputDir, descInput = (0,0), anotOn = 0):

  if max(descInput) >= len(descriptorMapping.keys()):
    print("Please select a descriptor index that is within the range. Maximum descriptor index can be " +
           str(len(descriptorMapping)-1) + ". Check the descriptor index mapping again using function "
           "showDescriptorMapping().")

  dataDetails = fetchDataDetails(inputDir)
  #colors = ['r', 'g', 'c', 'b', 'k', 'm', 'y']


  colors = [(0.0, 0.0, 1.0),
    (0.0, 0.5, 0.0),
    (1.0, 0.0, 0.0),
    (0.0, 0.75, 0.75),
    (0.75, 0, 0.75),
    (0.75, 0.75, 0),
    (0.0, 0.0, 0.25),
    (1.0, 0.25, 1.0),
    (0.25, 0.0, 1.0),
    (0.25, 0.5, 0.0),
    (1.0, 0.25, 0.0),
    (0.25, 0.75, 0.75),
    (0.75, 0.25, 0.75),
    (0.75, 0.75, 0.25),
    (0.25, 0.0, 0.25),
    (1.0, 0.25, 1.0)]



  figure = plt.figure()
  plt.hold(True)
  legArray = []
  catArray = []
  for ii, category in enumerate(dataDetails.keys()):
    catArray.append(category)
    for soundId in dataDetails[category].keys():
      filepath = os.path.join(inputDir, category, soundId, dataDetails[category][soundId]['file'])
      descSound = convFtrDict2List(json.load(open(filepath, 'r')))
      x_cord = descSound[descInput[0]]
      y_cord = descSound[descInput[1]]

      plt.scatter(x_cord,y_cord, c = colors[ii], s=200, hold = True, alpha=0.75)
      if anotOn==1:
         plt.annotate(soundId, xy=(x_cord, y_cord), xytext=(x_cord, y_cord))

    circ = Line2D([0], [0], linestyle="none", marker="o", alpha=0.75, markersize=10, markerfacecolor=colors[ii])
    legArray.append(circ)

  plt.ylabel(descriptorMapping[descInput[1]], fontsize =16)
  plt.xlabel(descriptorMapping[descInput[0]], fontsize =16)
  plt.legend(legArray, catArray ,numpoints=1,bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=len(catArray), mode="expand", borderaxespad=0.)

  return figure




def convFtrDict2List(ftrDict):
  """
  This function converts descriptor dictionary to an np.array. The order in the numpy array (indices) 
  are same as those mentioned in descriptorMapping dictionary.
  
  Input: 
    ftrDict (dict): dictionary containing descriptors downloaded from the freesound
  Output: 
    ftr (np.ndarray): Numpy array containing the descriptors for processing later on
  """
  ftr = []
  for key in range(len(descriptorMapping.keys())):
    try:
      ftrName, ind = '.'.join(descriptorMapping[key].split('.')[:-1]), int(descriptorMapping[key].split('.')[-1])
      ftr.append(ftrDict[ftrName][0][ind])
    except:
      ftr.append(ftrDict[descriptorMapping[key]][0])
  return np.array(ftr)


def computeSimilarSounds(queryFile, targetDir, descInput = []):
  """
  This function returns similar sounds for a specific queryFile. Given a queryFile this function 
  computes the distance of the query to all the sounds found in the targetDir and sorts them in 
  the increasing order of the distance. This way we can obtain similar sounds to a query sound.
  
  Input:
    queryFile (string): Descriptor file (.json, unless changed)
    targetDir (string): Target directory to search for similar sounds (using their descriptor files)
    descInput (list) : list of indices of the descriptors to be used for similarity/distance computation 
                       (see descriptorMapping)
  Output: 
    List containing an ordered list of similar sounds. 
  """
  
  dataDetails = fetchDataDetails(targetDir)
  
  #reading query feature dictionary
  qFtr = json.load(open(queryFile, 'r'))
  
  dist = []
  # Iterating over classes
  for cname in dataDetails.keys():
    # Iterating over sounds
    for sname in dataDetails[cname].keys():
      eucDist = eucDistFeatures(qFtr, dataDetails[cname][sname]['feature'], descInput)
      dist.append([eucDist, sname, cname])
  
  # Sorting the array based on the distance
  indSort = np.argsort(np.array(dist)[:,0])
  return (np.array(dist)[indSort,:]).tolist()

def classifySoundkNN(queryFile, targetDir, K, descInput = []):
  """
  This function performs the KNN classification of a sound. The nearest neighbors are chosen from 
  the sounds in the targetDir.
   
  Input:
    queryFile (string): Descriptor file (.json, unless changed)
    targetDir (string): Target directory to search for similar sounds (using their descriptor files)
    K (int) : Number of nearest neighbors to consider for KNN classification.
    descInput (list) : List of indices of the descriptors to be used for similarity/distance computation 
                      (see descriptorMapping)
  Output:
    predClass (string): Predicted class of the query sound
  """
  distances = computeSimilarSounds(queryFile, targetDir, descInput)
  
  if len(np.where((np.array(distances)[:,0].astype(np.float64))==0)[0])>0:
    print("Warning: We found an exact copy of the query file in the target directory. "
          "Beware of duplicates while doing KNN classification.")
  
  classes = (np.array(distances)[:K,2]).tolist()
  freqCnt = []
  for ii in range(K):
    freqCnt.append(classes.count(classes[ii]))
  indMax = np.argmax(freqCnt)
  predClass =  classes[indMax]
  print "This sample belongs to class: " + str(predClass)
  return predClass

def clusterSounds(targetDir, nCluster = -1, descInput=[]):
  """
  This function clusters all the sounds in targetDir using kmeans clustering.
  
  Input:
    targetDir (string): Directory where sound descriptors are stored (all the sounds in this 
                        directory will be used for clustering)
    nCluster (int): Number of clusters to be used for kmeans clustering.
    descInput (list) : List of indices of the descriptors to be used for similarity/distance 
                       computation (see descriptorMapping)
  Output:
    Prints the class of each cluster (computed by a majority vote), number of sounds in each 
    cluster and information (sound-id, sound-class and classification decision) of the sounds 
    in each cluster. Optionally, you can uncomment the return statement to return the same data.
  """
  
  dataDetails = fetchDataDetails(targetDir)
  
  ftrArr = []
  infoArr = []
  
  if nCluster ==-1:
    nCluster = len(dataDetails.keys())
  for cname in dataDetails.keys():
    #iterating over sounds
    for sname in dataDetails[cname].keys():
      ftrArr.append(convFtrDict2List(dataDetails[cname][sname]['feature'])[descInput])
      infoArr.append([sname, cname])
  
  ftrArr = np.array(ftrArr)
  infoArr = np.array(infoArr)
  
  ftrArrWhite = whiten(ftrArr)
  centroids, distortion = kmeans(ftrArrWhite, nCluster)
  clusResults = -1*np.ones(ftrArrWhite.shape[0])
  
  for ii in range(ftrArrWhite.shape[0]):
    diff = centroids - ftrArrWhite[ii,:]
    diff = np.sum(np.power(diff,2), axis = 1)
    indMin = np.argmin(diff)
    clusResults[ii] = indMin
  
  ClusterOut = []
  classCluster = []
  globalDecisions = []  
  for ii in range(nCluster):
    ind = np.where(clusResults==ii)[0]
    freqCnt = []
    for elem in infoArr[ind,1]:
      freqCnt.append(infoArr[ind,1].tolist().count(elem))
    indMax = np.argmax(freqCnt)
    classCluster.append(infoArr[ind,1][indMax])
    
    print("\n(Cluster: " + str(ii) + ") Using majority voting as a criterion this cluster belongs to " + 
          "class: " + classCluster[-1])
    print "Number of sounds in this cluster are: " + str(len(ind))
    decisions = []
    for jj in ind:
        if infoArr[jj,1] == classCluster[-1]:
            decisions.append(1)
        else:
            decisions.append(0)
    globalDecisions.extend(decisions)
    print "sound-id, sound-class, classification decision"
    ClusterOut.append(np.hstack((infoArr[ind],np.array([decisions]).T)))
    print ClusterOut[-1]
  globalDecisions = np.array(globalDecisions)
  totalSounds = len(globalDecisions)
  nIncorrectClassified = len(np.where(globalDecisions==0)[0])
  print("Out of %d sounds, %d sounds are incorrectly classified considering that one cluster should "
        "ideally contain sounds from only a single class"%(totalSounds, nIncorrectClassified))
  print("You obtain a classification (based on obtained clusters and majority voting) accuracy "
         "of %.2f percentage"%round(float(100.0*float(totalSounds-nIncorrectClassified)/totalSounds),2))
  # return ClusterOut

def doClusterSounds(targetDir, nCluster = -1, descInput=[]):

  dataDetails = fetchDataDetails(targetDir)

  ftrArr = []
  infoArr = []

  if nCluster ==-1:
    nCluster = len(dataDetails.keys())
  for cname in dataDetails.keys():
    #iterating over sounds
    for sname in dataDetails[cname].keys():
      ftrArr.append(convFtrDict2List(dataDetails[cname][sname]['feature'])[descInput])
      infoArr.append([sname, cname])

  ftrArr = np.array(ftrArr)
  infoArr = np.array(infoArr)

  ftrArrWhite = whiten(ftrArr)
  centroids, distortion = kmeans(ftrArrWhite, nCluster)
  clusResults = -1*np.ones(ftrArrWhite.shape[0])

  for ii in range(ftrArrWhite.shape[0]):
    diff = centroids - ftrArrWhite[ii,:]
    diff = np.sum(np.power(diff,2), axis = 1)
    indMin = np.argmin(diff)
    clusResults[ii] = indMin

  ClusterOut = []
  classCluster = []
  globalDecisions = []
  for ii in range(nCluster):
    ind = np.where(clusResults==ii)[0]
    freqCnt = []
    for elem in infoArr[ind,1]:
      freqCnt.append(infoArr[ind,1].tolist().count(elem))
    indMax = np.argmax(freqCnt)
    classCluster.append(infoArr[ind,1][indMax])

    decisions = []
    for jj in ind:
        if infoArr[jj,1] == classCluster[-1]:
            decisions.append(1)
        else:
            decisions.append(0)
    globalDecisions.extend(decisions)
    ClusterOut.append(np.hstack((infoArr[ind],np.array([decisions]).T)))
  globalDecisions = np.array(globalDecisions)
  totalSounds = len(globalDecisions)
  nIncorrectClassified = len(np.where(globalDecisions==0)[0])

  return nIncorrectClassified



def fetchDataDetails(inputDir, descExt = '.json'):
  """
  This function is used by other functions to obtain the information regarding the directory structure 
  and the location of descriptor files for each sound 
  """
  dataDetails = {}
  for path, dname, fnames  in os.walk(inputDir):
    for fname in fnames:
      if descExt in fname.lower():
        remain, rname, cname, sname = path.split('/')[:-3], path.split('/')[-3], path.split('/')[-2], path.split('/')[-1]
        if not dataDetails.has_key(cname):
          dataDetails[cname]={}
        fDict = json.load(open(os.path.join('/'.join(remain), rname, cname, sname, fname),'r'))
        dataDetails[cname][sname]={'file': fname, 'feature':fDict}
  return dataDetails

def eucDistFeatures(ftrDict1, ftrDict2, ftrInds):
  """
  This function computes Euclidean distance between two descriptor vectors (input as dictionaries). 
  Additionally, also provide a list of the indices of the descriptor vectors that need to be used 
  in the distance computation.
  
  Input:
    ftrDict1 (dict): Feature vector dictionary 1
    ftrDict2 (dict): Feature vector dictionary 2
    ftrInds (list): List of indices of descriptor vectors to be used in
                    distance computation (see descriptorMapping)
  """
  f1 =  convFtrDict2List(ftrDict1)
  f2 =  convFtrDict2List(ftrDict2)  
  return eucDist(f1[ftrInds], f2[ftrInds])

def eucDist(vec1, vec2):
  """
  Computes the euclidean distance between two vectors
  """
  return np.sqrt(np.sum(np.power(np.array(vec1) - np.array(vec2), 2)))
