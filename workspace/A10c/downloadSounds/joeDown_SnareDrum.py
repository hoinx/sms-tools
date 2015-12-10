import soundDownload as sd
import myFreesoundConfig as conf

def download(testMode=False):

    params = {
        'tag' : '',
        'duration' : (0,10),
        'API_Key' : conf.myAPI_Key,
        'outputDir' : conf.myOutputDir,
        'topNResults' : 10,
        'featureExt' : '.json',
        'preview' : False,
        'emptyDir' : False,
        'folderName' : 'snare_drum',
        'pack' : '',
        'freeSoundId' : ''}

    params['noDownload'] = testMode
    if testMode:
        params['topNResults'] = 1

    params['tag'] = '(snare drum 1-shot)'

    packs = ["Snaredrum-13x03inchPearl-MediumLowPitch-multisampled",
        "Snaredrum-13x03inchPearl-LowPitch-multisampled",
        "Snaredrum-14x08inchTama-HighPitch-multisampled",
        "Snaredrum-14x08inchTama-MediumHighPitch-multisampled",
        "Snaredrum-14x08inchTama-MediumPitch-multisampled",
        "Snaredrum-14x08inchTama-MediumLowPitch-multisampled",
        "Snaredrum-14x08inchTama-VeryLowPitch-multisampled",
        "Snaredrum-13x03inchPearl-VeryHighPitch-multisampled",
        "Snaredrum-13x03inchPearl-HighPitch-multisampled",
        "Snaredrum-13x03inchPearl-MediumHighPitch-multisampled"]

    for pack in packs:
        params['pack'] = pack
        sd.downloadFreesound(**params)

#download(testMode=True)