import soundDownload as sd
import myFreesoundConfig as conf

def download(testMode=False):

    params = {
        'tag' : '',
        'duration' : (0,10),
        'API_Key' : conf.myAPI_Key,
        'outputDir' : '../joeTestOut',
        'topNResults' : 1,
        'featureExt' : '.json',
        'preview' : False,
        'emptyDir' : True,
        'folderName' : '_test',
        'pack' : '',
        'freeSoundId' : ''}

    params['noDownload'] = testMode

    if testMode:
        params['topNResults'] = 1

    #params['queryText'] = 'guitar'
    #params['pack'] = 'ClassicalGuitar-multisampled'

    params['freeSoundId'] = '228622'
    sd.downloadFreesound(**params)

download()
