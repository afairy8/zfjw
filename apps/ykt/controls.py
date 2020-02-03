

from apps.ykt import vars
from common.fileAction.controls import fileInfo
from databaseconfig.connectdbs import connect
def getInfo(con):
    for key,value in vars.code.items():
        L=[]
        title=()
        if key=='机构信息':
            title=['学院名称']
        elif key=='班级信息':
            title=['学院（必填项）',	'专业（可省略）'	,'行政班级名称（必填项）',	'班级入学学年（必填项）']
        elif key=='用户信息':
            title=['学院名称（必填项）',	'行政班级（学生必填，其他角色可无）','姓名（必填项）	学号或工号（必填项）'	,'身份（必填项）','入学学年（同前，学生必填，其他角色可选填）']
        elif key=='开课信息':
            title=['学院名称','课程号','教学班选课课号','开课教师工号','开课教师姓名','课程名称','教学班名称','开课学年','开课学期']
        elif key=='选课信息':
            title=['教学班选课课号','学号']
        else:
            pass
        L.append(title)
        L.extend(con.execute(value))
        #print(L)
        xlsx=fileInfo(key)
        xlsx.expXlsx(content=L)

getInfo(connect())