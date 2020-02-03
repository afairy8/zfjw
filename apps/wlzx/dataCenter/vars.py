debug=False
headers={'HTTP_DC_SECRECT':'','charsets':'utf-8'}
############数据中心分配###############
headers['HYYP_DC_SECRECT']='hJ5kBRuV'#网络中心分配
name='JWXT'#数据中心分配
token='chst9Fgk'#网络中心分配
baseUrl='http://dapi.gzhu.edu.cn:8012/datacenter/core/cpi'
###教师同步存储过程
updateAndinsertJzg='LIKAI_JW_PUBLICINTERFACE.UPDATEANDINSERTJZG'
urlDir={
    'tch':'/hUolEw8l',
        }
page_count=300
params={'name':name,'token':token,'page_count':page_count}

####将数据中心的教师信息插入教务系统
getJzg='''
insert into LIKAI_SJTB_JZGXXB(jgh_id,jgh,xm,xb,csrq,dqzt,zcmc,jgdm) values (:1,:2,:3,:4,:5,:6,:7,:8)
'''

backUpCode='''
create table jw_jg_jzgxxb_back as (select * from jw_jg_jzgxxb)
'''