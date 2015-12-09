import soundDownload as sd
import myFreesoundConfig as conf



def download():

    params = {
        'tag' : '',
        'duration' : (0,10),
        'API_Key' : conf.myAPI_Key,
        'outputDir' : conf.myOutputDir,
        'topNResults' : 100,
        'featureExt' : '.json',
        'preview' : True,
        'emptyDir' : False,
        'folderName' : 'clarinet',
        'pack' : '',
        'freeSoundId' : '',
        'noDownload': False}

    params['preview'] = False
    #params['noDownload'] = True

    # ["3", "4", "5"]
    params['topNResults'] = 3
    notes = ["%s%s%s" % (name, ext, oct) for name in ["C", "D", "E", "F", "G", "A", "B"] for ext in ["", "sharp"] for oct in ["3", "4", "5", "6"]]
    for note in notes:
        params['tag'] = "(%s clarinet single-note pabloproject)" % (note, )
        sd.downloadFreesound(**params)
