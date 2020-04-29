###执行学生学业完成审核
procname = 'likai_jw_publicinterface.likai_xywcqk'

###毕业年度
bynd = '''select zdz from ZFTAL_XTGL_XTSZB where zdm='DQBYND' and 1=1'''

###毕业生信息
bysfzxx = '''select xh_id from JW_BYGL_BYSFZXXB fzb 
where fzb.BYNF='{}' and 1=1'''
xjbysxx = '''select xh_id from JW_XJGL_XSJBXXB  xsj 
where to_number(nvl(xsj.NJDM_ID,0))+to_number(nvl(xsj.xz,'4'))=to_number('{}')
'''
####查询语句
basicSelectXs = '''select xh_id from JW_XJGL_XSJBXXB xsj where 1=1\n'''
basicCondition1 = ' and 1=1'
basicJgCondition = '''
 and xsj.jg_id in (select jg_id from zftal_xtgl_jgdmb where jgmc||jgdm like '%{}%')
'''
basicZyCondition = ''' and xsj.zyh_id in (select zyh_id from zftal_xtgl_zydmb where zyh||zymc like '%{}%')
'''
basicNjCondition = '''
 and xsj.njdm_id ='{}'
'''
extendNjConditon = '''
 and to_number(nvl(xsj.njdm_id,0))+to_number(nvl(xsj.xz,'4'))=to_number('{}')
'''
##########课程替代审核通过引发的学业完成情况重新审核
# kctdXyShtmp = '''select distinct xh_id from JW_CJ_XSGRCJDTB t
#           '''
kctdXySh = '''select distinct xh_id from JW_CJ_XSGRCJDTB t
where exists(select 1 from JW_CJ_XSGRDTZB tt where t.KCTHZH_ID=tt.KCTHZH_ID
          and tt.ZSSJ like '%{}%' and tt.ZSZT='3')
          '''

###获取专业信息
getZyxx = '''select distinct zyh_id from JW_XJGL_XSJBXXB xsj where xsj.NJDM_ID='{}' and 1=1'''
###获取年级专业的学习正常进度
getNormalJd = '''
select *
from (select njdm_id, zyh_id, zyfx, to_number(xyjd) xyjd, row_number() over (partition by NJDM_ID, ZYH_ID, zyfx
  order by rc desc) rn
      from (select xsj.NJDM_ID, xsj.ZYH_ID, nvl(xsj.ZYFX_ID, 'wfx') zyfx, XYJD, count(t.XH_ID) rc
            from JW_BYGL_xsxyyjjgb t,
                 JW_XJGL_XSJBXXB xsj
            where t.XH_ID = xsj.XH_ID
              and xsj.NJDM_ID = '{}'
              and xsj.ZYH_ID = '{}'
            group by xsj.NJDM_ID, xsj.ZYH_ID, nvl(xsj.ZYFX_ID, 'wfx'), XYJD)) t
where t.rn = 1
'''
###获取年级专业学习进度低于diff差额的学生信息
getDiffXsxx = '''
select xsj.XH,xsj.xm,zy.zymc,xsj.NJDM_ID,t.XYJD,
(select bj from ZFTAL_XTGL_BJDMB where bh_id=xsj.BH_ID) bj,
(select jgmc from ZFTAL_XTGL_JGDMB where jg_id=xsj.jg_id) jgmc,'{}'
 from JW_BYGL_XSXYYJJGB t,JW_XJGL_XSJBXXB xsj,ZFTAL_XTGL_ZYDMB zy
where t.XH_ID=xsj.XH_ID and xsj.ZYH_ID=zy.ZYH_ID
and exists(select 1 from JW_XJGL_XJZTDMB where SFYXJ='1' and xsj.XJZTDM=xjztdm)
and xsj.NJDM_ID='{}' and xsj.ZYH_ID='{}' 
'''
###########当前学年学生已获、已选学分与各归属要求的最低学分的差额总和
getKcgsAndJsjy = '''
select
    t.XFYQJDMC,sum(case when
    t.yqzdxf-t.hdxf-to_number(nvl(LIKAI_KCGS_ZXF(t.XH_ID,t.XNM,t.xqm,t.kcgsdm),0))<0 then 0
    else t.yqzdxf-t.hdxf-to_number(nvl(LIKAI_KCGS_ZXF(t.XH_ID,t.XNM,t.xqm,t.kcgsdm),0))
    end) sumdiff
from
(select
xjb.XNM
,xjb.xqm
,xsjh.XH_ID
    ,xsjh.XFYQJDMC
    ,to_number(nvl(xsjh.YQZDXF,7)) yqzdxf
    ,to_number(nvl(xsjh.HDXF,0)) hdxf
    ,(select WM_CONCAT(KCGSDM) from JW_JH_JXZXJHXFYQXXFB xffb where xffb.XFYQJD_ID=xsjh.XFYQJD_ID) kcgsdm
    from JW_JH_XSJXZXJHXFYQXXB xsjh,JW_XJGL_XSXJXXB xjb
where xsjh.XH_ID=xjb.XH_ID
and xjb.XNM=(select zdz from ZFTAL_XTGL_XTSZB where zs='当前学年')
and xjb.XQM=(select zdz from ZFTAL_XTGL_XTSZB where zs='当前学期')
and xjb.NJDM_ID='{}'
and xsjh.ZGSHZT='N'
and nvl(xsjh.SFMJD,'0')='1'
and to_number(nvl(xsjh.YQZDXF,100))<10) t
where instr(t.kcgsdm,',')<=0 or XFYQJDMC like '%教师%选修%'
group by t.XFYQJDMC
'''

###毕业年度的毕业生辅助信息是否首次加载信息

sfScjzBysfzxx='''
select zdz from LIKAI_XTGL_XTSZB where zdm='BYSFZXXBSFSCJZ(@1)'
'''

###更新学制
upXz=[
    '''update JW_XJGL_XSXJXXB xjb set xjb.xz=(select xz from ZFTAL_XTGL_ZYDMB where zyh_id=xjb.zyh_id)
where xjb.XNM=(select zdz from ZFTAL_XTGL_XTSZB where zs='当前学年')
and  xjb.XQM=(select ZDZ from ZFTAL_XTGL_XTSZB where zs='当前学期')
and xjb.xz is null''',
    '''update jw_xjgl_xsjbxxb xsj set xsj.xz=(select xz from JW_XJGL_XSXJXXB xjb where xjb.XH_ID=xsj.XH_ID
    and xjb.XNM=(select zdz from ZFTAL_XTGL_XTSZB where zs='当前学年') 
    and xjb.XQM=(select ZDZ from ZFTAL_XTGL_XTSZB where zs='当前学期')
    )
    where xsj.xz <>(select xz from JW_XJGL_XSXJXXB xjb where xjb.XH_ID=xsj.XH_ID
    and xjb.XNM=(select zdz from ZFTAL_XTGL_XTSZB where zs='当前学年') 
    and xjb.XQM=(select ZDZ from ZFTAL_XTGL_XTSZB where zs='当前学期')
    )
    '''
    ]


# 插入毕业生辅助信息表

inBysFzxxb = '''
insert into JW_BYGL_BYSFZXXB(BYNF,xh_id)
select distinct 
'{}',xjb.XH_ID
from JW_XJGL_XSXJXXB xjb
where xjb.XNM=(select zdz from ZFTAL_XTGL_XTSZB where zs='当前学年')
and xjb.XQM=(select ZDZ from ZFTAL_XTGL_XTSZB where zs='当前学期')
and xjb.XJZTDM in (select XJZTDM from JW_XJGL_XJZTDMB where SFYXJ='1')
and nvl(xjb.SFZX,'0')='1'
and to_number(nvl(xjb.NJDM_ID,'0'))+to_number(nvl(xjb.xz,'4'))='{}'
and xjb.JG_ID<>'30'
and not exists(select 1 from JW_BYGL_BYSFZXXB fzb where fzb.XH_ID=xjb.XH_ID)
'''
###异动学生加载进入毕业生辅助信息表
ydInBysFzxxb='''
insert into JW_BYGL_BYSFZXXB(bynf,xh_id)
select distinct '{}',ydb.XH_ID
from (select *
from (select t.*,
             row_number() over (partition by t.XH_ID
               order by t.ZZSHSJ,t.XJYD_ID desc) rn
      from JW_XJGL_XJYDB t
      where nvl(t.YDSXXNM,xnm) = (select zdz from ZFTAL_XTGL_XTSZB where zs = '当前学年')
        and nvl(t.YDSXXQM, xqm) = (select zdz from ZFTAL_XTGL_XTSZB where zs = '当前学期') ) t
where t.rn=1) ydb
where nvl(ydb.YDHNJDM_ID,'0')+(case
          when ydb.YDHXZ is null then (select xz from zftal_xtgl_zydmb where zyh_id=ydb.YDHZYH_ID)
    else ydb.YDHXZ end )='{}'
and ydb.YDHXJZT in (select xjztdm from JW_XJGL_XJZTDMB where SFYXJ='1')
and nvl(ydb.YDHSFZX,'0')='1'
and nvl(ydb.YDHJG_ID,'30')<>'30'
and nvl(ydb.SHZT,'0')='3'
and not exists(select 1 from JW_BYGL_BYSFZXXB fzb where fzb.XH_ID=ydb.XH_ID);
'''
###添加毕业审核、学位审核名单
inbyshb='''
insert into JW_BYGL_BYSHB(BYND,XH_ID)
select bynf,xh_id from JW_BYGL_BYSFZXXB fzb
where not exists(select 1 from jw_bygl_byshb where xh_id=fzb.XH_ID)
and not exists(select 1 from JW_XJGL_XSJBXXB xsj where xsj.XH_ID=fzb.XH_ID and xsj.JG_ID='30')
and fzb.BYJR is null
and fzb.BYNF='{}'
'''
inXwshb='''
insert into JW_BYGL_XWSHB(bynd,xh_id)
select bynd,xh_id from JW_BYGL_BYSHB byb
where not exists(select 1 from JW_BYGL_XWSHB where byb.XH_ID=xh_id and byb.BYND=bynd)
and BYND='{}'
'''
###删除毕业审核、学位审核名单
deByshb='''
delete from JW_BYGL_BYSHB byb
where byb.BYND='{}'
and not exists(select 1 from JW_BYGL_BYSFZXXB fzb where fzb.XH_ID=byb.XH_ID)
'''

deXwshb='''
delete from JW_BYGL_XWSHB byb
where byb.BYND='{}'
and not exists(select 1 from JW_BYGL_BYSFZXXB fzb where fzb.XH_ID=byb.XH_ID)
'''


############毕业生自动刷新学业完成情况，自动进行毕业审核，学位审核机器
bysZdXywc='''
select fzb.BYND,(select njdm_id from jw_xjgl_xsjbxxb where xh_id=fzb.xh_id) nj,
(select zyh_id from JW_XJGL_XSJBXXB where fzb.XH_ID=xh_id) zyh_id,
'1' tjsy,
fzb.XH_ID
from JW_BYGL_BYSHB fzb

where fzb.BYND = (select ZDZ from ZFTAL_XTGL_XTSZB where zs = '当前毕业年度')
and not EXISTS(select
1
from JW_CJ_XSCJB cjb

where
cjb.XNM = (select zdz from ZFTAL_XTGL_XTSZB where zs = '当前学年')
          and cjb.XQM = (select zdz from ZFTAL_XTGL_XTSZB where zs = '当前学期')
                        and cjb.XH_ID = fzb.XH_ID
                                        and to_number(cjb.CJZT)< = 1
)
  and nvl(fzb.JSBYF,'2')='2'
'''

################清空已毕业且在当前学年学期有选课还没有成绩的学生的选课信息
deleteYbyButKccjNotExists='''
delete from JW_XK_XSXKB xkb
where xkb.XNM=(select zdz from ZFTAL_XTGL_XTSZB where zs='当前学年')
and xkb.XQM=(select zdz from ZFTAL_XTGL_XTSZB where zs='当前学期')
and exists (select 1 from JW_BYGL_BYSFZXXB fzb where fzb.BYJR='毕业'
and fzb.XH_ID=xkb.XH_ID)
and not exists (select 1 from JW_CJ_XSCJB cjb where cjb.XH_ID=xkb.XH_ID and cjb.JXB_ID=xkb.JXB_ID)
and xkb.XH_ID not in ['s564400010']
'''

deleteYbyButKccjNotExists_ksmd='''
delete from JW_KW_XSKSXXB xkb
where xkb.XNM=(select zdz from ZFTAL_XTGL_XTSZB where zs='当前学年')
and xkb.XQM=(select zdz from ZFTAL_XTGL_XTSZB where zs='当前学期')
and exists (select 1 from JW_BYGL_BYSFZXXB fzb where fzb.BYJR='毕业'
and fzb.XH_ID=xkb.XH_ID)
and not exists (select 1 from JW_CJ_XSCJB cjb where cjb.XH_ID=xkb.XH_ID and cjb.JXB_ID=xkb.JXB_ID)
and xkb.XH_ID not in ['s564400010'];
'''