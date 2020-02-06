from common.fileAction import controls
import os
import shutil
classifyKeyWords=[
    '.xls',
    '.docx',
    '.exe',
    '.zip'
]

path=r'C:\Users\xjk-lenovo\Downloads'

def createDir(savepath=path):
    for word in classifyKeyWords:
        if not os.path.exists(os.path.join(savepath,word)):
            os.mkdir(os.path.join(savepath,word))

def classifyFiles(savepath=path):
    createDir(savepath)
    files=controls.pathCommon(path)['files']
    for file in files:
        for word in classifyKeyWords:
            if file.lower().find(word.lower())>=0:
                shutil.move(os.path.join(savepath,file),os.path.join(savepath,word))

classifyFiles(path)


