import requests
from lxml import etree
import sqlite3
import time
from apps.scrapys.gd import vars

def paraseHtml(etreeHtml,headers,zdz):
    xpath='//div[@class="text-list"]/ul/li'
    divs=etreeHtml.xpath(xpath)
    L=[]
    for div in divs:
        xpath='.//span/text()'###文章发布时间
        ctime=div.xpath(xpath)[0] if len(div.xpath(xpath))>0 else None
        if ctime is not None and (zdz=='1' or ctime==time.strftime('%Y-%m-%d')):
            xpath='.//a/@href'###文章链接
            link=vars.url+div.xpath(xpath)[0] if len(div.xpath(xpath))>0 else None
            xpath='.//a/text()' ###文章标题
            title=div.xpath(xpath)[0] if len(div.xpath(xpath))>0 else None
            #print(title)
            detail=getDetails(link,headers) if vars.xwSfGetDetail else ''###文章详情
            t=(ctime,link,title,detail)
            L.append(t)
    return L

def getDetails(link,headers):
    try:
        r=requests.get(url=link,headers=headers)
        #print(r.url)
        content=etree.HTML(r.content)
        xpath='//div[@id="vsb_content"]//text()'
        detail=''.join(content.xpath(xpath)) if len(content.xpath(xpath))>0 else None
        return detail.replace('  ',' ')
    except:
        pass

def main():
    start=1
    L=[]
    url=vars.xwurl
    index=vars.xwindex
    headers=vars.headers
    con=sqlite3.connect(vars.sqliteDB)
    cur=con.cursor()
    zdz = cur.execute('''select zdz from xzb where lower(appname)='oa' and 1=1''').fetchone()[0]
    while index:
        r=requests.get(url=url+index,headers=headers)
        #print(r.url)
        etreeHtml=etree.HTML(r.content)
        ###解析当前页
        L.extend(paraseHtml(etreeHtml,headers,zdz))
        print('当前处理第{}页,url={}'.format(str(start),r.url))
        ###下一页链接
        if start==1:
            xpath='//a[@class="Next"][1]/@href'
            maxPage=etreeHtml.xpath(xpath)[0].split('/')[1].split('.')[0] if len(etreeHtml.xpath(xpath)) > 0 else None
        time.sleep(1)
        if (zdz=='1' and int(maxPage)<start-1) or (zdz=='0' and start==3):
            break
        else:
            index='ttgd/'+str(int(maxPage)-start+1)+'.htm'
            print('下一页',index)
            start=start+1
    #print(L)
    code='''insert into xw(ctime,link,title,detail) values(:1,:2,:3,:4)'''
    cur.executemany(code,L)
    con.commit()
    con.close()

    return 'Gdxw获取完成！'