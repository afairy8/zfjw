
from common.fileAction.controls import fileInfo
# # from apps.jwglxt.xjgl import vars
# from databaseconfig.connectdbs import connect

# con=connect()

###读取本年度的招生计划
def getNjZsjhXlsx(path):
    '''获取本年度的招生计划xlsx文件'''
    xlsx=fileInfo(path)
    content=xlsx.getFileContent()
    return content
# contentFommat=('xqmc','jg','nj','zymc','zsjhrs','bjs')

def getBjMinrs(zyh):
    '''返回分班的最小人数'''
    if zyh[0:2] in ['21','11','09','18'] or zyh[0:3] in ['203']:
        return 30
    else:
        return 40

def getBjmcKeywords(con,zyh):
    '''获取班级名称的关键字'''
    pass
    bjmcxx='''
    select bj from ZFTAL_XTGL_BJDMB bj,ZFTAL_XTGL_ZYDMB zy 
    where bj.ZYH_ID=zy.ZYH_ID
    and bj.NJDM_ID=to_char(to_number(to_char(sysdate,'YYYY'))-1)
    and zy.zyh='{}'
    and rownum=1
    order by bj
    '''
    return con.execute(bjmcxx.format(zyh))

def expXlsx(filenameKeywords,content):
    '''导出需要导入的文件'''
    file=fileInfo(filenameKeywords)
    file.expXlsx(content=content)





def clacBjsAndBjrs(con,path):
    '''获取本年度的招生计划分班数与班级人数
    format:bjrs_snd_avg=round(zsjhrs_snd/bjs_snd,0)
    bjs_bnd=round(zsjhrs_bnd/bjrs_snd_avg,0)
    bjrs_bnd=round(zsjhrs/bjs_bnd,0)
    diff=bjrs_bnd*bjs_bnd-zsjhrs_bnd
    if diff>0:人数分多了
    elif diff=0:刚好
    else:人数分少了
    '''
    content=getNjZsjhXlsx(path)###现招生计划（校区，学院，年级，专业，招生计划人数)

    bjRes=[
        ('班号id','班号','班级名称','班级简称','所属大队','校区名称','机构名称','年级名称','专业名称','','','在校人数')
    ]
    zsjhRes=[
        ('校区名称','机构名称','年级','专业','招生计划人数','班级数')
    ]

    xqmc_zyh_jgmc_code='''
    select decode(t.XQH_ID,'1','大学城','桂花岗')xqmc,zy.zyh,(select jgmc from ZFTAL_XTGL_JGDMB where jg_id=zy.jg_id) jgmc 
    from JW_XJGL_NJZYZSJHB t,ZFTAL_XTGL_ZYDMB zy where
    t.ZYH_ID=zy.ZYH_ID and  
    t.NJDM_ID=to_char(to_number(to_char(sysdate,'YYYY'))-1) and zy.zymc='{}'
    '''
    # xqmc_zyh_jgmc=con.execute(xqmc_zyh_jgmc_code.format(cont[3]))
    for cont in content:
        xqmc_zyh_jgmc = con.execute(xqmc_zyh_jgmc_code.format(cont[3]))[0]
        xqmc=xqmc_zyh_jgmc[0]
        if len(xqmc[0]):#招生
            zyh,jgmc=xqmc_zyh_jgmc[1],xqmc_zyh_jgmc[2]
            bjrs=getBjMinrs(zyh)###获取专业最小分班人数
            bjs=int(round(int(cont[4])/bjrs,0))###应分班的数量
            diff=int((bjrs*bjs-int(cont[4]))/bjs)
            bjrs=bjrs-diff
            seq=str(int(cont[2][0:1])-1)
            try:
                bjmcKeyWords=getBjmcKeywords(con,zyh)[0][0].split(seq)[0]+cont[2][0:2]
            except:
                if cont[3].find('智能')>=0:
                    bjmcKeyWords='智能' +cont[2][0:2]
                elif cont[3].find('艺术')>=0 or cont[3].find('科学')>=0:
                    bjmcKeyWords=cont[3][0:1]+cont[3][2:3]+cont[2][0:2]
                else:
                    pass
            for i in range(1,bjs+1):
                bh=cont[2][0:2]+zyh+'0'+str(i) if i>9 else cont[2][0:2]+zyh+'00'+str(i)##20XXXX001,20XXXX010
                bjmc=bjmcKeyWords+str(i) ###XXX201,XXX2010
                t=(bh,bh,bjmc,'','',xqmc,jgmc,cont[2],cont[3],'','',bjrs)
                bjRes.append(t)
            t=(xqmc,jgmc,cont[2],cont[3],cont[4],bjs)
            zsjhRes.append(t)
        else:
            pass
                # t = (bh, bh, bjmc, '', '', xqmc, jgmc, tent[2], tent[3], '', '', bjrs_bnd)
    expXlsx('班级信息',content=bjRes)
    expXlsx('专业招生计划',content=zsjhRes)
    return '招生计划输出完成!'


# path=r"C:\Users\80662\Downloads\IMPORT_N101015_NJZYZSJHB_1588166235929.xlsx"
# clacBjsAndBjrs(con,path)






























