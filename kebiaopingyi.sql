create table nocv_rwlsb as (
select fn_jqzd(fn_jxbsjcdxx(t.jxb_id, '0'), '|', 1) as sj, fn_jqzd(fn_jxbsjcdxx(t.jxb_id, '0'), '|', 2) as dd, t.jxb_id
from jw_jxrw_jxbxxb t
where t.XNM='2019' and t.XQM='12');


declare
  v_sign varchar2(255);
begin
  --课表地点表
  update jw_pk_kbcdb cdb set cdb.ZCD = 2 * zcd
  where cdb.KB_ID in (select kb_id
                      from JW_PK_KBSJB sjb
                      where sjb.XNM = '2019'
                        and sjb.XQM = '12');
  --课表时间表
  update JW_PK_KBSJB sjb set sjb.ZCD = 2 * ZCD
  where sjb.XNM = '2019'
    and sjb.XQM = '12';
  commit ;
  --调停课申请表
  update JW_PK_TTKSQB sqb
  set sqb.YZCD = 2 * sqb.YZCD
  where sqb.JXB_ID in (select jxb_id
                       from JW_JXRW_JXBXXB jxb
                       where jxb.XNM = '2019'
                         and jxb.XQM = '12')
    and sqb.YZCD is not null;
  commit ;
  update JW_PK_TTKSQB sqb
  set sqb.XZCD = 2 * sqb.XZCD
  where sqb.JXB_ID in (select jxb_id
                       from JW_JXRW_JXBXXB jxb
                       where jxb.XNM = '2019'
                         and jxb.XQM = '12')
    and sqb.xZCD is not null;
  --场地预约,场地预约无须平移
--   update JW_PK_JXCDYUYSJB yubsjb
--   set yubsjb.ZCD = 2 * yubsjb.ZCD
--   where yubsjb.YYXX_ID in (select yub.YYXX_ID
--                            from JW_PK_JXCDYUYB yub
--                            where yub.XNM = '2019'
--                              and yub.XQM = '12');
  --更新场地预约对应的日期
  update JW_PK_JXCDYUYSJB yubsjb
  set yubsjb.rq=(select rq from jw_pk_rcmxb xl where xl.ZC=FN_BITTOZC(2*yubsjb.zcd) and xl.XQJ=yubsjb.XQJ
                 and xl.rq>'2020-03-01'
                )
    where yubsjb.YYXX_ID in (select yub.YYXX_ID
                           from JW_PK_JXCDYUYB yub
                           where yub.XNM = '2019'
                             and yub.XQM = '12');
--更新场地中的开始日期与结束日期
  update jw_pk_jxcdyuyb yub
set yub.KSRQ=(select min(rq) from JW_PK_JXCDYUYSJB yusjb where yusjb.YYXX_ID=yub.YYXX_ID),
    yub.JSRQ=(select max(rq) from JW_PK_JXCDYUYSJB yusjb where yusjb.YYXX_ID=yub.YYXX_ID)
where yub.XNM='2019' and yub.XQM='12';



  ---教学任务部分
  update JW_JXRW_JXBXXB jxb set jxb.QSJSZ=2*jxb.QSJSZ,
  jxb.sksj=(select sj from nocv_rwlsb t where t.jxb_id=jxb.jxb_id),
--   jxb.jxdd=(select dd from nocv_rwlsb t where t.jxb_id=jxb.jxb_id),
  jxb.qsz=to_number(nvl(jxb.qsz,'0'))+1,
  jxb.zzz=to_number(nvl(jxb.zzz,'0'))+1
  where jxb.XNM='2019' and jxb.XQM='12';
  --教师任课表
  update JW_JXRW_JXBJSRKB rkb set rkb.QSJSZ=2*rkb.QSJSZ where rkb.JXB_ID in (
      select jxb_id from JW_JXRW_JXBXXB jxb where jxb.XNM='2019' and jxb.xqm='12'
      );
  commit;
end;

-- select * from JW_JXRW_JXBHBXXB hbb
-- select * from JW_KW_KSCCB where XNM='2019' and xqm='12'

-- -- select * from jw_pk_rcmxb rc where rc.rq like '2020-03-02'
-- select xqj,FN_BITTOZC(2*jc), FN_BITTOZC(2*zcd) from JW_PK_KBSJB jxb where jxb.JXB_ID='979509A20D4F0A89E053206411AC58BB';
--
-- select * from JW_JXRW_JXBXXB jxb where jxb.jxbmc='(2019-2020-2)-180720003-3';
--
--
-- select max(rq),min(rq) from JW_PK_JXCDYUYSJB yusjb where yusjb.YYXX_ID='9AF9CD4573247F7BE053206411ACC677';
-- select * from jw_pk_jxcdyuyb where LSH='31549';
-- select * from JW_PK_JXCDYUYMXB mxb where mxb.YYXX_ID='9AF9CD4573247F7BE053206411ACC677';
--
-- select * from jw_pk_jxcdyuyb yub where yub.XNM='2019' and yub.XQM='12';
--
-- update jw_pk_jxcdyuyb yub
-- set yub.KSRQ=(select min(rq) from JW_PK_JXCDYUYSJB yusjb where yusjb.YYXX_ID=yub.YYXX_ID),
--     yub.JSRQ=(select max(rq) from JW_PK_JXCDYUYSJB yusjb where yusjb.YYXX_ID=yub.YYXX_ID)
-- where yub.XNM='2019' and yub.XQM='12'
--
-- select qsjsz,fn_bittozc(2*qsjsz) from JW_JXRW_JXBJSRKB rkb where rkb.JXB_ID='979509A20D4F0A89E053206411AC58BB'