from apps.jwglxt.xjgl import vars
from common.fileAction.controls import fileInfo
from common.actionPre import actionpre
import os
def getZdTzXsxx(con,zjhmQzm=None,sydKeyWors=None):
    '''导出符合条件的证件前缀码，或生源地满足要求的'''
    if not zjhmQzm:
        zjhmQzm='%'
    if not sydKeyWors:
        sydKeyWors='%'
    L=[]
    title = ('学号', '姓名', '学院', '专业', '班级', '年级', '生源地', '证件号码前六位')
    L.append(title)
    res=con.execute(vars.getZdTzXs.format(zjhmQzm,sydKeyWors))
    for data in res:
        L.append(data)
    #expXls.exp(filename=sydKeyWors,content=L)
    xlsx=fileInfo(sydKeyWors+'学生')
    return xlsx.expXlsx(content=L)

def findZp(con,path,level=0):
    L=[]
    dirs=os.listdir(path)
    for dir in dirs:
        dirpath=os.path.join(path,dir)
        if os.path.isdir(dirpath):
            findZp(con,dirpath,level=level+1)
        else:
            if dirpath.split('.')[-1].lower() in ['jpg','jpeg','png']:
                f=open(dirpath,'rb')
                clobdata=f.read()
                f.close()
                filename=os.path.split(dirpath)[1].split('.')[0]
                L.append((filename,clobdata))
    if L:
        if con.objectExists('zpb')[0][0]:
            con.execute(vars.dropZpb)
        con.execute(vars.createZpb)
        con.execute(vars.insertZp,L)
    return 1

def imZp(con,type='rhxzp',pk='zjhm',path=''):
    '''
    导入照片
    :param con:
    :param type: type is rhxzp or byzp;
    :param pk: pk is the primary key to join the student and photo ,is zjhm or xh
    :param path: the path of photos has been saved path;
    :return: 1 Success!
    '''
    res=1
    if findZp(con=con,path=path):
        exceptionXs=con.execute(vars.checkCode)
        if exceptionXs:
            xlsx=fileInfo('文件名匹配不上的学生信息')
            title=('文件名')
            content=[]
            content.append(title)
            content.extend(exceptionXs)
            xlsx.expXlsx(content=content)
            print('存在不匹配的文件名，信息已导出在{}'.format(xlsx.fileName))
        if pk=='zjhm':
            if type=='rxhzp':
                con.execute(vars.rxhZjhmCode)
            elif type=='byzp':
                con.execute(vars.byZjhmCode)
            else:
                res=None
        elif pk=='xh':
            if type=='rxhzp':
                con.execute(vars.rxhXhCode)
            elif type=='byzp':
                con.execute(vars.byXhCode)
            else:
                res=None
        else:
            res=None
    else:
        res=None
    return res

def xjglInterface(con,actionName='',type=None,pk=None,zpPath=None):
    if actionpre.unique('imZp')==actionName:
        if type in ['rxhzp','byzp'] and pk in ['zjhm','xh'] and zpPath:
            if imZp(con=con,type=type,pk=pk,path=zpPath):
                return 'type={},,pk={}照片导入成功,如有异常文件，请检查异常文件！'
        else:
            return '导入照片,参数type={},pk={},zpPath={}输入有误'.format(type,pk,zpPath)
    elif actionpre.unique('getZdTzXsxx')==actionName:
        pass
    else:
        pass