##补充教学任务中的学时代码，常见有重修班
upRwXsdm='''
update JW_JXRW_JXBXXB jxb set jxb.xsdm='01'
where
((jxb.XNM=(select zdz from ZFTAL_XTGL_XTSZB t where t.zs='当前学年')
and
jxb.XQM=(select zdz from ZFTAL_XTGL_XTSZB t where t.zs='当前学期'))
or (jxb.XNM=(select zdz from ZFTAL_XTGL_XTSZB t where t.zs='任务落实学年')
and jxb.XQM=(select zdz from ZFTAL_XTGL_XTSZB t where t.zs='任务落实学期')
))
and jxb.XSDM is null
and jxb.KKLXDM not in ('00')
'''
###更新kklxdm=10教学任务中的课程归属、课程性质
createKKlx10TmpTable='''
create table likai_jw_txkcxzandgs as (
select rkb.JXB_ID,kc.KCH_ID,kc.KCXZDM,kc.KCGSDM,kc.KCLBDM from
JW_JXRW_JXBHBXXB rkb,JW_JXRW_JXBXXB jxb,JW_JH_KCDMB kc
where rkb.JXB_ID=jxb.JXB_ID
and jxb.KCH_ID=kc.KCH_ID
and jxb.XNM=(select zdz from ZFTAL_XTGL_XTSZB where zs='任务落实学年')
and jxb.XQM=(select zdz from ZFTAL_XTGL_XTSZB where zs='任务落实学期')
and jxb.KKLXDM in ('10','06'))
'''
upDateRwKklx10BaseInfo='''
update jw_jxrw_jxbhbxxb hbb
set 
hbb.KCXZDM=(select kcxzdm from likai_jw_txkcxzandgs t where t.jxb_id=hbb.JXB_ID),
hbb.KCGSDM=(select kcgsdm from likai_jw_txkcxzandgs t where t.jxb_id=hbb.JXB_ID),
hbb.KCLBDM=(select KCLBDM from likai_jw_txkcxzandgs t where t.jxb_id=hbb.JXB_ID)
where exists(select 1 from likai_jw_txkcxzandgs t where t.jxb_id=hbb.JXB_ID)
'''
dropKklx10TmpTable='''
drop table likai_jw_txkcxzandgs
'''

###更新重修报名开关
upCxbmKg='''
update JW_JXRW_JXBXXB jxb 
set jxb.CXBMKG='1'
where jxb.XNM=(select zdz from ZFTAL_XTGL_XTSZB t where t.zs='选课学年')
and jxb.XQM=(select zdz from ZFTAL_XTGL_XTSZB t where t.zs='选课学期')
and jxb.KKLXDM in ('01','06')
and jxb.CXBMKG<>'1'
and jxb.KKBM_ID<>'30' and 1=1
'''

#####插入板块类型班级对照表####
insertBkxsmd='''
insert into JW_XJGL_XSBKLXCJB (xh_id, BKLXDJB_ID, BKLX_ID)
select XH_ID, BKLXDJB_ID, BKLX_ID
from (select XH_ID,
             (select djb.BKLXDJB_ID
              from JW_JXRW_BKLXDJB djb,
                   JW_JXRW_BKLXB lxb
              where djb.BKLX_ID = lxb.BKLX_ID
                and lxb.BKLXMC like '体育%'
                and lxb.BKLXMC = t.bklxmc) BKLXDJB_ID,
             (select djb.BKLX_ID
              from JW_JXRW_BKLXDJB djb,
                   JW_JXRW_BKLXB lxb
              where djb.BKLX_ID = lxb.BKLX_ID
                and lxb.BKLXMC like '体育%'
                and lxb.BKLXMC = t.bklxmc) BKLX_ID
      from (select XH_ID, XNM, NJDM_ID, '体育' ||
                                        to_char((to_number(XNM) - to_number(nvl(NJDM_ID, 0)) + 1) *
                                                decode(XQM, '3', 1, '12', 2)) bklxmc
            from JW_XJGL_XSXJXXB xjb
            where xjb.XNM = (select zdz from ZFTAL_XTGL_XTSZB t where t.zs = '选课学年')
              and xjb.xqm = (select zdz from ZFTAL_XTGL_XTSZB t where t.zs = '选课学期')
              and xjb.XJZTDM in (select XJZTDM from JW_XJGL_XJZTDMB where SFYXJ = '1')
              and xjb.SFZX = '1'
              and xjb.JG_ID <> '30'
              and to_number(nvl(NJDM_ID, 0)) + 1 >= to_number(XNM)) t) t
where not exists(select 1
                 from JW_XJGL_XSBKLXCJB z
                 where z.XH_ID = t.XH_ID
                   and z.BKLX_ID = t.BKLX_ID
                   and z.BKLXDJB_ID = t.BKLXDJB_ID)
'''

###更新是否可选课
upxkbjSfkxk='''
update jw_jxrw_jxbxxb jxb 
set jxb.SFKXK='1'
where jxb.xnm=(select zdz from ZFTAL_XTGL_XTSZB t where t.zs='选课学年')
and jxb.xqm=(select zdz from ZFTAL_XTGL_XTSZB t where t.zs='选课学期')
'''


############小班研讨课的面向对象处理,没有设置面向对象的设为本学院高年级
xbYtkMxdx='''
insert into JW_JXRW_MXDXB (mxdxb_id, xnm, xqm, jxb_id, xzlb, xqh_id, jg_id, njdm_id)
select sys_guid()               mxdxb_id,
       jxb.XNM,
       jxb.XQM,
       jxb.jxb_id,
       'mx'                     xzlb,
       nvl(jxb.XQH_ID, '1')     xqh_id,
       jxb.KKBM_ID              jg_id,
       (to_number(jxb.XNM) - 1) njdm_id
from jw_jxrw_jxbxxb jxb
where (jxb.FJXB_ID is null or jxb.FJXB_ID = '1')
  and jxb.XNM = (select zdz from ZFTAL_XTGL_XTSZB where zs = '选课学年')
  and jxb.XQM = (select zdz from ZFTAL_XTGL_XTSZB where zs = '选课学期')
  and jxb.KCH_ID in (select kch_id from JW_JH_KCDMB where kch like '%XB%' and kch not in ('XB181660428','XB186700917'))
  and not exists(select 'x' from JW_JXRW_MXDXB mxb where mxb.JXB_ID = jxb.JXB_ID)
union
select sys_guid()               mxdxb_id,
       jxb.XNM,
       jxb.XQM,
       jxb.jxb_id,
       'mx'                     xzlb,
       nvl(jxb.XQH_ID, '1')     xqh_id,
       jxb.KKBM_ID              jg_id,
       (to_number(jxb.XNM) - 2) njdm_id
from jw_jxrw_jxbxxb jxb
where (jxb.FJXB_ID is null or jxb.FJXB_ID = '1')
  and jxb.XNM = (select zdz from ZFTAL_XTGL_XTSZB where zs = '选课学年')
  and jxb.XQM = (select zdz from ZFTAL_XTGL_XTSZB where zs = '选课学期')
  and jxb.KCH_ID in (select kch_id from JW_JH_KCDMB where kch like '%XB%' and kch not in ('XB181660428','XB186700917'))
  and not exists(select 'x' from JW_JXRW_MXDXB mxb where mxb.JXB_ID = jxb.JXB_ID)
union
select sys_guid()               mxdxb_id,
       jxb.XNM,
       jxb.XQM,
       jxb.jxb_id,
       'mx'                     xzlb,
       nvl(jxb.XQH_ID, '1')     xqh_id,
       jxb.KKBM_ID              jg_id,
       (to_number(jxb.XNM) - 3) njdm_id
from jw_jxrw_jxbxxb jxb
where (jxb.FJXB_ID is null or jxb.FJXB_ID = '1')
  and jxb.XNM = (select zdz from ZFTAL_XTGL_XTSZB where zs = '选课学年')
  and jxb.XQM = (select zdz from ZFTAL_XTGL_XTSZB where zs = '选课学期')
  and jxb.KCH_ID in (select kch_id from JW_JH_KCDMB where kch like '%XB%' and kch not in ('XB181660428','XB186700917'))
  and not exists(select 'x' from JW_JXRW_MXDXB mxb where mxb.JXB_ID = jxb.JXB_ID)
'''

#########面向对象中的学生类别去掉
upMxdxXslb='''
update JW_JXRW_MXDXB mxb set mxb.XSLBM='',CCDM=''
where exists(select 1 from JW_JXRW_JXBXXB jxb
             where jxb.XNM=(select zdz from ZFTAL_XTGL_XTSZB t where t.zs='选课学年')
          and jxb.XQM=(select zdz from ZFTAL_XTGL_XTSZB t where t.zs='选课学期')
          and jxb.KKLXDM='10'
          )
and mxb.XSLBM is not null or mxb.CCDM is not null
'''