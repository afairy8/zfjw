import os
import shutil
def clearEmpDir(basePath):
    '''待清理为空的文件夹'''
    for root,dir,files in os.walk(basePath,topdown=False):
        #print('root={},dir={},files={}'.format(root,dir,files))
        if not files and not dir:
            #print(root)
            os.system('icacls {} /grant wlzx:F'.format(root))
            #os.rmdir(root)
        else:
            print('{} pass'.format(root))

#clearEmpDir(r'D:\projects\zfjw\common\expfiles\mooc')