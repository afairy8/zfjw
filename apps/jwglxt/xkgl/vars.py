###清除选课又报名的情形
delCxbmAndYxk='''
delete from JW_CJ_CXBMB bmb
where exists(select 1 from jw_xk_xsxkb xkb where 
bmb.XH_ID=xkb.XH_ID and bmb.KCH_ID=xkb.KCH_ID
and bmb.XNM=xkb.xnm and bmb.xqm=xkb.XQM)
and bmb.XNM=(select zdz from ZFTAL_XTGL_XTSZB where zs='选课学年')
and bmb.XQM=(select zdz from ZFTAL_XTGL_XTSZB where zs='选课学期')
'''
###更新重修标记
updateCxbj='''
update jw_xk_xsxkb xkb
set xkb.CXBJ='1'
where xkb.CXBJ='0' and exists(select 'x' from JW_CJ_XSCJB
where xkb.XH_ID=xh_id and xkb.KCH_ID=kch_id and xqm!=xkb.XQM and xnm!=xkb.XNM)
and xkb.XNM=(select zdz from ZFTAL_XTGL_XTSZB where zs='选课学年')
and xkb.XQM=(select zdz from ZFTAL_XTGL_XTSZB where zs='选课学期')
'''
###配课管理
pkgllist=[
    'analyze table jw_xjgl_xsxjxxb compute statistics',
    'analyze table jw_xk_xsxkb compute statistics',
    'analyze table jw_jxrw_jxbxxb compute statistics',
    'analyze table jw_jxrw_jxbhbxxb compute statistics',
    'analyze table jw_xk_xspkztb compute statistics',
    'analyze table jw_xk_xsxkpklsb compute statistics',
    'analyze table jw_jcdm_cdxqxxb compute statistics',
    'analyze table jw_pk_kbcdb compute statistics',
    'analyze table jw_pk_kbsjb compute statistics',
    'analyze table jw_cj_xscjb compute statistics',
    '''update jw_xjgl_xsxjxxb set ZYFX_ID='wfx' where xnm=(select zdz from ZFTAL_XTGL_XTSZB where zs='选课学年')
    and xqm=(select zdz from ZFTAL_XTGL_XTSZB where zs='选课学期') and ZYFX_ID is null 
    and XJZTDM in (select XJZTDM from JW_XJGL_XJZTDMB where SFYXJ='1')'''
]
###缺子教学班的选课情形
insertFjxbOrZjxb='''
insert into JW_XK_XSXKB (JXB_ID,
                         xh_id,
                         xklc,
                         xkbj,
                         sxbj,
                         cxbj,
                         fxbj,
                         jcytbj,
                         zy,
                         qz,
                         xkfbbj,
                         xksj,
                         sxsj,
                         jgh_id,
                         xkxnm,
                         xkxqm,
                         xkkch_id,
                         xnm,
                         xqm,
                         kch_id,
                         jcydsj,
                         bxbj,
                         lszy,
                         sfqzbj,
                         cxbmlx,
                         sfkp,
                         xdbj,
                         bz,
                         bklx_id,
                         KKLXDM,
                         zxbj)
select case
         when t.FJXB_ID is null then (select jxb_id
                                      from (select JXB_ID, FJXB_ID, row_number() over (partition by fJXB_ID
                                        order by JXBRS asc) rn
                                            from JW_JXRW_JXBXXB jxb) a
                                      where a.rn = 1
                                        and a.fJXB_ID = t.jxb_id)
         else t.fjxb_id end jxb_id,
       t.XH_ID              xh_id,
       '0'                  xklc,
       '10'                 xkbj,
       '1'                  sxbj,
       '0'                  cxbj,
       '0'                  fxbj,
       '0'                  jcytbj,
       '1'                  zy,
       '0'                  qz,
       '0'                  xkfbbj,
       sysdate              xksj,
       '0'                  sxsj,
       t.XH_ID              jgh_id,
       ''                   xkxnm,
       ''xkxqm,
       ''xkkch_id,
       t.xnm                xnm,
       t.xqm                xqm,
       t.KCH_ID             kch_id,
       ''jcydsj,
       '0'                  bxbj,
       '0'                  lszy,
       '0'                  sfqzbj,
       '0'                  cxbmlx,
       '1'                  sfkp,
       ''                   xdbj,
       ''                   bz,
       ''                   bklx_id,
       t.KKLXDM             kklxdm,
       '0'                  zxbj
from (select *
      from (select b.kklxdm,
                   b.xnm,
                   b.xqm,
                   a.xh_id,
                   b.jxb_id,
                   b.kch_id,
                   b.jxbmc,
                   b.fjxb_id,
                   nvl(b.fjxb_id, b.jxb_id) zzjxb_id
            from jw_xk_xsxkb a,
                 jw_jxrw_jxbxxb b
            where a.xnm || a.xqm = (select zdz from zftal_xtgl_xtszb t where t.zs = '选课学年') ||
                                   (select zdz from zftal_xtgl_xtszb t where t.zs = '选课学期')
              and a.jxb_id in
                  (select jxb_id
                   from jw_jxrw_jxbxxb
                   where xnm || xqm = (select zdz from zftal_xtgl_xtszb t where t.zs = '选课学年') ||
                                      (select zdz from zftal_xtgl_xtszb t where t.zs = '选课学期')
                     and fjxb_id is not null--二级教学班
                   union all
                   select jxb_id
                   from jw_jxrw_jxbxxb
                   where xnm || xqm = (select zdz from zftal_xtgl_xtszb t where t.zs = '选课学年') ||
                                      (select zdz from zftal_xtgl_xtszb t where t.zs = '选课学期')
                     and jxb_id in (select fjxb_id
                                    from jw_jxrw_jxbxxb
                                    where xnm || xqm = (select zdz from zftal_xtgl_xtszb t where t.zs = '选课学年') ||
                                                       (select zdz from zftal_xtgl_xtszb t where t.zs = '选课学期')
                                      and fjxb_id is not null))
              and a.jxb_id = b.jxb_id)
      where (xh_id, zzjxb_id) in (select xh_id, zzjxb_id
                                  from (select a.xh_id, b.jxb_id, b.jxbmc, b.fjxb_id, nvl(b.fjxb_id, b.jxb_id) zzjxb_id
                                        from jw_xk_xsxkb a,
                                             jw_jxrw_jxbxxb b
                                        where a.xnm || a.xqm =
                                              (select zdz from zftal_xtgl_xtszb t where t.zs = '选课学年') ||
                                              (select zdz from zftal_xtgl_xtszb t where t.zs = '选课学期')
                                          and a.jxb_id in
                                              (select jxb_id
                                               from jw_jxrw_jxbxxb
                                               where xnm || xqm =
                                                     (select zdz from zftal_xtgl_xtszb t where t.zs = '选课学年') ||
                                                     (select zdz from zftal_xtgl_xtszb t where t.zs = '选课学期')
                                                 and fjxb_id is not null
                                               union all
                                               select jxb_id
                                               from jw_jxrw_jxbxxb
                                               where xnm || xqm =
                                                     (select zdz from zftal_xtgl_xtszb t where t.zs = '选课学年') ||
                                                     (select zdz from zftal_xtgl_xtszb t where t.zs = '选课学期')
                                                 and jxb_id in (select fjxb_id
                                                                from jw_jxrw_jxbxxb
                                                                where xnm || xqm = (select zdz
                                                                                    from zftal_xtgl_xtszb t
                                                                                    where t.zs = '选课学年') || (select zdz
                                                                                                             from zftal_xtgl_xtszb t
                                                                                                             where t.zs = '选课学期')
                                                                  and fjxb_id is not null))
                                          and a.jxb_id = b.jxb_id)
                                  group by xh_id, zzjxb_id
                                  having count(*) = 1)
      order by xh_id, jxbmc) t      
'''

preQuickExpXkmd='''
select count(1) from JW_XK_XSXKB xkb
where xkb.XNM=(select zdz from ZFTAL_XTGL_XTSZB where zs='选课学年')
and xkb.XQM=(select zdz from ZFTAL_XTGL_XTSZB where zs='选课学期')
'''

quickExpXkmd='''
select * from (
select
       (select zdz from ZFTAL_XTGL_XTSZB where zs='选课学年') xn,
        (select zdz from ZFTAL_XTGL_XTSZB where zs='选课学期') xq,
       xsj.xh,
        xsj.XM,
       (select jgmc from ZFTAL_XTGL_JGDMB where jg_id=xsj.JG_ID) jgmc,
       (select zymc from ZFTAL_XTGL_ZYDMB where xsj.ZYH_ID=zyh_id) zymc,
       (select bj from ZFTAL_XTGL_BJDMB where xsj.BH_ID=bh_id) bj,
       xsj.NJDM_ID,
       (select kcmc from JW_JH_KCDMB where xkb.KCH_ID=kch_id) kcmc,
       (select WM_CONCAT(hbb.KCXZMC) from (select distinct hbb.JXB_ID, t.kcxzmc from JW_JH_KCXZDMB t,JW_JXRW_JXBHBXXB hbb
       where t.KCXZDM=hbb.KCXZDM) hbb where hbb.JXB_ID=xkb.JXB_ID) kcxz,
       (select WM_CONCAT(jzg.XM||'(工号：'||jzg.JGH||',教师所属学院：'||jg.jgmc||')') from ZFTAL_XTGL_JGDMB jg,JW_JXRW_JXBJSRKB rkb,JW_JG_JZGXXB jzg where rkb.JGH_ID=jzg.JGH_ID
       and rkb.JXB_ID=xkb.JXB_ID and jzg.JG_ID=jg.JG_ID) rkjsxx,
       (select jxbmc from JW_JXRW_JXBXXB where xkb.JXB_ID=jxb_id) jxbmc,
       ROWNUM rowCount
from JW_XK_XSXKB xkb,JW_XJGL_XSJBXXB xsj
where xkb.XNM=(select zdz from ZFTAL_XTGL_XTSZB where zs='选课学年')
and xkb.XQM=(select zdz from ZFTAL_XTGL_XTSZB where zs='选课学期')
and xkb.XH_ID=xsj.XH_ID) t
where t.rowCount between {} and {}
'''