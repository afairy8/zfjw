import os
from apps.mails import vars
import datetime
from common.fileAction.controls import fileInfo
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
def coreSendMain(smtp,pathfile='',content=None,From='1532398723@qq.com'):
    '''
    :param smtp:
    :param pathfile: 包含附件的路径与附件名
    :param content: 邮件正文
    :return:
    '''
    ##包装内容与主题
    smtp=smtp.con
    filename=os.path.split(pathfile)[1]
    receiver=filename.split('】')[0]
    ###封装发送邮件的头部
    mimeContent=MIMEMultipart()
    mimeContent['From']=From
    mimeContent['To']=receiver
    mimeContent['Subject']=filename
    ###封装发送邮件的正文
    if content:#添加正文
        content=MIMEText(content,_charset='utf-8')
        mimeContent.attach(content)
    ##封装发送邮件的附件
    #file=''
    if filename.endswith('xlsx'):
        file=MIMEApplication(open(pathfile,'rb').read())
        file.add_header('Content-Disposition', 'attachment',filename=filename)
        mimeContent.attach(file)
    #发送
    try:
        smtp.sendmail(From,receiver,mimeContent.as_string())
        # ssh.quit()
        return 1
    except:
        return 0


def uniFile(savePath):
    #######将xls文件全部转存为xlsx格式
    os.system('attrib -R {} /S /D'.format(savePath))
    files=os.listdir(savePath)
    for file in files:
        if file.endswith('.xls'):
            xls=fileInfo(os.path.join(savePath,file))
            xls.xlsToXlsx()
    return 1

def uniContent(content):
    '''该部分内容暂时弃用'''
    if content:
        res = []
        for e in content:
            row = []
            for ee in e:
                if ee is None:
                    row.append(' ')
                else:
                    row.append(ee)
            rowToStr='\t'.join(row)
            res.append('<div>{}</div>'.format(rowToStr))
        return ('<br>'.join(res))
    else:
        return None


def sendmail(smtp,oracle,suffix=None,fileSuffix='.xlsx'):
    ####
    # if parseMail(con.con,jgHours,suffix,subject,max_receiver,fileSuffix):
    #     print('接收完成')
    savePath=os.path.join(vars.savePath,datetime.datetime.now().strftime('%Y-%m-%d'))
    if os.path.exists(savePath) and uniFile(savePath):
        ###处理xlsx文件中内容
        files=os.listdir(savePath)
        for file in files:
            if file.endswith(fileSuffix) and file.find(suffix)>=0:
                pathfile=os.path.join(savePath,file)
                xlsx=fileInfo(pathfile)
                content=xlsx.getFileContent()
                L = []
                for data in content:
                    if data[12] is None or data[12].find('◎属实◎不属实')<0:
                        L.append(data)
                    else:
                        ress = oracle.execute(vars.getbysxx.format(data[4]))
                        for res in ress:
                            if res[2] == '1' and res[3].replace(' ', '').replace('学位', '') == data[6].replace(' ', '').replace('学位', '')and res[4].replace(' ', '') == str(data[11]).replace(' ', ''):
                                L.append(tuple(list(data) + ['属实']))
                            else:
                                L.append(tuple(list(data) + ['存疑']))
                if L:
                    xlsx=None
                    os.remove(pathfile)
                    xlsx = fileInfo(pathfile)
                    xlsx.expXlsx(content=L)
                    if coreSendMain(smtp=smtp,pathfile=pathfile,content='内容见附件'):
                        print ('pathfile={}回复成功'.format(pathfile))
                    else:
                        print ('pathfile={}回复失败'.format(pathfile))
        return '处理完成！'
    else:
        return '没有要处理的！'
# sendMain('','')
# uniFile(os.path.join(vars.savePath,datetime.datetime.now().strftime('%Y-%m-%d')))
