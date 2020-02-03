from apps.jyxt.pyfa import vars as bv
from common.actionPre import actionpre
import uuid
import time
from apps.jyxt.jxdg import controls as jxdg
def insertNewCourse(con):
    '''
    插入课程时一定要先插入课程的学时对照，再执行插入课程操作，否则学时插入不会成功
    如果是调试模式，则打印哪些课程是新增的
    :return:
    '''
    if not bv.debug:#更新课程库
        if con.execute(bv.insertNewKcXs):#插入全系课程学时
            if con.execute(bv.insertNewKc):#插入全新课程
                print('stableKc->insertNewCourse 成功')
    else:
        print("全新插入课程列表")
        print(con.execute(bv.printNewKc))
    return 1

def updateExistsCourse(con):
    '''
    如果是调试模式，则打印哪些课程是需要更新的
    未落实的更新，以课程代码为关键字，只考虑课程名称、学分、开课部门不同的情况下进行更新
    '''
    L=[]
    pyfakc=[]
    res = con.execute(bv.getExistsButNotUsed)
    for data in res:
        #data(kcdm,Kch,kcmc,Kcmc,kcywmc,Kcywmc,kkbm_id,Kkbm_id,zxf,kxf,zzxs,kzxs,kch_id)
        if data[2]!=data[3] or data[4]!=data[5] or data[6]!=data[7] or data[8]-data[9]!=0 or data[10]-data[11]!=0:
            L.append((data[2],data[4].title(),data[6],str(data[8]),data[10],data[0]))
            if data[6]!=data[7] or data[8]-data[9]!=0:
                pyfakc.append((str(data[8]),data[6],data[12]))
    #print(pyfakc)
    if not bv.debug:
        if con.execute(bv.updateExistsButNotUsed,L):
            print("已存在将更新的课程信息更新完成")
            if con.execute(bv.updateExistsButNotUsedPyfa,pyfakc):#更新其它年度的培养方案信息
                print("已存在将更新的其它年度培养方案课程信息更新完成")
                if con.execute(bv.updateExistsButNotUsedJxjh,pyfakc):
                    print("已存在将更新其它年度的教学执行计划课程信息更新完成")
    else:
        print("已存在将更新的课程信息为")
        con.execute(bv.updateExistsButNotUsed,L)
    return 1


def writeFile(data):
    '''记录单回合中已处理，以免有异常'''
    f=open('success.txt','a+')
    f.write(data)
    f.close()
    return
def readFile():
    '''单次处理中已经成功的'''
    try:
        f=open('D:\\projects\\jwAuto\\common\\readFiles\\success.txt','r')
        L=f.read().split('$')
        f.close()
    except:
        L=[]
    return L
def pyfaxxandSynj(con,data):
    #print(data)
    #print([data])
    #print(data[6])
    con.execute(bv.insertPyfaxx,[(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[10],data[11])])
    con.execute(bv.insertPyfaxxNj,[(data[0],data[1])])
    return 1

def calcTxxffb(data,sign='tx'):
    '''插入通选学分要求,14学分按1-12（4）,2-3（4）,2-12（4）,3-3（2）分配
    插入教师教育类选修学分要求，7学分按2-3（2），2-12（2），3-3（2），3-12(1)分配'''
    xffblist=[]
    if sign=='tx':
        xqlist=['12','3','12','3']
        xfyqjd_id=data[0] + 'zxxx' + 'tx10000'
        xf='4.0'
        xnlist = ['1', '2', '2', '3']
    else:
        xqlist=['3','12','3','12']
        xfyqjd_id=data[0] + 'zxxx' + 'jsjy11111'
        xf='2.0'
        xnlist=['2','1','3','2']
    maxCount=3
    #插入通选学分要求
    for i in range(len(xqlist)):
        if i<maxCount:
            t=(
                str(uuid.uuid1()).replace('-',''),
                data[0],
                xfyqjd_id,
                xnlist[i]+'-'+xqlist[i],
                xf,
                '1'
            )
        else:
            t=(
                str(uuid.uuid1()).replace('-',''),
                data[0],
                xfyqjd_id,
                xnlist[i]+'-'+xqlist[i],
                str(float(xf)/2),
                '1'
            )
        xffblist.append(t)
    return xffblist

def addCommonNode(con,data):
    '''
    :param t:tuple type，data[0]为pyfaxx_id
    :param L: common Nodes list
    :return:
    '''
    L=[]
    L.append((data[0], data[0] + 'zx', '主修', '1', None, None, None, None, None, None, 'zx',None))
    L.append((data[0], data[0] + 'zxbx', '必修类',None, 'wfx', None, data[0]+'zx', '1', '0', None, 'zx','1'))
    L.append((data[0], data[0] + 'zxxx', '选修类', None, 'wfx', None, data[0] + 'zx', '20', '0', None, 'zx','1'))
    L.append((data[0], data[0] + 'zxxx' + 'tx10000', '通识类选修课程', None, 'wfx', '14', data[0] + 'zxxx', '99', '0', None, 'zx','1'))
    con.execute(bv.insertTxorJxjyXffb, calcTxxffb(data, 'tx'))  # 插入通识选修类学分分布
    if data[3] and data[3].find('师范')>=0 and data[3] not in ['教育技术学(师范)','学前教育(师范)','小学教育(师范)','特殊教育(师范)']:###要把师范专业没有师范去除掉
        L.append((data[0], data[0] + 'zxxx' + 'jsjy11111', '教师教育类选修课程', '1', 'wfx', '7', data[0] + 'zxxx', '98', '1', None, 'zx',None))
        con.execute(bv.insertTxorJxjyXffb, calcTxxffb(data, 'jsjy'))  # 插入教师教育类学分分布
        jsjykc=con.execute(bv.getJsjylKc)
        kclist=[]
        yxkklist=[]
        for kc in jsjykc:#教师教育类允许开课学年学期
            kc=list(kc)
            kc[0]=data[0] + 'zxxx' + 'jsjy11111'+kc[20]#pyfakcxx_id
            kc[1]=data[0] + 'zxxx' + 'jsjy11111'#xfyqjd_id
            t=(kc[0],'2','3')
            yxkklist.append(t)
            t=(kc[0],'2','12')
            yxkklist.append(t)
            t=(kc[0],'3','3')
            yxkklist.append(t)
            t=(kc[0],'3','12')
            yxkklist.append(t)
            #print(kc)
            kclist.append(tuple(kc[0:20]))
        con.execute(bv.insertJsjyKc,kclist)#插入教师教育类课程
        con.execute(bv.insertJsjyKcYxKk,yxkklist)#插入教师教育类课程开课
        jsjykc=con.execute(bv.getJsjylkcXs)
        kclist=[]
        for kc in jsjykc:#插入教师教育类课程
            kc=list(kc)
            kc[0]=data[0] + 'zxxx' + 'jsjy11111'+kc[7]
            kclist.append(tuple(kc[0:7]))
        con.execute(bv.insertJsjyKcXs,kclist)#插入教师教育类培养方案学时
    if bv.sfcjtxkcgsnode:
        txfjd=data[0] + 'zxxx' + 'tx10000'
        L.append((data[0], txfjd+'kcgs12', '哲学与逻辑', '3', 'wfx', '2', txfjd, '1', '1', None, 'zx',None))
        L.append((data[0], txfjd+'kcgs13', '历史与文化', '3', 'wfx', '2', txfjd, '2', '1', None, 'zx',None))
        L.append((data[0], txfjd+'kcgs14', '社会与经济', '3', 'wfx', '2', txfjd, '3', '1', None, 'zx',None))
        L.append((data[0], txfjd+'kcgs15', '创新与创业', '3', 'wfx', '2', txfjd, '4', '1', None, 'zx',None))
        L.append((data[0], txfjd+'kcgs16', '科学与技术', '3', 'wfx', '2', txfjd, '5', '1', None, 'zx',None))
        L.append((data[0], txfjd+'kcgs17', '艺术与审美', '3', 'wfx', '2', txfjd, '6', '1', None, 'zx',None))
        L.append((data[0], txfjd+'kcgs18', '运动与健康', '3', 'wfx', '2', txfjd, '7', '1', None, 'zx',None))
        ##L.append((data[0], txfjd+'kcgs19', '通选（其它归属）', '3',  'wfx', '7',txfjd, '8', '1', None, 'zx', None))
        con.execute(bv.insertPyfaxfyq,L)#插入通选学分要求节点
        L=[]
        for i in range(12,19):
            L.append((str(uuid.uuid1()).replace("-",""),txfjd + 'kcgs'+str(i),str(i)))
        #print(L)
        con.execute(bv.insertPyfaKcgs,L)#插入通选学分要求节点与课程归属之间的关系

    return 1

def jdidExists(L,jdid):
    '''判断jdid是否已经被添加到L中'''
    for t in L:
        if jdid==t[1]:
            return 1
    return 0

def genPyfaFrame(con):
    '''
    generate the main pyfa Frame;
    contains 1,2,3,4 level xfyqjd_id and the ralations of 1->2->3->4;
    contains the min credits of the leaf node
    var L:refer to the pyfaxxb,pyfasynjb and the kinds of level nodes sets
    如果是调试模式，则打印哪些节点是需要添加的
    path:--nj||zydm||zx||xbx(bx/xx)||kcxz||kcxzdm(jw_jh_kcxzdmb)||fxmk/kmk||modulekey
    :return:
    '''
    zyxxRes=con.execute(bv.getPyfaxxb)
    successZydm=readFile()#已经同步成功的专业
    for data in zyxxRes:
        #data[0] pyfaxx_id,data[1] nj,data[2] zyh_id,data[3] pyfamc,data[9] zydm
        if data[9]  not in successZydm:# in ['0210']:#in ['0110','0210']:#in ['0111']:#:
            print('当前处理的专业为:{}'.format(data[9]))
            pyfaxxandSynj(data)#插入培养方案信息表、培养方案适用年级表
            addCommonNode(data)#一次性添加主修、必修、选修、通识类选修、教师教育类选修节点
            kcxzfjd=(data[0]+'zxbx',data[0]+'zxxx')#课程性质对应的父路径
            kcxzData=con.execute(bv.getPyfaxfyqJd.format(data[9],data[1]))
            L=[]#培养方案结构列表
            px=2
            #生成培养方案结构
            for kcxz in kcxzData:
                #print(bv.getZyfxCount.format(data[9],data[1],kcxz[2]))
                zyfxCount=con.execute(bv.getZyfxCount.format(data[9],data[1],kcxz[2]))[0][0]#一个课程性质的模块数量
                if kcxz[4]=='bx':
                    mkfjd=kcxzfjd[0]+'kcxz'+kcxz[2]
                    if  kcxz[6] and zyfxCount>=1:#有多个模块
                        if not jdidExists(L,mkfjd):
                            px=px+1
                            #print(bv.getPyfaxfyqJdXf.format(mkfjd + 'fxmk'))
                            try:
                                xf = con.execute(bv.getPyfaxfyqJdXf.format(mkfjd + 'fxmk'))[0]
                            except:
                                xf = con.execute(bv.getPyfaxfyqJdXf.format(mkfjd))[0]
                            #t(pyfaxx_id,xfyqjd_id,xfyqjdmc,jdkcsx,zyfx_id,yqzdxf,fxfyqjd_id,px,sfmjd,kcxzdm,xdlx,xfyqzjdgx)
                            t = (data[0], mkfjd, kcxz[3], '1', 'wfx', str(xf[1]), kcxzfjd[0], px, '0', None, 'zx', '1')
                            L.append(t)
                        if kcxz[6].find('跨模块')>=0 :#且为跨模块,此时同时添加跨模块，方向模块，课程性质模块
                            px=px+1
                            if zyfxCount>1:
                                px=px+1
                                xf = con.execute(bv.getPyfaxfyqJdXf.format(mkfjd+'fxmk'))[0]
                                t = (
                                    data[0], mkfjd + 'fxmk', '方向模块', '1', 'wfx', str(xf[2]), mkfjd, px, '0', None, 'zx',
                                    '0')  # 非末节点
                                L.append(t)
                            else:
                                xf = con.execute(bv.getPyfaxfyqJdXf.format(mkfjd))[0]
                            px=px+1
                            t = (data[0], mkfjd+'kmk',kcxz[6], '1', 'wfx', str(xf[1]-xf[2]), mkfjd, px, '1', None, 'zx', None)#末节点
                            con.execute(bv.insertPyfakcxxkmk,[(mkfjd,kcxz[6])])
                            L.append(t)
                        else:#非跨模块，则此时只添加相应的具体方向模块
                            pass
                            px=px+1
                            xf = con.execute(bv.getPyfaxfyqJdXf.format(mkfjd + 'fxmk'))[0]
                            t = (data[0], mkfjd+'fxmk'+str(kcxz[5]), kcxz[6], '1', 'wfx', str(xf[2]), mkfjd+'fxmk', px, '1', None, 'zx', None)#末节点
                            con.execute(bv.insertPyfakcxxfxmk,[(mkfjd,kcxz[6])])
                            L.append(t)
                    else:
                        if not jdidExists(L, mkfjd):
                            px=px+1
                            #print(bv.getPyfaxfyqJdXf.format(mkfjd))
                            try:
                                xf = con.execute(bv.getPyfaxfyqJdXf.format(mkfjd))[0]
                            #print(xf)
                            except:
                                #print(bv.missBxKcxzXf.format(mkfjd))
                                xf = con.execute(bv.missBxKcxzXf.format(mkfjd))[0]

                            t = (data[0], mkfjd, kcxz[3], '1', 'wfx', str(xf[1]), kcxzfjd[0], px, '1', None, 'zx',None)
                            #print(bv.insertPyfakcxxWmk.format(mkfjd))
                            con.execute(bv.insertPyfakcxxWmk.format(mkfjd))
                            L.append(t)
                elif kcxz[4]=='xx':
                    mkfjd=kcxzfjd[1]+'kcxz'+kcxz[2]#末节点模块父节点id，也是相应课程性质的节点id
                    if  kcxz[6] and zyfxCount>=1:#有模块
                        if not jdidExists(L,mkfjd):
                            px=px+1
                            try:
                                xf = con.execute(bv.getPyfaxfyqJdXf.format(mkfjd + 'fxmk'))[0]
                            except:
                                xf = con.execute(bv.getPyfaxfyqJdXf.format(mkfjd))[0]
                            #print(bv.getPyfaxfyqJdXf.format(mkfjd))
                            #t(pyfaxx_id,xfyqjd_id,xfyqjdmc,jdkcsx,zyfx_id,yqzdxf,fxfyqjd_id,px,sfmjd,kcxzdm,xdlx,xfyqzjdgx)
                            t = (data[0], mkfjd, kcxz[3], '1', 'wfx', str(xf[1]), kcxzfjd[1], px, '0', None, 'zx', '1')
                            L.append(t)
                            # print(kcxz[6])
                            # print(isinstance(kcxz[6],None))
                        if  kcxz[6].find('跨模块')>=0 :#xx且为跨模块,此时同时添加跨模块，方向模块，课程性质模块
                            if zyfxCount>1:
                                px=px+1
                                xf = con.execute(bv.getPyfaxfyqJdXf.format(mkfjd+'fxmk'))[0]
                                t = (
                                    data[0], mkfjd + 'fxmk', '方向模块', '1', 'wfx', str(xf[2]), mkfjd, px, '0', None, 'zx',
                                    '0')  # 非末节点
                                L.append(t)
                            else:
                                xf = con.execute(bv.getPyfaxfyqJdXf.format(mkfjd))[0]
                            px=px+1
                            t = (data[0], mkfjd+'kmk', '跨模块', '1', 'wfx', str(xf[1]-xf[2]), mkfjd, px, '1', None, 'zx', None)#xx末节点
                            con.execute(bv.insertPyfakcxxkmk,[(mkfjd,kcxz[6])])
                            L.append(t)
                        else:#非跨模块，则此时只添加相应的具体方向模块
                            pass
                            px=px+1
                            xf = con.execute(bv.getPyfaxfyqJdXf.format(mkfjd + 'fxmk'))[0]
                            t = (data[0], mkfjd+'fxmk'+str(kcxz[5]), kcxz[6], '1', 'wfx', str(xf[2]), mkfjd+'fxmk', px, '1', None, 'zx', None)#xx末节点
                            con.execute(bv.insertPyfakcxxfxmk, [(mkfjd, kcxz[6])])
                            L.append(t)
                    else:
                        if not jdidExists(L,mkfjd):
                            px=px+1
                            #print(bv.getPyfaxfyqJdXf.format(mkfjd))
                            try:
                                xf = con.execute(bv.getPyfaxfyqJdXf.format(mkfjd))[0]
                            except:
                                xf = con.execute(bv.getPyfaxfyqJdXf.format(mkfjd+'fxmk'))[0]
                            t = (data[0], mkfjd, kcxz[3], '1', 'wfx', str(xf[1]), kcxzfjd[1], px, '1', None, 'zx',None)
                            con.execute(bv.insertPyfakcxxWmk.format(mkfjd))
                            L.append(t)
                    pass
                else:
                    pass
            #print(L)
            con.execute(bv.insertPyfaxfyq, L)#插入培养方案结构
            if con.execute(bv.beautifyPyfa.format(data[1],data[9])):#美化培养方案
                if con.execute(bv.insertPyfakcYxKkXnxq.format(data[1],data[9])):#插入允许开课学年学期
                    #print(bv.insertPyfaKcXsDzb.format(data[1],data[9]))
                    if con.execute(bv.insertPyfaKcXsDzb.format(data[1],data[9])):#插入培养方案学时对照
                        if con.execute(bv.insertPyfaxffb.format(data[9],data[1])):#插入培养方案学分分布表
                            writeFile(data[9]+'$')
                            print('专业{}已经处理'.format(data[9]))
        else:
            print(data[9]+'已经处理过了，本次忽略')
    return 1

def initPyfaxxbData(con):
    '''从中间表获取培养方案信息
    特殊点在于该表中存在clob字段，要处理
    '''
    try:
        queryString = '''
        select pyfaxx_id,nj,zydm,yqzdxf,major,pymbzw,pymbyw,zyhxkc,pyts,byyq,xdzd,sxh
        from zfjwjkfs.ODS_RCPY_SJTB_PYFAXXB
            '''
        res = con.execute(queryString)
    except:
        print("从数据中心获取数据失败！")
    L=[]
    for data in res:
        #pymbzw = data[5]
        pymbzw=data[5].read()[0:1800]
        #byyq=data[9]
        byyq=data[9].read()[0:1800]
        #xdzd=data[10]
        xdzd=data[10].read()[0:1800]
        L.append((data[0],data[1],data[2],data[3],data[4],pymbzw,data[6],data[7],data[8],byyq,xdzd,data[11]))
    return con.execute('''insert into zftal_sjtb_pyfaxxb(pyfaxx_id,nj,zydm,yqzdxf,major,pymbzw,pymbyw,zyhxkc,pyts,byyq,xdzd,sxh)
    values(:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12)
    ''',L)


def initCreatePyfaTable(con,sign='pyfa'):
    '''从中间表读取数据'''
    if sign=='pyfa':
        tableExists=con.objectExists('zftal_sjtb_pyfaxxb')
        #tableExists=connections.tableExists('zftal_sjtb_pyfaxxb')
        if tableExists[0][0]:
            con.execute("drop table zftal_sjtb_pyfaxxb")
        con.execute('''create table zftal_sjtb_pyfaxxb(
        pyfaxx_id varchar2(255),nj varchar2(255),zydm varchar2(255),
        yqzdxf varchar2(255),major varchar2(255),pymbzw varchar2(4000),
        pymbyw varchar2(4000),zyhxkc varchar2(4000),pyts varchar2(4000),
        byyq varchar2(4000),xdzd varchar2(4000),sxh varchar2(255)
        )''')
        if initPyfaxxbData(con):
            print("获取pyfaxxb完成")
        L=[
            'ods_rcpy_sjtb_pyfakcxxb',
            'ods_rcpy_SJTB_PYFAKCXZXFXXB',
            'ods_rcpy_SJTB_PYFAKCXSDZB',
            'ods_rcpy_SJTB_PYFAYXKKXNXQB'
        ]
    elif sign=='jxdg':
        L=[
            'ods_rcpy_LY_JXDG_DGNR',
            'ods_rcpy_LY_JXDG_JXMB_BYYQ',
            'ods_rcpy_LY_JXDG_KCFPB',
            'ods_rcpy_LY_JXDG_KCKH'
        ]
    elif sign=='kc':
        L=[
            'ods_rcpy_sjtb_kcxzdmb',
            'ods_rcpy_SJTB_KCXSDMB',
            'ods_rcpy_sjtb_kcdmb'
        ]
    else:
        pass
    dropString='''drop table {}'''
    createString='''create table {} as (SELECT * FROM zfjwjkfs.{})'''
    for li in L:
        jwTableName=li.replace('ods_rcpy','zftal').replace('LY','sjtb')
        t=con.objectExists(jwTableName)
        if t[0][0]:
            print('删除'+dropString.format(jwTableName))
            try:
                con.execute(dropString.format(jwTableName))
            except:
                print("drop faile {}".format(jwTableName))
        print('当前创建'+createString.format(jwTableName,li.upper()))
        con.execute(createString.format(jwTableName,li.upper()))
    return 1


def jyxtInterface(con,actionNamme=''):
    if actionNamme==actionpre.unique('pyfa'):
        start=time.clock()
        if initCreatePyfaTable(con,sign='kc'):
            if updateExistsCourse(con):
                if insertNewCourse(con):
                    if initCreatePyfaTable(con,'pyfa'):
                        if genPyfaFrame(con):
                            end=time.clock()
                            return '课程、培养方案同步完成！共耗时{}秒'.format(str(end-start))
                        else:
                            return '培养方案结构生成失败！'
                    else:
                        return '培养方案中间表读取失败！'
                else:
                    return '新课程插入失败！'
            else:
                return '已存在的课程学分、开课部分更新完成！'
        else:
            return '课程中间表生成失败'
    elif actionNamme==actionpre.unique('jxdg'):
        if initCreatePyfaTable(con,sign='jxdg'):
            if jxdg.createJxdg(con):
                return '教学大纲同步完成！'
            else:
                return '教学大纲同步失败！'
        else:
            return '中间表创建教学大纲失败！'
    else:
        pass
# def pyfaMain():
#     initCreatePyfaTable()
#     start=time.clock()
#     genPyfaFrame()
#     end=time.clock()
#     print(end-start)