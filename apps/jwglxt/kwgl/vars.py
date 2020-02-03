upJkjg='''
update JW_KW_KSDDB ddb
set ddb.JG_ID=LIKAI_JW_PUBLICINTERFACE.RETURN_CDJKXYANKSRS(ddb.CD_ID,ddb.XNM,ddb.XQM,ddb.KSHKBJ_ID)
where ddb.CD_ID is null
and ddb.XNM=(select zdz from ZFTAL_XTGL_XTSZB where zs='排考试学年')
and ddb.xqm=(select zdz from ZFTAL_XTGL_XTSZB where zs='排考试学期')
'''

upSfhk='''
update JW_KW_BKMDB bkb set bkb.SFHK='1'
where bkb.SFHK='0'
and exists(select 1 from jw_xmgl_jxxmxsbmqkb hkb
        where hkb.JXB_ID=bkb.YJXB_ID and hkb.XH_ID=bkb.XH_ID
          and hkb.SHJG='3'
          and hkb.JXXMLBDM='1005')
'''