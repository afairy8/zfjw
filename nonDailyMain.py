from apps.jwglxt import jwglxtcontrols as jwglxt
from databaseconfig.connectdbs import connect
####交换生成绩文件路径
xsFilePath=''

###交换生成绩录入
def jhsCjlr(con):
    print(jwglxt.jwxtCjgl(con,actionName='jhsCjImp;',jhscjFilePath=xsFilePath))

###照片导入
###学生照片文件根路径
xsZpFilePath=''
xsZpPrimaryKey='zjhm'
xsZpDrType='rxhzp'
def zpDr(con):
    print(jwglxt.jwxtXjgl(con,actionName='impZp;',type=xsZpDrType,pk=xsZpPrimaryKey,zpPath=xsZpFilePath))

###中途退回学生评价
###学生照片文件根路径
xhlist=[]
def roolXspj(con):
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
    for jgh,valueInfo in LdThdict.items():
        LdThlist=list(jgh)
        jxbmc=valueInfo['jxbmc']
        pjsj=valueInfo['pjsj']
        bpjgh=valueInfo['bpjgh']
        print(jwglxt.jwxtLdThpj(con,actionName='roolLdThpj;',LdThlist=LdThlist,jxbmc=jxbmc,pjsj=pjsj,bpjgh=bpjgh,minpf=100))

###考务管理，更新监考学院
def upJkjg(con):
    print(jwglxt.jwxtKwgl(con,actionName='upJkjgid;'))

def expAllXkmd(con):
    print(jwglxt.jwxtXkgl(con,actionName='expAllXkmd'))

def expZdxs(con,njdm_id):
    print(jwglxt.jwxtXjgl(con=con,actionName='getZdTzXsxx;',njdm_id='2019'))
# ####
con=connect()
# expAllXkmd(con)
# expZdxs(con,njdm_id='2019')
con.close()
# print(jwglxt.jwxtXkgl(con,actionName='inZjxb;'))
