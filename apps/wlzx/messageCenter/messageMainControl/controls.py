
from apps.wlzx.messageCenter.messageInterface import send
from apps.wlzx.messageCenter.messageMainControl import commonfunc as connat, vars as gv
from common.fileAction.controls import fileInfo
import datetime
import uuid

def getBaseQuery(xxlx):
    queryString=''
    if xxlx in ['01','01_jJR','18']:
        queryString=gv.getNextDayKbCode
    if xxlx=='02':
        queryString=gv.getNextDayXsKbCode
    if xxlx=='03':
        queryString=gv.getXjYdxxCode
    if xxlx=='04':
        queryString=gv.getCdJyCode
    if xxlx=='05':
        queryString=gv.getXsKsCode
    if xxlx=='06':
        queryString=gv.getJsJkCode
    if xxlx=='07':
        queryString=gv.getJsTtkCode
    if xxlx=='08':
        queryString =gv.getXsTtkCode
    if xxlx=='09':
        queryString=gv.getXsHkCode
    if xxlx=='031':
        queryString=gv.getXjYdxxCode031
    if xxlx=='10':
        queryString=gv.getNjBxKcTxCode
    if xxlx=='11':
        queryString=gv.getJsLrCjTxCode
    if xxlx=='12':
         queryString=gv.getXscjCode
    if xxlx=='13':
        queryString=gv.getXsWlspk
    if xxlx=='14':
        queryString=gv.getXsXyYjCode
    if xxlx=='15':
        queryString=''
    if xxlx=='16':
        queryString=gv.getJsTkKcxx
    if xxlx=='091':#学生缓考消息待审核消息发学院
        queryString=gv.getXsHktoXyCode
    if xxlx=='19':#邀请教师完善研究方向、个人简介
        queryString=gv.getNotJsjjOrYjfx
    if xxlx=='20':#学生评价未完成
        queryString=gv.getXsPjWwc
    if xxlx.lower()=='cjxg01':
        queryString=gv.cjXgShtoDepaAdmin
    if xxlx.lower()=='xjyddshxy':
        queryString=gv.getXjydDshFxXy
    # print('xxlx={}'.format(xxlx)+'*'*15+queryString+'\n'+'*'*30)
    return queryString

def sfJjr(con,txTime):
    '''判断日期是否节假日,如果是则返回替代日期，否则返回相应日期'''
    queryString=gv.getJjrTdrq.format(txTime)
    res=con.execute(queryString)
    tdrq=txTime
    if res:
        tdrq=res[0][0]
    return tdrq


def getNextDay(jgDay):
    '''获取发送消息的目标日期'''
    '''jgDay指目标日期与当前时间的间隔天数'''
    '''节假日课表替换可在此处设置'''
    if isinstance(jgDay,int):
        nowTime = datetime.datetime.now()
        txTime = (nowTime + datetime.timedelta(days=jgDay)).strftime('%Y-%m-%d')
    else:
        txTime=jgDay
    return txTime

def getZcXqj(con,jgDay):
    '''获取校历，元组（周次，星期几）,只返回第一行'''
    if isinstance(jgDay,int):#传递的是整数，间隔日期
        queryString=gv.getXtZcXqjSqlCode.format(getNextDay(jgDay))
    else:#传递的是实际日期
        queryString=gv.getXtZcXqjSqlCode.format(jgDay)
    data = con.execute(queryString)[0]
    return data


def setContentTemplate(xxlx):
    '''返回消息模板'''
    contentTemplate=''
    if xxlx=='01':
        contentTemplate="{}老师，您好！{}日（第{}周，星期{}），第{}，请您按时在{}，{}，{}室给{}讲授《{}》课程。详情可登陆教务系统查询，祝您工作愉快！"
    elif xxlx=='02':
        contentTemplate="{}同学，您好！{}日（第{}周，星期{}），第{}，请您按时在{}，{}室上《{}》课程。详情可登陆教务系统查询，祝您学习愉快！"
    elif xxlx=='031':
        contentTemplate="{}同学,您好!您办理的 “{}”,{}"
    elif xxlx=='03':
        contentTemplate="{}老师，您好！您学院的{}同学办理的“{}”，{}，请关注该生的课表情况。祝您工作愉快！"
    elif xxlx=='04':
        contentTemplate="{}您好!您申请使用的{},第{}周，星期{} 第{}节，{}。详情可登陆教务系统查询，祝您工作愉快！"
    elif xxlx=='05':
        contentTemplate="{}同学,您好!您所修《{}》课程的考试时间为：{}，考试地点为{}，请携带相关证件准时参加，遵守考场纪律，考试作弊取消学位。详情可登陆教务系统查询，祝您学习愉快！"
    elif xxlx=='06':
        contentTemplate="{}老师，您好！请您准时在{}，{}，监考《{}》课程！温馨提醒：要先领试卷与考生签名表（广州大学考场记录单）;监考期间全程录像，请您认真履行监考规定，不做与监考无关的事情，如看手机或打电话等！祝您工作愉快！"
    elif xxlx=='07':
        contentTemplate="{}（课程：《{}》），{}。详细课表信息可登陆教务系统查询，祝您工作愉快！"
    elif xxlx=='08':
        contentTemplate="{}同学，您好！您的{}，详细课表信息可登陆教务系统查询，祝您学习愉快！"
    elif xxlx=='09':
        contentTemplate="{}同学，您好!您{}，{}，详情可登陆教务系统查询，祝您学习愉快！"
    elif xxlx=='10':
        contentTemplate="温馨提醒：{}同学，您好！根据您的年级专业教学计划，您还有{}等必修课程未选！如上述课程已选或已获学分，请忽略，学期应选课程要求，学分要求等可以向学生所在学院教学办公室联系，祝您学习愉快!"
    elif xxlx=='11':
        contentTemplate="温馨提醒：{}老师,您好!距您的教学班:{}的成绩提交{}"
    elif xxlx=='12':
        contentTemplate="{}同学，您好！您今天有新成绩进入，成绩概要信息为{},详细信息可登陆教务系统查询，祝您学习愉快！"
    elif xxlx=='13':
        contentTemplate="温馨提醒：{}同学，您好！您所选《{}》课程，选课结果已经进入{},请及时登录、按课程要求进行修读与考核，忘记密码可联系平台客服！(如已参与学习，请忽略该条消息）"
    elif xxlx=='14':
        contentTemplate="{}同学，您好!您{}，详情可登陆教务系统查询或与学生学院教务办沟通，祝您学习愉快！"
    elif xxlx=='15':
        contentTemplate='''温馨提醒，成绩作废申请将在{}-{}时间段内开放！注意：1）如果一门课程您需要或必须要被保留，那么您不需要对该门课程的任何成绩进行作废，相反如果一门课程您完全不需要，那么您需要对该门课程的所有成绩进行作废；2）作废后的成绩不可找回，请您谨慎申请；3）申请时，请检查您的申请是否处于保存状态，如是，请妥善决定是提交还是撤销，详情可与学生学院联系，祝您学习愉快！'''
    elif xxlx=='16':
        contentTemplate='''{}老师，您好！您的{}，祝您工作愉快！'''
    elif xxlx=='01_jJR':
        contentTemplate='''{}老师，您好！根据学校节假日安排，{}日（补{}日的课程）第{}，请您按时在{}，{}，{}室给{}讲授《{}》课程。详情可登陆教务系统查询，祝您工作愉快！'''
    elif xxlx=='18':
        contentTemplate='{}老师，您好！，根据'+gv.tkyy+'您{}日(第{}周,星期{},第{})的{}课程，停课一次。若需补课，请在教务系统中申请补课（注：所有补课不会统计入调课量），祝您工作愉快！。'
    elif xxlx=='091':#缓考待审核发学院
        contentTemplate='{}老师，您好！{}，祝您工作愉快！'
    elif xxlx in ['19','20','xjyddshxy'] or xxlx.lower()=='cjxg01':
        contentTemplate='{}'
    else:
        pass
    return contentTemplate+gv.messageComments
def lrCjTxPara(jgDay,jssj):
    data=''
    if jgDay>0:
        data='已不足{}天（录入结束时间为：{}），请您及时录入、提交该教学班成绩,如您已提交或正在录入，请忽略该条信息！祝您工作愉快！'.format(jgDay,jssj.replace(' ','日'))
    elif jgDay==0:
        data='须于今日完成（录入结束时间为：{}），请您尽快提交该教学班成绩,如您已提交或正在录入，请忽略该条信息！祝您工作愉快！'.format(jssj.replace(' ','日'))
    elif jgDay<0:
        data='已滞后{}天（录入结束时间为：{}），请尽快联系各学院教务办公室,如您已提交或正在录入，请忽略该条信息！祝您工作愉快！,'.format(abs(jgDay),jssj.replace(' ','日'))
    else:
        pass
    return data

def setTitle(xxlx):
    ''''''
    if xxlx=='01' or xxlx=='02':
        return '【课表消息】'
    elif xxlx=='03' or xxlx=='031' or xxlx=='xjyddshxy':
        return '【学籍异动消息】'
    elif xxlx=='04':
        return '【场地借用消息】'
    elif xxlx=='05' or xxlx=='06':
        return '【考试消息】'
    elif xxlx=='07' or xxlx=='08':
        return '【课表变动信息】'
    elif xxlx=='09' or xxlx=='091':
        return '【缓考消息】'
    elif xxlx=='10' or xxlx=='17' or xxlx=='19':
        return '【选课消息】'
    elif xxlx in['11','12','15']:
        return '【成绩消息】'
    elif xxlx=='xlsx01':
        return '【教务消息】'
    elif xxlx=='13':
        return '【慕课修读消息】'
    elif xxlx=='14':
        return '【学业预警消息】'
    elif xxlx=='16':
        return '【教学任务信息】'
    elif xxlx=='01_jJR':
        return '【节假日课表消息】'
    elif xxlx=='18':
        return '【停课消息】'
    elif xxlx=='20':
        return '【教学评价消息】'
    elif xxlx.lower()=='cjxg01':
        return '【成绩消息】'
    else:
        return ''

def sendAndWrite(user,title,content):

    if gv.debug:
        t= send.LocalsendToUser(user, title, content)
    else:
        t = send.sendToUser(user, title, content)  # 发送
    return t


def dealData(con,jgDay,xxlx):
    ##nextDay,发送的目标日期，title，标题，content，内容
    nextDay=getNextDay(jgDay)
    title=setTitle(xxlx)
    contentTem=setContentTemplate(xxlx)
    L=[]
    baseQueryString=getBaseQuery(xxlx)
    user,content=None,None
    if xxlx in ['01','02'] and nextDay not in gv.tkrq:#课表,有多个周次，星期参数
        zcxqj=getZcXqj(con,jgDay)
        if xxlx in ['01','02'] and zcxqj[0] in gv.keBiaoZc:#在周次范围内，发送
            queryString=baseQueryString.format(zcxqj[0],zcxqj[1])
            #print(queryString)
            res=con.execute(queryString)
            for data in res:
                if xxlx=='01':####jgh,xm,skjc,xqmc,jxlmc,cdmc,jxbzc,kcmc#####
                    user = data[0]  # '103885'#测试时
                    content = title + contentTem.format(data[1], nextDay, zcxqj[0], zcxqj[1], data[2], data[3], data[4],data[5], data[6], data[7])
                else:#jgh,xm,skjc,xqmc,jxlmc,cdmc,jxbzc,kcmc,xsxh,xsxm
                    if not gv.keBiaoXsClose: #允许向学生发送课表
                        user = data[8]  # '103885'#测试时
                        content = title + contentTem.format(data[9], nextDay, zcxqj[0], zcxqj[1], data[2], data[4], data[5],data[7])
                if user:
                    t=sendAndWrite(user,title,content)
                    sendtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    L.append((str(uuid.uuid1()), user, content, t['MESSAGE'], sendtime))
    elif xxlx in ['01_jJR']:
        tdrq=sfJjr(con,nextDay)#原日期
        if tdrq!=nextDay and tdrq not in gv.tkrq:
            zcxqj=getZcXqj(con,tdrq)
            #print(zcxqj)
            queryString=baseQueryString.format(zcxqj[0],zcxqj[1])
            #print(queryString)
            res=con.execute(queryString)
            for data in res:
                #{}老师，您好！根据学校节假日安排，{}日（补{}日的课程）第{}，请您按时在{}，{}，{}室给{}讲授《{}》课程。详情可登陆教务系统查询，祝您工作愉快！
                user=data[0]
                content=title+contentTem.format(data[1],nextDay,tdrq,data[2],data[3],data[4],data[5],data[6],data[7])
                #print(content)
                t = sendAndWrite(user, title, content)
                sendtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                L.append((str(uuid.uuid1()), user, content, t['MESSAGE'], sendtime))
    elif xxlx in ['18'] and nextDay in gv.tkrq:#停课消息
        zcxqj=getZcXqj(con,jgDay)
        queryString=baseQueryString.format(zcxqj[0],zcxqj[1])
        res=con.execute(queryString)
        #'{}老师，您好！，根据'+gv.tkyy+'您{}日(第{}周,星期{},第{})的{}，需停课一次，，您可根据实际的教学进度需求，在教务系统中申请补课。'
        for data in res:
            user=data[0]
            content=title+contentTem.format(data[1],nextDay,zcxqj[0],zcxqj[1],data[2],data[7])
            t=sendAndWrite(user,title,content)
            sendtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            L.append((str(uuid.uuid1()), user, content, t['MESSAGE'], sendtime))
    elif xxlx in ['10','13']:
        zcxqj=getZcXqj(con,0)
        if xxlx=='10':#选课提醒传递的是年级
            tDay = getNextDay(0)
            if tDay in gv.xkTxRq or (zcxqj[0] in gv.xkTxZc and zcxqj[1] in gv.xkTxXqj):
                queryString=baseQueryString.format(nextDay)
                res=con.execute(queryString)
                for data in res:
                    user=data[0]
                    content = title + contentTem.format(data[1], data[2])
                    t=sendAndWrite(user,title,content)
                    sendtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    L.append((str(uuid.uuid1()), user, content, t['MESSAGE'], sendtime))
        elif xxlx=='13':#慕课修读网址提醒
            if nextDay in gv.xkMkTxRq or(zcxqj[0] in gv.xkMkTxZc and zcxqj[1] in gv.xkMkTxXqj):
                queryString=baseQueryString
                res=con.execute(queryString)
                for data in res:
                    user=data[0]
                    content=title+contentTem.format(data[1],data[2],data[3])
                    t=sendAndWrite(user,title,content)
                    sendtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    L.append((str(uuid.uuid1()), user, content, t['MESSAGE'], sendtime))
        else:
            pass
    elif xxlx in ['03','031','04','05','06','07','08','09','12']:#只有日期一个参数
        #学籍异动发向学生与发向教务员不能是同一段代码 发向教师用03，发向学生用031
        zcxqj=getZcXqj(con,jgDay)
        if xxlx in ['12']:
            queryString=baseQueryString.format(gv.xsCjTxSfFsCjb,nextDay,nextDay)
            #print(queryString)
        else:
            queryString=baseQueryString.format(nextDay)
        res=con.execute(queryString)
        for data in res:
            user,content=None,None
            if xxlx=='031':
                if data[2] not in ['分方向（转入）', '大类分流（转入）','转专业']:
                    user = data[0]
                    if int(zcxqj[0])<7:
                        content=title+contentTem.format(data[1],data[2],data[3]).replace('【广州大学教务处】','')+'，请关注您的个人课表，详情可与学生学院沟通，祝您学习愉快！【广州大学教务处】'
                    else:
                        content=title+contentTem.format(data[1],data[2],data[3]).replace('【广州大学教务处】','')+'，目前已过退课时间，您个人课表中的课程都会被记载成绩，详情可与学生学院沟通，祝您学习愉快！【广州大学教务处】'
            elif xxlx=='03':
                if data[2] not in ['分方向（转入）', '大类分流（转入）','转专业']:
                    user = data[4]  
                    content = title + contentTem.format(data[5], data[1], data[2], data[3])
            elif xxlx in ['07','09']:
                user=data[0]#'104660'#测试时
                content=title+contentTem.format(data[1],data[2],data[3])##
            elif xxlx in ['04']:
                user=data[0]
                #{}您好!您申请使用的{},第{}周，星期{},第{}节，{}。详情可登陆教务系统查询，祝您工作愉快！
                content=title+contentTem.format(data[1],data[2],connat.uniZxXqOrJc(data[3]),data[4],connat.uniZxXqOrJc(data[5]),data[6])
            elif xxlx in ['05']:
                user = data[0]  # '102813'
                content = title + contentTem.format(data[1], data[2], data[4], data[3])
            elif xxlx in ['06']:
                user=data[0]
                content = title + contentTem.format(data[1], data[2], data[3], data[4])
            elif xxlx in['08','12']:
                user = data[0]  # '104660'#测试时
                content = title + contentTem.format(data[1], data[2])
            else:
                pass
            if user:
                t=sendAndWrite(user, title, content)
                sendtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                L.append((str(uuid.uuid1()), user, content, t['MESSAGE'], sendtime))
    elif xxlx in ['11','14','xjyddshxy']:#无日期时间参数
        queryString=baseQueryString
        res=con.execute(queryString)
        nextDay=datetime.datetime.now()
        if xxlx=='11':
            for data in res:
                lrjs=datetime.datetime.strptime(data[3],'%Y-%m-%d %H:%M:%S')
                jgDay=(lrjs-nextDay).days+1
                if jgDay<=gv.jsCjLrJgDay:
                    user=data[0]
                    content=title+contentTem.format(data[1],data[2],lrCjTxPara(jgDay,data[3]))
                    if user and user not in gv.cjLrExcludeUser:
                        t=sendAndWrite(user, title, content)
                        sendtime = nextDay.strftime('%Y-%m-%d %H:%M:%S')
                        L.append((str(uuid.uuid1()), user, content, t['MESSAGE'], sendtime))
        elif xxlx=='14':#学业预警消息
            for data in res:
                user=data[0]
                content=title+contentTem.format(data[1],data[2])
                if user:
                    t=sendAndWrite(user,title,content)
                    sendtime=nextDay.strftime('%Y-%m-%d %H:%M:%S')
                    L.append((str(uuid.uuid1()), user, content, t['MESSAGE'], sendtime))
        elif xxlx=='xjyddshxy':
            for data in res:
                user=data[0]
                content=title+contentTem.format(data[1])
                if user:
                    t=sendAndWrite(user,title,content)
                    sendtime=nextDay.strftime('%Y-%m-%d %H:%M:%S')
                    L.append((str(uuid.uuid1()), user, content, t['MESSAGE'], sendtime))
        else:
            pass
    elif xxlx in ['15','17']:
        pass
        # njZyXsxx=con.execute(gv2.getZyxxCode)
        # zfksjssj=con.execute(gv2.getCjZfQsJsSj)
        # sendtime=datetime.datetime.now()
        # if xxlx=='15':#成绩作废提醒
        #     if (datetime.datetime.strptime(zfksjssj[0][0],'%Y-%m-%d %H:%M:%S')-sendtime).days==gv2.cjZfTxJgDay:
        #         for njzy in njZyXsxx:
        #             queryString=baseQueryString.format(njzy[0],njzy[1])
        #             res=con.execute(queryString)
        #             for data in res:
        #                 user=data[0].split(',')###该处与众不同，传递的是列表
        #                 sendtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #                 content=contentTem.format(zfksjssj[0][0],zfksjssj[0][1])
        #                 #print(content)
        #                 t=sendAndWrite(user,title,content)
        #                 L.append((str(uuid.uuid1()), user, content, t['MESSAGE'], sendtime))
        # elif xxlx=='17':#选课业务提醒
        #     pass
        # else:
        #     pass
    elif xxlx in ['16']:
        zcxqj = getZcXqj(con,jgDay)
        if zcxqj[0] in gv.jsJxrwTtkTxZc and zcxqj[1] in gv.jsJxrwTtkTxXqj:
            queryString=baseQueryString
            res=con.execute(queryString)
            for data in res:
                user=data[0]
                content=title+contentTem.format(data[1],data[2])
                t=sendAndWrite(user,title,content)
                sendtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                L.append((str(uuid.uuid1()), user, content, t['MESSAGE'], sendtime))
    elif xxlx in ['091']:
        res=con.execute(baseQueryString)
        for data in res:
            user=data[0]
            content=title+contentTem.format(data[1],data[2])
            t=sendAndWrite(user,title,content)
            sendtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            L.append((str(uuid.uuid1()), user, content, t['MESSAGE'], sendtime))
    elif xxlx in ['19']:
        zcxqj=getZcXqj(con,jgDay)
        if zcxqj[0] in gv.yQJsZc and zcxqj[1] in gv.yQJsXqj:
            res=con.execute(baseQueryString)
            for data in res:
                user=data[0]
                content=contentTem.format(data[1])
                t = sendAndWrite(user, title, content)
                sendtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                L.append((str(uuid.uuid1()), user, content, t['MESSAGE'], sendtime))
    elif xxlx in ['20']:
        zcxqj=getZcXqj(con,jgDay)
        if zcxqj[0] in gv.xsJxpjTxZc and zcxqj[1] in gv.xsJxpjTxXqj:
            res=con.execute(baseQueryString)
            for data in res:
                user=data[0]
                content=contentTem.format(data[1])
                t = sendAndWrite(user, title, content)
                sendtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                L.append((str(uuid.uuid1()), user, content, t['MESSAGE'], sendtime))
    elif xxlx.lower() in ['cjxg01']:
        queryString=baseQueryString
        res=con.execute(queryString)
        for data in res:
            user=data[0]
            content=title+contentTem.format(data[1])
            t=sendAndWrite(user,title,content)
            sendtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            L.append((str(uuid.uuid1()), user, content, t['MESSAGE'], sendtime))
    else:
        pass
    # print(L)
    if L:
        con.execute(gv.writeTologs,L)###insertSqlite(L)#发送完成后插入数据库
    return 1




def dealXls(con,jgDay,xxlx,fileName=None):
    '''发送xlsx文件中的内容！'''
    tday=getNextDay(jgDay)
    xlsx=fileInfo(gv.xlsxSavePath+fileName)
    res=xlsx.getFileContent()
    user,contet,sendtime=None,None,None
    L=[]
    for row in res:
        user,content,sendtime=row[0],row[1],row[2]
        if user and tday==sendtime.strip():
            title=setTitle(xxlx)
            t=sendAndWrite(user=user,title=title,content=content)
            sendtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            L.append((str(uuid.uuid1()), user, content, t['MESSAGE'], sendtime))

    if L:
       con.execute(gv.writeTologs,L)
    return 1


def controlMain(con,jgDay,xxlx,fileName='sf.xlsx'):
    '''消息业务控制主函数'''
    if xxlx in ['xlsx01']:
        if fileName:
            if dealXls(con,jgDay,xxlx,fileName):
                return '{}中的内容发送成功!'.format(fileName)
            else:
                return '{}中的内容发送失败!'.format(fileName)
        else:
            return '外表信息请传入xlsx文件，注意路径为{}'.format(gv.xlsxSavePath)
    else:
        if dealData(con,jgDay,xxlx):
            return '{}已发送成功'.format(xxlx)
        else:
            return '{}发送失败'.format(xxlx)



def messageInterface(con,xxlx=None):
    '''消息发送对外主接口'''
    ###xxlx=[(None,None,None,None)]
    L=[]
    if xxlx is None:
        xxlx=gv.getXxlx()
    for xx in xxlx:
        if xx[2] is not None:
            L.append(controlMain(con, xx[2], xx[1]))
    return L