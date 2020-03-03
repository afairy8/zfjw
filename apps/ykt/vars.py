jgxx = '''
select jgmc from ZFTAL_XTGL_JGDMB t where t.JGYXBS='1'
and (length(jgdm)=4 or JG_ID='30') and jgdm not like '08%'
'''
bjxx = '''
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
yhxx = '''
select
distinct
       (select jgmc from ZFTAL_XTGL_JGDMB where xsj.JG_ID=jg_id) jgmc,
       (select bj from ZFTAL_XTGL_BJDMB where xsj.BH_ID=bh_id) bj,
       xsj.XM,
       xsj.xh,
       '3' sf,
       xsj.NJDM_ID,
       xsj.xm||'同学,你好!'bz1,
       '请你及时查询个人课表；绑定企业微信号；进入“雨课堂”查询相应课程公告、并加入课程的学习群。祝您身体健康！学习进步！【广州大学教务处】' bz
from JW_XK_XSXKB xkb,JW_XJGL_XSJBXXB xsj
where xkb.XNM='2019' and xkb.XQM='12'
and xkb.XH_ID=xsj.XH_ID
union
select distinct (select jgmc from ZFTAL_XTGL_JGDMB where jg_id=jzg.JG_ID) jgmc,
       '' bj,
       jzg.xm,
       jzg.JGH,
       '2' sf,
       '' njdm_id,
       jzg.xm||'老师，您好！'bz1,
       '请您及时在“雨课堂”发布课程学习QQ群、上课平台等课程信息，以便您的学生及时加入。谢谢！祝您身体健康！阖家幸福！【广州大学教务处】'bz

from
(select distinct rkb.JGH_ID
from JW_JXRW_JXBJSRKB rkb,JW_JXRW_JXBXXB jxb
where rkb.JXB_ID=jxb.JXB_ID
and jxb.XNM='2019' and jxb.XQM='12') t,jw_jg_jzgxxb jzg
where jzg.JGH_ID=t.JGH_ID
union
select distinct (select jgmc from ZFTAL_XTGL_JGDMB where jg_id=jzg.JG_ID) jgmc,
       '' bj,
       jzg.xm,
       jzg.JGH,
       '2' sf,
       '' njdm_id,
       jzg.xm||'老师，您好！'bz1,
       '请您及时在“雨课堂”发布课程学习QQ群、上课平台等课程信息，以便您的学生及时加入。谢谢！祝您身体健康！阖家幸福！【广州大学教务处】'bz

from
jw_jg_jzgxxb jzg
where jzg.DQZT='1'
'''

kkxx = '''
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

xkxx = '''
select
       (select jxbmc from JW_JXRW_JXBXXB where xkb.JXB_ID=jxb_id) jxbmc,
       (select xh from JW_XJGL_XSJBXXB where xkb.XH_ID=xh_id) xh
from JW_XK_XSXKB xkb
where xkb.XNM='2019'
and xkb.XQM='12'
'''
xkxx2Counts = '''select count(*) from JW_XK_XSXKB where xnm='2019' and xqm='12' and 1=1'''
xkxx2maxPc = 10000.0
xkxx2 = '''
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
mooc='''
select jgh,xm from JW_JG_JZGXXB xxb
where xxb.JGH_ID in (select hbb.jgh_id from JW_JXRW_JXBXXB 
jxb,JW_JXRW_JXBJSRKB hbb where jxb.JXB_ID=hbb.JXB_ID
and jxb.XNM='2019' and jxb.XQM='12')
'''

zgdxmooc='''
    select xsj.XH,xsj.xm,xsj.ZJHM,substr(xsj.ZJHM,length(xsj.ZJHM)-5,6) hlw,
     (select jgmc from ZFTAL_XTGL_JGDMB where JG_ID=xsj.jg_id) jgmc,
     (select bj from ZFTAL_XTGL_BJDMB where bh_id=xsj.bh_id) bj
     from JW_XJGL_XSJBXXB xsj where exists(select 1 from JW_XK_XSXKB xkb
    where xkb.XNM='2019' and xkb.XQM='12' and xkb.XH_ID=xsj.XH_ID)
'''
# code = {
#     # '机构信息': jgxx
#     # ,
#     # '班级信息': bjxx,
#     '用户信息': zgdxmooc
#     # '开课信息': kkxx,
#     # '选课信息': xkxx,
#     #'mooc':mooc
# }
code={
    '机构信息':jgxx,
    '班级信息':bjxx,
    '用户信息':yhxx,
    '开课信息':kkxx,
    '选课信息':xkxx
}

