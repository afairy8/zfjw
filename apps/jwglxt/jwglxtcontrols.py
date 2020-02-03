#encoding:utf-8
from common.actionPre import actionpre
from apps.jwglxt import jwglxtvar
from apps.jwglxt.jxpj.xspj import controls as xspj
from apps.jwglxt.jxpj.ldthddpj import controls as ldthpj
from apps.jwglxt.jxzxjh.kcth import controls as kctd
from apps.jwglxt.bysh import controls as bysh
from apps.jwglxt.jxrw import controls as jxrw
from apps.jwglxt.xkgl import controls as xkgl
from apps.jwglxt.xjgl import controls as xjgl
from apps.jwglxt.cjgl import controls as cjgl
from apps.jwglxt.kwgl import controls as kwgl
##
###actionName的格式为"操作1;操作2;"
# #########学生评价
def jwxtXspj(con,actionName=None,xhlist=None):
    '''学生评价'''
    if not actionName:
        actionName= jwglxtvar.xspjAction
    actionName=actionpre.actionList(actionName)
    L=[]
    for switch in actionName:
        if switch:
            if switch==actionpre.unique('addCpxsxz'):##,17周之后才开始添加参评学生限制
                if con.currentZcXqj[0]>=17:
                    L.append(xspj.xspjInterface(con, switch=switch, qzDelLf60=jwglxtvar.xspjQzDelLf60, xhlist=jwglxtvar.xspjRoolList))
            elif switch==actionpre.unique('delXsPjxx'):
                if con.currentZcXqj[0]==20:###20周删除学生
                    L.append(xspj.xspjInterface(con, switch=switch, qzDelLf60=jwglxtvar.xspjQzDelLf60, xhlist=jwglxtvar.xspjRoolList))
            elif switch==actionpre.unique('roolbackXspj'):
                if xhlist:##退回不受时间限制
                    L.append(xspj.xspjInterface(con, switch=switch, qzDelLf60=jwglxtvar.xspjQzDelLf60, xhlist=xhlist))
            elif switch==actionpre.unique('getWccPjXs'):
                if con.currentZcXqj[0]>=16:
                    L.append(xspj.xspjInterface(con, switch=switch, qzDelLf60=jwglxtvar.xspjQzDelLf60, xhlist=jwglxtvar.xspjRoolList))
            else:
                pass
    if L:
        return L
def jwxtLdThpj(con,actionName=None,LdThlist=None,jxbmc=None,pjsj=None,bpjgh=None,minpf=None):
    ##########领导、同行评价
    if not actionName:
        actionName= jwglxtvar.ldthAction
    actionName=actionpre.actionList(actionName)
    L=[]
    for switch in actionName:
        if switch:
            if switch==actionpre.unique('roolLdThpj'):
                if not minpf:
                    minpf=jwglxtvar.ldthRoollf
                L.append(ldthpj.LdThPjInterface(con=con, minpf=minpf
                                                , LdThlist=LdThlist, actionName=switch,jxbmc=jxbmc,pjsj=pjsj,bpjgh=bpjgh))
    if L:
        return L
def jwxtJxjh(con,actionName=None):
    '''课程替代'''
    if not actionName:
        actionName= jwglxtvar.jxzxjhAction
    actionName=actionpre.actionList(actionName)
    L=[]
    for switch in actionName:
        if switch:
            L.append(kctd.kctdInterface(con,actionName=switch))
    if L:
        return L
def jwxtBysh(con,njdm_id=None,jgmc=None,zyh=None,xslist=None,diff=10.0,type=None,actionName=None):
    '''
    毕业审核,actionName,课程替代触发学业完成进度审查,导出,执行部分学业完成情况审查
    常见用法：1-jwxtBysh(con,njdm_id='2018',diff=10.0,actionName='exp',type='xyjd')
    2-jwxtBysh(con,njdm_id='2018',actionName='导出',type='kcgs')
    3-jwxtBysh(con,actionName='课程替代')
    '''
    # actionName=actionName.strip().replace(' ','')
    if not actionName:
        actionName= jwglxtvar.byshAction
    actionName=actionpre.actionList(actionName)
    L=[]
    for switch in actionName:
        if switch:
            L.append(bysh.byshInterface(con=con,njdm_id=njdm_id,jgmc=jgmc,zyh=zyh,xslist=xslist,diff=diff,type=type,action=switch))
    if L:
        return L
def jwxtCjgl(con,actionName=None,jhscjFilePath=None):
    '''成绩管理'''
    if not actionName:
        actionName=jwglxtvar.cjglAction
    actionName=actionpre.actionList(actionName)
    L=[]
    for swith in actionName:
        if swith:
            L.append(cjgl.cjglInterface(con=con,actionName=swith,jhscjFilePath=jhscjFilePath))
    if L:
        return L
def jwxtXkgl(con,actionName=None):
    # actionName=actionName.strip().replace(' ','')
    if not actionName:
        actionName= jwglxtvar.xkglAction
    actionName=actionpre.actionList(actionName)
    L=[]
    for switch in actionName:
        if switch in [actionpre.unique('upcxbj'),actionpre.unique('delcxbmandxk') ]and (con.currentZcXqj[0]>=20 or con.currentZcXqj[0]<=7):
            L.append(xkgl.xkglInterface(con,actionName=switch))
        elif switch in [actionpre.unique('upPkgl')] and con.currentZcXqj[0]>=16:
            L.append(xkgl.xkglInterface(con, actionName=switch))
        elif switch:
            L.append(xkgl.xkglInterface(con, actionName=switch))
        else:
            pass
    if L:
        return L
def jwxtJxrw(con,actionName=''):
    '''教学任务更新'''
    if not actionName:
        actionName= jwglxtvar.jxrwAction
    actionName=actionpre.actionList(actionName)
    L=[]
    for switch in actionName:
        if switch:
            if switch==actionpre.unique('upxsdm'):
                L.append(jxrw.jxrwInterface(con,switch))
            else:
                if con.currentZcXqj[0] >= 16:
                    L.append(jxrw.jxrwInterface(con, switch))
    if L:
        return L
#########学籍管理中还可以补充无学籍等与学生选课之间的关系检测问题
def jwxtXjgl(con,actionName='',type=None,pk=None,zpPath=None):
    if not actionName:
        actionName=jwglxtvar.xjglAction
    actionName=actionpre.actionList(actionName)
    L=[]
    for switch in actionName:
        if switch:
            L.append(xjgl.xjglInterface(con=con,actionName=switch,type=type,pk=pk,zpPath=zpPath))
        else:
            pass
    if L:
        return L

def jwxtKwgl(con,actionName=''):
    if not actionName:
        actionName=jwglxtvar.kwglAction
    actionName=actionpre.actionList(jwglxtvar.kwglAction)
    L=[]
    for switch in actionName:
        if switch:
            if switch==actionpre.unique('upsfhk'):
                if con.currentZcXqj[0]<=1:
                    L.append(kwgl.kwglInterface(con, actionName=switch))
                else:
                    L.append('不在是否缓考更新的时间范围内')
            elif switch==actionpre.unique('upjkjgid'):
                L.append(kwgl.kwglInterface(con,actionName=switch))
            else:
                pass
        else:
            pass
    if L:
        return L