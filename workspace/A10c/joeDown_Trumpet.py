import soundDownload as sd
import myFreesoundKey as secret

myOutputDir = 'joeDown'

trumpetParams = {
    'tag' : '',
    'duration' : (0,10),
    'API_Key' : secret.myAPI_Key,
    'outputDir' : myOutputDir,
    'topNResults' : 100,
    'featureExt' : '.json',
    'preview' : True,
    'emptyDir' : False,
    'folderName' : 'trumpet',
    'pack' : '',
    'freeSoundId' : '',
    'noDownload': False}

trumpetParams['preview'] = False
#trumpetParams['noDownload'] = True

notes = ["%s%s%s" % (name, ext, oct) for name in ["C", "D", "E", "F", "G", "A", "B"] for ext in ["", "sharp"] for oct in ["4", "5"]]
for note in notes:
    trumpetParams['tag'] = "(%s trumpet single-note pabloproject)" % (note, )
    sd.downloadFreesound(**trumpetParams)


