
from apps.jwglxt.jxzxjh.kcth import vars
from common.actionPre import actionpre
def upKctdDtly(con):
    ''''''
    con.execute(vars.initKctdMain)##首先将待审核课程替代的替代理由#之后的部分全部清空
    resData=con.execute(vars.getKctdMain)##获取待审核课程替代信息
    for res in resData:
        ##1、成绩、计划学分判断
        tdly=res[1]
        kctdid=res[0]
        cjxf=con.execute(vars.getKctdCj.format(kctdid))
        xh_id=cjxf[0][1]
        jhxf=con.execute(vars.getKctdJh.format(kctdid))
        tdly=tdly+'替代课程学分和：'+str(cjxf[0][2])+',被替代课程学分和：'+str(jhxf[0][2])
        ##2、当前修读信息
        dqxdzt=con.execute(vars.getXsDqxdZt.format(kctdid))
        tdly=tdly+',被替代课程中的当前修读课程为：'+dqxdzt[0][0]+','
        ##3、学生信息
        xsxx=con.execute(vars.getXsxx.format(xh_id))
        tdly=tdly+xsxx[0][0]
        ##3-1转专业、延长在读年限信息信息
        ydxx=con.execute(vars.getXsxjydxx.format(xh_id))
        if ydxx[0][0]>0:
            tdly=tdly+','+'转专业或延长在读年限：有'
        else:
            tdly=tdly+','+'转专业或延长在读年限：无'
        ##4、被替代课程中是否存在最晚转专业、延长在读年限之后的应修读信息
        zwzzzyczd=con.execute(vars.getZwZzyYczdxn.format(kctdid,xh_id,xh_id))
        tdly=tdly+',晚于异动生效学年学期的被替代课程：'+zwzzzyczd[0][0]+';'
        # print(vars.btdkExistsYxd.format(kctdid))
        tdly=tdly+con.execute(vars.tdkcExistsJhn.format(kctdid))[0][0]+';'+con.execute(vars.btdkExistsYxd.format(kctdid))[0][0]+'。'
        con.execute(vars.upKctdMain.format(tdly,kctdid))
    return 1
def kctdInterface(con,actionName=None):
    '''教学执行计划对外接口'''
    if actionName==actionpre.unique('upKctdDtly'):
        if upKctdDtly(con):
            return '课程替代理由补充完成!'