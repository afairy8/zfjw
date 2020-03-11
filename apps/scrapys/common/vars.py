

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3742.400 QQBrowser/10.5.3866.400"
}
####################OA相关参数
filesSavePath=r"D:\projects\zfjw\common\expfiles\oa\files"
oaurl = "http://oa.gzhu.edu.cn/cms/searchInfo.do?method=toSearchByCodition&catalogId=1236&contentNature=1&currentWebsiteCode=exoa&systemEnvironmentSign=exoa&simplePublishDateType=All&page={}"
cookies="df=fit; mi=mi6257; USER_INFO=MTAzNjY3; username=103667; password=F98286B8AAA07A6397438CDCB1AAAC6E; style-cookie-exoa-exoa-1834=style1; JSESSIONID=VlG9YS-JMeX9J8DxU5yo0yCIvA2SiD4Khfogdmsj4UxxJIDCpoHK!-1519103370; sentWorkItemList=; frameContext=/resources/siteFrame/default"

####################广大XW相关参数
xwurl='http://news.gzhu.edu.cn/'
xwindex='ttgd.htm'
xwSfGetDetail=False

####################数据库存放位置
sqliteDB=r"D:\projects\gd.sqlite3"

##################深大XW相关参数
sdxwurl='https://news.szu.edu.cn/xyxw/'
sdxwindex=['sdyw.htm','zhxw.htm']
sdxwSfGetDetail=False

#################中大XW相关参数
zdxwurl='http://news2.sysu.edu.cn/news01/'
zdxwindex='index.htm'
zdxwSfGetDetail=False