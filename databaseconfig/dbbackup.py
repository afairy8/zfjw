import os
from databaseconfig import connectString as cs
from datetime import datetime
# path=os.path.join(os.getcwd(),datetime.now().strftime('%Y-%m-%d')+'.dmp')
# params='''
# owner=(gzdx_jw_user)
# '''
# # backCom='''exp {} {} {}'''.format(cs.appBksJw,path,params)
# backCom=('exp'+' '+cs.appBksJw+" file='"+path+"' "+params+' ').replace('\n',' ')
# print(backCom)
# #os.system(backCom)



##https://www.cnblogs.com/wuzhiblog/p/python_zip.html
import zipfile
backPath='D:\\oracleback'
# files=os.listdir(backPath)
# # for file in files:
# #     #print(file.lower())
# #     print(os.path.join(backPath,file.replace('dmp','zip').replace('DMP','zip')))
# #     # z=zipfile.ZipFile(
# #     #     file=os.path.join(backPath,file.replace('dmp','zip').replace('DMP','zip'))
# #     #     ,mode='w'
# #     # ,allowZip64=True)
# #     # z.write(os.path.join(backPath,file))
# #     # z.close()
# #     print('-----')


# 1-备份数据库
# 2-遍历备份目录下，列举出备份目录下的文件
# 3-如果备份目录下不存在当前文件的zip文件，则创建压缩，否则忽略；

def backup():
    pass

def createZip(dmpFile=''):
    file=dmpFile.replace('DMP','zip').replace('dmp','zip')
    if not os.path.exists(file):
        zip=zipfile.ZipFile(
            file=file
            ,mode='w'
            ,allowZip64=True
        )
        zip.write(dmpFile)
        zip.close()

def backMain():
    filelist=os.listdir(backPath)
    for file in filelist:
        if file.upper().endswith('.DMP'):
            createZip(os.path.join(backPath,file))


backMain()