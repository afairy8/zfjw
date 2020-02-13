import os

def clearEmpDir(basePath):
    '''待清理为空的文件夹'''
    for root,dir,files in os.walk(basePath,topdown=False):
        if not files:
            os.rmdir(root)

# clearEmpDir(r'D:\projects\zfjw\common\expfiles\mooc')