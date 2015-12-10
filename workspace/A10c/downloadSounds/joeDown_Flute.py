import soundDownload as sd
import myFreesoundConfig as conf



def download(testMode=False):

    params = {
        'tag' : '',
        'duration' : (0,10),
        'API_Key' : conf.myAPI_Key,
        'outputDir' : conf.myOutputDir,
        'topNResults' : 3,
        'featureExt' : '.json',
        'preview' : False,
        'emptyDir' : False,
        'folderName' : 'flute',
        'pack' : '',
        'freeSoundId' : '',
        'noDownload': False}

    params['noDownload'] = testMode

    if testMode:
        params['topNResults'] = 1

    noteRange = ["C", "D", "E", "F", "G", "A", "B"]
    octaveRange = ["3", "4", "5", "6"]
    extRange = ["", "sharp"]

    notes = ["%s%s%s" % (name, ext, oct) for oct in octaveRange for name in noteRange for ext in extRange]
    for note in notes:
        params['tag'] = "(%s flute single-note pabloproject)" % (note, )
        sd.downloadFreesound(**params)


#download(testMode=True)
