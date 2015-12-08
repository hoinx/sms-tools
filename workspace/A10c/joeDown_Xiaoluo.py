import soundDownload as sd
import myFreesoundKey as secret


def download(testMode=False):

    myOutputDir = 'joeDown'

    params = {
        'tag' : '',
        'duration' : (0,10),
        'API_Key' : secret.myAPI_Key,
        'outputDir' : myOutputDir,
        'topNResults' : 50,
        'featureExt' : '.json',
        'preview' : False,
        'emptyDir' : False,
        'pack' : '',
        'freeSoundId' : '',
        'noDownload': False}

    params['noDownload'] = testMode

    if testMode:
        params['topNResults'] = 1


    params['folderName'] = 'xiaoluo'
    params['tag'] = 'xiaoluo-instrument'

    sd.downloadFreesound(**params)

#download(testMode=True)
