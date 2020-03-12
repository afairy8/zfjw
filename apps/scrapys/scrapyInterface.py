from apps.scrapys.common import oa
from common.actionPre import actionpre
from apps.scrapys.common import xw
def scrInterface(actions="oa;xw;"):
    '''爬虫对外接口'''
    L=[]
    for action in actionpre.actionList(actions):
        if action=='oa':
            print('--oa')
            L.append(oa.main())
        elif action=='xw':
            print('--xw')
            L.extend(xw.main())
        else:
            pass
    return L

