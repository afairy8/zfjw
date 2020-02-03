from apps.jwglxt.kwgl import vars
from common.actionPre import actionpre


def upJkjgid(con):
    '''更新监考学院'''
    con.execute(vars.upJkjg)
    return 1

def upSfhk(con):
    '''更新是否缓考标记'''
    con.execute(vars.upSfhk)
    return 1


def kwglInterface(con,actionName):
    if actionName==actionpre.unique('upjkjgid'):
        if upJkjgid(con):
            return '监考学院按考试人数已更新完成!'
    elif actionName==actionpre.unique('upSfhk'):
        if upSfhk(con):
            return '补考名单中是否缓考标记更新完成！'
    else:
        pass