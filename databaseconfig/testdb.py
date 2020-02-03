from databaseconfig import connectdbs

con=connectdbs.connect()

selectTest='''
select * from JW_XJGL_XSJBXXB xsj,ZFTAL_XTGL_JGDMB jg,ZFTAL_XTGL_ZYDMB zy,ZFTAL_XTGL_BJDMB bj
where xsj.JG_ID=jg.JG_ID
and xsj.ZYH_ID=zy.ZYH_ID
and xsj.BH_ID=bj.BH_ID
and xsj.XH like '2001%%0'
'''
if con.execute(selectTest):
    print(1)
print(con.execute(selectTest))
# from datetime import datetime
# print(datetime.now().strftime('%Y-%m-%d'))
#
# t='''select zc,xqj from jw_pk_rcmxb where rq='{}' and 1=1'''.format(datetime.strftime('%Y-%m-%d'))
# print(t)