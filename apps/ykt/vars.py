jgxx='''
select jgmc from ZFTAL_XTGL_JGDMB t where t.JGYXBS='1'
and (length(jgdm)=4 or JG_ID='30') and jgdm not like '08%'
'''
bjxx='''
select jg.JGMC,''zy,bj.bj,bj.NJDM_ID
from ZFTAL_XTGL_JGDMB jg,ZFTAL_XTGL_BJDMB bj
where jg.JG_ID=bj.JG_ID
and exists(select 1 from (
select xsj.BH_ID
from JW_XJGL_XSJBXXB xsj,JW_XK_XSXKB xkb
where xsj.XH_ID=xkb.XH_ID
and xkb.XNM='2019'
and xkb.XQM='12') t where t.BH_ID=bj.BH_ID)
'''
yhxx='''
select
distinct
       (select jgmc from ZFTAL_XTGL_JGDMB where xsj.JG_ID=jg_id) jgmc,
       (select bj from ZFTAL_XTGL_BJDMB where xsj.BH_ID=bh_id) bj,
       xsj.XM,
       xsj.xh,
       '3' sf,
       xsj.NJDM_ID
from JW_XK_XSXKB xkb,JW_XJGL_XSJBXXB xsj
where xkb.XNM='2019' and xkb.XQM='12'
and xkb.XH_ID=xsj.XH_ID
union
select distinct (select jgmc from ZFTAL_XTGL_JGDMB where jg_id=jzg.JG_ID) jgmc,
       '' bj,
       jzg.xm,
       jzg.JGH,
       '2' sf,
       '' njdm_id
from
(select distinct rkb.JGH_ID
from JW_JXRW_JXBJSRKB rkb,JW_JXRW_JXBXXB jxb
where rkb.JXB_ID=jxb.JXB_ID
and jxb.XNM='2019' and jxb.XQM='12') t,jw_jg_jzgxxb jzg
where jzg.JGH_ID=t.JGH_ID
'''

kkxx='''
 select (select jgmc from ZFTAL_XTGL_JGDMB where jxb.KKBM_ID=jg_id) jgmc,
        (select kch from jw_jh_kcdmb where jxb.KCH_ID=kch_id) kch,
        jxb.jxbmc,
        t.rkjs,
        t.rkxm,
        (select kcmc from JW_JH_KCDMB where kch_id=jxb.KCH_ID) kcmc,
        (select nvl(WM_CONCAT(bj.bj),'无') from ZFTAL_XTGL_BJDMB bj,JW_JXRW_JXBHBXXB hbb where hbb.BH_ID=bj.BH_ID and hbb.JXB_ID=jxb.JXB_ID) jxbzc,
        jxb.XNM,
        '2' xqm
 from
(select rkb.JXB_ID,WM_CONCAT(jzg.JGH) rkjs,WM_CONCAT(jzg.xm) rkxm from JW_JXRW_JXBJSRKB rkb,JW_JG_JZGXXB jzg
where rkb.JGH_ID=jzg.JGH_ID
group by rkb.JXB_ID) t,JW_JXRW_JXBXXB jxb
where t.JXB_ID=jxb.JXB_ID
and jxb.XNM='2019' and jxb.xqm='12'
'''

xkxx='''
select
       (select jxbmc from JW_JXRW_JXBXXB where xkb.JXB_ID=jxb_id) jxbmc,
       (select xh from JW_XJGL_XSJBXXB where xkb.XH_ID=xh_id) xh
from JW_XK_XSXKB xkb
where xkb.XNM='2019'
and xkb.XQM='12'
'''

code={
    '机构信息':jgxx
    ,
    '班级信息':bjxx,
    '用户信息':yhxx,
    '开课信息':kkxx,
    '选课信息':xkxx
}
# code={
#     '机构信息':jgxx,
#     '班级信息':bjxx,
#     '用户信息':yhxx,
#     '开课信息':kkxx,
#     '选课信息':xkxx
# }