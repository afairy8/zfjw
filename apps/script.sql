create table likai_message_log(
  id varchar2(255) default (sys_guid()) primary key ,
  receiver varchar2(255),
  content varchar2(3000),
  message varchar2(255),
  sendtime varchar2(255)
);

create table LIKAI_XTGL_XTSZB
(
  XTSZ_ID  VARCHAR2(32) not null,
  ZDM      VARCHAR2(200),
  ZDZ      VARCHAR2(400),
  SSMK     VARCHAR2(300),
  ZS       VARCHAR2(300),
  BZ       VARCHAR2(500),
  SSGNMKDM VARCHAR2(30),
  ZDZYQ    VARCHAR2(255),
  ZDLX     NUMBER       not null,
  ZDLY     VARCHAR2(1000),
  XTSZBLYB VARCHAR2(30)
);
INSERT INTO GZDX_JW_USER.LIKAI_XTGL_XTSZB (XTSZ_ID, ZDM, ZDZ, SSMK, ZS, BZ, SSGNMKDM, ZDZYQ, ZDLX, ZDLY, XTSZBLYB) VALUES ('BYSFZXXBSFSCJZ(@1)', 'BYSFZXXBSFSCJZ(@1)', '2020;0', 'BYMK', '毕业生辅助信息表是否首次加载', '毕业年度，毕业生辅助信息表是否首次加载，1，是首次；0不是首次；', null, '{required:true}', 3, 'fixed:0,1', null);

create table LIKAI_XK_XSXKB as (
select * from jw_xk_xsxkb where XH_ID='###');


