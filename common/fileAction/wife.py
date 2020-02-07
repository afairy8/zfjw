from common.fileAction import controls
import os
# from tkinter import *
# action=''##是否合并操作
# curr=''##是否只合并当前文件夹，为否，则合并当前文件夹以及子文件夹
# posix=''##合并方式，1，全部合并成一个工作表，2，每个工作薄作为结果表的一个sheet
# path=''###要合并的文件路径，或根路径
# resfileName=''
def merge(action,curr,posix,resfileName):
    if action=='merge':
        path=r'C:\Users\xjk-lenovo\Desktop\20191219交换生'
        resfile=controls.fileInfo(os.path.join(path,resfileName))
        content=[]
        if curr=='curr':
            pathfiles=os.listdir(path)
        else:
            pathfiles=controls.pathCommon(path)['files']
        if posix=='1':
            for pathfile in pathfiles:
                if pathfile.endswith('.xls'):
                    xlsx=controls.fileInfo(os.path.join(path,pathfile))
                    xlsx.xlsToXlsx()
                    xlsx=controls.fileInfo(os.path.join(path,pathfile+'x'))
                else:
                    xlsx=controls.fileInfo(os.path.join(path,pathfile))
                content=content+xlsx.getFileContent(sheetName=None,containTitle=True)
            resfile.expXlsx(content=content)
        elif posix=='2':
            for pathfile in pathfiles:
                if pathfile.endswith('.xls'):
                    xlsx=controls.fileInfo(os.path.join(path,pathfile))
                    xlsx.xlsToXlsx()
                    xlsx=controls.fileInfo(os.path.join(path,pathfile+'x'))
                else:
                    xlsx=controls.fileInfo(os.path.join(path,pathfile))
                content=xlsx.getFileContent(sheetName=None,containTitle=True)
                resfile.expXlsx(content=content,mode='',sheetName=pathfile.split('.')[0])
        else:
            pass
    elif action=='file':
        pass
    else:
        pass
    return 1


# merge('merge','curr','2','res')
