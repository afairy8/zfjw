
####恢复学生评价
restoreXspj='''
insert into JW_PJ_XSPFB
select * from likai_jw_pj_xspfb  t where not exists(select 1 from JW_PJ_XSPFB z where z.XSPFB_ID=t.XSPFB_ID
and z.XNM=t.XNM and z.XQM=t.XQM) and t.XNM=(select zdz from ZFTAL_XTGL_XTSZB where zs='评价学年')
and t.XQM=(select zdz from ZFTAL_XTGL_XTSZB where zs='评价学期')
'''


###删除学生评价数据之前先备份
backXspj='''
insert into LIKAI_JW_PJ_XSPFB
select * from JW_PJ_XSPFB t where not exists(select 1 from JW_PJ_XSPFB z where z.XSPFB_ID=t.XSPFB_ID
and z.XNM=t.XNM and z.XQM=t.XQM) and t.XNM=(select zdz from ZFTAL_XTGL_XTSZB where zs='评价学年')
and t.XQM=(select zdz from ZFTAL_XTGL_XTSZB where zs='评价学期')
'''
###删除无效数据
###1-删除评价教学班中的限制数据以及学生不可评但已评的数据
delPjjxbXz='''
delete from JW_PJ_XSPFB pfb
where
  (exists(select 1 from JW_PJ_PJJXBXZB xz where xz.XNM=pfb.XNM and xz.XQM=pfb.XQM
and pfb.JXB_ID=xz.JXB_ID and pfb.JGH_ID=xz.JGH_ID)
or exists(select 1 from JW_XK_XSXKB xkb where pfb.xnm=xkb.xnm and pfb.xqm=xkb.xqm
and pfb.XH_ID=xkb.XH_ID and pfb.JXB_ID=xkb.JXB_ID and xkb.SFKP='0')
  )
and pfb.XNM=(select zdz from ZFTAL_XTGL_XTSZB where zs='评价学年')
and pfb.XQM=(select zdz from ZFTAL_XTGL_XTSZB where zs='评价学期')
'''
#####2-删除评分低于60分的学生评价
delPjlt60='''
delete from JW_PJ_XSPFB pfb 
where to_number(nvl(pfb.BFZPF,0))<to_number('{}')
and pfb.XNM=(select zdz from ZFTAL_XTGL_XTSZB where zs='评价学年')
and pfb.XQM=(select zdz from ZFTAL_XTGL_XTSZB where zs='评价学期')
'''
###3-删除参评学生限制的学生评价
delcpxsxz='''
delete from JW_PJ_XSPFB pfb where pfb.XNM=(select zdz from ZFTAL_XTGL_XTSZB where zs='评价学年')
and pfb.xqm=(select zdz from ZFTAL_XTGL_XTSZB where zs='评价学期')
and exists(select 1 from JW_PJ_CPXSXZB xz where xz.XH_ID=pfb.XH_ID and xz.XNM=pfb.XNM and xz.XQM=pfb.XQM)
'''
###退回学生评价信息
rollXspj='''
update jw_pj_xspfb set tjzt='0' 
where TJZT='1'
and xnm=(select zdz from ZFTAL_XTGL_XTSZB where zs='评价学年')
and xqm=(select zdz from ZFTAL_XTGL_XTSZB where zs='评价学期')
and XH_ID in (select xh_id from JW_XJGL_XSJBXXB where xh='{}')
and BFZPF is not null 
and to_number(BFZPF)<60
'''

getWpjXsNum='''
select count(*) from (
SELECT T.XH
    ,T.XM||'同学，您好！本学期，您还有'||WM_CONCAT(T.KCMC)||
     '等课程未进行教学评价，请您尽快登录教务系统进行客观、公正的教学评价！温馨提醒：未全部完成评价的学生不可以选课！' CONTENT
    FROM
(SELECT
       (SELECT XH FROM JW_XJGL_XSJBXXB XSJ WHERE XSJ.XH_ID=XKB.XH_ID) XH,
       (SELECT XM FROM JW_XJGL_XSJBXXB XSJ WHERE XSJ.XH_ID=XKB.XH_ID) XM,
  XKB.XH_ID
  ,XKB.JXB_ID
  ,RKB.JGH_ID
  ,JXB.KCH_ID
  ,(SELECT KCMC FROM JW_JH_KCDMB WHERE JXB.KCH_ID=KCH_ID) KCMC
FROM
     JW_XK_XSXKB XKB
    ,JW_JXRW_JXBJSRKB RKB
    ,JW_JXRW_JXBXXB JXB
WHERE
    XKB.JXB_ID=RKB.JXB_ID AND JXB.JXB_ID=RKB.JXB_ID AND JXB.XNM=XKB.XNM AND JXB.XQM=XKB.XQM AND XKB.SFKP='1'
AND XKB.XNM=(SELECT ZDZ FROM ZFTAL_XTGL_XTSZB T WHERE T.ZS='评价学年')
AND XKB.XQM=(SELECT ZDZ FROM ZFTAL_XTGL_XTSZB T WHERE T.ZS='评价学期')
--教学班、教师能评价
AND NOT EXISTS(SELECT 1 FROM JW_PJ_PJJXBXZB XZ WHERE XZ.XNM=XKB.XNM AND XZ.XQM=XKB.XQM
    AND XKB.JXB_ID=XZ.JXB_ID AND RKB.JGH_ID=XZ.JGH_ID)
--学生能评价
AND NOT EXISTS(SELECT 1 FROM JW_PJ_CPXSXZB XZ WHERE XZ.XNM=XKB.XNM AND XZ.XQM=XKB.XQM
    AND XKB.XH_ID=XZ.XH_ID)
--学生还没有评价
AND NOT EXISTS(SELECT 1 FROM JW_PJ_XSPFB PF WHERE PF.XNM=XKB.XNM AND PF.XQM=XKB.XQM
    AND PF.XH_ID=XKB.XH_ID AND PF.JGH_ID=RKB.JGH_ID AND PF.JXB_ID=XKB.JXB_ID AND PF.TJZT='1')
--有设置课程评价模板
AND EXISTS(SELECT 1 FROM JW_PJ_PJKCSZB SZ WHERE SZ.XNM=JXB.XNM AND SZ.XQM=JXB.XQM AND SZ.KCH_ID=JXB.KCH_ID
        AND SZ.LX=JXB.XSDM)
--学生有学籍
AND EXISTS(SELECT 1 FROM JW_XJGL_XSXJXXB XJB WHERE XJB.XNM=XKB.XNM AND XJB.XQM=XKB.XQM AND XJB.XH_ID=XKB.XH_ID
        AND XJZTDM IN (SELECT XJZTDM FROM JW_XJGL_XJZTDMB WHERE SFYXJ='1'))
) T
where t.xh not like 's%'
GROUP BY T.XH,T.XM)
'''

####把在校学生一门课都没有选的学生进行参评学生限制
insertCpxsxz='''
insert into JW_PJ_CPXSXZB(XNM,XQM,xh_id)
--一门课都没选的
select xnm,xqm,xh_id from
    (select xjb.XNM,xjb.XQM,xjb.XH_ID
from JW_XJGL_XSXJXXB xjb
where xjb.XNM = (select zdz from ZFTAL_XTGL_XTSZB where zs = '评价学年')
  and xjb.XQM = (select zdz from ZFTAL_XTGL_XTSZB where zs = '评价学期')
  and xjb.XJZTDM in (select XJZtdm from JW_XJGL_XJZTDMB where SFYXJ = '1')
  and xjb.JG_ID<>'30'
  and xjb.SFZX='1'
  and not exists(select 1
                 from JW_XK_XSXKB xkb
                 where xkb.XNM = xjb.XNM
                   and xkb.XQM = xjb.XQM
                   and xkb.XH_ID = xjb.XH_ID)
  and exists(select 1 from JW_JXRW_JXBHBXXB hbb,JW_JXRW_JXBXXB jxb
             where jxb.JXB_ID=hbb.JXB_ID and jxb.xnm=xjb.XNM and jxb.XQM=xjb.XQM
          and hbb.BH_ID=xjb.BH_ID)
union
--选的都是没有模板的
select t1.XNM,t1.XQM,t1.xh_id
from (select xkb.XNM,xkb.XQM,xkb.XH_ID, count(xkb.JXB_ID) wmpkcms
      from JW_XK_XSXKB xkb
      where exists(select 1
                   from (select jxb.XNM, jxb.XQM, jxb.JXB_ID
                         from JW_JXRW_JXBXXB jxb
                         where jxb.XNM = (select zdz from ZFTAL_XTGL_XTSZB where zs='评价学年')
                           and jxb.XQM = (select zdz from ZFTAL_XTGL_XTSZB where zs='评价学期')
                           and not exists(select 1
                                          from JW_PJ_PJKCSZB sz
                                          where sz.XNM = jxb.XNM
                                            and sz.xqm = jxb.XQM
                                            and sz.KCH_ID = jxb.KCH_ID
                                            and sz.lx = jxb.XSDM)
                           and jxb.KKLXDM <> '00') t--课程无末班的教学班
                   where t.XNM = xkb.XNM
                     and t.XQM = xkb.XQM
                     and t.JXB_ID = xkb.JXB_ID)
      group by xkb.XNM,xkb.XQM,xkb.XH_ID) t1,
     (select xkb.XNM,xkb.XQM,xkb.XH_ID, count(xkb.JXB_ID) gxkms
      from JW_XK_XSXKB xkb
      where xkb.xnm = (select zdz from ZFTAL_XTGL_XTSZB where zs='评价学年')
        and xkb.xqm = (select zdz from ZFTAL_XTGL_XTSZB where zs='评价学期')
      group by xkb.xnm,xkb.XQM,xkb.XH_ID) t2
where t1.XH_ID = t2.XH_ID and t1.XNM=t2.XNM and t1.XQM=t2.XQM
  and t1.wmpkcms = t2.gxkms
 union
 --选了有模板，但是教学班教师都被限制参评了
 select t1.XNM,t1.XQM,t1.XH_ID from
(select
xkb.XNM,xkb.xqm,xkb.XH_ID,count(*) bkpjxbjssl
from
     JW_JXRW_JXBJSRKB rkb,JW_XK_XSXKB xkb
where rkb.JXB_ID=xkb.JXB_ID
and exists(select 1 from JW_PJ_PJJXBXZB xz where xz.JXB_ID=rkb.JXB_ID and xz.JGH_ID=rkb.JGH_ID)
and xkb.XNM=(select zdz from ZFTAL_XTGL_XTSZB where zs='评价学年')
and xkb.XQM=(select zdz from ZFTAL_XTGL_XTSZB where zs='评价学期')
group by xkb.XNM,xkb.XQM,xkb.XH_ID) t1,
(select
xkb.XNM,xkb.xqm,xkb.XH_ID,count(*) zgkpjxbjssl
from
     JW_JXRW_JXBJSRKB rkb,JW_XK_XSXKB xkb
where rkb.JXB_ID=xkb.JXB_ID
and xkb.XNM=(select zdz from ZFTAL_XTGL_XTSZB where zs='评价学年')
and xkb.XQM=(select zdz from ZFTAL_XTGL_XTSZB where zs='评价学期')
group by xkb.XNM,xkb.XQM,xkb.XH_ID)t2
where t1.XNM=t2.XNM and t1.XQM=t2.XQM and t1.XH_ID=t2.XH_ID and t1.bkpjxbjssl=t2.zgkpjxbjssl
  ) t1
where not exists(select 1 from JW_PJ_CPXSXZB xz where xz.XNM=t1.XNM and xz.XQM=t1.XQM and xz.XH_ID=t1.XH_ID)
'''


####获取学生评语
getXsPy='''
select xh_id,py from JW_PJ_XSPFB
where py is not null
'''