from common.fileAction import controls
import os
action=''##是否合并操作
curr=''##是否只合并当前文件夹，为否，则合并当前文件夹以及子文件夹
posix=''##合并方式，1，全部合并成一个工作表，2，每个工作薄作为结果表的一个sheet
path=''###要合并的文件路径，或根路径
resfileName=''

if action=='merge':
    resfile=controls.fileInfo(os.path.join(path,resfileName))
    content=[]
    if curr:
        pathfiles=os.listdir(path)
    else:
        pathfiles=controls.pathCommon(path)['files']
    if posix=='1':
        for pathfile in pathfiles:
            xlsx=controls.fileInfo(os.path.join(path,pathfile))
            content=content+xlsx.getFileContent(sheetName=None,containTitle=True)
        resfile.expXlsx(content=content)
    elif posix=='2':
        for pathfile in pathfiles:
            xlsx=controls.fileInfo(pathfile)
            content=xlsx.getFileContent(sheetName=None,containTitle=True)
            resfile.expXlsx(content=content,mode='',sheetName=pathfile.split('.')[0])
    else:
        pass
elif action=='file':
    pass
else:
    pass
