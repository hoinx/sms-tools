import soundDownload as sd
import myFreesoundConfig as conf
import time


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
        'pack' : '',
        'freeSoundId' : '',
        'noDownload': False}

    params['noDownload'] = testMode

    if testMode:
        params['topNResults'] = 1

    params['folderName'] = 'mridangam'

    nameRange = ["c", "d", "e", "f", "g", "a", "b"]
    extRange = ["", "sh"]
    soundRange = ["ta", "tha", "tham", "thi", "thom", "cha", "dhin", "dheem", "bheem", "num"]

    notes = ["%s-%s%s" % (sound, name, ext) for sound in soundRange for name in nameRange for ext in extRange]
    for note in notes:
        params['tag'] = "(mridangam-%s mridangam-stroke-dataset)" % (note, )
        sd.downloadFreesound(**params)
        time.sleep(1)


#download(testMode=True)
