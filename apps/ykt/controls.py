

from apps.ykt import vars
from common.fileAction.controls import fileInfo
from databaseconfig.connectdbs import connect
import math
import time
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
        elif key=='mooc':
            title=['工号','姓名']
        else:
            pass
        L.append(title)
        L.extend(con.execute(value))
        #print(L)
        xlsx=fileInfo(key)
        xlsx.expXlsx(content=L)
def getxkxx2(con):
    content=[]
    content.append(['学年','学期','学号','姓名','学生学院','专业','班级','年级','课程名称','课程性质','任课教师信息','教学班名称（选课课号）'])
    counts=con.execute(vars.xkxx2Counts)[0]
    if counts:
        counts=counts[0]
    iters=math.ceil(counts/vars.xkxx2maxPc)
    for index in range(iters):
        #print(vars.xkxx2.format(int(index * vars.xkxx2maxPc), int((index + 1) * vars.xkxx2maxPc)))
        content.extend(con.execute(vars.xkxx2.format(int(index*vars.xkxx2maxPc),int((index+1)*vars.xkxx2maxPc))))
    xlsx=fileInfo('选课详细信息')
    xlsx.expXlsx(content=content)

# start=time.perf_counter()
# con=connect()
# getInfo(con)
# con.close()
# end=time.perf_counter()
# print(end-start)