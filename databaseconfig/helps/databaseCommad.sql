----------创建用户

create user gzdx_jw_user identified by Likai2010 account unlock default tablespace ZF temporary tablespace TEMP;
grant "CONNECT" to gzdx_jw_user;
grant "DBA" to gzdx_jw_user;

create user gzdx_cj_user identified by Likai2010 account unlock default tablespace ZFcj temporary tablespace TEMP;
grant "CONNECT" to gzdx_cj_user;
grant "DBA" to gzdx_cj_user;

---创建表空间
create tablespace ZF datafile 'D:\app\80662\oradata\orcl\zf.dbf' size 25000M AUTOEXTEND on next 3000M;
-- create temporary tablespace temp tempfile 'D:\app\80662\oradata\orcl\temp.dbf' size 2000M AUTOEXTEND on next 100M;
create tablespace ZFCJ datafile 'D:\app\80662\oradata\orcl\zfcj.dbf' size 5000M AUTOEXTEND on next 500M;



