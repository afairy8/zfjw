from apps.jwglxt import jwglxtcontrols as jwglxt
from apps.wlzx import wlzxcontrols as wlzx
from databaseconfig.connectdbs import connect
from common.fileAction.controls import fileInfo
import time
from apps.mails import mailInterface as mail

def mailmain(con):
    '''回复学位中心中心的日常任务！'''
    pop=connect('mailpop')
    smtp=connect('mailsmtp')
    ####print('yjwc')
    return mail.replyXwCenter(pop=pop,smtp=smtp,oracle=con)
def jwxtmain(con):
    L=[]
    L.extend(jwglxt.jwxtCjgl(con=con,actionName='upXsCjjd;'))
    ####print('cjwc')
    ####print('pjwc')
    L.extend(jwglxt.jwxtLdThpj(con))
    ####print('ldwc')
    L.extend(jwglxt.jwxtBysh(con=con,actionName='inBysfzxxb;'))
    ####print('bysfzxxwc')
    L.extend(jwglxt.jwxtJxrw(con))
    ####print('jxrwwc')
    L.extend(jwglxt.jwxtKwgl(con,actionName='upSfhk'))
    ####print('kwwc')
    L.extend(jwglxt.jwxtXkgl(con=con,actionName='delcxbmandxk;upcxbj;inZjxb;expMooc;'))#;upPkgl
    ####print('jwwc')
    L.extend(jwglxt.jwxtXspj(con, actionName='getWccPjXs;addCpxsxz;delXsPjxx;'))
    return L

def wlzxmain(con):
    L=[]
    L.extend(wlzx.wlzxDataCenter(con))
    L.extend(wlzx.wlzxMsg(con))
    ####print('xxwc')
    return L

def main():
    con=connect()
    L=['*'*30]
    L.append('当前周次={}，当前星期={}'.format(con.currentZcXqj[0],con.currentZcXqj[1]))
    start=time.perf_counter()
    try:
        L=L+wlzxmain(con)
    except:
        L=L+['网络中心数据中心或消息中心有问题']
    try:
        L=L+jwxtmain(con)
    except:
        L=L+['教务系统日常维护未能完成']
    try:
        L=L+mailmain(con)
    except:
        L=L+['邮件回复有问题']
    # L=L+wlzxmain(con)+jwxtmain(con)+mailmain(con)
    logsname='D:\\projects\\zfjw\\logs\\'
    txt=fileInfo(logsname+time.strftime('%Y-%m-%d',time.localtime())+'.txt')
    end=time.perf_counter()
    L.append('共耗时{}秒'.format(str(end-start)))
    L.append('*'*30)
    res=''
    for ele in L:
        if ele is None:
            ele=';\n'
        res=res+ele+';\n'
    # print(';\n'.join(L))
    txt.expXlsx(content=res,suffix='.txt')
    con.close()

if __name__=='__main__':
    main()