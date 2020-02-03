from apps.jwglxt.cjgl.jhscjgl import controls as jhscj
from common.actionPre import actionpre
from apps.jwglxt.cjgl import vars


def upXsCjjd(con,procname):
    '''更新学生成绩绩点'''
    if procname:
        con.execute(procname)
        return 1
    else:
        pass


def cjglInterface(con,actionName,jhscjFilePath,procname=vars.updateXsJd):
    if actionName==actionpre.unique('jhscjimp'):
        return jhscj.jhsCjInterface(con=con,xsFilePath=jhscjFilePath)
    elif actionName==actionpre.unique('upXsCjjd'):
        if upXsCjjd(con,procname):
            return '学生成绩绩点更新完成！'
    else:
        pass