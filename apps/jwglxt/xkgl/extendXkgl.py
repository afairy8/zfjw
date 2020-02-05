
from apps.jwglxt.xkgl import vars
import os
from databaseconfig.connectdbs import connect
from datetime import datetime
from common.fileAction.controls import fileInfo


###规定慕课上课网址的备注为开课平台中文冒号：平台名称半角逗号，
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
    # print(vars.getMoocXkxx.format(kch_id,jxb_id))
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
        pass
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
    else:
        pass
    return [title,type,addr]
def expMooc(con):
    kcxx=getMoocKcxx(con)
    pathDate=datetime.now().strftime('%Y-%m-%d')
    for kc in kcxx:
        print(kc)
        print('*'*30)
        title,exptype,suffix=getTitle(kc[1].split('//')[1].split('/')[0])
        if exptype=='kc':
            content = []
            content.append(title)
            xkxx=getMoocXkxx(con,kc[0])
            filename=os.path.join(moocSavePath(pathDate+'\\'+suffix),kc[2])
            for xk in xkxx:
                if suffix=='智慧树':
                    t = (xk[1], xk[2], xk[3], '', xk[5], xk[6], '', '', xk[7] + ',任课教师：' + xk[4].split('/')[0])
                    content.append(t)
                elif suffix=='优课':##实际上就是中国近现代史纲要
                    if xk[4].split('/')[0] in vars.zgjxdsgyRkjs:
                        t=(xk[0],xk[1],xk[2],xk[3]+xk[4].split('/')[1])
                        content.append(t)
                else:
                    pass
            if len(content)>1:
                print(content)
                xlsx=fileInfo(filename)
                xlsx.expXlsx(content=content)
                con.execute(vars.writeToBack.format(kc[0],'####'))
        elif exptype=='jxb':
            jxbxx=getMoocJxbxx(con,kc[0])
            for jxb in jxbxx:
                content=[]
                content.append(title)
                xkxx=getMoocXkxx(con,jxb_id=jxb[0])
                filename=os.path.join(moocSavePath(pathDate+'\\'+suffix),kc[2].replace(' ','')+'%'+jxb[2].split('/')[1]+'%'+jxb[1])
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
                    else:
                        pass
                if len(content) > 1:
                    print(content)
                    xlsx = fileInfo(filename)
                    xlsx.expXlsx(content=content)
                    con.execute(vars.writeToBack.format('####',jxb[0]))
        else:
            pass

# con=connect()
# expMooc(con)




