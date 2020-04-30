
##获取指定特征的学生信息
getZdTzXs='''
select xsj.xh,xsj.xm,
(select jgmc from ZFTAL_XTGL_JGDMB where xsj.JG_ID=jg_id) jgmc,
(select zymc from zftal_xtgl_zydmb where xsj.ZYH_ID=zyh_id) zymc,
(select bj from ZFTAL_XTGL_BJDMB where xsj.BH_ID=bh_id) bj,
NJDM_ID,
xsj.SYD,
substr(xsj.ZJHM,1,6) prefixzjhm
from JW_XJGL_XSJBXXB xsj where xsj.NJDM_ID like '{}%'
and xsj.JG_ID<>'30'
order by xsj.JG_ID,xsj.ZYH_ID,xsj.BH_ID
'''
####导入照片相关
dropZpb='''drop table zpb'''
createZpb='''create table zpb(xh varchar2(255),zp blob)'''
insertZp='''insert into zpb(xh,zp) values (:1,:clobdata)'''
checkCode='''
select xh  from zpb where xh not in (select zjhm xh from jw_xjgl_xsjbxxb union select xh from jw_xjgl_xsjbxxb)
'''

rxhZjhmCode='''
update jw_xjgl_xszpb t set rhxzp=(select zp from zpb z,jw_xjgl_xsjbxxb xsj where lower(z.xh)=lower(xsj.zjhm) and xsj.xh_id=t.xh_id)
where t.xh_id in (select xh_id from  zpb z,jw_xjgl_xsjbxxb xsj where lower(z.xh)=lower(xsj.zjhm))
'''
byZjhmCode='''
update jw_xjgl_xszpb t set byzp=(select zp from zpb z,jw_xjgl_xsjbxxb xsj where lower(z.xh)=lower(xsj.zjhm) and xsj.xh_id=t.xh_id)
where t.xh_id in (select xh_id from  zpb z,jw_xjgl_xsjbxxb xsj where lower(z.xh)=lower(xsj.zjhm))
'''
rxhXhCode='''
update jw_xjgl_xszpb t set rhxzp=(select zp from zpb z,jw_xjgl_xsjbxxb xsj where lower(z.xh)=lower(xsj.xh) and xsj.xh_id=t.xh_id)
where t.xh_id in (select xh_id from  zpb z,jw_xjgl_xsjbxxb xsj where lower(z.xh)=lower(xsj.xh))
'''
byXhCode='''
update jw_xjgl_xszpb t set byzp=(select zp from zpb z,jw_xjgl_xsjbxxb xsj where lower(z.xh)=lower(xsj.xh) and xsj.xh_id=t.xh_id)
where t.xh_id in (select xh_id from  zpb z,jw_xjgl_xsjbxxb xsj where lower(z.xh)=lower(xsj.xh))
'''

zsjhWhXlsxPath=''
zsjhWhBjmcExists='''
select count(1) from ZFTAL_XTGL_BJDMB bj,ZFTAL_XTGL_ZYDMB zy 
where bj.ZYH_ID=zy.ZYH_ID
and bj.NJDM_ID='{}'
and zy.zymc='{}'
'''
zsjhWhBjAvg='''

'''
zsjhWhBjmc='''
select bh,bj from ZFTAL_XTGL_BJDMB bj,ZFTAL_XTGL_ZYDMB zy 
where bj.ZYH_ID=zy.ZYH_ID
and bj.NJDM_ID='{}'
and zy.zymc='{}'
and rownum=1
'''