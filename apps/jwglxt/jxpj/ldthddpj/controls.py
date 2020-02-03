from apps.jwglxt.jxpj.ldthddpj import vars
from common.actionPre import actionpre

def roolLdThpj(con, minpf, LdThlist,jxbmc,pjsj,bpjgh):
    '''退回领导、同行评价'''
    if LdThlist:
        if jxbmc and pjsj and bpjgh:
            formatCode = vars.rollLdThPj.format(str(minpf),vars.rollLdThPjCondition1)
            for LdTh in LdThlist:
                con.execute(formatCode.format(LdTh,jxbmc,pjsj,bpjgh))
    else:
        formatCode = vars.rollLdThPj.format(str(minpf),vars.rollLdThPjCondition2)
        con.execute(formatCode)
    return 1


def LdThPjInterface(con, minpf=None, LdThlist=None,actionName=None,jxbmc=None,pjsj=None,bpjgh=None):
    '''领导同行评价对外接口'''
    if actionName==actionpre.unique('roolLdThpj'):
        res = ''
        if roolLdThpj(con, minpf, LdThlist,jxbmc,pjsj,bpjgh):
            if LdThlist:
                res = '{}退回成功！'.format(','.join(LdThlist))
            else:
                res = '可能存在异常的领导同行评价退回成功！'
        return res
    else:
        pass


