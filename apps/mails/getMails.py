import email
from email.parser import Parser
from email.header import decode_header
import os
import datetime
import time
from common.fileAction.controls import fileInfo
from apps.mails import vars
from databaseconfig.connectdbs import connect

def fileSavePath(sendtime):
    '''当日接收的附件存放位置'''
    sendtime=datetime.datetime.strftime(sendtime,'%Y-%m-%d')
    savePath=os.path.join(vars.savePath,sendtime)
    if not os.path.exists(savePath):
        os.mkdir(os.path.join(vars.savePath,sendtime))
    return savePath

def paraseMailBody(mailContent,sendtime,mailFrom):
    '''解析邮件正文部分'''
    count=1
    for part in mailContent.walk():
        file=part.get_filename()
        if file:
            h=email.header.Header(file)###将附件信息转换为header格式
            dh=decode_header(h)###解析转换后的附件header信息
            if dh[0][1]:##如果header中存在编码信息，则先将header用该编码转换为字符串，然后用header解析，最后用解析出来的heade信息，header编码解析为字符串
                filename=decode_str(decode_header(str(dh[0][0],dh[0][1]))[0])
                filetime=mailFrom.replace('@','=')+'】'+'['+str(count)+']'+datetime.datetime.strftime(sendtime,'%Y-%m-%d %H-%M-%S')
                filename=filetime+filename
                # pathtime=datetime.datetime.strftime(sendtime,'%Y-%m-%d')
                content = part.get_payload(decode=True)
                f=open(os.path.join(fileSavePath(datetime.datetime.now()),filename),'wb')
                f.write(content)
                f.close()
                count=count+1
            pass
        pass

def decode_str(s):
    '''解析字符,返回按邮件中指定的编码进行解码'''
    value, charset = s[0],s[1]
    if charset:
        if charset.lower() == 'gb2312':
            charset = 'gb18030'
        value = value.decode(charset)
    return value

def headerCheck(source,chekWords):
    '''发件人或者是主题检测，source邮件中的发件人；chekWords，输入的检测关键字'''
    sign=False
    if chekWords:
        if source.endswith(chekWords) or source.find(chekWords)>=0:
            sign=True
    else:
        sign=True
    return sign


def parseMail(con,jgHours=24,suffix='1532398723@qq.com',subject=None,max_receiver=100,fileSuffix='.xlsx'):
    '''
    :param ssh:邮箱连接
    :param jgDay: 收取近几日的邮件
    :param suffix: 发件人后缀名
    :param subject: 收取主题
    :return:
    '''
    # L=[]
    ssh=con.con
    mails=ssh.list()[1]#获取收信列表
    counts = len(mails)##
    count=min(max_receiver,counts)#最大收取份数
    for index in range(1,count+1):
        line=ssh.retr(counts-index+1)[1]#获取邮件中的所有行,从最近开始往后读取
        ###解析发送时间
        mailcontent=b'\r\n'.join(line[0:50]).decode('utf-8','ignore')
        parasemail = Parser().parsestr(mailcontent)
        headerSendTime = email.utils.parsedate(parasemail.get('Date'))
        mailFrom = email.utils.parseaddr(parasemail.get('From'))[1]
        mailSubject = decode_str(decode_header(parasemail['Subject'])[0])
        if headerCheck(mailFrom,suffix) and headerCheck(mailSubject,subject):
            if headerSendTime and isinstance(headerSendTime,tuple):
                headerSendTime=datetime.datetime.strptime(time.strftime('%Y-%m-%d %H:%M:%S',headerSendTime),'%Y-%m-%d %H:%M:%S')
                if headerSendTime+datetime.timedelta(hours=jgHours)>=con.currentZcXqj:
                    ####解析邮件内容部分###
                    mailcontent = b'\r\n'.join(line).decode('utf-8', 'ignore')
                    parasemail = Parser().parsestr(mailcontent)
                    paraseMailBody(mailContent=parasemail,sendtime=headerSendTime,mailFrom=mailFrom)
                    pass
    # ssh.quit()
    return 1

def uniFile(savePath):
    #######将xls文件全部转存为xlsx格式
    files=os.listdir(savePath)
    for file in files:
        if file.endswith('.xls'):
            xls=fileInfo(os.path.join(savePath,file))
            xls.xlsToXlsx()
    return 1

def sendMain(con,oracle,jgHours=24,suffix='1532398723@qq.com',subject=None,max_receiver=100,fileSuffix='.xlsx'):
    ####
    # if parseMail(con.con,jgHours,suffix,subject,max_receiver,fileSuffix):
    #     print('接收完成')
    savePath=os.path.join(vars.savePath,datetime.datetime.now().strftime('%Y-%m-%d'))
    if os.path.exists(savePath) and uniFile(savePath):
        ###处理xlsx文件中内容
        files=os.listdir(savePath)
        for file in files:
            if file.endswith(fileSuffix):
                xlsx=fileInfo(os.path.join(savePath,file))
                content=xlsx.getFileContent()
                L = []
                for data in content:
                    if data[12] is None or data[12].find('◎属实◎不属实')<0:
                        L.append(data)
                    else:
                        # L.append(tuple(list(data) + ['属实']))
                        ress = oracle.getData(vars.getbysxx.format(data[4]))
                        for res in ress:
                            if res[2] == '1' and res[3].replace(' ', '').replace('学位', '') == data[6].replace(' ', '').replace('学位', '')and data[4].replace(' ', '') == str(data[11]).replace(' ', ''):
                                L.append(tuple(list(data) + ['属实']))
                            else:
                                L.append(tuple(list(data) + ['存疑']))
                if L:
                    xlsx=None
                    os.remove(os.path.join(savePath,file))
                    xlsx = fileInfo(os.path.join(savePath, file))
                    xlsx.expXlsx(content=L)
                    # reciever=file.split('】')[0].replace('=','@')
                    ##发送邮件


# sendMain('','')