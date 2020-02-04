
from apps.jwglxt.xkgl import vars
from common.actionPre import actionpre
from common.fileAction.controls import fileInfo
import math

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

def expAllXkmd(con,maxPc):
    '''快速导出选课名单的详细信息'''
    content=[]
    content.append(['学年','学期','学号','姓名','学生学院','专业','班级','年级','课程名称','课程性质','任课教师信息','教学班名称（选课课号）'])
    xlsx=fileInfo('选课详细信息')
    xlsx.expXlsx(content=content)
    counts=con.execute(vars.preQuickExpXkmd)[0]
    if counts:
        counts=counts[0]
    indexs=math.ceil(counts/float(maxPc))
    for index in range(indexs):
        content=[]
        left=int(index*maxPc)
        right=int((index+1)*maxPc)
        content.extend(con.execute(vars.quickExpXkmd.format(left,right)))
        xlsx.expXlsx(content=content,mode='')
    return 1


def xkglInterface(con,actionName='',maxPc=30000):
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
    elif actionName==actionpre.unique('expAllXkmd'):
        if expAllXkmd(con,maxPc=maxPc):
            return '选课学年的选课名单已导出！'
    else:
        pass