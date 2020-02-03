#是否启用大纲调试模式，默认为否
debug=False
#同步完成后是否直接更新课程库
update=False
###分批次交的最大课程数
pcMax=10
#教学大纲nr1，nr2,等基本内容
getJxdgNr='''
select *
from (select
        kc.kcbh,
        dg.*,
        row_number()
        over (
          partition by dg.dgid
          order by dg.pkid )
          rn
      from zftal_sjtb_JXDG_DGNr dg, zftal_sjtb_JXDG_KCFPB kc
      where kc.pkid = dg.dgid and to_number(substr(kc.kcbh,1,2))>=18) t
where t.rn = 1 
'''

##获取毕业要求的明细
getByyqMxData='''
select kcjxmb,byyq,row_number()
    over(partition by dgid order by pkid) rn from zftal_sjtb_JXDG_JXMB_BYYQ 
    where dgid in (select pkid from zftal_sjtb_JXDG_KCFPB where kcbh='{}')
'''

##获取考核要求明细
getKckhyq='''
select * from (select decode(khlx,'0','期末考试','1','平时考试','其它') khlx
    ,khqz||'%' qz,khfs||','||khyq,row_number()over (partition by dgid order by khlx desc) rn from zftal_sjtb_JXDG_KCKH
    where dgid in ( select pkid from zftal_sjtb_JXDG_KCFPB where kcbh='{}'))
'''
##插入教学大纲临时表
insertLkJxdb='''
insert into likai_jxdg(kch,kczwjj,kczwjxdg)
values(:1,:2,:clobdata)
'''
###更新kcdmb中的课程简介和课程中文教学大纲
updateKcdmb='''
update jw_jh_kcdmb kc set kc.zwkcjj=(select kczwjj from likai_jxdg t where kc.kch=t.kch),
kc.zwjxdg=(select kczwjxdg from likai_jxdg t where kc.kch=t.kch)
where exists(select 'x' from likai_jxdg t where t.kch=kc.kch)
'''