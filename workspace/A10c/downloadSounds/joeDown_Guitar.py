import soundDownload as sd
import myFreesoundConfig as conf

def download():

    params = {
        'tag' : '',
        'duration' : (0,10),
        'API_Key' : conf.myAPI_Key,
        'outputDir' : conf,
        'topNResults' : 50,
        'featureExt' : '.json',
        'preview' : True,
        'emptyDir' : False,
        'folderName' : 'guitar',
        'pack' : '',
        'freeSoundId' : ''}

    params['preview'] = False
    params['queryText'] = 'guitar'

    params['pack'] = 'ClassicalGuitar-multisampled'
    sd.downloadFreesound(**params)

    params['pack'] = 'acoustic_guitar'
    sd.downloadFreesound(**params)
