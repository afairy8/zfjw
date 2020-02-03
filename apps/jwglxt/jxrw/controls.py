from apps.jwglxt.jxrw import vars
from common.actionPre import actionpre


def upXsdm(con):
    '''补充教学任务中的学时代码'''
    con.execute(vars.upRwXsdm)
    return 1


def upRwBaseInfo(con):
    '''更新开课类型为10的课程类别，课程性质，课程归属'''
    # test=con.objectExists('likai_jw_txkcxzandgs')
    if con.objectExists('likai_jw_txkcxzandgs')[0][0]:
        con.execute(vars.dropKklx10TmpTable)
    con.execute(vars.createKKlx10TmpTable)
    con.execute(vars.upDateRwKklx10BaseInfo)
    con.execute(vars.dropKklx10TmpTable)
    ###update sfkxk='1'
    con.execute(vars.upxkbjSfkxk)
    return 1

def upRwCxbmkg(con):
    '''更新重修报名开关'''
    con.execute(vars.upCxbmKg)
    return 1

def inRwBklxXsmd(con):
    '''插入任务学生板块类型对照'''
    con.execute(vars.insertBkxsmd)
    return 1
def upMxdx(con):
    '''处理面向对象'''
    pass
    con.execute(vars.xbYtkMxdx)
    con.execute(vars.upMxdxXslb)
    return 1

def jxrwInterface(con, actionName=''):
    '''教学任务对外接口'''
    if actionName == actionpre.unique('upXsdm'):
        if upXsdm(con):
            return '教学任务学时代码更新完成！'
    elif actionName == actionpre.unique('upRwBaseInfo'):
        if upRwBaseInfo(con):
            return '开课类型为10的任务基础,sfkxk标记更新完成信息更新完成！'
    elif actionName==actionpre.unique('uprwcxbmkg'):
        if upRwCxbmkg(con):
            return '重修报名开关更新完成！'
    elif actionName==actionpre.unique('inRwBklxXsmc'):
        if inRwBklxXsmd(con):
            return '板块类型学生名单补充完成！'
    elif actionName==actionpre.unique('upMxdx'):
        if upMxdx(con):
            return '小班等面向对象处理完成！'
    else:
        return '{}不支持'.format(actionName)
