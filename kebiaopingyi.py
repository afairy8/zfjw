from databaseconfig.connectdbs import connect

#############备份code
nocvBakTableNames=[
    'jw_pk_kbsjb',
    'jw_pk_kbcdb',
    'jw_pk_ttksqb',
    'JW_PK_JXCDYUYB',
    'JW_PK_JXCDYUYSJB',
    'JW_PK_JXCDYUYMXB',
    'jw_jxrw_jxbxxb',
    'jw_jxrw_jxbjsrkb',
    'jw_jxrw_jxbhbxxb'
]

nocvBakCode='''
create table {} as (select * from {})
'''

def bak(con):
    for tablename in nocvBakTableNames:
        createname='nocv_'+tablename
        print(nocvBakCode.format(createname,tablename).strip().lower()+';')
        print('--'+'*'*30)
        if not con.objectExists(createname)[0][0]:
            con.execute(nocvBakCode.format(createname,tablename))
            print('{}创建成功'.format(createname))
        else:
            pass

####################################################################


######################平移code

nocvPyCodelist=[
    '''
    create table nocv_rwlsb as (
select fn_jqzd(fn_jxbsjcdxx(t.jxb_id, '0'), '|', 1) as sj, fn_jqzd(fn_jxbsjcdxx(t.jxb_id, '0'), '|', 2) as dd, t.jxb_id
from jw_jxrw_jxbxxb t
where t.XNM='2019' and t.XQM='12')
    ''',
    '''update jw_pk_kbcdb cdb set cdb.ZCD = 2 * zcd
  where cdb.KB_ID in (select kb_id
                      from JW_PK_KBSJB sjb
                      where sjb.XNM = '2019'
                        and sjb.XQM = '12')''',
    '''  update JW_PK_KBSJB sjb set sjb.ZCD = 2 * ZCD
  where sjb.XNM = '2019'
    and sjb.XQM = '12' ''',
    '''
      update JW_PK_TTKSQB sqb
  set sqb.YZCD = 2 * sqb.YZCD
  where sqb.JXB_ID in (select jxb_id
                       from JW_JXRW_JXBXXB jxb
                       where jxb.XNM = '2019'
                         and jxb.XQM = '12')
    and sqb.YZCD is not null
    ''',
    '''
      update JW_PK_TTKSQB sqb
  set sqb.XZCD = 2 * sqb.XZCD
  where sqb.JXB_ID in (select jxb_id
                       from JW_JXRW_JXBXXB jxb
                       where jxb.XNM = '2019'
                         and jxb.XQM = '12')
    and sqb.xZCD is not null
    ''',
    '''
      update JW_PK_JXCDYUYSJB yubsjb
  set yubsjb.rq=(select rq from jw_pk_rcmxb xl where xl.ZC=FN_BITTOZC(2*yubsjb.zcd) and xl.XQJ=yubsjb.XQJ
                 and xl.rq>'2020-03-01'
                )
    where yubsjb.YYXX_ID in (select yub.YYXX_ID
                           from JW_PK_JXCDYUYB yub
                           where yub.XNM = '2019'
                             and yub.XQM = '12')
    ''',
    '''
    update jw_pk_jxcdyuyb yub
set yub.KSRQ=(select min(rq) from JW_PK_JXCDYUYSJB yusjb where yusjb.YYXX_ID=yub.YYXX_ID),
    yub.JSRQ=(select max(rq) from JW_PK_JXCDYUYSJB yusjb where yusjb.YYXX_ID=yub.YYXX_ID)
where yub.XNM='2019' and yub.XQM='12'
    ''',
    '''
  update JW_JXRW_JXBXXB jxb set jxb.QSJSZ=2*jxb.QSJSZ,
  jxb.sksj=(select sj from nocv_rwlsb t where t.jxb_id=jxb.jxb_id),
--   jxb.jxdd=(select dd from nocv_rwlsb t where t.jxb_id=jxb.jxb_id),
  jxb.qsz=to_number(nvl(jxb.qsz,'0'))+1,
  jxb.zzz=to_number(nvl(jxb.zzz,'0'))+1
  where jxb.XNM='2019' and jxb.XQM='12'
    ''',
    '''
      update JW_JXRW_JXBJSRKB rkb set rkb.QSJSZ=2*rkb.QSJSZ where rkb.JXB_ID in (
      select jxb_id from JW_JXRW_JXBXXB jxb where jxb.XNM='2019' and jxb.xqm='12'
      )
    '''
]

def py(con):
    for code in nocvPyCodelist:
        print(code.strip().lower()+';')
        print('--'+'*'*30)

def clearTables(con):
    '''清理一些过期的表'''
    code='''select table_name  from all_tables
where lower(table_name) like '%2018%'
or lower(table_name) like '%yyh' or lower(table_name ) in ('likai_t','likai_ttt')
or lower(table_name) like 'nocv%' and 1=1'''
    res=con.execute(code)
    for data in res:
        cle='''drop table {} '''.format(data[0])
        con.execute(cle)
