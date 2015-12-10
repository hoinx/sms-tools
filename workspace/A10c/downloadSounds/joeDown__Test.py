import soundDownload as sd
import myFreesoundConfig as conf


"""
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
"""




def downloadBassoon(testMode=False):

    params = {
        'tag' : '',
        'duration' : (0,10),
        'API_Key' : conf.myAPI_Key,
        'outputDir' : '../joeDown_Norm',
        'topNResults' : 100,
        'featureExt' : '.json',
        'preview' : False,
        'emptyDir' : False,
        'folderName' : 'bassoon',
        'pack' : '',
        'freeSoundId' : '',
        'normalizedDescriptors': True,
    }

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


def downloadGuitar(testMode=False):

    params = {
        'tag' : '',
        'duration' : (0,10),
        'API_Key' : conf.myAPI_Key,
        'outputDir' : '../joeDown_Norm',
        'topNResults' : 50,
        'featureExt' : '.json',
        'preview' : True,
        'emptyDir' : False,
        'folderName' : 'guitar',
        'pack' : '',
        'freeSoundId' : '',
        'normalizedDescriptors': True,
    }

    params['preview'] = False
    params['queryText'] = 'guitar'

    params['pack'] = 'ClassicalGuitar-multisampled'
    sd.downloadFreesound(**params)

    params['pack'] = 'acoustic_guitar'
    sd.downloadFreesound(**params)


downloadBassoon()
downloadGuitar()
