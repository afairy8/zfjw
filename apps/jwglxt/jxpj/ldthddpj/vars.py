

rollLdThPj='''
update JW_PJ_JXBPFB pfb set pfb.tjzt='0'
where pfb.XNM=(select zdz from ZFTAL_XTGL_XTSZB t where t.zs='评价学年')
and pfb.XQM=(select zdz from ZFTAL_XTGL_XTSZB t where t.zs='评价学期')
and pfb.CPDXDM in ('02','05')
and pfb.BFZPF not in ('优','良','中','差')
and pfb.TJZT='1'
and pfb.BFZPF is not null
and to_number(pfb.BFZPF)>0 and to_number(pfb.BFZPF)<to_number('{}')
{}
'''
rollLdThPjCondition1='''
and pfb.jgh_id in (select jgh_id from jw_jg_jzgxxb where jgh='{}')
and pfb.jxb_id in (select jxb_id from jw_jxrw_jxbxxb where jxbmc='{}')
and pfb.pjsj like '{}%'
and pfb.bpjgh_id in (select jgh_id from jw_jg_jzgxxb where jgh='{}')
'''
rollLdThPjCondition2=''' and 1=1
'''

# print(rollLdThPj.format(str('40'),rollLdThPjCondition1).format('103667'))