from apps.syjxxt import controls as syjxxt
from databaseconfig.connectdbs import connect

####实验教学系统导入项目序号的后缀码,default='DG'+年份后两位
syxmHzm='default'
def syjxt():
    '''实验系统'''
    mscon=connect('mssql')
    syjxxt.syjxxtInterface(mscon,syxmHzm)