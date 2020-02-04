import poplib
import email
from email.parser import Parser
import os
import time
import shutil
import csv

poplib._MAXLINE = 204800
# '''
#     该文件为批量处理下载附件，已经经过优化
# '''
###批量收取附件的脚本附件

def getSameFileCount(filename):
    '''返回已经是第几个同名的附件'''
    count = 1
    filelist = os.listdir(downloadFileDir())
    for file in filelist:
        if file.find(filename) >= 0:
            count = count + 1
    return count


def downloadFileDir():
    '''附件保存路径'''
    currentDir = os.getcwd()
    todady = time.strftime('%Y-%m-%d', time.localtime())
    joinPath = os.path.join(currentDir, todady)
    return joinPath


def createDir(dirmode):
    '''创建接收文件夹'''
    joinPath = downloadFileDir()
    if dirmode=='zj':
        if not os.path.exists(joinPath):
            os.mkdir(joinPath)
    else:
        if os.path.exists(joinPath):
            shutil.rmtree(joinPath)
        os.mkdir(joinPath)
    return 1


def decode_str(s):
    '''解析字符,返回按邮件中指定的编码进行解码'''
    value, charset = email.header.decode_header(s)[0]
    if charset:
        if charset.lower() == 'gb2312':
            charset = 'gb18030'
        value = value.decode(charset)
    return value


def checkFrom(headerFrom, suffix):
    '''在发件人列表中则收取'''
    if len(suffix.replace('，', '')) > 0:
        suffix = suffix.split('，')
        if headerFrom in suffix:
            return 1
        else:
            return 0
    else:
        return 1


def checkSubject(headerSubject, keyWords):
    '''主题检测，如包含关键字则收取,如未指定关键字，默认收取全部'''
    if len(keyWords.replace('，','')) > 0:
        words = keyWords.split('，')
        for word in words:
            if headerSubject.find(word)>0:
                return 1
        return 0
    else:
        return 1


def pareseBody(parasemail, headerFrom, headerSendTime):
    '''解析正文，主要是下载附件'''
    joinPath = downloadFileDir()
    headerSendTime = str(headerSendTime[0]) + '-' + str(headerSendTime[1]) + '-' + str(headerSendTime[2])+'se'+str(headerSendTime[5])
    for part in parasemail.walk():
        file = part.get_filename()
        # print(headerSendTime)
        if file:  # 有附件
            h = email.header.Header(file)  # 解析附件名称,将附件名改为header格式
            dh = email.header.decode_header(h)  ##解析附件名的header格式
            #value, charset = email.header.decode_header(str(dh[0][0], dh[0][1]))[0]
            if dh[0][1]:  # 编码格式
                filename = decode_str(str(dh[0][0], dh[0][1]))  ##完整解析附件名
                if filename.endswith('.xlsx') or filename.endswith('.xls') or filename.endswith(
                        '.et') or filename.endswith('.zip') or filename.endswith('.rar'):
                    # print(headerSendTime)
                    filename = 'from' + headerFrom.split('@')[0] + 'sendtime' + headerSendTime + 'fjm' + filename
                    count = getSameFileCount(filename)
                    if count > 1:
                        filename = os.path.join(joinPath, '【同名第' + str(count) + '个】' + filename)
                    else:
                        filename = os.path.join(joinPath, filename)
                    content = part.get_payload(decode=True)
                    f = open(filename, 'wb')
                    f.write(content)
                    f.close()
                else:
                    pass
def uniquefilename(name):
    name= name.replace('：','').replace(':','').replace('\\','').replace('*','').replace('?','').replace(' ','')
    name=name.replace('<','').replace('>','').replace('|','').replace('"','')
    if not name or len(name)==0:
        name='-'
    return name
def getFromTxlXx(headerFrom):
    '''解析通讯录信息'''
    pass
    isExists=0
    joinPath=os.path.join(os.getcwd(),'txl\\address.csv')
    #with open(joinPath,newline='',encoding='utf-8') as f:
    f=open(joinPath,newline='',encoding='utf-8')
    lines=csv.reader(f)
    for line in lines:
        if headerFrom in line:
            Fromxx='(姓名'+uniquefilename(line[2])+')(联系地址'+uniquefilename(line[5])+')(联系电话'+uniquefilename(line[4])+')'
            isExists=1
            break
    f.close()
    if isExists:
        return Fromxx
    else:
        return headerFrom
def pareseHeader(parasemail, jgDay, suffix, keyWords,headerSendTime):
    '''解析头部'''
    # headerTo=email.utils.parseaddr(parasemail.get('To'))
    headerFrom = email.utils.parseaddr(parasemail.get('From'))[1]  ##解析发件人
    headerSubject = parasemail.get('Subject', '')  ##解析主题
    headerSubject = decode_str(headerSubject)
    #headerSendTime = email.utils.parsedate(parasemail.get('Date'))  ##解析发送时间
    #localtime = time.localtime()
    # if headerSendTime[0] == localtime.tm_year and headerSendTime[1] == localtime.tm_mon and headerSendTime[
    #     2] + jgDay >= localtime.tm_mday:
    if checkFrom(headerFrom, suffix) and checkSubject(headerSubject, keyWords):
        print('当前收取发件人{},主题{}'.format(headerFrom, headerSubject))
        pass#从通讯录中获取姓名等详细信息
        headerFrom=getFromTxlXx(headerFrom)
        pareseBody(parasemail, headerFrom, headerSendTime)
def isInDate(headerSendTime,jgDay):
    '''判断邮件是否在间隔时间范围内'''
    isIn=0
    localtime = time.localtime()
    if isinstance(headerSendTime,tuple) and headerSendTime[0] == localtime.tm_year and headerSendTime[1] == localtime.tm_mon and headerSendTime[2] + jgDay >= localtime.tm_mday:
        isIn=1
    return isIn
# def decodeline(line):
#     return line.decode('utf-8','ignore')
def parseMail(user='yxfyxxk@163.com', password='yxfyxxk83837979', server='pop.163.com', port=995, jgDay=2, suffix='',keyWords='',max_receiver=100,dirmode='fg'):
    '''整体解析邮件'''
    ssh = login(user=user, password=password, server=server, port=port)
    if createDir(dirmode):
        print('接收附件文件夹创建成功！')
    #resp, mails, octets = ssh.list()  ##获取收信列表
    mails=ssh.list()[1]#获取收信列表
    counts = len(mails)##
    count=min(max_receiver,counts)#最大收取份数
    #print(counts)
    for index in range(1,count+1):
        line=ssh.retr(counts-index+1)[1]#获取邮件中的所有行,从最近开始往后读取
        ###解析发送时间
        mailcontent=b'\r\n'.join(line[0:30]).decode('utf-8','ignore')
        parasemail = Parser().parsestr(mailcontent)
        headerSendTime = email.utils.parsedate(parasemail.get('Date'))
        ###解析发送时间完成
        #print('当前处理第{}封,时间{},类型{}'.format(str(counts-index+1),headerSendTime,type(headerSendTime)))
        if isInDate(headerSendTime,jgDay):
            mailcontent = b'\r\n'.join(line).decode('utf-8', 'ignore')  #
            parasemail = Parser().parsestr(mailcontent)  # 将邮件解析为字符串
            pareseHeader(parasemail, jgDay, suffix, keyWords,headerSendTime)
    ssh.quit()
    return 1


def login(user, password, server, port):
    ssh=None
    try:
        ssh = poplib.POP3_SSL(server, port)
        ssh.user(user)
        ssh.pass_(password)
        print('登录成功!')
    except:
        print('登录失败')
    return ssh



def checkMode():
    user='1532398723@qq.com'#'yxfyxxk@163.com'
    password='raueqepnyttjjhfg'#'yxfyxxk83837979'
    server='pop.qq.com'
    jgDay=3
    port=995
    max_receiver=100
    suffix=''#中文逗号分隔，格式为XXX@XX.com，YYY@YY.com
    keyWords=''#格式为：XX,XX,中文逗号
    #mode=input("请输入选择的模式，default表示为默认模式；others表示非默认模式\n默认模式介绍：收取近15天的所有人所有主题的邮件\n")
    mode = ''
    if len(mode) == 0 or uniquefilename(mode).lower().find('default') >= 0 :
        #     mode = "default"
        # if mode.lower().find('default') >= 0:
        #keyWords = input("请输入收取的目标主题关键字，多个主题关键字用中文逗号隔开，如不输入，则表示收取全部主题")
        return parseMail(user=user,password=password,server=server,port=port,jgDay=jgDay,suffix=suffix,keyWords=keyWords,max_receiver=max_receiver)
    else:
        user = input("请输入登录邮箱用户名(如XXX@XX.com)")
        password = input("请输入登录邮箱的授权码")
        server = 'pop' + user.split('@')[1]
        jgDay = input("请输入收取的时间范围，如15，表示：收取近15天的邮件")
        try:
            jgDay = int(jgDay)
        except:
            jgDay=15
        suffix = input("请输入收取的目标发件人，多个发件人用中文逗号隔开,如不输入，则表示收取全部发件人")
        keyWords = input("请输入收取的目标主题关键字，多个主题关键字用中文逗号隔开，如不输入，则表示收取全部主题")
        return parseMail(user=user,password=password,server=server,port=port,jgDay=jgDay,suffix=suffix,keyWords=keyWords,max_receiver=max_receiver)


def main():
    start = time.clock()
    if checkMode():
        end = time.clock()
        print("收取完成!共耗时{}秒".format(str(end - start)))
    else:
        print("收取失败!请重新收取！")



