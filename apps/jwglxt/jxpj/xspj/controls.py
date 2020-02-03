from apps.jwglxt.jxpj.xspj import vars as xspjvar
from common.actionPre import actionpre

def delXsPjxx(con, minpf=60, qzDelLf60=0):
    '''删除学生评价
    （1.删除教学班、教师限制参评；2.删除学生被限制参评，具体教学班教师，3.删除学生被限制参评，全部）
    '''
    if con:
        con.execute(xspjvar.backXspj)  # 备份学生评价
        #print('备份学生评价likai_jw_pj_xspfb成功！')
        con.execute(xspjvar.delPjjxbXz)  ##删除评价教学班，教师限制；删除学生某个教学班、教师被限制参评
        con.execute(xspjvar.delcpxsxz)  ##删除参评学生限制中已评价的数据
        if con.currentZcXqj[0] >= 19 or qzDelLf60:  ##如果当前周次大于19或者是qzDelLf60，则执行删除低于minpf的数据
            con.execute(xspjvar.delPjlt60.format(str(minpf)))
        return 1


def addCpxsxz(con):
    '''添加学生评价限制，一门都没选，选了都是没模板的，选了的都被限制了'''
    if con:
        if con.currentZcXqj[0] >= 17:
            con.execute(xspjvar.insertCpxsxz)
            return 1


def getWccPjXs(con):
    '''获取未完成评价的学生人数'''
    if con:
        res = con.execute(xspjvar.getWpjXsNum)
        if not res:
            res=0
        return res


def roolbackXspj(con, xhlist=[]):
    '''退回具体的学生评价'''
    if xhlist:
        for xh in xhlist:
            con.execute(xspjvar.rollXspj.format(xh))
        return 1


def xspjInterface(con, switch='', qzDelLf60=0, xhlist=[]):
    '''对外接口'''
    if switch==actionpre.unique('getWccPjXs'):
        # if con.currentZcXqj >= 17:
        return '当前未评价的学生共有{}'.format(str(getWccPjXs(con)))
    elif switch == actionpre.unique('addCpxsxz'):
        if addCpxsxz(con):
            return '参评学生限制添加成功！'
    elif switch == actionpre.unique('delXsPjxx'):
        if delXsPjxx(con, qzDelLf60):
            return '备份学生评价likai_jw_pj_xspfb成功！无效评价学生信息删除成功'
    elif switch == actionpre.unique('roolbackXspj'):
        if roolbackXspj(con, xhlist):
            return '{}的评价信息退回成功！'.format(','.join(xhlist))
    else:
        return 'actionName={}不受支持！'.format(switch)
