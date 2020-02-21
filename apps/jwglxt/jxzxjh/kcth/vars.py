# 1-首先取未审核的课程替代信息；
# 2-对于一个未审核的课程替代信息，从以下几个方面考虑
# 2-1：替代课程的学分和与被替代课程的学分和；
# 2-2：被替代课程中最晚开课学年学期；被替代课程的最晚开课学年学期在当前学年学期之后，要标出
# 2-3：学生的基本信息：1）学籍异动情况；2）入学情况；3）现年级专业情况；
###取未审核的课程替代信息
getKctdMain='''
select KCTHZH_ID,nvl(dtly,'#') dtly from JW_CJ_XSGRDTZB t where t.ZSZT='1' 
'''
upKctdMain='''
update jw_cj_xsgrdtzb set dtly=DTLY||'#{}' where KCTHZH_ID='{}' and 1=1
'''
initKctdMain='''
update JW_CJ_XSGRDTZB t set DTLY=substr(dtly,1,instr(dtly,'#')-1) where t.ZSZT='1'
'''
##取未审核的替代课程信息
getKctdCj='''
select t.KCTHZH_ID,t.XH_ID,sum(nvl(cjb.xf,0)) xfh from JW_CJ_XSGRCJDTB t,JW_CJ_XSCJB cjb 
where t.KCTHZH_ID='{}'
and t.XH_ID=cjb.XH_ID and t.JXB_ID=cjb.JXB_ID
group by t.KCTHZH_ID,t.XH_ID
'''
###取未审核的被替代课程学分信息
getKctdJh='''
select t.KCTHZH_ID,t.XH_ID,sum(nvl(t.xf,0)) xfh from JW_CJ_XSGRjhDTB t where t.KCTHZH_ID='{}'
group by t.KCTHZH_ID,t.XH_ID
'''
#########取未审核的被替代课程的课程最大学年学期信息
getKctdJhXn='''
select max(XNM) from JW_CJ_XSGRJHDTB t where t.KCTHZH_ID='{}'
'''
getKctdJhxq='''
select max(Xqm) from JW_CJ_XSGRJHDTB t where t.KCTHZH_ID='{}' and XNm='{}' and 1=1
'''
####取未审核的课程替代中学生的当前修读状况
getXsDqxdZt='''
select nvl(WM_CONCAT(kcmc),'无') from (
select distinct kc.kcmc from JW_CJ_XSGRjhDTB t ,JW_JH_KCDMB kc
where exists(select 1 from JW_XK_XSXKB xkb where xkb.XH_ID=t.XH_ID
and t.KCH_ID=xkb.KCH_ID and xkb.XNM=(select zdz from ZFTAL_XTGL_XTSZB where zs='当前学年')
and xkb.XQM=(select zdz from ZFTAL_XTGL_XTSZB where zs='当前学期'))
and not exists(select 1 from JW_CJ_XSCJB where t.XH_Id=xh_id and kch_id=kc.KCH_ID)
and t.KCH_ID=kc.KCH_ID and t.KCTHZH_ID='{}')
'''
###############取最晚的异动学年学期信息
getXsYdxn='''
select max(YDSXXNM) from JW_XJGL_XJYDB t where t.XH_ID='{}'
and t.YDLBM in (select ydlbm from JW_XJGL_XJYDLBDMB where XJYDMC in ('转专业','延长在读年限')) and 1=1
'''
getXsydxq='''
select max(YDSXXQM) from JW_XJGL_XJYDB t where t.XH_ID='{}'
and t.YDLBM in (select ydlbm from JW_XJGL_XJYDLBDMB where XJYDMC in ('转专业','延长在读年限'))
and t.YDSXXNM='{}' and 1=1
'''
##############取学生的现信息
getXsxx='''
select '学号'||(select xh from JW_XJGL_XSJBXXB where xh_id=xjb.xh_id)||'年级'||xjb.NJDM_ID||'专业号'||zy.zyh||'专业名称'||zy.zymc from JW_XJGL_XSXJXXB xjb,ZFTAL_XTGL_ZYDMB zy
where 
xjb.ZYH_ID=zy.ZYH_ID and 
xjb.XNM=(
select max(zdz) from (
select zdz from ZFTAL_XTGL_XTSZB t where t.zs='选课学年'
union 
select zdz from ZFTAL_XTGL_XTSZB t where t.zs='当前学年'
)
)
and xjb.xqm=(
select max(zdz) from (
select zdz from ZFTAL_XTGL_XTSZB t where t.zs='选课学期'
union 
select zdz from ZFTAL_XTGL_XTSZB t where t.zs='当前学期'
))
and xjb.XH_ID='{}' and 1=1
'''
############取学生的转专业、延长在读年限信息
getXsxjydxx='''
select nvl(count(1),0) from jw_xjgl_xjydb ydb,JW_XJGL_XJYDLBDMB dmb
where ydb.YDLBM=dmb.YDLBM
and dmb.XJYDMC in ('转专业','延长在读年限') 
and ydb.XH_ID='{}' and 1=1
'''

getZwZzyYczdxn='''
select nvl(WM_CONCAT(kcxx),'无') from (
select kc.kcmc kcxx
from JW_CJ_XSGRJHDTB jh,
     JW_JH_KCDMB kc
where jh.KCH_ID = kc.KCH_ID
  and jh.KCTHZH_ID = '{}'
  and jh.XH_ID = '{}'
  and exists(select 1
             from (select max(to_number(nvl(ydb.YDSXXNM, 0)) * 100 + to_number(nvl(ydb.YDSXXQM, 0))) zwsx
                   from JW_XJGL_XJYDB ydb,
                        JW_XJGL_XJYDLBDMB dmb
                   where ydb.XH_ID = '{}'
                     and ydb.YDLBM = dmb.YDLBM
                     and dmb.YDLBM in ('转专业', '延长在读年限')) t
             where to_number(nvl(jh.XNM, 0)) * 100 + to_number(nvl(jh.XQM, 0)) >= t.zwsx))
'''

