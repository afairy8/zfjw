from apps.wlzx.messageCenter.messageMainControl import controls as msg
from apps.wlzx.dataCenter import controls as dataCenter
from apps.wlzx import wlzxvars
from common.actionPre import actionpre


def wlzxDataCenter(con,actionName=None,max_index=25):
    L=[]
    if not actionName:
        actionName=wlzxvars.dataCenterAction
    actionName=actionpre.actionList(actionName)
    for switch in actionName:
        L.append(dataCenter.dataCenterInterface(con=con,actionName=switch,max_index=max_index))
    return L

def wlzxMsg(con,xxlx=None,fileName='sf.xlsx'):
    return msg.messageInterface(con=con,xxlx=xxlx,fileName=fileName)
