
from apps.jwglxt.xkgl import vars
from common.actionPre import actionpre
def delCxBmAndXk(con):
    '''删除重修选课时又报名又选课情形'''
    con.execute(vars.delCxbmAndYxk)
    return 1

def upCxbj(con):
    '''更新重修标记'''
    con.execute(vars.updateCxbj)
    return 1

def upPkgl(con):
    '''配课管理分析语句'''
    for code in vars.pkgllist:
        con.execute(code)
        print('{}{}执行完成'.format('*'*30,code))
    return 1

def inZjxb(con):
    '''插入缺子教学班的学生名单'''
    con.execute(vars.insertFjxbOrZjxb)
    return 1

def xkglInterface(con,actionName=''):
    '''选课管理对外接口'''
    if actionName==actionpre.unique('delcxbmandxk'):
        if delCxBmAndXk(con):
            return '删除重修选课时既报名又选课的学生名单完成！'
    elif actionName==actionpre.unique('upcxbj'):
        if upCxbj(con):
            return '重修标记更新完成！'
    elif actionName==actionpre.unique('upPkgl'):
        if upPkgl(con):
            return (';'.join(vars.pkgllist)+'执行完成！')
    elif actionName==actionpre.unique('inZjxb'):
        if inZjxb(con):
            return '缺子教学班的学生名单补充完成！'
    else:
        pass