
###获取专业教学执行计划信息
getJxzxjhZyxx='''select jhb.JXZXJHXX_ID from JW_JH_JXZXJHXXB jhb where jhb.NJDM_ID='{}'
'''
####获取专业教学执行计划集中性实践教学环节和专业选修课程信息
getXfyqjdXx='''
select xfb.XFYQJD_ID,xfb.XFYQJDMC,xfb.YQZDXF,px from JW_JH_JXZXJHXFYQXXB xfb 
where xfb.JXZXJHXX_ID='{}' and xfb.XFYQJDMC in ('集中性实践教学环节','专业选修课程') and xfb.SFMJD='1' ;
'''

####插入学分要求要求子模块A，课程性质名称B


###取集中性实践教学环节或专业选修课程节点的课程信息
getJxzxjhKcxx='''
select * from jw_jh_jxzxjhkcxxb jhkc where jhkc.XFYQJD_ID='{}'
'''
###插入节点
insertNodes='''
insert into JW_JH_JXZXJHXFYQXXB
(JXZXJHXX_ID,XFYQJD_ID,XFYQJDMC,JDKCSX,ZYFX_ID,YQZDXF,FXFYQJD_ID,px,SFMJD,KCXZDM,XDLX,JCBJ,SFZDJS,xfyqzjdgx)
values(:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13,:14)
'''

###更新课程
upJhkc='''
update JW_JH_JXZXJHKCXXB jhkc set jhkc.XFYQJD_ID='{}' where jhkc.XFYQJD_ID='{}'

'''
###更新父节点的sfmjd关系
upFjdxx='''
update jw_jh_jxzxjhxfyqxxb xfb set xfb.sfmjd='0',xfb.xfyqzjdgx='1' where xfb.xfyqjd_id='{}'
'''