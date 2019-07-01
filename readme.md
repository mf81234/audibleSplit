# audibleSplit

This is a rough tool to overcome the inaccuracies in existing methods for splitting Audible audiobooks. Most tools use the chapter marks embedded, which aren't always accurate. The Audible app from the Windows Store uses separate JSON files to store chapter details. These are used to more accurately split chapters.

## Requirements
* Python 3 (Use pip to install modules from requirements.txt)
* Audible App (Windows Store)
* OpenAudible (To download higher bitrate MP3s)
* ffmpeg (To split the MP3s)