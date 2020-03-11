
import requests
import time
import re
from lxml import etree
import os
import sqlite3
from apps.scrapys.common import vars


def savePath(title):
    '''指定文件的存储路径'''
    #"广大[2019]108号（广州大学关于公布2019年6月转专业学生名单的通知）"
    pass
    perffix=title.split('[')[0] if title.split('[')[0] else '----'
    suffixPatt=re.compile('.+\[(\d+)\].+')
    year=suffixPatt.findall(title)[0] if len(suffixPatt.findall(title))>0 else '####'
    path=os.path.join(vars.filesSavePath, year + '\\' + perffix)
    if not os.path.exists(path):
        os.makedirs(path)
    return path
#savePath(title="广大[2019]108号（广州大学关于公布2019年6月转专业学生名单的通知）")
def setCookies(cookies):
    '''返回字典型的cookies'''
    return {item.split('=')[0]: item.split('=')[1] for item in cookies.split(";")}
###获取Oa中的发文
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3742.400 QQBrowser/10.5.3866.400"
# }
#cookies = "JSESSIONID=X--4XenOQGiMHD6Gq1xBTPAznLLPzpvZ35DnkNfBlEzlkeDR12ID!-1519103370; USER_INFO=MTAzNjY3; username=103667; password=F98286B8AAA07A6397438CDCB1AAAC6E; style-cookie-exoa-exoa-1834=style1; frameContext=/resources/siteFrame/default"
#cookies = setCookies(cookies)
# url = "http://gd.gzhu.edu.cn/cms/searchInfo.do?method=toSearchByCodition&catalogId=1236&contentNature=1&currentWebsiteCode=exoa&systemEnvironmentSign=exoa&page={}&simplePublishDateType=All"
# data = {
#     "method": "toSearchByCodition",
#     "catalogId": "1236",
#     "contentNature": "1",
#     "currentWebsiteCode": "exoa",
#     "systemEnvironmentSign": "exoa",
# }

###//div[@class='contentDiv']/table/tbody//td[contains(@class,'mainCol')]/@title
def paraseHtml(etreeHtml,headers,cookies,zdz):
    '''处理一页'''
    L=[]
    divs = etreeHtml.xpath("//div[@class='contentDiv']/table[contains(@class,'contentList contentList2')]//tr")
    for div in divs:
        item={}
        xpath = './/td[4]/text()'
        item["titleTime"]=div.xpath(xpath)[0] if len(div.xpath(xpath))>0 else None ###发文时间
        if (zdz=='1' or (item["titleTime"]==time.strftime('%Y-%m-%d'))) and item["titleTime"] is not None:
            xpath = './/td[2]/@title'
            item["title"] = div.xpath(xpath)[0] if len(div.xpath(xpath)) > 0 else None  ###文章标题
            xpath = './/td[2]/a/@href'
            item["titleBh"] = div.xpath(xpath)[0] if len(div.xpath(xpath)) > 0 else None  ###文章链接编号
            xpath='.//td[3]/text()'
            item["titleBM"]=div.xpath(xpath)[0] if len(div.xpath(xpath))>0 else None ###发文部门
            xpath='.//td[5]/a/text()'
            item['counts']=div.xpath(xpath)[0] if len(div.xpath(xpath))>0 else None ###阅读量
            # time.sleep(15)
            if item["title"] is not None:
                item["down"] = getFile(item["titleBh"],headers,cookies)  ###下载附件
                t=(item["titleTime"],item["down"],item["title"],item["titleBM"],item["counts"])
                L.append(t)
            else:
                pass
        else:
            pass
    return L


def getFile(titleBh,headers,cookies):
    patt=re.compile('.+\((\d+)\)')
    res=patt.findall(titleBh)[0]
    ###获取文章fileid
    url='http://oa.gzhu.edu.cn/cms/frontContent.do?method=toAttachList'
    data={
        "contentId":res
    }
    r=requests.post(url=url,data=data,headers=headers,cookies=cookies)
    time.sleep(1)
    # print(r.url)
    assert r.status_code==200
    # print(r.text)
    text=r.text
    fileIdPatt=re.compile(r'.*fileId="(\d+)"')
    fileids=fileIdPatt.findall(text)####文件号
    titlePatt=re.compile(r'.*<span.*>(.*)</span>')
    title=titlePatt.findall(text)[0]###文件名
    # filePath=os.path.join('D:\\projects\\peaums\\gd\\files\\',time.strftime('%Y-%d-%m',time.localtime()))
    ##############下载附件
    for fileId in fileids:###如果有多个附件文件
        filename=os.path.join(savePath(title),title)
        url='http://oa.gzhu.edu.cn/cms/file.do'
        params={
            "method":"toFilePreview",
            "fileId":fileId
        }
        try:
            r=requests.get(url=url,params=params,headers=headers,cookies=cookies)
        except:
            print(fileId)
        with open(filename,'wb') as f:
            f.write(r.content)
            f.close()
    return filename

def main():
    start=end=1
    res=[]
    headers= vars.headers
    url= vars.oaurl
    cookies=setCookies(vars.cookies)
    con=sqlite3.connect(vars.sqliteDB)
    cur=con.cursor()
    zdz=cur.execute('''select zdz from xzb where lower(code)='11078oa' and 1=1''').fetchone()[0]
    while start<=int(end):
        r = requests.get(url=url.format(str(start)), headers=headers, cookies=cookies)
        assert r.status_code == 200
        etreeHtml=etree.HTML(r.content)
        if start==1:
            pageCountPatt = re.compile('.*共(\d+)页.*')
            end=pageCountPatt.findall(r.text)[0]
            if zdz=='0':
                end='3'
        print('当前处理第{}页,url={}'.format(str(start),r.url)+'共{}页'.format(end))
        res.extend(paraseHtml(etreeHtml,headers,cookies,zdz))
        start=start+1
    if res:
        code='''insert into oa(ctime,filePath,title,bm,readCounts) values (:1,:2,:3,:4,:5)'''
        cur.executemany(code,res)
        if zdz=='1':
            cur.execute('''update xzb set zdz='0' where lower(code)='11078oa' and zdz='1' and 1=1''')
        con.commit()
        con.close()
    else:
        pass
    return 'Oa获取完成！'
