import poplib
import email
from email.parser import Parser
import os
import datetime
import time
import shutil
import csv
from databaseconfig.connectdbs import connect


def parseMail(con,jgDay=0,suffix=None,subject=None,max_receiver=100):
    '''
    :param ssh:邮箱连接
    :param jgDay: 收取近几日的邮件
    :param suffix: 发件人后缀名
    :param subject: 收取主题
    :return:
    '''
    ssh=con.con
    mails=ssh.list()[1]#获取收信列表
    counts = len(mails)##
    count=min(max_receiver,counts)#最大收取份数
    for index in range(1,count+1):
        line=ssh.retr(counts-index+1)[1]#获取邮件中的所有行,从最近开始往后读取
        ###解析发送时间
        mailcontent=b'\r\n'.join(line[0:30]).decode('utf-8','ignore')
        parasemail = Parser().parsestr(mailcontent)
        headerSendTime = email.utils.parsedate(parasemail.get('Date'))
        headerSendTime=datetime.datetime.strptime(time.strftime('%Y-%m-%d %H:%M:%S',headerSendTime),'%Y-%m-%d %H:%M:%S')
        print(headerSendTime+datetime.timedelta(hours=24))
        print(con.currentZcXqj-datetime.timedelta(hours=24))
        if headerSendTime+datetime.timedelta(hours=24)>=con.currentZcXqj:
            print('1')

        ###解析发送时间完成
        #print('当前处理第{}封,时间{},类型{}'.format(str(counts-index+1),headerSendTime,type(headerSendTime)))
        # if isInDate(headerSendTime,jgDay):
        #     mailcontent = b'\r\n'.join(line).decode('utf-8', 'ignore')  #
        #     parasemail = Parser().parsestr(mailcontent)  # 将邮件解析为字符串
        #     pareseHeader(parasemail, jgDay, suffix, keyWords,headerSendTime)
    ssh.quit()
    return 1


parseMail(connect('mail'))