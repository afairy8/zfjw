from apps.jwglxt import jwglxtcontrols as jwglxt
from databaseconfig.connectdbs import connect
from apps.wlzx import wlzxcontrols as wlzx
####交换生成绩文件路径
xsFilePath=''

###交换生成绩录入
def jhsCjlr(con):
    '''交换生成绩录入'''
    print(jwglxt.jwxtCjgl(con,actionName='jhsCjImp;',jhscjFilePath=xsFilePath))

###照片导入
###学生照片文件根路径
xsZpFilePath=''
xsZpPrimaryKey='zjhm'
xsZpDrType='rxhzp'
def zpDr(con):
    '''导入照片'''
    print(jwglxt.jwxtXjgl(con,actionName='impZp;',type=xsZpDrType,pk=xsZpPrimaryKey,zpPath=xsZpFilePath))

###中途退回学生评价
###学生照片文件根路径
xhlist=[]
def roolXspj(con):
    '''退回学生评价'''
    print(jwglxt.jwxtXspj(con,actionName='roolbackXspj;',xhlist=xhlist))

####中途退回领导同行评价
LdThdict={
    'jgh':{
        'jxbmc':'',
        'pjsj':'',
        'bpjgh':''
    },
    '':{

    }
}
def rollLdTh(con):
    '''退回领导、同行评价'''
    for jgh,valueInfo in LdThdict.items():
        LdThlist=list(jgh)
        jxbmc=valueInfo['jxbmc']
        pjsj=valueInfo['pjsj']
        bpjgh=valueInfo['bpjgh']
        print(jwglxt.jwxtLdThpj(con,actionName='roolLdThpj;',LdThlist=LdThlist,jxbmc=jxbmc,pjsj=pjsj,bpjgh=bpjgh,minpf=100))

###考务管理，更新监考学院
def upJkjg(con):
    '''考务管理，更新监考学院'''
    print(jwglxt.jwxtKwgl(con,actionName='upJkjgid;'))

def expAllXkmd(con):
    '''导出慕课选课名单'''
    print(jwglxt.jwxtXkgl(con,actionName='expAllXkmd'))
    #print(jwglxt.jwxtXkgl(con=con, actionName='expMooc;'))

def expZdxs(con,njdm_id):
    '''导出指定学生'''
    print(jwglxt.jwxtXjgl(con=con,actionName='getZdTzXsxx;',njdm_id='2019'))

def signalSendMsg(con,filename='sf.xlsx'):
    '''单独发送外表数据'''
    xxlx = [('外表数据发送', 'xlsx01', 0, 2)]
    print(wlzx.wlzxMsg(con,xxlx=xxlx,fileName=filename))
def signalSysJs(con):
    '''单独同步教师'''
    print(wlzx.wlzxDataCenter(con,actionName='sytojs'))

def kctdly(con):
    print(jwglxt.jwxtJxjh(con,'upKctdDtly;'))

con=connect()
#expAllXkmd(con)
#signalSendMsg(con=con,filename='用户信息.xlsx')
con.close()