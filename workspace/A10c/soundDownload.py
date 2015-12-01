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

#---------------------------------------------------------------------------------------------
def downloadFreesound(
		queryText = '',         tag=None,
		duration = None,        API_Key = '',
		outputDir = '',         topNResults = 5,
		featureExt = '.json',   preview=True,
		emptyDir=False,         omitQueryText=False,
        pack='',                freeSoundId=''):

    if queryText == "" or API_Key == "" or outputDir == "" or not os.path.exists(outputDir):
        print "\n"
        print "Error: Wrong parameters"
        return -1

    # Setting up the Freesound client and the authentication key
    fsClnt = fs.FreesoundClient()
    fsClnt.set_token(API_Key,"token")

    page_size = 30

    filter = ""
    if tag and type(tag) == str:
        flt_tag = "tag:\""+tag+"\""
        filter += flt_tag

    if duration and type(duration) == tuple:
        flt_dur = "duration:[" + str(duration[0])+ " TO " +str(duration[1]) + "]"
        if not filter == "":
            filter += ' '
        filter += flt_dur

    if pack and type(pack) == str:
        flt_pack = "pack:\""+pack+"\""
        if not filter == "":
            filter += ' '
        filter += flt_pack

    if freeSoundId and type(freeSoundId) == str:
        flt_freeSoundId = "id:\""+freeSoundId+"\""
        if not filter == "":
            filter += ' '
        filter += flt_freeSoundId

    search = {'sort':'score',
              'fields':'id,name,previews,username,url,analysis',
              'descriptors':','.join(descriptors),
              'page_size':page_size,
              'normalized':1}

    if not omitQueryText:
        search['query'] = queryText

    if not filter == "":
        search['filter'] = filter

    qRes = fsClnt.text_search(**search) # Querying Freesound

    outDir2 = os.path.join(outputDir, queryText)
    if os.path.exists(outDir2):
        if emptyDir:
            os.system("rm -r " + outDir2)
            os.mkdir(outDir2)
    else:
        os.mkdir(outDir2)

    pageNo = 1
    sndCnt = 0
    indCnt = 0
    totalSnds = min(qRes.count,200)   # System quits after trying to download after 200 times

    # Creating directories to store output and downloading sounds and their descriptors
    downloadedSounds = []
    while(1):

        if indCnt >= totalSnds:
            print "Not able to download required number of sounds..."
            break

        sound = qRes[indCnt - ((pageNo-1)*page_size)]
        print "Downloading mp3 and descriptors for sound with id: %s"%str(sound.id)
        outDir1 = os.path.join(outputDir, queryText, str(sound.id))

        if os.path.exists(outDir1):
            os.system("rm -r " + outDir1)

        os.system("mkdir " + outDir1)

        mp3Path = os.path.join(outDir1, str(sound.previews.preview_lq_mp3.split("/")[-1]))
        ftrPath = mp3Path.replace('.mp3', featureExt)

        try:
            param = {'client':fsClnt, 'path':mp3Path, 'url':sound.previews.preview_hq_mp3}
            if preview:
                param['url'] = sound.previews.preview_lq_mp3

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
        fid = open(os.path.join(outDir2, queryText+'_SoundList.txt'), 'ab+')
        fid.seek(0, 1) # seek end
        for elem in downloadedSounds:
            fid.write('\t'.join(elem)+'\n')
        fid.close()

