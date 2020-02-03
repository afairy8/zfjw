###是否导入课程
SFKQKCTB=False
###是否已经检查了课表中的地点
SFJCKCDD=False
##是否直接插入到实验项目，不使用外部导入的方式
SFZJINSYXM=True
###导入的实验项目是否需要导出为xlsx文件
SFDCSYXM=False
###课表xls文件存放位置
kbPath='''D:\LIP_DATA_BAK_AUTO'''
###备份文件的路径
sourcePath='''D:\LIP_DATA_BAK_AUTO'''
##数据库文件的存放位置
dbStorePath='''D:\sqlserver\syjxxtdb'''
##恢复语句的格式
restoreCode='''
restore database {} from disk='{}'
with replace,
move '{}' to '{}',
move '{}_log' to '{}'
'''
####以命令行形式执行
sqlcmd='''sqlcmd -i {}'''
####创建链路服务器
addlink='''
USE [master]
GO
EXEC sp_dropserver @server=N'JWXT' 'droplogins'
GO
EXEC master.dbo.sp_addlinkedserver @server = N'JWXT', @srvproduct=N'Oracle', @provider=N'OraOLEDB.Oracle', @datasrc=N'127.0.0.1:1521/orcl'

GO
EXEC master.dbo.sp_serveroption @server=N'JWXT', @optname=N'collation compatible', @optvalue=N'false'
GO
EXEC master.dbo.sp_serveroption @server=N'JWXT', @optname=N'data access', @optvalue=N'true'
GO
EXEC master.dbo.sp_serveroption @server=N'JWXT', @optname=N'dist', @optvalue=N'false'
GO
EXEC master.dbo.sp_serveroption @server=N'JWXT', @optname=N'pub', @optvalue=N'false'
GO
EXEC master.dbo.sp_serveroption @server=N'JWXT', @optname=N'rpc', @optvalue=N'false'
GO
EXEC master.dbo.sp_serveroption @server=N'JWXT', @optname=N'rpc out', @optvalue=N'false'
GO
EXEC master.dbo.sp_serveroption @server=N'JWXT', @optname=N'sub', @optvalue=N'false'
GO
EXEC master.dbo.sp_serveroption @server=N'JWXT', @optname=N'connect timeout', @optvalue=N'0'
GO
EXEC master.dbo.sp_serveroption @server=N'JWXT', @optname=N'collation name', @optvalue=null
GO
EXEC master.dbo.sp_serveroption @server=N'JWXT', @optname=N'lazy schema validation', @optvalue=N'false'
GO
EXEC master.dbo.sp_serveroption @server=N'JWXT', @optname=N'query timeout', @optvalue=N'0'
GO
EXEC master.dbo.sp_serveroption @server=N'JWXT', @optname=N'use remote collation', @optvalue=N'true'
GO
EXEC master.dbo.sp_serveroption @server=N'JWXT', @optname=N'remote proc transaction promotion', @optvalue=N'true'
GO
USE [master]
GO
EXEC master.dbo.sp_addlinkedsrvlogin @rmtsrvname = N'JWXT', @locallogin = NULL , @useself = N'False', @rmtuser = N'gzdx_jw_user', @rmtpassword = N'Likai2010'
GO
'''
###读取机构、专业、班级、学籍、教师信息信息
readJgZyBjXj='''
IF (OBJECT_ID('lip_baseinfo.DBO.ZFTAL_XTGL_JGDMB') IS NOT NULL)
  BEGIN
  DROP TABLE lip_baseinfo.DBO.ZFTAL_XTGL_JGDMB
  END
GO
IF (OBJECT_ID('lip_baseinfo.DBO.ZFTAL_XTGL_ZYDMB') IS NOT NULL)
  BEGIN
  DROP TABLE lip_baseinfo.DBO.ZFTAL_XTGL_ZYDMB
  END
GO
IF (OBJECT_ID('lip_baseinfo.DBO.ZFTAL_XTGL_BJDMB') IS NOT NULL)
  BEGIN
  DROP TABLE lip_baseinfo.DBO.ZFTAL_XTGL_BJDMB
  END
GO
IF (OBJECT_ID('lip_baseinfo.DBO.JW_XJGL_XSJBXXB') IS NOT NULL)
  BEGIN
  DROP TABLE lip_baseinfo.DBO.JW_XJGL_XSJBXXB
  END
GO
SELECT * INTO lip_baseinfo.DBO.ZFTAL_XTGL_JGDMB
FROM OPENQUERY(JWXT, 'SELECT * FROM ZFTAL_XTGL_JGDMB')
GO
SELECT * INTO lip_baseinfo.DBO.ZFTAL_XTGL_ZYDMB
FROM OPENQUERY(JWXT, 'SELECT * FROM ZFTAL_XTGL_ZYDMB WHERE SFTY=''0'' and 1=1')
GO
SELECT * INTO lip_baseinfo.DBO.ZFTAL_XTGL_BJDMB
FROM OPENQUERY(JWXT, 'SELECT * FROM ZFTAl_XTGL_BJDMB')
GO
SELECT * INTO lip_baseinfo.DBO.JW_XJGL_XSJBXXB
FROM OPENQUERY(JWXT,
               'SELECT * FROM JW_XJGL_XSJBXXB WHERE XJZTDM IN (SELECT XJZTDM FROM JW_XJGL_XJZTDMB WHERE SFYXJ=''1'')')
GO
use lip_baseinfo
GO
if (object_id('likai_xsbj') is not null)
    begin
      drop view likai_xsbj
    end
GO
create view likai_xsbj
as
SELECT t.xh,t.xm,t.XBM xb,t2.id attbjid
FROM lip_baseinfo.dbo.JW_XJGL_XSJBXXB t,
     lip_baseinfo.dbo.ZFTAL_XTGL_BJDMB t1,
     lip_baseinfo.dbo.Base_ClassInfo t2
where
      t.BH_ID=t1.BH_ID
and t1.BH=t2.BJBH;
GO
if object_id('likai_jsxx') is not null
    begin
      drop view likai_jsxx
    end
GO
create view likai_jsxx as
SELECT t.jgh,t.xm,t.xb,t.jsxy,t2.id
FROM OPENQUERY(JWXT, 'select distinct JGH,xm,decode(xbmc,''男'',''1'',''2'') xb,JSXY
from LIKAI_QXKB t
where t.XNM=(select zdz from ZFTAL_XTGL_XTSZB where zs=''任务落实学年'')
and t.XQM=(select zdz from ZFTAL_XTGL_XTSZB where zs=''任务落实学期'')') t,lip_baseinfo.dbo.base_department t2
where t.jsxy=t2.departmentname;
GO
'''

##################专业，班级，学籍插入，学籍、教师信息更新
insertbj='''
insert into lip_baseinfo.dbo.Base_SpecialtyInfo(SpecialtyNO,SpecialtyName,AttDepID,QYBS)
SELECT t.zyh specialtyno,t.zymc specialtyname,t1.id attdepid,'1' qybs
FROM lip_baseinfo.dbo.ZFTAL_XTGL_ZYDMB t,lip_baseinfo.dbo.Base_Department t1,lip_baseinfo.dbo.ZFTAL_XTGL_JGDMB t2
where t.zyh not in
      (select specialtyno from lip_baseinfo.dbo.Base_SpecialtyInfo)
and   t1.DepartmentName=t2.jgmc
and t.JG_ID=t2.JG_ID;
---
insert into lip_baseinfo.dbo.Base_ClassInfo(BJBH, BJMC, NJ, AttSpeID, RS, State)
select * from (
select t.bh bjbh,t.bj bjmc,t.NJDM_ID nj,t1.id
    ,(select count(*) from lip_baseinfo.dbo.jw_xjgl_xsjbxxb where bh_id=t.bh_id) rs,'1' state
from lip_baseinfo.dbo.ZFTAL_XTGL_BJDMB t,lip_baseinfo.dbo.Base_SpecialtyInfo t1,lip_baseinfo.dbo.ZFTAL_XTGL_ZYDMB t2
where t.BH not in
      (select bjbh from lip_baseinfo.dbo.Base_ClassInfo)
and t.zyh_id=t2.zyh_id and t.JG_ID<>'30'
and t2.zyh=t1.SpecialtyNO) t where t.rs>5;
---
insert into lip_baseinfo.dbo.Base_StudentInfo(xh,xm,xb,AttBJID)
SELECT * FROM likai_xsbj t
where t.xh not in (select xh from lip_baseinfo.dbo.Base_StudentInfo);
-----
update lip_baseinfo.dbo.Base_StudentInfo set attbjid=a.attbjid from likai_xsbj a
where a.xh=lip_baseinfo.dbo.Base_StudentInfo.xh and a.attbjid<>lip_baseinfo.dbo.Base_StudentInfo.attbjid;
---
insert into lip_baseinfo.dbo.Base_TeacherInfo(Code,name,SexID,DepartmentID)
select t.jgh,t.xm,t.xb,t.id from likai_jsxx t where t.jgh not in (select code from lip_baseinfo.dbo.Base_TeacherInfo);
-----
update lip_baseinfo.dbo.Base_TeacherInfo set DepartmentID=t.id,name=t.xm from lip_baseinfo.dbo.likai_jsxx t
where t.jgh=lip_baseinfo.dbo.Base_TeacherInfo.code
and (t.id<>lip_baseinfo.dbo.Base_TeacherInfo.DepartmentID or t.xm<>lip_baseinfo.dbo.base_teacherinfo.name)
GO
'''

