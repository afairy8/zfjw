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
    return mail.replyXwCenter(pop=pop,smtp=smtp,oracle=con)
def jwxtmain(con):
    L=[]
    L.extend(jwglxt.jwxtCjgl(con=con,actionName='upXsCjjd;'))
    L.extend(jwglxt.jwxtXspj(con,actionName='getWccPjXs;addCpxsxz;delXsPjxx;'))
    L.extend(jwglxt.jwxtLdThpj(con))
    L.extend(jwglxt.jwxtBysh(con=con,actionName='inBysfzxxb;'))
    L.extend(jwglxt.jwxtJxrw(con))
    L.extend(jwglxt.jwxtKwgl(con,actionName='upSfhk'))
    L.extend(jwglxt.jwxtXkgl(con=con,actionName='delcxbmandxk;upcxbj;inZjxb;'))#;upPkgl
    return L

def wlzxmain(con):
    L=[]
    L.extend(wlzx.wlzxDataCenter(con))
    L.extend(wlzx.wlzxMsg(con))
    return L

def main():
    con=connect()
    L=['*'*30]
    L.append('当前周次={}，当前星期={}'.format(con.currentZcXqj[0],con.currentZcXqj[1]))
    start=time.perf_counter()
    L=L+wlzxmain(con)+jwxtmain(con)+mailmain(con)
    txt=fileInfo(time.strftime('%Y-%m-%d',time.localtime())+'.txt')
    end=time.perf_counter()
    L.append('共耗时{}秒'.format(str(end-start)))
    L.append('*'*30)
    txt.expXlsx(content=L,suffix='.txt')
    con.close()

if __name__=='__main__':
    main()