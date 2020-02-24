import requests

def get_access_token():
    '''获取access_token'''
    corpid='wxeecd4f1f44f855da'
    #appid='1000018'
    corpsecret='G2dm-9QgDf3uZGGB6ZQ9qVSjq58V4gbfIKwmQ-jQA94'
    url='https://qyapi.weixin.qq.com/cgi-bin/gettoken'
    paras={
        "corpid":corpid,
        "corpsecret":corpsecret
    }
    response=requests.get(url=url,params=paras)
    access_token=response.json()['access_token']
    return access_token

def sendMsg(touser,content,title,access_token,url):
    '''直接在企业微信号中发送消息'''
    paras={
       "touser" : touser,
       "msgtype" : "textcard",
       "agentid" : 1000018,
       "textcard" : {
           "title":title,
           "description" : "<div class=\"highlight\">"+content+"</div>",
           "url":url

       }
    }
    sendurl='https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}'.format(access_token)
    t=requests.post(url=sendurl,json=paras)
    return t.json()
###############

def qywxInterface(touser,tit,content,url='https://cas.gzhu.edu.cn/cas_server/login'):
    access_token=get_access_token()
    if tit is None:
        tit='教务消息'
    return sendMsg(touser=touser,title=tit,content=content,access_token=access_token,url=url)


