import os
from apps.jwglxt.xkgl import vars
from common.actionPre import actionpre
from common.fileAction.controls import fileInfo
import math
from datetime import datetime

def moocSavePath(pathsuffix):
    '''慕课导出名单保存路径'''
    path=os.path.join(vars.moocBasePath,pathsuffix)
    if not os.path.exists(path):
        os.makedirs(path)
    os.system('attrib -R {} /S /D'.format(path))
    return path

def getMoocKcxx(con):
    return con.execute(vars.getMoocKcxx)##(kch_id,bz,kcmc)

def getMoocJxbxx(con,kch_id):
    '''
    :param con:
    :param kch_id:the mooc kch_id
    :return:
    '''
    return con.execute(vars.getMoocKcJxb.format(kch_id))

def getMoocXkxx(con,kch_id='####',jxb_id='####'):
    '''
    :param con:
    :param kch_id: if kch_id is ### refer export xkmd by jxb_id
    :param jxb_id: if jxb_id is ### refer export xkmd by kch_id
    :return:
    '''

    #print(vars.getMoocXkxx.format(kch_id,jxb_id))
    return con.execute(vars.getMoocXkxx.format(kch_id,jxb_id))

def getTitle(sign):
    title,type,addr=None,None,None
    if sign.lower().strip().find('zhihuishu')>=0:# in ['www.zhihuishu.com']:##智慧树
        title=('*学号','*姓名','*教学班','学校','院系','专业','手机','邮箱','备注')
        type='kc'
        addr='智慧树'
    elif sign.lower().strip().find('mooc.gzhu')>=0:# in ['mooc.gzhu.edu.cn']:##广大慕课
        title = ('学号（必填）','姓名（必填）','所属机构（必填）','所在小组(一级小组)','所在小组(二级小组)','证件号码','性别','电话','院系','专业','年级','入学时间','毕业时间','学历')
        type='jxb'
        addr='广大慕课'
    elif sign.lower().strip().find('xuetangx')>=0:# in ['gzhu.xuetangx.com']:##学堂在线
        title=('* 学号','* 姓名','院系','专业','行政班','入学年份','教学班名称')
        type='kc'
        addr='学堂在线'
    elif sign.lower().strip().find('chaoxing')>=0:#in ['gzhdx.fanya.chaoxing.com']:#超星
        title = ('学号/工号', '姓名*', '角色(教师或者学生)', '性别',
                 '手机号', '邮箱', '院系', '专业', '行政班级', '入学年份', '身份证号', '学校代码', '密码')
        type='jxb'
        addr='超星'
    elif sign.lower().strip().find('uooconline')>=0:# ['www.uooconline.com']:#优课联盟
        title = ('学校', '学号', '姓名', '班级')
        type='jxb'
        addr='优课'
    elif sign.lower().strip().find('中国近现代史')>=0:
        title = ('学校', '学号', '姓名', '班级')
        type='kc'
        addr='优课'
    elif sign.lower().strip().find('毛泽东思想和中国特色社会主义理论体系概论') or sign.lower().strip().find('思想道德修养与法律基础')or sign.lower().strip().find('马克思主义基本原理'):
        title=('*学号','*姓名','*教学班','学校','院系','专业','手机','邮箱','备注')
        type='kc'
        addr='智慧树'
    elif sign.lower().strip().find('gdhkmooc')>=0:
        title=('学生姓名','学生账号','手机号码')
        type='jxb'
        addr='粤港澳大湾区'
    else:
        pass
    return [title,type,addr]
def expMooc(con):
    '''按相应平台的导入格式导出慕课的选课名单'''
    kcxx=getMoocKcxx(con)
    pathDate=datetime.now().strftime('%Y-%m-%d')
    for kc in kcxx:
        ###title:模板标题，exptype:按教学班还是按课程；suffix文件保存的尾路径
        #print(kc[2]+'####'+kc[1].split('//')[1].split('/')[0])
        title,exptype,suffix=getTitle(kc[1].split('//')[1].split('/')[0])
        #print(suffix)
        if exptype=='kc':
            content = []
            content.append(title)
            xkxx=getMoocXkxx(con,kc[0])
            for xk in xkxx:
                if suffix=='智慧树':
                    t = (xk[1], xk[2], xk[3], '', xk[5], xk[6], '', '', xk[7] + '#任课教师：' + xk[4].split('/')[0])
                    content.append(t)
                elif suffix=='优课':##实际上就是中国近现代史纲要
                    if xk[4].split('/')[0] in vars.zgjxdsgyRkjs:
                        t=(xk[0],xk[1],xk[2],xk[3]+xk[4].split('/')[1])
                        content.append(t)
                elif suffix=='学堂在线':
                    #title = ('* 学号', '* 姓名', '院系', '专业', '行政班', '入学年份', '教学班名称')
                    t=(xk[1],xk[2],xk[5],xk[6],xk[7],'',xk[3])
                    content.append(t)
                else:
                    pass
            if len(content)>1:
                #print(content)
                filename = os.path.join(moocSavePath(pathDate + '\\' + suffix), kc[2])
                xlsx=fileInfo(filename)
                xlsx.expXlsx(content=content)
                con.execute(vars.writeToBack.format(kc[0],'####'))
        elif exptype=='jxb':
            jxbxx=getMoocJxbxx(con,kc[0])
            for jxb in jxbxx:
                content=[]
                content.append(title)
                xkxx=getMoocXkxx(con,jxb_id=jxb[0])
                # filename=os.path.join(moocSavePath(pathDate+'\\'+suffix),kc[2].replace(' ','')+'%'+jxb[2].split('/')[1]+'%'+jxb[1])
                for xk in xkxx:
                    if suffix=='广大慕课':
                        t = (xk[1], xk[2], xk[0])
                        content.append(t)
                    elif suffix=='超星':
                        t = (xk[1], xk[2], '学生', xk[8], '', '', xk[5], xk[6], xk[7])
                        content.append(t)
                    elif suffix=='优课':
                        t=(xk[0],xk[1],xk[2],xk[3]+xk[4].split('/')[1])
                        content.append(t)
                    elif suffix=='粤港澳大湾区':
                        t=(xk[2],xk[1],'')
                        content.append(t)
                    else:
                        pass
                if len(content) > 1:
                    #print(content)
                    filename = os.path.join(moocSavePath(pathDate + '\\' + suffix),
                                            kc[2].replace(' ', '') + '%' + jxb[2].split('/')[1] + '%' + jxb[1])
                    xlsx = fileInfo(filename)
                    xlsx.expXlsx(content=content)
                    con.execute(vars.writeToBack.format('####',jxb[0]))
        else:
            pass
    return 1


def delCxBmAndXk(con):
    '''删除重修选课时又报名又选课情形'''
    con.execute(vars.delCxbmAndYxk)
    return 1

def upCxbj(con):
    '''更新重修标记'''
    con.execute(vars.updateCxbj)
    return 1

def upPkgl(con):
    '''配课管理分析语句'''
    for code in vars.pkgllist:
        con.execute(code)
        print('{}{}执行完成'.format('*'*30,code))
    return 1

def inZjxb(con):
    '''插入缺子教学班的学生名单'''
    con.execute(vars.insertFjxbOrZjxb)
    return 1

def expAllXkmd(con,maxPc):
    '''快速导出选课名单的详细信息'''
    content=[]
    content.append(['学年','学期','学号','姓名','学生学院','专业','班级','年级','课程名称','课程性质','任课教师信息','教学班名称（选课课号）'])
    xlsx=fileInfo('选课详细信息')
    xlsx.expXlsx(content=content)
    counts=con.execute(vars.preQuickExpXkmd)[0]
    if counts:
        counts=counts[0]
    indexs=math.ceil(counts/float(maxPc))
    for index in range(indexs):
        content=[]
        left=int(index*maxPc)
        right=int((index+1)*maxPc)
        content.extend(con.execute(vars.quickExpXkmd.format(left,right)))
        xlsx.expXlsx(content=content,mode='')
    return 1


def xkglInterface(con,actionName='',maxPc=30000):
    '''选课管理对外接口'''
    if actionName==actionpre.unique('delcxbmandxk'):
        if delCxBmAndXk(con):
            return '删除重修选课时既报名又选课的学生名单完成！'
    elif actionName==actionpre.unique('upcxbj'):
        if upCxbj(con):
            return '重修标记更新完成！'
    elif actionName==actionpre.unique('upPkgl'):
        if upPkgl(con):
            return (';'.join(vars.pkgllist)+'执行完成！')
    elif actionName==actionpre.unique('inZjxb'):
        if inZjxb(con):
            return '缺子教学班的学生名单补充完成！'
    elif actionName==actionpre.unique('expAllXkmd'):
        if expAllXkmd(con,maxPc=maxPc):
            return '选课学年的选课名单已导出！'
    elif actionName==actionpre.unique('expMooc'):
        if expMooc(con):
            return '慕课名单已执行完成，请检查{}文件夹下是否有新文件'.format(vars.moocBasePath)
    else:
        pass