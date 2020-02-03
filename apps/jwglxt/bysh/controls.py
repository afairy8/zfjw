
from apps.jwglxt.bysh import  vars
from datetime import datetime
from common.fileAction.controls import fileInfo
from common.actionPre import actionpre
def callProc(con,procname,paras):
    ''''''
    try:
        con.execute(procname,[paras])
    except:
        print('{}执行{}失败'.format(paras[0],procname))

def getCallPrcoParas(con,procname=vars.procname,njdm_id=None,jgmc=None,zyh=None,xslist=None):
    ''''''
    if not xslist:
        queryString=vars.basicSelectXs
        if not njdm_id:
            bynd=con.execute(vars.bynd)
            njCondition=vars.extendNjConditon.format(bynd[0][0])
        else:
            njCondition=vars.basicNjCondition.format(njdm_id)
        if jgmc:
            jgCondition=vars.basicJgCondition.format(jgmc)
        else:
            jgCondition=vars.basicCondition1
        if zyh:
            zyCondition=vars.basicZyCondition.format(zyh)
        else:
            zyCondition=vars.basicCondition1
        queryString=queryString+njCondition+jgCondition+zyCondition+'\n order by xsj.jg_id,xsj.zyh_id,xsj.bh_id,xsj.xh'
        xslist=con.execute(queryString)
        for xh in xslist:
            callProc(con,procname,xh[0])
    else:
        if not isinstance(xslist,list):
            xslist=list(xslist)
        for xh in xslist:
            callProc(con=con,procname=procname,paras=xh)
    return 1

def inBysfzxxb(con):
    '''插入毕业生辅助信息表,添加删除毕业审核表、学位审核表'''
    bynd = con.execute(vars.bynd)
    for upxz in vars.upXz:
        con.execute(upxz)
    sfscjz=con.execute(vars.sfScjzBysfzxx)
    if sfscjz[0][0]==bynd[0][0]+';0':##不是首次加载
        con.execute(vars.ydInBysFzxxb.format(bynd[0][0],bynd[0][0]))
    else:
        con.execute(vars.inBysFzxxb.format(bynd[0][0],bynd[0][0]))
    con.execute(""
                "update likai_xtgl_xtszb set zdz='{}' where ZDM='{}' "
                "".format(bynd[0][0]+';0','BYSFZXXBSFSCJZ(@1)')
                )

    con.execute(vars.inbyshb.format(bynd[0][0]))
    con.execute(vars.inXwshb.format(bynd[0][0]))
    con.execute(vars.deByshb.format(bynd[0][0]))
    con.execute(vars.deXwshb.format(bynd[0][0]))
    return 1

def acitonByKctd(con):
    '''课程审核通过的学业完成情况重新审查'''
    today=datetime.now().strftime('%y-%d-%m')

    queryString=vars.kctdXySh.format(today)
    #queryString = vars.kctdXyShtmp
    res=con.execute(queryString)
    xslist=[]
    for data in res:
        xslist.append(data[0])
    if xslist:
        return getCallPrcoParas(con=con,xslist=xslist)
    else:
        print('今日目前无课程替代审核通过的学生信息！')
        return None

def exp(con,njdm_id,diff=10.0,type=''):
    '''导出进度误差'''
    res=None
    if njdm_id:
        getCallPrcoParas(con,njdm_id=njdm_id)
        if type.strip().lower()=='kcgs':
            getCallPrcoParas(con, njdm_id=njdm_id)
            pass###导出课程归属量
            title=(njdm_id+'学分要求节点名称','差额')
            content=[]
            content.append(title)
            res=con.execute(vars.getKcgsAndJsjy.format(njdm_id))
            content.extend(res)
            xlsx=fileInfo(njdm_id+'级课程归属教师教育差额')
            if xlsx.expXlsx(content=content):
                res=xlsx.fileName##expXls.exp(njdm_id+'课程归属教师教育差额',content=content)
        elif type.strip().lower()=='xyjd':
            ##导出血液进度误差与正常学生进度存在diff以上的学生
            title = ('学号', '姓名', '专业','年级','学习进度','班级','学院')
            content = []
            content.append(title)
            zyxx=con.execute(vars.getZyxx.format(njdm_id))
            # print(vars.getZyxx)
            for zyh_id in zyxx:
                if zyh_id[0] in ['0210']:
                    xyjd=con.execute(vars.getNormalJd.format(njdm_id,zyh_id[0]))
                    #print(vars.getNormalJd.format(njdm_id,zyh_id[0]))
                    #print(vars.getDiffXsxx.format(njdm_id,zyh_id[0],str(float(xyjd[0][3])-diff)))
                    diffxs=con.execute(vars.getDiffXsxx.format(njdm_id,zyh_id[0],str(float(xyjd[0][3])-diff)))
                    content.extend(diffxs)
            xlsx=fileInfo('{}级比正常进度晚{}个百分点的学生名单'.format(njdm_id,str(diff)))
            if xlsx.expXlsx(content=content):
                res=xlsx.fileName###expXls.exp(filename='{}级比正常进度晚{}个百分点的学生名单'.format(njdm_id,str(diff)),content=content)

        else:
            return res
        return res
    else:
        return res

def byshInterface(con,njdm_id,jgmc=None,zyh=None,xslist=None,diff=None,type='',action='',procname=vars.procname):
    '''毕业审核对外接口'''
    if action==actionpre.unique('acitonByKctd'):##'kctd':##课程替代学生学业完成情况审核
        if acitonByKctd(con):
            return '课程替代学业完成情况更新完成！'
    elif action==actionpre.unique('exp'):##导出
        res=exp(con=con,njdm_id=njdm_id,diff=diff,type=type)
        if res:
            return 'exp:{};xlsx文件完成,文件名:{}'.format(type,res)
        else:
            return 'njdm_id={}或type={}的导出功能不受支持'.format(njdm_id,type)
    elif action==actionpre.unique('getCallPrcoParas'):##单独执行学业完成情况审核
        if getCallPrcoParas(con=con,procname=procname,njdm_id=njdm_id,jgmc=jgmc,zyh=zyh
                         ,xslist=xslist):
            return '单独执行学业完成情况审核成功！'
    elif action==actionpre.unique('inBysfzxxb'):
        if inBysfzxxb(con):
            return '毕业生辅助信息补充完成！'
    else:
        pass
