from apps.mails import getMails
from apps.mails import sendMails

def replyXwCenter(pop,smtp,oracle,suffix='cdgdc.edu.cn',jgHours=24):
    L=[]
    if getMails.parseMail(pop,jgHours=jgHours,suffix=suffix):
        L.append('收取{}的邮件完成'.format(suffix))
        L.append(sendMails.sendmail(smtp,oracle,suffix=suffix,fileSuffix='.xlsx'))
    else:
        L.append('收取{}的邮件失败，未进行回复！'.format(suffix))
    return L