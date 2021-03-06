import soundDownload as sd
import myFreesoundConfig as conf

def download(testMode=False):

    params = {
        'tag' : '',
        'duration' : (0,10),
        'API_Key' : conf.myAPI_Key,
        'outputDir' : conf.myOutputDir,
        'topNResults' : 100,
        'featureExt' : '.json',
        'preview' : False,
        'emptyDir' : False,
        'folderName' : 'bassoon',
        'pack' : '',
        'freeSoundId' : ''}

    params['noDownload'] = testMode

    params['queryText'] = 'bassoon'

    params['pack'] = 'Bassoon: Fortissimo and Pianissimo samples G3'
    sd.downloadFreesound(**params)

    params['pack'] = 'Bassoon: Staccato Non Vibrato C2-C4'
    sd.downloadFreesound(**params)

    params['pack'] = 'Bassoon: Tenuto Non Vibrato C2-C4'
    sd.downloadFreesound(**params)

    params['pack'] = 'Bassoon: Tenuto Vibrato C2-C4'
    sd.downloadFreesound(**params)
