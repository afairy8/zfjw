from apps.wlzx.dataCenter import vars as dv
import requests
from common.actionPre import actionpre
def insertJzg(con,L):
    '''同步前将likai_sjtb_jzgxxb中的内容先清空,后插入'''
    if not dv.debug:
        ##清空likai_sjtb_jzgxxb
        con.execute('delete from likai_sjtb_jzgxxb')
        # con.commit()
        #将数据中心的教师用户同步至jw数据库
        con.execute(dv.getJzg,L)
        bakTableExists=con.execute('jw_jg_jzgxxb_back')[0]
        if bakTableExists[0]:
            con.execute('drop table jw_jg_jzgxxb_back')
        con.execute(dv.backUpCode)
        con.execute(dv.updateAndinsertJzg)
        return 1
    else:
        pass
def sytojs(con,max_index=35):
    '''接收数据中心的教师信息'''
    url=dv.baseUrl+dv.urlDir['tch']
    L=[]
    params=dv.params
    for index in range(1,max_index):
        params['page_index']=index
        #print(params)
        results=requests.get(url,params=params,headers=dv.headers).json()['result']
        for data in results:
            if data['O_STAFF_BASIC_PARENTORG_CODE']:
                jgh=data['O_STAFF_BASIC_STAFFID']
                jgh_id=jgh
                xm=data['O_STAFF_BASIC_NAME']
                xb=data['O_STAFF_BASIC_SEX_CODE']
                csrq=data['O_STAFF_BASIC_BIRTHDAY']
                dqzt=data['O_STAFF_BASIC_WORKSTATE_CODE']
                zcmc=data['O_STAFF_BASIC_MAJORQ']
                jgdm=data['O_STAFF_BASIC_ORG_CODE']
                L.append((jgh_id,jgh,xm,xb,csrq,dqzt,zcmc,jgdm))
    return insertJzg(con,L)

def dataCenterInterface(con,actionName,max_index=25):
    if actionName==actionpre.unique('sytojs'):
        if sytojs(con,max_index):
            return '教师信息同步成功！'
        else:
            return '教师信息同步失败'
    else:
        pass