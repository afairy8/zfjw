from apps.jyxt.jxdg import vars as jv
from databaseconfig import connectdbs


def uniCLOB(con, data, mode='r'):
    '''处理clob字段'''
    if data:
        # con=connections.conn()
        # cur=con.cursor()
        if mode == 'w':
            clob = con.cur.var(connectdbs.cx_Oracle.CLOB)
            clob.setvalue(0, data)
        else:
            clob = data.read()
    else:
        clob = ''
    return clob


def convertHtml(title, content):
    if content:
        return '<p>' + title + '</br>&nbsp;&nbsp;' + content + '</p>'
    else:
        return '<p>' + title + '</p>'


def convertByyqTable(con, kch):
    '''将毕业要求转换为html格式'''
    tableContent = con.execute(jv.getByyqMxData.format(kch))
    countTableRows = len(tableContent)
    if countTableRows >= 1:
        table = '''<table style="width: 100.0%;" cellpadding="2" cellspacing="0" border="1">
        <tr><td>序号</td><td>教学目标</td><td>毕业要求</td></tr>'''
        for content in tableContent:
            # print(content[2])
            if content[2] < countTableRows:
                table = table + "<tr><td>" + str(content[2]) + "</td><td>" + uniCLOB(con,
                    content[0]) + "</td><td>" + uniCLOB(con,content[1]) + "</td></tr>"
            else:
                table = table + "<tr><td>" + str(content[2]) + "</td><td>" + uniCLOB(con,
                    content[0]) + "</td><td>" + uniCLOB(con,content[1]) + "</td></tr></table>"
        # print(table)
    else:
        table = ""
    # print(table)
    return table


def convertKckhTable(con,kch):
    '''将考核方式转换为html格式'''
    tableContent = con.execute(jv.getKckhyq.format(kch))
    countTableRows = len(tableContent)
    if countTableRows >= 1:
        table = '''<table style="width: 100.0%;" cellpadding="2" cellspacing="0" border="1">
        <tr><td>考核方式</td><td>考核要求</td><td>考核权重</td></tr>'''
        for content in tableContent:
            if content[3] < countTableRows:
                table = table + "<tr><td>" + content[0] + "</td><td>" + uniCLOB(con,content[2]) + "</td><td>" + content[1] + "</td></tr>"
            else:
                table = table + "<tr><td>" + content[0] + "</td><td>" + uniCLOB(con,content[2]) + "</td><td>" + content[1] + "</td></tr>" + "</td></tr></table>"
    else:
        table = ""
    return table


def insertToDB(con,L):
    '''将教学大纲数据插入临时表'''
    # clobdata=uniCLOB(content,'w')
    if not jv.debug:  # 是否为调试模式
        con.execute(jv.insertLkJxdb, L)
        if jv.update:  # 同步完成之后，是否直接更新课程库
            con.execute(jv.updateKcdmb)
    else:
        print(L)


def createJxdg(con):
    kcdglist = []
    tableExists = con.objectExists('likai_jxdg')[0][0]
    if tableExists:
        con.execute('drop table likai_jxdg')
    con.execute(
        '''create table likai_jxdg 
        (kch varchar2(255),kczwjj varchar2(4000),kczwjxdg clob )'''
    )
    res = con.execute(jv.getJxdgNr)
    # data[0] kcbh,data[3]nr1,data[4]nr2,data[5]nr13,data[6] nr1_4,
    # data[7] nr1_5,data[8]
    count = 1
    for data in res:
        nr1 = convertHtml('一、教学大纲说明</br>(一)课程的性质、地位、作用和任务', uniCLOB(con,data[3]))
        if convertByyqTable(con,data[0]):
            byyq = convertHtml('(二)课程教学目标及其与本专业毕业要求的对应关系', '') + convertByyqTable(con,data[0])
        else:
            byyq = ''
        nr1_3 = convertHtml('(三)课程教学方法与手段', uniCLOB(con,data[6]))
        nr1_4 = convertHtml('（四）课程与其它课程的联系', uniCLOB(con,data[7]))
        nr1_5 = convertHtml('(五)教材与教学参考书', uniCLOB(con,data[8]))
        nr2 = convertHtml('二、课程的教学内容、重点和难点', uniCLOB(con,data[4]))
        # print(convertKckhTable(data[0]))
        if convertKckhTable(con,data[0]):
            kcch = convertHtml('三、课程考核', '') + convertKckhTable(con,data[0])
        else:
            kcch = ''
        content = nr1 + byyq + nr1_3 + nr1_4 + nr1_5 + nr2 + kcch
        kcdglist.append((data[0], nr1, content))
        count = count + 1
        print('---------')
        if count % jv.pcMax == 0:
            insertToDB(con,kcdglist)
            kcdglist = []
            print('{}已处理'.format(str(count)))
    if kcdglist:
        insertToDB(con,kcdglist)
        print('后{}已处理'.format(len(kcdglist)))
    return 1