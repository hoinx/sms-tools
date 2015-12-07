import soundDownload as sd
import myFreesoundKey as secret

myOutputDir = 'joeDown'

guitarParams = {
    'tag' : '',
    'duration' : (0,10),
    'API_Key' : secret.myAPI_Key,
    'outputDir' : myOutputDir,
    'topNResults' : 50,
    'featureExt' : '.json',
    'preview' : True,
    'emptyDir' : False,
    'folderName' : 'guitar',
    'pack' : '',
    'freeSoundId' : ''}

guitarParams['preview'] = False
guitarParams['queryText'] = 'guitar'

guitarParams['pack'] = 'ClassicalGuitar-multisampled'
sd.downloadFreesound(**guitarParams)

guitarParams['pack'] = 'acoustic_guitar'
sd.downloadFreesound(**guitarParams)
