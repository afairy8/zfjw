# 是否创添加通选归属节点
sfcjtxkcgsnode = True  # ,默认为是
debug = False  # 是否开启调试模式
##是否开启更新课程调试模式
initPyfaCode = '''
likai_jw_publicinterface.delPyfaSjtb
'''
##检查专业号
checkZyh = '''
select * from zftal_SJTB_PYFAXXB t where t.ZYdm not in (select zyh from ZFTAL_XTGL_ZYDMB t where t.SFTY='0')
'''
# 检查课程性质
checkKcxz = '''
select distinct t2.kcxzdm from likai_sjtb_pyfakcxxb t,likai_sjtb_kcxzdmb t2 where t.kcxzdm=t2.kcxzdm and t2.kcxzmc not in (select kcxzmc from jw_jh_kcxzdmb)
'''
# 获取培养方案信息
getPyfaxxb = '''
select t.nj||t.ZYdm pyfaxx_id,t.nj,t2.zyh_id,t.nj||t2.zymc pyfamc,'zy' dlbs,t.yqzdxf,t.PYMBZW,
t.byyq,t.ZYHXKC,t.zydm,to_char(sysdate,'yyyy-mm-dd HH24:mm:ss')||'培养方案同步' sm,'0' sqzt
from zftal_SJTB_PYFAXXB t,ZFTAL_XTGL_ZYDMB t2
where t.zydm=t2.ZYH
order by t.zydm
'''
# 插入培养方案信息表
insertPyfaxx = '''
insert into JW_JH_PYFAXXB(pyfaxx_id,bbh,zyh_id,pyfamc,dlbs,zdxf,pymb,pyyq,HXKC,sm,sqzt) 
values(:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11)
'''
# 插入培养方案适用年级表
insertPyfaxxNj = '''
insert into JW_JH_PYFASYNJB(pyfaxx_id,njdm_id) values(:1,:2)
'''
# 插入培养方案学分要求信息表
insertPyfaxfyq = '''
insert into JW_JH_PYFAXFYQXXB(PYFAXX_ID,XFYQJD_ID,xfyqjdmc,JDKCSX,ZYFX_ID,
  yqzdxf,FXFYQJD_ID,px,SFMJD,KCXZDM,XDLX,xfyqzjdgx) values(:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12)
'''
# 插入培养方案学分要求归属表
insertPyfaKcgs = '''
insert into jw_jh_pyfaxfyqxxfb(PYFAXFYQXXF_ID,xfyqjd_id,kcgsdm) values(:1,:2,:3)
'''
# 获取培养方案节点信息
getPyfaxfyqJd = '''
select distinct nj,zydm,
(select t.kcxzdm FROM jw_jh_kcxzdmb t,zftal_sjtb_kcxzdmb t2 where t.kcxzmc=t2.kcxzmc and t2.kcxzdm=kc.kcxzdm ) kcxzdm,
(select t.kcxzmc FROM jw_jh_kcxzdmb t,zftal_sjtb_kcxzdmb t2 where t.kcxzmc=t2.kcxzmc and t2.kcxzdm=kc.kcxzdm ) kcxzmc,
(select t.xbx FROM jw_jh_kcxzdmb t,zftal_sjtb_kcxzdmb t2 where t.kcxzmc=t2.kcxzmc and t2.kcxzdm=kc.kcxzdm ) xbx,
  zyfxdm,case when zydm in ('1020','1026') and ZYFXMC is null then '跨模块' else  ZYFXMC end zyfxmc from zftal_SJTB_PYFAKCXXB KC WHERE ZYdm='{}' and nj='{}'
   order by nj,zydm,kcxzdm,zyfxdm,zyfxmc
'''
# 获取培养方案节点要求学分信息
getPyfaxfyqJdXf = '''
select * from (
select
  nj||zydm||xbx||'kcxz'||kcxzdm||modulekey id,to_number(yqzdxf)yqzdxf,to_number(mkxf) mkxf
from
(
  select t.nj,t.ZYdm,t2.KCXZDM,
   nvl(YQZDXF,'0') yqzdxf,
   case when MODULEKEY is not null then 'fxmk' else null end modulekey,
    nvl(mkxf,0) mkxf,t3.kcxzdm kcxzdm1,'zx'||t2.xbx xbx,
   row_number() over(partition by NJ,ZYdm,t.KCXZDM order by MODULEKEY,0) rn
  from zftal_SJTB_PYFAKCXZXFXXB t,jw_jh_kcxzdmb t2,zftal_SJTB_KCXZDMB t3
where   t.kcxzdm=t3.kcxzdm and t3.kcxzmc=t2.kcxzmc
) t where t.rn=1 and KCXZDM1 not in (10000,11111)) t
where t.id='{}'
'''
###美化培养方案，如不存在跨模块时，多个模块应该直接向上一级

beautifyPyfa = '''
update JW_JH_PYFAXFYQXXB xfb set xfb.FXFYQJD_ID=replace(xfb.FXFYQJD_ID,'fxmk','')
where xfb.PYFAXX_ID='{}'||'{}'
and xfb.FXFYQJD_ID like '%fxmk'
and not exists( select 'x' from JW_JH_PYFAXFYQXXB t where
  t.PYFAXX_ID=xfb.PYFAXX_ID and t.XFYQJD_ID=xfb.FXFYQJD_ID)
'''
##插入全新课程
###插入全新课程学时对照
insertNewKcXs = '''
insert into jw_jh_kcxsdzb(kcxsdzb_id,kch_id,xsdm,zhxs,zxs,sjbj,zxsbj)
SELECT SYS_GUID(),xs.kcdm KCH_ID,DECODE(replace(XS.XSMC,' ',''),'理论','01','实验','02','04') xsdm,
CASE WHEN ZKC.SFSJK='1' THEN '1' ELSE  likai_jw_publicinterface.jwKcXsfxZhxs(XS.XSFX) END ZHXS,
to_char(round(to_number(XS.XSFX),0)) ZXS,
CASE WHEN ZKC.SFSJK='1' THEN '1' ELSE NULL END SJBJ,
CASE WHEN ZKC.SFSJK='1' THEN '1' WHEN replace(XS.XSMC,' ','')='理论' then '1' else '0' end zxsbj
FROM ZFTAL_SJTB_KCXSDMB XS,ZFTAL_SJTB_KCDMB ZKC
WHERE NOT EXISTS(SELECT 'X' FROM JW_JH_KCDMB KC WHERE KC.KCH=XS.KCDM OR KC.KCH_ID=XS.KCDM)
AND XS.KCDM=ZKC.KCDM
'''
###插入全新课程
insertNewKc = '''
insert into jw_jh_kcdmb(kch_id,kch,kcmc,KCYWMC,xf,kkbm_id,kcxzdm,kclbdm,sfsjk,sfyxsjzct,zxs,cjlrjb,tkbj,bz)
select distinct kcdm kch_id,kcdm,kcmc,kcywmc,xf,
  (select jg_id from zftal_xtgl_jgdmb where jgdm=t.kkbmdm) kkbm_id, t3.kcxzdm,
t3.bz kclbdm,SFSJK,case when SFSJK<=0 then null else SFSJKYXCT end sfsjkyxct,zxs,'4','0'
  ,to_char(sysdate,'yyyy-mm-dd HH24:mm:ss')||'培养方案插入'
from ZFTAL_SJTB_KCDMB t,ZFTAL_SJTB_KCXZDMB t2,jw_jh_kcxzdmb t3
where t.kcxzdm=t2.kcxzdm and t2.kcxzmc=t3.kcxzmc and
  not exists(select 'x' from jw_jh_kcdmb kc where kc.kch=t.kcdm or kc.kch_id=t.kcdm)
'''
####打印全新课程
printNewKc = '''
select distinct kcdm kch_id,kcdm,kcmc,kcywmc,xf,
  (select jg_id from zftal_xtgl_jgdmb where jgdm=t.kkbmdm) kkbm_id, t3.kcxzdm,
t3.bz kclbdm,SFSJK,case when SFSJK<=0 then null else SFSJKYXCT end sfsjkyxct,zxs,'4','0'
  ,to_char(sysdate,'yyyy-mm-dd HH24:mm:ss')||'培养方案插入'
from ZFTAL_SJTB_KCDMB t,ZFTAL_SJTB_KCXZDMB t2,jw_jh_kcxzdmb t3
where t.kcxzdm=t2.kcxzdm and t2.kcxzmc=t3.kcxzmc and
  not exists(select 'x' from jw_jh_kcdmb kc where kc.kch=t.kcdm or kc.kch_id=t.kcdm)
'''
####获取已存在未落实的课程信息
getExistsButNotUsed = '''
select ZKC.KCDM,KC.KCH,
  ZKC.KCMC,KC.KCMC KCMC1,
  ZKC.KCYWMC,KC.KCYWMC KCYWMC1,
  (SELECT JG_ID FROM ZFTAL_XTGL_JGDMB WHERE JGDM=ZKC.kkbmdm) KKBM_ID,KC.KKBM_ID KKBM_ID1,
  to_number(nvl(ZKC.XF,0)) zxf,to_number(nvl(KC.XF,0)) kxf,
  to_number(nvl(ZKC.ZXS,0)) zzxs,to_number(nvl(KC.ZXS,0)) kzxs
  ,kc.kch_id
from ZFTAL_SJTB_KCDMB ZKC,JW_JH_KCDMB KC
WHERE ZKC.KCDM=KC.KCH
and not exists(select 1 from JW_JXRW_JXBXXB jxb where jxb.KCH_ID=kc.KCH_ID)
'''
####根据有不同的则更新教务课程库
updateExistsButNotUsed = '''
update jw_jh_kcdmb kc
set kc.kcmc=(:1),kc.kcywmc=(:2),kc.kkbm_id=(:3),kc.xf=(:4),
kc.zxs=(:5),kc.bz=kc.bz||to_char(sysdate,'yyyy-mm-d:HH24:mm:ss')||'培养方案更新' where kc.kch=(:6)
'''
####根据有不同的则更新培养方案课程信息
updateExistsButNotUsedPyfa = '''
update JW_JH_PYFAKCXXB pyfakc
set pyfakc.xf=(:1),pyfakc.KKBM_ID=(:2),pyfakc.bz=pyfakc.bz||to_char(sysdate,'yyyy-mm-d:HH24:mm:ss')||'培养方案更新'
where pyfakc.KCH_ID=(:3)
'''

updateExistsButNotUsedJxjh = '''
update JW_JH_jxzxjhkcxxb pyfakc
set pyfakc.xf=(:1),pyfakc.KKBM_ID=(:2),pyfakc.bz=pyfakc.bz||to_char(sysdate,'yyyy-mm-d:HH24:mm:ss')||'培养方案更新'
where pyfakc.KCH_ID=(:3)
'''

# 插入培养方案课程信息跨模块或无方向模块
insertPyfakcxxkmk = '''
insert into jw_jh_pyfakcxxb (pyfakcxx_id, xfyqjd_id, kch_id, jyxdnjdm, jyxdxqm, kcxzdm, kclbdm, xf, kkbm_id, khfsdm, zxbj,
                             fxbj, ezybj, exwbj, zyhxkcbj, zyfx_id, shzt, zykfkcbj, qsjsz, bz)
SELECT pyfakc.nj||pyfakc.zydm||pyfakc.kcdm pyfakcxx_id,
  pyfakc.NJ||pyfakc.ZYDM||'zx'||jkc.XBX||'kcxz'||jkc.KCXZDM||'kmk' xfyqjd_id,
  kc.kch_id kch_id,
  pyfakc.JYXDXN,DECODE(pyfakc.JYXDXQ,'1','3','2','12') JYXDXQ,
  jkc.KCXZDM,jkc.bz kclbdm,kc.xf,kc.KKBM_ID,
  decode(pyfakc.KHFS,'考试','1','2') khfsdm,'1'zxbj,'0'fxbj,'0' ezybj,'0' exwbj,
'0' zyhxkcbj,'wfx' zyfx_id,'0' shzt,'0' zykfkcbj,'65535' qsjsz,
  to_char(sysdate,'yyyy-mm-dd HH24:mm:ss')||'培养方案插入' bz
FROM ZFTAL_SJTB_PYFAKCXXB pyfakc,ZFTAL_SJTB_KCXZDMB ZKC,jw_jh_kcxzdmb jkc,jw_jh_kcdmb kc
where zkc.KCXZDM=pyfakc.KCXZDM and zkc.kcxzmc=jkc.KCXZMC
and pyfakc.NJ||pyfakc.ZYDM||'zx'||jkc.XBX||'kcxz'||jkc.KCXZDM=(:1)
and pyfakc.kcdm=kc.kch and pyfakc.zyfxmc=(:2)
and pyfakc.zyfxmc is not null
'''
# 插入培养方案课程信息方向模块
insertPyfakcxxfxmk = '''
insert into jw_jh_pyfakcxxb (pyfakcxx_id, xfyqjd_id, kch_id, jyxdnjdm, jyxdxqm, kcxzdm, kclbdm, xf, kkbm_id, khfsdm, zxbj,
                             fxbj, ezybj, exwbj, zyhxkcbj, zyfx_id, shzt, zykfkcbj, qsjsz, bz)
SELECT pyfakc.nj||pyfakc.zydm||pyfakc.kcdm pyfakcxx_id,
  pyfakc.NJ||pyfakc.ZYDM||'zx'||jkc.XBX||'kcxz'||jkc.KCXZDM||'fxmk'||pyfakc.ZYFXDM xfyqjd_id,
  kc.kch_id kch_id,
  pyfakc.JYXDXN,DECODE(pyfakc.JYXDXQ,'1','3','2','12') JYXDXQ,
  jkc.KCXZDM,jkc.bz kclbdm,kc.xf,kc.KKBM_ID,
  decode(pyfakc.KHFS,'考试','1','2') khfsdm,'1'zxbj,'0'fxbj,'0' ezybj,'0' exwbj,
'0' zyhxkcbj,'wfx' zyfx_id,'0' shzt,'0' zykfkcbj,'65535' qsjsz,
  to_char(sysdate,'yyyy-mm-dd HH24:mm:ss')||'培养方案插入' bz
FROM ZFTAL_SJTB_PYFAKCXXB pyfakc,ZFTAL_SJTB_KCXZDMB ZKC,jw_jh_kcxzdmb jkc,jw_jh_kcdmb kc
where zkc.KCXZDM=pyfakc.KCXZDM and zkc.kcxzmc=jkc.KCXZMC
and pyfakc.NJ||pyfakc.ZYDM||'zx'||jkc.XBX||'kcxz'||jkc.KCXZDM=(:1)
and pyfakc.kcdm=kc.kch and pyfakc.zyfxmc=(:2)
and pyfakc.zyfxmc is not null
'''
# 插入培养方案课程信息无模块
insertPyfakcxxWmk = '''
insert into jw_jh_pyfakcxxb (pyfakcxx_id, xfyqjd_id, kch_id, jyxdnjdm, jyxdxqm, kcxzdm, kclbdm, xf, kkbm_id, khfsdm, zxbj,
                             fxbj, ezybj, exwbj, zyhxkcbj, zyfx_id, shzt, zykfkcbj, qsjsz, bz)
SELECT pyfakc.nj||pyfakc.zydm||pyfakc.kcdm pyfakcxx_id,
  pyfakc.NJ||pyfakc.ZYDM||'zx'||jkc.XBX||'kcxz'||jkc.KCXZDM xfyqjd_id,
  kc.kch_id kch_id,
  pyfakc.JYXDXN,DECODE(pyfakc.JYXDXQ,'1','3','2','12') JYXDXQ,
  jkc.KCXZDM,jkc.bz kclbdm,kc.xf,kc.KKBM_ID,
  decode(pyfakc.KHFS,'考试','1','2') khfsdm,'1'zxbj,'0'fxbj,'0' ezybj,'0' exwbj,
'0' zyhxkcbj,'wfx' zyfx_id,'0' shzt,'0' zykfkcbj,'65535' qsjsz,
  to_char(sysdate,'yyyy-mm-dd HH24:mm:ss')||'培养方案插入' bz
FROM ZFTAL_SJTB_PYFAKCXXB pyfakc,ZFTAL_SJTB_KCXZDMB ZKC,jw_jh_kcxzdmb jkc,jw_jh_kcdmb kc
where zkc.KCXZDM=pyfakc.KCXZDM and zkc.kcxzmc=jkc.KCXZMC
and pyfakc.NJ||pyfakc.ZYDM||'zx'||jkc.XBX||'kcxz'||jkc.KCXZDM='{}'
and pyfakc.kcdm=kc.kch 
'''

insertPyfakcYxKkXnxq = '''
insert into JW_JH_PYFAKCYXXDXNXQB(pyfakcxx_id,YXKKNJM,YXKKXQM)
select pyfakc.nj||pyfakc.zydm||pyfakc.KCDM,pyfakc.JYXDXN,decode(pyfakc.JYXDXQ,'2','12','3')  
from ZFTAL_SJTB_PYFAKCXXB pyfakc 
where pyfakc.NJ='{}' and pyfakc.zydm='{}' and 1=1
'''
insertPyfaKcXsDzb = '''
insert into JW_JH_PYFAKCXSDZB(PYFAKCXX_ID,KCH_ID,XSDM,ZHXS,zxs,sjbj,zxsbj)
SELECT
xsdz.NJ||XSDZ.ZYDM||XSDZ.KCDM PYFAKCXX_ID,
  (SELECT KCH_ID FROM JW_JH_KCDMB WHERE KCH=XSDZ.KCDM) KCH_ID,
  DECODE(replace(XSDZ.XSMC,' ',''),'理论','01','实验','02','04') XSDM,
  CASE WHEN (SELECT SFSJK FROM JW_JH_KCDMB WHERE KCH=XSDZ.KCDM)='1' THEN '1' ELSE LIKAI_JW_PUBLICINTERFACE.jwKcXsfxZhxs(XSDZ.XS) END ZHXS,
  to_char(to_number(XSDZ.XS)) ZXS,
  CASE WHEN (SELECT SFSJK FROM JW_JH_KCDMB WHERE KCH=XSDZ.KCDM)='1' THEN '+' ELSE NULL END SJBJ,
  CASE WHEN (SELECT SFSJK FROM JW_JH_KCDMB WHERE KCH=XSDZ.KCDM)='1' and xsmc='实践' THEN '1'
  WHEN XSDZ.XSMC='理论' then '1'
  ELSE '0' END zxsbj
FROM ZFTAL_SJTB_PYFAKCXSDZB XSDZ
where xsdz.nj='{}' and xsdz.zydm='{}' and to_number(xsdz.xs)>0
'''

getZyfxCount = '''
select nvl(count(*),0) zyfxcount from
(select distinct
  nj,
  zydm,
  (select t.kcxzdm
   FROM jw_jh_kcxzdmb t, zftal_sjtb_kcxzdmb t2
   where t.kcxzmc = t2.kcxzmc and t2.kcxzdm = kc.kcxzdm) kcxzdm,
  (select t.kcxzmc
   FROM jw_jh_kcxzdmb t, zftal_sjtb_kcxzdmb t2
   where t.kcxzmc = t2.kcxzmc and t2.kcxzdm = kc.kcxzdm) kcxzmc,
  (select t.xbx
   FROM jw_jh_kcxzdmb t, zftal_sjtb_kcxzdmb t2
   where t.kcxzmc = t2.kcxzmc and t2.kcxzdm = kc.kcxzdm) xbx,
  zyfxdm,
  ZYFXMC
from zftal_SJTB_PYFAKCXXB KC
WHERE ZYdm = '{}' and nj = '{}')
where kcxzdm='{}' and zyfxmc is not null
'''
# 一个专业只分了一个模块，该模块为必修，在推送过来的数据中少了学分时
missBxKcxzXf = '''
select sum(to_number(xf)) xfh,sum(to_number(xf)) xfh2 from 
(SELECT pyfakc.nj||pyfakc.zydm||pyfakc.kcdm pyfakcxx_id,
  pyfakc.NJ||pyfakc.ZYDM||'zx'||jkc.XBX||'kcxz'||jkc.KCXZDM xfyqjd_id,
  kc.kch_id kch_id,
  pyfakc.JYXDXN,DECODE(pyfakc.JYXDXQ,'1','3','2','12') JYXDXQ,
  jkc.KCXZDM,jkc.bz kclbdm,kc.xf,kc.KKBM_ID,
  decode(pyfakc.KHFS,'考试','1','2') khfsdm,'1'zxbj,'0'fxbj,'0' ezybj,'0' exwbj,
'0' zyhxkcbj,'wfx' zyfx_id,'0' shzt,'0' zykfkcbj,'65535' qsjsz,
  to_char(sysdate,'yyyy-mm-dd HH24:mm:ss')||'培养方案插入' bz
FROM ZFTAL_SJTB_PYFAKCXXB pyfakc,ZFTAL_SJTB_KCXZDMB ZKC,jw_jh_kcxzdmb jkc,jw_jh_kcdmb kc
where zkc.KCXZDM=pyfakc.KCXZDM and zkc.kcxzmc=jkc.KCXZMC
and pyfakc.NJ||pyfakc.ZYDM||'zx'||jkc.XBX||'kcxz'||jkc.KCXZDM='{}'
and pyfakc.kcdm=kc.kch )
'''

getJsjylKc = '''
select 'pk' pk,'xfyqjd_id' xfyqjd_id,kc.KCH_ID,'2','3','15','5',kc.xf,kc.KKBM_ID,'2','1','0','0','0','0','wfx','0','0','65535',to_char(sysdate,'yyyy-mm-dd HH24:mm:ss')||'与培养方案同时插入',
kc.kch
from jw_jh_kcdmb kc
where kc.KCXZDM='24' and  kc.TKBJ='0'
'''

insertJsjyKc = '''
insert into jw_jh_pyfakcxxb (pyfakcxx_id, xfyqjd_id, kch_id, jyxdnjdm, jyxdxqm, kcxzdm, kclbdm, xf, kkbm_id, khfsdm, zxbj,
                             fxbj, ezybj, exwbj, zyhxkcbj, zyfx_id, shzt, zykfkcbj, qsjsz, bz)
values(:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13,:14,:15,:16,:17,:18,:19,:20)
'''
insertJsjyKcXs = '''
insert into JW_JH_PYFAKCXSDZB(PYFAKCXX_ID,KCH_ID,XSDM,ZHXS,zxs,sjbj,zxsbj)
values(:1,:2,:3,:4,:5,:6,:7)
'''
getJsjylkcXs = '''
select '' pk,dzb.KCH_ID,dzb.XSDM,dzb.ZHXS,dzb.zxs,dzb.SJBJ,dzb.ZXSBJ,kc.kch from JW_JH_KCXSDZB dzb,JW_JH_KCDMB kc
where kc.KCXZDM='24' and kc.KCH_id=dzb.KCH_ID and kc.TKBJ='0' and 1=1
'''
insertJsjyKcYxKk = '''
insert into JW_JH_PYFAKCYXXDXNXQB(PYFAKCXX_ID,YXKKNJM,YXKKXQM)
    values(:1,:2,:3)
'''
# 插入培养方案学分分布表
insertPyfaxffb = '''
insert into JW_JH_PYFAXFFB(pyfaxffb_id,pyfaxx_id,xfyqjd_id,xq,XF,sftj)
select sys_guid() pyfaxffb_id,
  t1.nj||t1.zydm pyfaxx_id,
  t1.nj||t1.zydm||'zx'||t3.XBX||'kcxz'||t3.KCXZDM xfyqjd_id,
  t1.kknj||'-'||decode(t1.xq,'1','3','2','12') xq,
  t1.yqzdxf,
  '1' sftj
from ZFTAL_SJTB_PYFAYXKKXNXQB t1,ZFTAL_SJTB_KCXZDMB t2,JW_JH_KCXZDMB t3
where t1.kcxzdm=t2.KCXZDM and t2.kcxzmc=t3.kcxzmc
and t1.zydm='{}' and t1.nj='{}'
and nvl(t1.yqzdxf,0)>0
'''

# 插入通选或教师教育类学分分布
insertTxorJxjyXffb = '''
insert into JW_JH_PYFAXFFB(pyfaxffb_id,pyfaxx_id,xfyqjd_id,xq,XF,sftj)
values (:1,:2,:3,:4,:5,:6)
'''
