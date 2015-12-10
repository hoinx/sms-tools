import os, sys
import freesound as fs
import json

descriptors = [ 'lowlevel.spectral_centroid.mean',
                'lowlevel.spectral_contrast.mean',
                'lowlevel.dissonance.mean',
                'lowlevel.hfc.mean',
                'lowlevel.mfcc.mean',
                'sfx.logattacktime.mean',
                'sfx.inharmonicity.mean']

# ---------------------------------------------------------------------------------------------
def inParenthesis(str):
    return str.startswith('(') and str.endswith(')')

# ---------------------------------------------------------------------------------------------
def appendQuery(filter, key, value):
    if not value or not type(value) == str:
        return filter
    if not filter == "":
        filter += (' ')
    filter += (key+": ")
    if inParenthesis(value):
        filter += (value)
        return filter
    filter += ("\""+value+"\"")
    return filter

# ---------------------------------------------------------------------------------------------
def appendRangeQuery(filter, key, duration):
    if not duration or not type(duration) == tuple:
        return filter
    if not filter == "":
        filter += (' ')
    filter += (key+":[" + str(duration[0]) + " TO " + str(duration[1]) + "]")
    return filter

# ---------------------------------------------------------------------------------------------
def downloadFreesound(
        queryText = '',         tag=None,
        duration = None,        API_Key = '',
        outputDir = '',         topNResults = 5,
        featureExt = '.json',   preview=True,
        emptyDir=False,         folderName = '',
        pack='',                freeSoundId='',
        noDownload=False,       normalizedDescriptors=True):

    """
    This function downloads sounds and their descriptors from freesound using the queryText and the
    tag specified in the input. Additionally, you can also specify the duration range to filter sounds
    based on duration.

    Inputs:
        (Input parameters marked with a * are optional)

        queryText (string): query text for the sounds (eg. "violin", "trumpet", "cello", "bassoon" etc.)
        tag* (string): tag to be used for filtering the searched sounds. (eg. "multisample",
                       "single-note" etc.)
        duration* (tuple): min and the max duration (seconds) of the sound to filter, eg. (0.2,15)
        API_Key (string): your api key, which you can obtain from : www.freesound.org/apiv2/apply/
        outputDir (string): path to the directory where you want to store the sounds and their
                            descriptors
        topNResults (integer): number of results(sounds) that you want to download
        featureExt (string): file extension for storing sound descriptors
        preview* (boolean): if true low quality sound is downloaded, if false high quality
        emptyDir* (boolean): if true the directory of name <queryText> will be deleted, if false
                            downloaded sounds will bee added and the file list will be appended
        folderName* (string): the queryText was also used to give the download folder a name,
                                 setting this parameter has precedence and the query string can be empty
        pack* (string): filtering for freesound pack names
        freeSoundId* (string): download a sound using its freesound-id
        noDownload* (boolean): if true only the sound list will be printed
    output:
        This function downloads sounds and descriptors, and then stores them in outputDir. In
        outputDir it creates a directory of the same name as that of the queryText. In this
        directory outputDir/queryText it creates a directory for every sound with the name
        of the directory as the sound id. Additionally, this function also dumps a text file
        containing sound-ids and freesound links for all the downloaded sounds in the outputDir.
        NOTE: If the directory outputDir/queryText exists, it deletes the existing contents
        and stores only the sounds from the current query.
    """

    if (queryText == "" and folderName == "") or API_Key == "" or outputDir == "" or not os.path.exists(outputDir):
        print "\n"
        print "Error: Wrong parameters"
        return -1

    # Setting up the Freesound client and the authentication key
    fsClnt = fs.FreesoundClient()
    fsClnt.set_token(API_Key,"token")

    page_size = 30

    filter = ""
    filter = appendQuery(filter, "tag", tag)
    filter = appendRangeQuery(filter, "duration", duration)
    filter = appendQuery(filter, "pack", pack)
    filter = appendQuery(filter, "id", freeSoundId)

    fields = 'id,name,username,url'
    if noDownload:
        fields += ',tags'
    else:
        fields += ',previews,analysis'

    search = {'sort': 'score',
              'fields': fields,
              'page_size': page_size,
              'normalized': 1}

    if not noDownload:
        search['descriptors'] = ','.join(descriptors)

    if not queryText == "":
        search['query'] = queryText

    if not filter == "":
        search['filter'] = filter

    if not normalizedDescriptors:
        search['normalized'] = 0

    qRes = fsClnt.text_search(**search) # Querying Freesound

    pageNo = 1
    sndCnt = 0
    indCnt = 0
    totalSnds = min(qRes.count,200)   # System quits after trying to download after 200 times

    print "Found %s sounds:" % (str(qRes.count), )
    if noDownload:
        if qRes.count == 0:
            return

        while True:

            if indCnt >= totalSnds:
                print "Not able to list required number of sounds..."
                return

            sound = qRes[indCnt - ((pageNo-1)*page_size)]
            tags = ','.join(sound.tags)
            print "Found [id: %s], [name: %s], [url: %s], [tags: %s]" % (str(sound.id), sound.name, sound.url, tags)

            indCnt +=1
            sndCnt +=1

            if indCnt%page_size==0:
                qRes = qRes.next_page()
                pageNo+=1

            if sndCnt>=topNResults:
                break

        return



    if folderName == "":
        folderName = queryText

    outDir2 = os.path.join(outputDir, folderName)
    if os.path.exists(outDir2):
        if emptyDir:
            os.system("rm -r " + outDir2)
            os.mkdir(outDir2)
    else:
        os.mkdir(outDir2)

    # Creating directories to store output and downloading sounds and their descriptors
    downloadedSounds = []
    while True:

        if indCnt >= totalSnds:
            print "Not able to download required number of sounds..."
            break

        sound = qRes[indCnt - ((pageNo-1)*page_size)]
        print "Downloading mp3 and descriptors for sound with [id: %s], [name: %s], [url: %s]" % (str(sound.id), sound.name, sound.url)
        outDir1 = os.path.join(outputDir, folderName, str(sound.id))

        if os.path.exists(outDir1):
            os.system("rm -r " + outDir1)

        os.system("mkdir " + outDir1)

        soundPreview = sound.previews.preview_hq_mp3
        if preview:
            soundPreview = sound.previews.preview_lq_mp3

        mp3Path = os.path.join(outDir1, str(soundPreview.split("/")[-1]))
        ftrPath = mp3Path.replace('.mp3', featureExt)

        try:
            param = {'client': fsClnt, 'path': mp3Path, 'url': soundPreview}

            fs.FSRequest.retrieve(**param)

            features = {} # Initialize a dictionary to store descriptors
            for desc in descriptors:
                features[desc]=[]
                features[desc].append(eval("sound.analysis."+desc))

            json.dump(features, open(ftrPath,'w')) # store them in a json file
            sndCnt+=1
            downloadedSounds.append([str(sound.id), sound.url])

        except:
            if os.path.exists(outDir1):
                os.system("rm -r " + outDir1)

        indCnt +=1

        if indCnt%page_size==0:
            qRes = qRes.next_page()
            pageNo+=1

        if sndCnt>=topNResults:
            break

        # Dump the list of files and Freesound links
        fid = open(os.path.join(outDir2, folderName+'_SoundList.txt'), 'ab+')
        fid.seek(0, 1) # seek end
        for elem in downloadedSounds:
            fid.write('\t'.join(elem)+'\n')
        fid.close()
