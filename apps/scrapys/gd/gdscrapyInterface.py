from apps.scrapys.gd import oa
from apps.scrapys.gd import xw
from common.actionPre import actionpre

def scrInterface(actions="oa;xw;"):
    '''广大爬虫对外接口'''
    L=[]
    for action in actionpre.actionList(actions):
        if action=='oa':
            L.append(oa.main())
        elif action=='xw':
            L.append(xw.main())
        else:
            pass
    return L

