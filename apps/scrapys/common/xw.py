import sqlite3
import requests
from lxml import etree
import time


class xwscrapy:
    '''新闻爬虫类'''
    def __init__(self, code=''):
        ##print(self.getCon())
        self.con = sqlite3.connect("D:\\projects\\gd.sqlite3")
        self.cur = self.con.cursor()
        self.data = self.cur.execute('''
        select zdz,pageXpath,contentXpath,titleXpath,ctimeXapth,linkXpath,indexs,url,h,savecode from xzb where xzb.code='{}' 
        '''.format(code)).fetchall()[0]
        data=self.data
        self.zdz, self.pageXpath, self.contentXpath, self.titleXpath, self.ctimeXapth, self.linkXpath, self.indexs, self.url,self.headers,self.saveCode=data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9]
        self.code=code
    def getdefaultHeades(self):
        '''将headers或cookies转换为字典类型'''
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3742.400 QQBrowser/10.5.3866.400"
        }
        return headers
    def save(self,L):
        '''将获取的数据保存到本地数据库中'''
        self.cur.executemany(self.saveCode,L)
        #self.cur.close()
        self.con.commit()
        #self.con.close()
    def close(self):
        self.cur.close()
        self.con.close()
    def getPageCounts(self,etreeHtml):
        '''获取下页的链接'''
        if self.code in ['10558','11078','10590']:
            maxPage=etreeHtml.xpath(self.pageXpath)[0].split('.')[0].split('/')[-1].split('ex')[-1] if len(etreeHtml.xpath(self.pageXpath)) > 0 else 0
        elif self.code in ['10561']:
            maxPage=etreeHtml.xpath(self.pageXpath)[0].split('.')[0].split('/')[-1].split('st')[-1] if len(etreeHtml.xpath(self.pageXpath)) > 0 else 0
        elif self.code in ['10574']:
            maxPage=etreeHtml.xpath(self.pageXpath)[0].split('.')[-1] if len(etreeHtml.xpath(self.pageXpath)) > 0 else 0
        else:
            maxPage=0
        return maxPage
    def getCon(self):
        '''返回数据库的位置'''
        with open('dbpath.ini') as f:
            content = f.readline().split('=')[-1]
            f.close()
        return "D:\\projects\\gd.sqlite3"
    def paraseHtml(self,etreeHtml,zdz):
        '''解析页面'''
        xpath = self.contentXpath
        divs = etreeHtml.xpath(xpath)
        L = []
        for div in divs:
            xpath = self.ctimeXapth  ###文章发布时间
            ctime = div.xpath(xpath)[0].replace('\n','') if len(div.xpath(xpath)) > 0 else None
            ##print(ctime.replace('\n','').replace(' ',''))
            if ctime is not None and (zdz == '1' or ctime.find(time.strftime('%Y-%m-%d'))>=0):
                xpath = self.linkXpath  ###文章链接
                link = self.url + div.xpath(xpath)[0] if len(div.xpath(xpath)) > 0 else None
                xpath = self.titleXpath  ###文章标题
                title = div.xpath(xpath)[0] if len(div.xpath(xpath)) > 0 else None
                # #print(title)
                detail = ''  ###文章详情
                t = (ctime, link, title, detail,self.code)
                L.append(t)
        return L
    def main(self):
        '''主函数'''
        url = self.url  ###起始url
        indexs = self.indexs.split(';')
        headers =self.getdefaultHeades()
        ##print(headers)
        zdz=self.zdz
        for index in indexs:
            next_index = index
            L=[]
            start=1
            while next_index:
                r = requests.get(url=url + next_index, headers=headers)
                #print(r.url)
                etreeHtml = etree.HTML(r.content)
                ###解析当前页
                L.extend(self.paraseHtml(etreeHtml, zdz))
                #print('当前处理第{}页,url={}'.format(str(start), r.url))
                ###下一页链接
                if start == 1:
                    maxPage = self.getPageCounts(etreeHtml)
                time.sleep(1)
                if (zdz == '1' and int(maxPage) <= start) or (zdz == '0' and start == 3):
                    break
                else:
                    if self.code in ['11078','10590']:
                        next_index = index.split('.')[0] + '/' + str(int(maxPage) - start + 1) + '.htm'
                    elif self.code in ['10558']:
                        next_index = index.split('.')[0] + str(start) + '.htm'
                    elif self.code in ['10561']:
                        next_index=index.split('.')[0][0:4]+str(max(2,start))+'.htm'
                    elif self.code in ['10574']:
                        next_index=index+'/'+str(max(2,start))
                    else:
                        next_index=None
                    #print('下一页', self.url+next_index)
                    start = start + 1
            self.save(L)
        if zdz=='1':
            self.cur.execute("update xzb set zdz='0' where zdz='1' and code='{}' ".format(self.code))
            self.con.commit()
        self.close()
        return '{}xw获取完成！'.format(self.code)

##########
def main():
    '''接口主函数'''
    L=[]
    for code in ['10590','11078','10558','10574']:
        gd=xwscrapy(code)
        L.append(gd.main())

