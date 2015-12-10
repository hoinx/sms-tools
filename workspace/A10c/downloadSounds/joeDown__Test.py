import soundDownload as sd
import myFreesoundConfig as conf

def download(testMode=False):

    """

    :param testMode:
    :return:
    """

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

    params = {
        'tag' : '',
        'duration' : (0,10),
        'API_Key' : conf.myAPI_Key,
        'outputDir' : '../joeTestOut',
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






download()
