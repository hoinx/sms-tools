import soundDownload as sd
import myFreesoundKey as secret

myOutputDir = 'joeDown'

params = {
    'queryText' : 'guitar',
    'tag' : '',
    'duration' : (0,10),
    'API_Key' : secret.myAPI_Key,
    'outputDir' : myOutputDir,
    'topNResults' : 50,
    'featureExt' : '.json',
    'preview' : False,
    'emptyDir' : True,
    'omitQueryText' : False,
    'pack' : '',
    'freeSoundId' : ''}


guitarParams = params
guitarParams['queryText'] = 'guitar'

guitarParams['pack'] = 'ClassicalGuitar-multisampled'
sd.downloadFreesound(**guitarParams)

guitarParams['emptyDir'] = False
guitarParams['pack'] = 'acoustic_guitar'
sd.downloadFreesound(**guitarParams)
