import soundDownload as sd
import myFreesoundKey as secret

def download():

    myOutputDir = 'joeDown'

    violinParams = {
        'tag' : '',
        'duration' : (0,10),
        'API_Key' : secret.myAPI_Key,
        'outputDir' : myOutputDir,
        'topNResults' : 100,
        'featureExt' : '.json',
        'preview' : True,
        'emptyDir' : False,
        'folderName' : 'violin',
        'pack' : '',
        'freeSoundId' : ''}

    violinParams['preview'] = False
    violinParams['queryText'] = 'violin'
    violinParams['pack'] = 'Violin: Single notes Tenuto Non Vibrato G4-G5'
    sd.downloadFreesound(**violinParams)

    violinParams['pack'] = 'Violin: Single notes Tenuto Vibrato G4-G5'
    sd.downloadFreesound(**violinParams)

    violinParams['pack'] = ''
    violinParams['tag'] = '(violin AND single-note AND mf)'
    sd.downloadFreesound(**violinParams)
