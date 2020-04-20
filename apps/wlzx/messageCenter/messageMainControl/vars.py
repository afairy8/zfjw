##############setting the messages control paramars############################

############
debug=False
sfqywxzjfs=True###是否直接发向企业微信
##########外表数据存放路径
xlsxSavePath='D:\\projects\\zfjw\\common\\readFiles\\'
##########set the send time paras######################
keBiaoZc=[100]#课表发送周次['1','2','3'],教师与学生共用
keBiaoJgDay=1#课表发送提前天数
####是否关闭学生课表发送提醒
keBiaoXsClose=True#为True时不向学生发送课表
ksJgDay=2#考试发送提前天数
otherJgDay=0#其他发送提前天数,常用的有调停课，场地借用，学籍异动，缓考，
###停课参数
tkJgDay=2#停课消息发送提前天数
tkrq=['2019-11-22']
tkyy='2019年学校运动会的安排'
##################setting the grade commits paras##########
jsCjLrJgDay=3#提醒教师提交成绩的时间间隔,
cjLrExcludeUser=[]
xsCjTxSfFsCjb=0#是否向学生发送cjb中的数据，为0表示只发送补录表中的数据
####################选课提醒参数，检测必修课是否有漏选情形##########
xkTxNj=['2019','2018','2017','2016']#选课提醒年级
xkTxZc=[18,19,20,1]#选课提醒周次
xkTxXqj=[2]#选课提醒星期几
xkTxRq=['2019-09-03','2019-09-04']#选课提醒日期
##############邀请教师完善教师简介、研究方向
yQJsZc=[16]
yQJsXqj=[4]
####################学生教学评价发送参数
xsJxpjTxZc=[16,17]
xsJxpjTxXqj=[1,3,5,6]
###############
############setting the xxlx status###########
############慕课修读提醒参数################
xkMkTxRq=['2019-09-23']
xkMkTxZc=[]
xkMkTxXqj=[]
############教学任务停开提醒
jsJxrwTtkTxZc=[19]
jsJxrwTtkTxXqj=[1]
#######set the MsgCenter paras#############
accountid = 'gzhujwxt'
accountkey = 'zpGZ5c5cku471M3741C3gdbPO0'
accountBaseURL = 'http://172.17.1.134'
#################setting the xxlx#########
def getXxlx():
    '''注册发送的消息类型，如没有提供jgDay,则表示不发送'''
    xxlx=[
        ('教师课表','01',keBiaoJgDay,1),
        ('教师节假日课表','01_jJR',keBiaoJgDay,1),
        ('学生课表Long', '02', keBiaoJgDay,3),
        ('教师（管理员）学籍异动','03',otherJgDay,1),
        ('学生学籍异动','031',otherJgDay,2),
        ('教师场地借用','04',otherJgDay,1),
        ('学生考试Long','05',ksJgDay,3),
        ('教师监考','06',ksJgDay,1),
        ('教师调停课','07',otherJgDay,1),
        ('学生调停课Long','08',otherJgDay,3),
        ('学生缓考','09',otherJgDay,1),
        ('教师（管理员）学生缓考', '091', otherJgDay,1),
        # ('学生选课提醒', '10', xkTxNj),
        ('教师成绩录入', '11', otherJgDay,1),
        ('学生新增成绩提醒', '12', otherJgDay,2),
        ('学生慕课修读提醒Long','13',otherJgDay,3),
        ('学业预警消息','14',None,2),
        ('学生成绩作废提醒','15',None,2),
        ('教师教学班停开', '16', otherJgDay,1),
        ('待定','17',None,3),
        ('教师停课课表', '18', tkJgDay,1),
        ('教师个人简介','19',otherJgDay,1),
        ('学生评教提醒','20',otherJgDay,2),
        ('教师管理员成绩修改', 'cjxg01', otherJgDay,1),
        ('外表数据发送','xslx01',otherJgDay,2)
    ]
    for nj in xkTxNj:
        xxlx=xxlx+[('学生选课提醒','10',nj,2)]
    xxlx=sorted(xxlx,key=lambda s:s[3],reverse=False)
    return xxlx
####################################setting the jw database sql code##################################
###############setint the message comments######################
messageComments='''【广州大学教务处】'''
#######################################################################################################
##取日期对应的周次，星期##
getXtZcXqjSqlCode='''select zc,xqj from jw_pk_rcmxb where rq='{}' '''
#取日期对应的周次，星期对应的教师课表####
getNextDayKbCode='''select distinct jgh,xm,skjc,xqmc,jxlmc,cdmc,jxbzc,kcmc from LIKAI_QXKB t where bitand(t.zcd,get_jctobinary('{}'))>0 and t.xqj='{}' and 1=1'''
##取日期对应的周次，星期对应的学生课表###
getNextDayXsKbCode='''select distinct jgh,xm,skjc,xqmc,jxlmc,cdmc,jxbzc,kcmc,
(select xh from jw_xjgl_xsjbxxb where xh_id=xkb.xh_id) xsxh,
(select xm from jw_xjgl_xsjbxxb where xh_id=xkb.xh_id) xsxm 
from LIKAI_QXKB t,
jw_xk_xsxkb xkb
where bitand(t.zcd,get_jctobinary('{}'))>0 and t.xqj='{}' and 1=1
and xkb.xnm=(select zdz from zftal_xtgl_xtszb where zs='当前学年')
and xkb.xqm=(select zdz from zftal_xtgl_xtszb where zs='当前学期')
and xkb.jxb_id=t.jxb_id'''
##取当天办理的学籍异动信息###
######发向教师 03
getXjYdxxCode='''select (select xh from jw_xjgl_xsjbxxb where xh_id=ydb.xh_id) xh,(select xm from jw_xjgl_xsjbxxb where xh_id=ydb.xh_id) xm,
(select xjydmc from jw_xjgl_xjydlbdmb where ydlbm=ydb.ydlbm) ydmc,(case when to_number(ydb.shzt)=3 then '已通过' else '不通过' end) jg,
  t.jgh,t.XM
from jw_xjgl_xjydb ydb,(select jzg.jgh,jzg.xm,jzg.JG_ID
from ZFTAL_XTGL_YHJSB yh,JW_JG_JZGXXB jzg
where yh.JSDM in (
  select jsdm
  from ZFTAL_XTGL_JSXXB jsb
  where jsb.jsmc = '学院')
and yh.YHM=jzg.JGH) t where ZZSHSJ like '%{}%' and to_number(shzt)>=3 and 1=1 and ydb.YDHJG_ID=t.JG_ID'''
######学籍异动发向学生 031
getXjYdxxCode031='''select (select xh from jw_xjgl_xsjbxxb where xh_id=ydb.xh_id) xh,(select xm from jw_xjgl_xsjbxxb where xh_id=ydb.xh_id) xm,
(select xjydmc from jw_xjgl_xjydlbdmb where ydlbm=ydb.ydlbm) ydmc,(case when to_number(ydb.shzt)=3 then '已通过' else '不通过' end) jg
from jw_xjgl_xjydb ydb where ZZSHSJ like '%{}%' and to_number(shzt)>=3 and 1=1 '''
###################################################################
###取场地借用信息
getCdJyCode='''
select distinct
  (select jgh
   from (select jgh,xm,jgh_id from JW_JG_JZGXXB
         union select xh jgh,xm,xh_id jgh_id from JW_XJGL_XSJBXXB where XJZTDM in (select XJZTDM from JW_XJGL_XJZTDMB where SFYXJ='1')) t
   where t.JGH_ID = nvl(yub.syr_id,yub.syrxh_id))                        jgh,
  (select xm
   from (select jgh,xm||'老师，' xm,jgh_id from JW_JG_JZGXXB
         union select xh jgh,xm||'同学，' xm,xh_id jgh_id from JW_XJGL_XSJBXXB where XJZTDM in (select XJZTDM from JW_XJGL_XJZTDMB where SFYXJ='1')) t
   where t.JGH_ID = nvl(yub.syr_id,yub.syrxh_id))                        xm,
  (select WM_CONCAT(cdb.CDMC)
   from JW_PK_JXCDYUYMXB mxb, JW_JCDM_CDXQXXB cdb
   where mxb.XNM = cdb.XNM and mxb.xqm = cdb.XQM and mxb.CD_ID = cdb.CD_ID
         and mxb.YYXX_ID = yub.YYXX_ID) cdmc
  ,LIKAI_JW_PUBLICINTERFACE.RETURN_CDYYXQ(yub.YYXX_ID,'zc') zc,
  LIKAI_JW_PUBLICINTERFACE.RETURN_CDYYXQ(yub.YYXX_ID,'xq') xq,
  LIKAI_JW_PUBLICINTERFACE.RETURN_CDYYXQ(yub.YYXX_ID,'jc') jc,
  decode(yub.SHZT, '3', '已通过', '4','被退回','不通过') || case when yub.SHZT ='5'
    then '(原因：' || (select SUGGESTION
                    from SP_WORK_NODE t
                    where t.W_ID = yub.YYXX_ID) || ')'
                                         else '' end shjg,yub.YYXX_ID
from JW_PK_JXCDYUYB yub
where yub.SHZT in('3','5') and yub.SHSJ like '%{}%' and 1 = 1
'''
#####################################################################
###取学生考试信息
getXsKsCode='''select xh,xm,kcmc,cdb.cdmc,ccb.KSRQ||'('||ccb.KSKSSJ||'-'||ccb.KSJSSJ||')' kssj from
  jw_kw_xsksxxb ksb,jw_xjgl_xsjbxxb xsj,JW_JXRW_JXBXXB jxb,JW_JH_KCDMB kc,JW_JCDM_CDXQXXB cdb,jw_kw_kssjb sjb,jw_kw_ksccb ccb
  where ksb.xh_id=xsj.xh_id and jxb.jxb_id=ksb.jxb_id and jxb.xnm=ksb.xnm and jxb.xqm=ksb.xqm and jxb.kch_id=kc.kch_id and ksb.xnm=cdb.xnm
  and ksb.xqm=cdb.xqm and ksb.xnm=sjb.xnm and ksb.xqm=sjb.xqm and ksb.cd_id=cdb.cd_id and ksb.sjbh_id=sjb.sjbh_id and sjb.ksccb_id=ccb.ksccb_id
  and ccb.ksrq like '%{}%' and exists(select 'x' from JW_KW_KSCXKZB where ccb.KSMCDMB_ID=ksb.KSMCDMB_ID and XSCZWH='1')
and not exists(select 'x' from JW_XMGL_JXXMXSBMQKB qtb where qtb.JXXMLBDM='1005' and SHJG='3' and qtb.XNM=ksb.XNM and qtb.XQM=ksb.XQM
and qtb.XH_ID=ksb.XH_ID and qtb.JXB_ID=ksb.JXB_ID) and 1=1'''
###################################################################
###取教师监考信息
getJsJkCode='''select distinct jzg.jgh,jzg.XM,t.kssj,cdb.cdmc,kc.KCMC, ddb.KSDD_ID,cdb.cdmc,kc.KCMC,t.kssj from JW_KW_KSDDB ddb,JW_KW_KSDDBJDZB dzb,JW_JCDM_CDXQXXB cdb,JW_JXRW_JXBXXB jxb,
  JW_JH_KCDMB kc,JW_JG_JZGXXB jzg,JW_KW_KSDDJKB jkb,(select sjb.KSMCDMB_ID,sjb.SJBH_ID,sjb.XNM,sjb.XQM,ccb.KSRQ||'('||KSKSSJ||'-'||ccb.KSJSSJ||')' kssj from JW_KW_KSSJB sjb,JW_KW_KSCCB ccb
where sjb.XNM=ccb.XNM and sjb.XQM=ccb.XQM and sjb.KSCCB_ID=ccb.KSCCB_ID and sjb.KSMCDMB_ID=ccb.KSMCDMB_ID) t
where ddb.XNM=ddb.Xnm and ddb.XQM=dzb.XQM and ddb.KSHKBJ_ID=dzb.KSHKBJ_ID
and cdb.XNM=ddb.XNM and cdb.XQM=ddb.XQM and cdb.CD_ID=ddb.CD_ID
and jxb.XNM=ddb.XNM and jxb.XQM=ddb.XQM and jxb.JXB_ID=dzb.JXB_ID and jxb.KCH_ID=kc.KCH_ID
and t.XNM=dzb.XNM and t.XQM=dzb.XQM and t.SJBH_ID=dzb.SJBH_ID
  and ddb.XNM=jkb.XNM and ddb.XQM=jkb.XQM and ddb.KSDD_ID=jkb.KSDD_ID
  and jkb.JGH_ID=jzg.JGH_ID
  and t.kssj like '%{}%'
  and exists(select 'x' from JW_KW_KSCXKZB where t.KSMCDMB_ID=KSMCDMB_ID and JSCJK='1')'''
##########################################
########调停课发送教师###############
getJsTtkCode='''
select jzg.jgh,
       jzg.xm||'老师，您好!您办理的'||decode(ttk.TKLXDM,'02','"补课"','03','"停课"','"调课"'),
       kc.KCMC || '(教学班名称:' || jxb.JXBMC || ')'                         tkxx,
       decode(ttk.SHZT, '3', '已通过', '4', '被退回', '不通过') || case
                                                            when ttk.SHZT = '5'
                                                                    then '(原因：' || (select SUGGESTION
                                                                                    from SP_WORK_NODE t
                                                                                    where t.W_ID = ttk.TTKXX_ID) || ')'
                                                            else '' end shjg
from JW_PK_TTKSQB ttk,
     JW_JG_JZGXXB jzg,
     JW_JXRW_JXBXXB jxb,
     JW_JH_KCDMB kc
where nvl(ttk.YJGH_ID,ttk.XJGH_ID) = jzg.JGH_ID
  and ttk.xnm = jxb.xnm
  and ttk.XQM = jxb.XQM
  and ttk.JXB_ID = jxb.JXB_ID
  and kc.KCH_ID = jxb.KCH_ID
  and ttk.SHZT in ('3', '4', '5')
  and ttk.shsj like '%{}%'
  and ttk.XNM = (select zdz from zftal_xtgl_xtszb where zs = '当前学年')
  and ttk.Xqm = (select zdz from zftal_xtgl_xtszb where zs = '当前学期')
  and 1 = 1
order by ttk.yjgh_id, ttk.jxb_id, ttk.shsj
'''
###########调停课发送学生################
###########
getXsTtkCode='''select distinct (select xh from jw_xjgl_xsjbxxb where xh_id=xkb.XH_ID)xh,(select xm from JW_XJGL_XSJBXXB where xh_id=xkb.XH_ID) xm,
  (select '《'||kcmc||'》课程,' from JW_JH_KCDMB where xkb.KCH_ID=kch_id)||'发生'||(case when ttk.tklxdm='02' then '（部分周次）临时补课' when
ttk.TKLXDM='03' then '（部分周次）临时停课' when ttk.YZCD||ttk.YXQJ||ttk.yjc<>ttk.XZCD||ttk.XXQJ||ttk.XJC then '上课时间变动'
else '上课地点或上课教师变动' end) kcmc
from JW_XK_XSXKB xkb,JW_PK_TTKSQB ttk
where xkb.JXB_ID=ttk.JXB_ID
and ttk.SHZT='3' and ttk.SHSJ like '%{}%'
and xkb.XNM=(select zdz from zftal_xtgl_xtszb where zs='当前学年')
and xkb.xqm=(select zdz from zftal_xtgl_xtszb where zs='当前学期')'''
#########################缓考发送学生#############
getXsHkCode='''select (select xh from JW_XJGL_XSJBXXB where xh_id=qtb.XH_ID) xh,
(select xm from JW_XJGL_XSJBXXB where xh_id=qtb.XH_ID) xm,
  '对教学班：'||(select jxbmc from JW_JXRW_JXBXXB where jxb_id=qtb.JXB_ID)||'申请的“'||(select szb.JXXMLBMC from JW_XMGL_JXXMBMSZB szb where szb.JXXMLBDM=qtb.jxxmlbdm)||'”' xmmc,
 decode(qtb.SHJG,'3','已通过','不通过') shjg
from JW_XMGL_JXXMXSBMQKB qtb where qtb.XNM=(select zdz from ZFTAL_XTGL_XTSZB where zs='当前学年')
and qtb.xqm=(select zdz from ZFTAL_XTGL_XTSZB where zs='当前学期') and qtb.SHSJ like '%{}%' and qtb.SHJG>=3'''
#############################缓考审核发学院#####################
getXsHktoXyCode='''
select t.jgh,t.xm,t1.xmmc from
(select
  (select jg_id
   from JW_XJGL_XSJBXXB
   where xh_id = qtb.XH_ID)                                                                      jg_id,
  '请您按照学校缓考申请规定，尽快审核贵学院'||(select xm
   from JW_XJGL_XSJBXXB
   where xh_id = qtb.XH_ID)||'同学'||
  (select '(学号：'||xh||'）'
   from JW_XJGL_XSJBXXB
   where xh_id = qtb.XH_ID)||
  '对教学班：' || (select jxbmc
              from JW_JXRW_JXBXXB
              where jxb_id = qtb.JXB_ID) || '提出的“' || (select szb.JXXMLBMC
                                                       from JW_XMGL_JXXMBMSZB szb
                                                       where szb.JXXMLBDM = qtb.jxxmlbdm) || '”申请' xmmc
from JW_XMGL_JXXMXSBMQKB qtb
where qtb.XNM = (select zdz
                 from ZFTAL_XTGL_XTSZB
                 where zs = '当前学年')
      and qtb.xqm = (select zdz
                     from ZFTAL_XTGL_XTSZB
                     where zs = '当前学期') and to_number(qtb.SHJG) = 1) t1,(select jzg.jgh,jzg.xm,jzg.JG_ID
from ZFTAL_XTGL_YHJSB yh,JW_JG_JZGXXB jzg
where yh.JSDM in (
  select jsdm
  from ZFTAL_XTGL_JSXXB jsb
  where jsb.jsmc = '学院')
and yh.YHM=jzg.JGH) t
where t.JG_ID=t1.JG_ID
'''





###################学生成绩有变动(含新增),成绩表，与成绩补录表
getXscjCode='''select distinct
  t.xh,
  t.xm,
  WM_CONCAT('《'||t.kcmc || '》课程,成绩为:' || t.cj)
from (
       select
         xsj.xh   xh,
         xsj.xm   xm,
         cjb.kcmc kcmc,
         cjb.cj
       from JW_CJ_XSCJB cjb, JW_XJGL_XSJBXXB xsj
       where cjb.XH_ID = xsj.XH_ID
             and cjb.XNM = (select zdz
             from ZFTAL_XTGL_XTSZB
             where zs = '成绩录入学年')
             and cjb.XQM = (select zdz
             from ZFTAL_XTGL_XTSZB
             where zs = '成绩录入学期')
             and '1'='{}'
             and cjb.CZSJ like '%{}%'
             and cjb.CJZT ='3'
       union
       select
         xsj.xh  xh,
         xsj.xm  xm,
         kc.KCMC kcmc,
         blb.CJ
       from JW_CJ_CJBLB blb, JW_XJGL_XSJBXXB xsj, JW_JH_KCDMB kc
       where blb.XH_ID = xsj.XH_ID
             and blb.KCH_ID = kc.KCH_ID
             and blb.shsj like '%{}%'
             and blb.SHZT = '3'
     ) t
group by t.xh, t.xm
'''
############教师录入成绩提醒表######################
getJsLrCjTxCode='''
select jzg.jgh,jzg.XM,jxb.JXBMC,szb.LRJSSJ
from JW_CJ_CJLRMMB mmb,JW_JG_JZGXXB jzg,JW_CJ_XMBLSZB szb,JW_JXRW_JXBXXB jxb
where mmb.XNM=(select zdz from ZFTAL_XTGL_XTSZB where zs='成绩录入学年')
and mmb.XQM=(select zdz from ZFTAL_XTGL_XTSZB where zs='成绩录入学期')
and mmb.YJXB_ID is null
and mmb.JXB_ID=jxb.JXB_ID
and mmb.JGH_ID=jzg.JGH_ID
and mmb.JXB_ID=szb.JXB_ID
and jxb.KKZT<>'4'
and exists(select 1 from JW_XK_XSXKB where jxb.JXB_ID=JXB_ID)
and szb.LRZT in ('1','2')
and szb.lrjssj is not null
and szb.ZHYCCJXBJ='1'
'''

################系统异常检测#############################
###############考试冲突################



##############选课容量不足，座位数不足###############



##############必修课程冲突#############






#############具体年级必修课程选课提醒#########################
getNjBxKcTxCode='''
select xh, xm, WM_CONCAT(kcmc) bxkc
from (select xsj.xh, xsj.xm, xjb.NJDM_ID, t.KCH_ID, kc.KCMC, xsj.XH_ID
      from (select distinct hbb.BH_ID, jxb.KCH_ID
            from JW_JXRW_JXBHBXXB hbb,
                 JW_JXRW_JXBXXB jxb
            where jxb.JXB_ID = hbb.JXB_ID
              and jxb.XNM = (select zdz from ZFTAL_XTGL_XTSZB where zs = '选课学年')
              and jxb.xqm = (select zdz from ZFTAL_XTGL_XTSZB where zs = '选课学期')
              and hbb.KCXZDM in (select kcxzdm from JW_JH_KCXZDMB where xbx = 'bx')
            union
            select distinct dzb.bh_id, t0.kch_id
            from JW_JXRW_BKZYBJDZB dzb,
                 JW_JXRW_BKXXB xxb,
                 JW_JXRW_BKLXB lxb,
                 (select BKLX_ID, KCH_ID
                  from JW_JXRW_BKLXKZDZB t1,
                       JW_JH_KZKCDMB t2
                  where t1.KZ_ID = t2.KZ_ID) t0
            where dzb.BKXXB_ID = xxb.BKXXB_ID
              and xxb.BKLX_ID = lxb.BKLX_ID
              and t0.BKLX_ID = lxb.BKLX_ID
              and xxb.XNM = (select zdz from ZFTAL_XTGL_XTSZB where zs = '选课学年')
              and xxb.XQM = (select zdz from ZFTAL_XTGL_XTSZB where zs = '选课学期')) t,
           jw_xjgl_xsjbxxb xsj,
           jw_xjgl_xsxjxxb xjb,
           JW_JH_KCDMB kc
      where t.BH_ID = xjb.BH_ID
        and kc.KCH_ID = t.KCH_ID
        and xsj.XH_id = xjb.XH_ID
        and nvl(xjb.sfzx, '1') = '1'
        and lower(nvl(kc.bz,'1')) not like '%cxb%'
        and xjb.XJZTDM in (select xjztdm from JW_XJGL_XJZTDMB where SFYXJ = '1')
        and xjb.XNM = (select zdz from ZFTAL_XTGL_XTSZB where zs = '选课学年')
        and xjb.XQM = (select zdz from ZFTAL_XTGL_XTSZB where zs = '选课学期')) t
where 1 = 1
  and not exists(select 'x'
                 from jw_xk_xsxkb xkb
                 where xkb.xnm = (select zdz from ZFTAL_XTGL_XTSZB where zs = '选课学年')
                   and xkb.XQM = (select zdz from ZFTAL_XTGL_XTSZB where zs = '选课学期')
                   and xkb.XH_ID = t.XH_ID
                   and xkb.KCH_ID = t.KCH_ID)
  and not exists(select 1
                 from JW_CJ_XSCJb cjb
                 where cjb.KCH_ID = t.KCH_ID
                   and cjb.XH_ID = t.XH_ID)
  and t.NJDM_ID like '%{}%'
group by xh, xm
'''


##################取当前学年，网络视频课选课名单
getXsWlspk='''
select (select xh from JW_XJGL_XSJBXXB where xh_id=xkb.xh_id) xh,
  (select xm from JW_XJGL_XSJBXXB where xkb.XH_ID=XH_ID) xm,
  kc.kcmc,
  kc.bz
from jw_jh_kcdmb kc,JW_XK_XSXKB xkb
where (kc.bz like '%开课平台%' or kc.bz like '%上课网址%')
and xkb.XNM=(select zdz from ZFTAL_XTGL_XTSZB where zs='当前学年')
and xkb.XQM=(select zdz from ZFTAL_XTGL_XTSZB where zs='当前学期')
and xkb.KCH_ID=kc.KCH_ID
--and kc.kcmc  like '%军事%训练%'
--and xkb.xh_id like '19%'
'''


###################取当前学年学期预警的学生名单
#######思路先发送当天处理的，并将当天发送的数据存入备份表likai_yesterdat_xyyjclb
getXsXyYjCode='''
select
  xsj.XH,
  xsj.xm,
  '截至当前，您共获学分为：' || jgb.TJTJZ || ',不足' || xsj.njdm_id || '级' || (select zymc
                                                                 from ZFTAL_XTGL_ZYDMB
                                                                 where xsj.ZYH_ID = zyh_id) || '专业学分要求的3/4(' ||
  tjb.SXZ || '学分)，已被给予学业预警,您共被预警' || (select count(*)
                                      from JW_CJ_XYYJCLJGB
                                      where jgb.CLZT = '1' and xh_id = jgb.xh_id) || '次。' || case when (select count(*)
                                                                                                        from
                                                                                                          JW_CJ_XYYJCLJGB
                                                                                                        where
                                                                                                          jgb.CLZT = '1'
                                                                                                          and xh_id =
                                                                                                              jgb.xh_id)
                                                                                                       > 1
    then '请您尽快办理“延长在读年限（编入下一年级）”！'
                                                                                             else '希望您牟足劲,补齐所缺学分!' end yjnr
from JW_CJ_XYYJJGB jgb, JW_XJGL_XSJBXXB xsj, JW_CJ_XYYJTJB tjb, JW_CJ_XYYJCLJGB clb
where jgb.XH_ID = xsj.XH_ID
      and jgb.XH_ID = clb.XH_ID
      and jgb.XYYJTJ_ID = tjb.XYYJTJ_ID
      and clb.XNM = (select zdz
                     from ZFTAL_XTGL_XTSZB
                     where zs = '当前学年')
      and clb.xqm = (select zdz
                     from ZFTAL_XTGL_XTSZB
                     where zs = '当前学期')
      and clb.XYYJJG_ID = jgb.XYYJJG_ID
and not exists(select 'x' from likai_yesterdat_xyyjclb where xnm=clb.XNM and xqm=clb.XQM and xh_id=clb.XH_ID )
'''
############取教师停开教学任务信息
getJsTkKcxx='''
select
  (select jgh
   from jw_jg_jzgxxb
   where rkb.JGH_ID = jgh_id) jgh,
  (select xm
   from JW_JG_JZGXXB
   where rkb.JGH_ID = jgh_id) xm,
  '课程《'||(select KCMC
   from JW_JH_KCDMB
   where jxb.KCH_ID = kch_id) || '》（教学班名称：' || jxb.JXBMC || ',选课人数：'||(select count(*)
                                                            from JW_XK_XSXKSXB sxb
                                                            where sxb.JXB_ID = jxb.jxb_id) || '),已经被停开，详情与开课学院或教务科联系！' content
from JW_JXRW_JXBXXB jxb, JW_JXRW_JXBJSRKB rkb
where jxb.XNM = (select zdz
                 from ZFTAL_XTGL_XTSZB
                 where zs = '选课学年')
      and jxb.xqm = (select zdz
                     from ZFTAL_XTGL_XTSZB
                     where zs = '选课学期')
      and jxb.JXB_ID = rkb.JXB_ID
and jxb.KKZT='4'
'''
#################邀请教师完善研究方向、教师个人简介####
getNotJsjjOrYjfx='''
select
  jzg.jgh,
  jzg.xm||'老师，您好！您在'||likai_jw_publicinterface.return_xnorxqmc(jxb.xnm)||'学年第'
  ||likai_jw_publicinterface.return_xnorxqmc(jxb.xqm)||'学期，承担了 '||WM_CONCAT('《'||kc.KCMC||'》')||' 课程的教学任务。' ||
  '为充分提升学生选课时对课程、教师的了解、熟悉程度，加强学生个人兴趣、规划与选课之间的关系，现邀请您在教务系统中完善您的研究方向与个人简介。概要的操作方法为：登录教务系统后-》信息维护-》个人信息修改-》选择申请-》进入教师简介、研究方向等信息修改页面。' content
from (select distinct
  jxb.XNM,
  jxb.XQM,
  jxb.KCH_ID,
  rkb.JGH_ID
from JW_JXRW_JXBXXB jxb, JW_JXRW_JXBJSRKB rkb
where jxb.JXB_ID=rkb.JXB_ID and  jxb.XNM = (select zdz
                 from ZFTAL_XTGL_XTSZB
                 where zs = '选课学年') and jxb.XQM = (select zdz
                                                   from ZFTAL_XTGL_XTSZB
                                                   where zs = '选课学期')) jxb, JW_JG_JZGXXB jzg,JW_JH_KCDMB kc
where jxb.JGH_ID = jzg.JGH_ID and kc.KCH_ID=jxb.KCH_ID
      and (length(jzg.JSJJ) <= 15 or jzg.JSJJ is null)
group by jzg.JGH,jzg.xm,jxb.XNM,jxb.XQM
'''
################学生教学评价未完成#######
getXsPjWwc='''
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
GROUP BY T.XH,T.XM
'''

####向学院发送教师成绩修改申请审核
cjXgShtoDepaAdmin='''
select z.JGH,z.xm
               ||'老师,您好！请您根据学校成绩管理规定，及时登录教务系统对'||
             t.xgxx||'申请的成绩修改进行审核!祝您工作愉快！' from
(select t.KKBM_ID,WM_CONCAT(xgxx) xgxx from (
select distinct jxb.KKBM_ID,jzg.XM||'老师' xgxx
from
JW_CJ_XSCJXGSQB sqb,JW_JXRW_JXBXXB jxb,JW_JG_JZGXXB jzg
where jxb.JXB_ID=sqb.JXB_ID
and sqb.SQRJGH_ID=jzg.JGH_ID
and sqb.SHZT='1'
    ) t
group by t.KKBM_Id) t,
(select jzg.jgh,jzg.xm,jzg.JG_ID
from ZFTAL_XTGL_YHJSB yh,JW_JG_JZGXXB jzg
where yh.JSDM in (
  select jsdm
  from ZFTAL_XTGL_JSXXB jsb
  where jsb.jsmc = '学院')
and yh.YHM=jzg.JGH) z
where t.KKBM_ID=z.JG_ID
'''
#############取节假日替代日期
getJjrTdrq='''
select yrq from JW_PK_JJRFASZB fzb
where fzb.XNM=(select zdz from ZFTAL_XTGL_XTSZB where zs='当前学年')
and fzb.xqm=(select zdz from ZFTAL_XTGL_XTSZB where zs='当前学期')
and fzb.TDRQ='{}' and 1=1
'''


#####发送完成记录日志
writeTologs='''
        insert into LIKAI_MESSAGE_LOG(id,RECEIVER,content,MESSAGE,SENDTIME)
        values (:1,:2,:3,:4,:5)'''


#####学籍异动待审核发向学院
getXjydDshFxXy='''
select jgh,glyxm||'老师，您好！您有'||WM_CONCAT(xm||'('||ydmc||')')||'待审核,若您不负责此项工作，请忽略！' from
(select (select xh from jw_xjgl_xsjbxxb where xh_id=ydb.xh_id) xh,(select xm from jw_xjgl_xsjbxxb where xh_id=ydb.xh_id) xm,
(select xjydmc from jw_xjgl_xjydlbdmb where ydlbm=ydb.ydlbm) ydmc,(case when to_number(SHzt)=1 then '待审核' else '' end) jg,
  t.jgh,t.XM glyxm
from jw_xjgl_xjydb ydb,(select jzg.jgh,jzg.xm,jzg.JG_ID
from ZFTAL_XTGL_YHJSB yh,JW_JG_JZGXXB jzg
where yh.JSDM in (
  select jsdm
  from ZFTAL_XTGL_JSXXB jsb
  where jsb.jsmc = '学院')
and yh.YHM=jzg.JGH) t where  to_number(shzt)=1 and 1=1 and nvl(ydb.YDHJG_ID,YDQJG_ID)=t.JG_ID)
    group by jgh,glyxm
'''