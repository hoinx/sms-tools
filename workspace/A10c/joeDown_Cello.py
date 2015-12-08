import soundDownload as sd
import myFreesoundKey as secret



def download(testMode=False):

    myOutputDir = 'joeDown'

    params = {
        'tag' : '',
        'duration' : (0,10),
        'API_Key' : secret.myAPI_Key,
        'outputDir' : myOutputDir,
        'topNResults' : 3,
        'featureExt' : '.json',
        'preview' : False,
        'emptyDir' : False,
        'folderName' : 'cello',
        'pack' : '',
        'freeSoundId' : '',
        'noDownload': False}

    params['noDownload'] = testMode

    noteRange = ["C", "D", "E", "F", "G", "A", "B"]
    #noteRange = ["B"]
    octaveRange = ["1", "2", "3", "4", "5", "6"]
    extRange = ["", "sharp"]

    # ["3", "4", "5"]
    if testMode:
        params['topNResults'] = 1

    notes = ["%s%s%s" % (name, ext, oct) for oct in octaveRange for name in noteRange for ext in extRange]
    for note in notes:
        params['tag'] = "(%s cello single-note pabloproject)" % (note, )
        sd.downloadFreesound(**params)


#download(testMode=True)
