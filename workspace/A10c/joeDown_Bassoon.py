import soundDownload as sd
import myFreesoundKey as secret

def download():

    myOutputDir = 'joeDown'

    bassoonParams = {
        'tag' : '',
        'duration' : (0,10),
        'API_Key' : secret.myAPI_Key,
        'outputDir' : myOutputDir,
        'topNResults' : 100,
        'featureExt' : '.json',
        'preview' : True,
        'emptyDir' : False,
        'folderName' : 'bassoon',
        'pack' : '',
        'freeSoundId' : ''}

    #bassoonParams['preview'] = False
    bassoonParams['queryText'] = 'bassoon'

    bassoonParams['pack'] = 'Bassoon: Fortissimo and Pianissimo samples G3'
    sd.downloadFreesound(**bassoonParams)

    bassoonParams['pack'] = 'Bassoon: Staccato Non Vibrato C2-C4'
    sd.downloadFreesound(**bassoonParams)

    bassoonParams['pack'] = 'Bassoon: Tenuto Non Vibrato C2-C4'
    sd.downloadFreesound(**bassoonParams)

    bassoonParams['pack'] = 'Bassoon: Tenuto Vibrato C2-C4'
    sd.downloadFreesound(**bassoonParams)
