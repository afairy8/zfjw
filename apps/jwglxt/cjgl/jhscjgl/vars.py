tmpTableNames = ['likai_jhc_kck', 'likai_jhc_cj']



###取当前学年学期
getDQXNXQ='''
select 
(select zdz from ZFTAL_XTGL_XTSZB where zs='当前学年'),
(select zdz from ZFTAL_XTGL_XTSZB where ZS='当前学期')
from dual
'''
####取成绩学年学期
getCJXNXQ='''
select 
(select LIKAI_JW_PUBLICINTERFACE.RETURN_XNORXQMC('{}') from ZFTAL_XTGL_XTSZB where zs='当前学年'),
(select LIKAI_JW_PUBLICINTERFACE.RETURN_XNORXQMC('{}') from ZFTAL_XTGL_XTSZB where ZS='当前学期')
from dual
'''


########
createJhsKck = '''
create table likai_jhc_kck(
kch_id varchar2(255) primary key ,
kch varchar2(255) not null,
kcmc varchar2(255) not null,
kcywmc varchar2(255) ,
kcjj varchar2(255),
kkbm_id varchar2(255) default('40'),
xf varchar2(55),
zxs varchar2(255) default ('16'),
kclbdm varchar2(255),
kcxzdm varchar2(255),
kcxz varchar2(255)
)
'''

initJhsKck='''
insert into likai_jhc_kck(kch_id,kch,kcmc,kcywmc,kcjj,KKBM_ID,xf,zxs,KCLBDM,kcxzdm,kcxz)
select kch_id,kch,kcmc,kcywmc,''kcjj,kkbm_id,xf,zxs,kclbdm,kcxzdm,
(select kcxzmc from JW_JH_KCXZDMB where kcxzdm=kc.kcxzdm) kcxz
from JW_JH_KCDMB kc
where upper(kc.kch) like 'JH%'
'''
####插入临时的课程库
inJhsKck='''
insert into likai_jhc_kck(kch_id,kch,kcmc,kcywmc,xf,kcxz)
values(:1,:2,:3,:4,:5,:6)
'''
####生成课程号规则
kcdmIsExists='''
select kch from likai_jhc_kck t
where t.KCMC='{}' and to_number(t.XF)=to_number('{}') and t.KCXZ='{}'
'''
kcdmMax='''
select 'JH'||to_char(kch) from (
select max(to_number(substr(kch,3,length(kch)-2)))+1 kch
from LIKAI_JHC_KCK)
'''

createJhsCj = '''
create table likai_jhc_cj(
cjxn varchar(20) not null,
cjxq varchar(20) not null,
fz varchar(29) not null, 
kch varchar(255) not null, 
kcxz varchar(255) not null, 
cjxz varchar(20) default('正常考试'), 
xh varchar(20) not null, 
cj varchar(255) not null, 
cjbz varchar(25), 
xm varchar(20), 
nj varchar(20), 
bj varchar(20), 
kcbj varchar(20) default('主修'))
'''
inJhsCj='''
insert into likai_jhc_cj(cjxn,cjxq,fz,kch,kcxz,xh,cj,xm)
values(:1,:2,:3,:4,:5,:6,:7,:8)
'''

writeToKck='''
insert into jw_jh_kcdmb(kch_id,kch,kcmc,kcywmc,kkbm_id,xf,zxs,kclbdm,kcxzdm,tkbj,bz)
select t.kch_id,t.kch,t.kcmc,t.kcywmc,t.kkbm_id,t.xf,t.zxs,
       (case when kcxz like '%专业%' then '3' when kcxz like '%通识%' then '1' else null end) kclbdm,
       (select kcxzdm from JW_JH_KCXZDMB where KCXZMC=t.kcxz) kcxzdm,
       '1' tkbj,
       to_char(sysdate,'yyyy-mm-dd HH24:mm:ss')||'交换生'
from likai_jhc_kck t
where not exists(select 1 from jw_jh_kcdmb kc where kc.KCH=t.kch)
'''