from tkinter import filedialog
import os
from eyed3 import mp3
import re
import subprocess
from pathvalidate import sanitize_filename

dir_mp3 = '~/OpenAudible/mp3'
files_mp3 = filedialog.askopenfilenames(title='Select mp3', defaultextension=['.mp3'], initialdir=dir_mp3)
for file_mp3 in files_mp3:
    if mp3.isMp3File(file_mp3):
        audioFile = mp3.Mp3AudioFile(file_mp3)
    else:
        raise ValueError('Not an mp3 file')

    title = audioFile.tag.title
    title_crop = title.replace(':', '_')[0:20]

    dir_lookup = '~/AppData/Local/Packages/AudibleInc.AudibleforWindowsPhone_xns73kv1ymhp2/LocalState/Content'
    dir_json = '~/AppData/Local/Packages/AudibleInc.AudibleforWindowsPhone_xns73kv1ymhp2/LocalState/filescache'

    files_lookup = os.listdir(dir_lookup)
    try:
        file_json = f'content_metadata_{[f[21:31] for f in files_lookup if title_crop in f][0]}.json'
    except:
        raise ValueError('Missing json, audiobook probably not downloaded')

    f_json = open(dir_json + '/' + file_json, encoding='utf8')
    raw_json = f_json.read()
    times = [int(t)/1000 for t in re.findall('"start_offset_ms":(\d{1,}),', raw_json)[1:]]
    titles = re.findall('"title":"([^}]{1,})"}', raw_json)
    titles = [t.replace('â€™', "'") for t in titles]

    dir_final = '~/Audiobooks/' + title.replace(':','_') + '/'
    dir_final = dir_final.replace("'", '')

    try:
        os.mkdir(dir_final)
    except FileExistsError:
        pass

    command = ['ffmpeg', '-i', "'" + file_mp3.replace('/', '\\') + "'", '-f', 'segment', '-segment_times', ','.join([str(t) for t in times]), '-c', 'copy', "'" + dir_final + '%03d.mp3' + "'"]
    command = ' '.join(command)
    print(command)
    os.system('pwsh.exe -Command ' + command)

    files_split = os.listdir(dir_final)
    for f in files_split:
        num = int(re.match('(\d{3}).mp3', f).group(1))
        # finalfile = dir_final + sanitize_filename(titles[num]) + '.mp3'
        # if sanitize_filename(titles[num]) + '.mp3' in os.listdir(dir_final):
        #     finalfile = finalfile[:-4] + ' (2).mp3'
        # os.rename(dir_final + f, finalfile)
        audioFile = mp3.Mp3AudioFile(dir_final + f)
        audioFile.tag.track_num = num+1
        audioFile.tag.title = titles[num]
        audioFile.tag.save()
