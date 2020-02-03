----------创建用户

create user gzdx_jw_user identified by Likai2010 account unlock default tablespace ZF temporary tablespace TEMP;
grant "CONNECT" to gzdx_jw_user;
grant "DBA" to gzdx_jw_user;

