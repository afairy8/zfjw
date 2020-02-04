####
savePath='D:\\projects\\zfjw\\common\\expfiles\\mails'

getbysxx='''
select fzb.BYJR,fzb.BYZSH,nvl(fzb.YWXW,'0') ywxw,fzb.XWLX,fzb.XWZSH from JW_BYGL_BYSFZXXB fzb,JW_XJGL_XSJBXXB xsj
where fzb.XH_ID=xsj.XH_id
and fzb.XWLX is not null and fzb.YWXW='1'
and lower(xsj.ZJHM)=lower('{}') and 1=1
'''