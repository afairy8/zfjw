import requests
from common.fileAction.controls import fileInfo
import datetime
import uuid
from databaseconfig.connectdbs import connect
def get_access_token():
    '''获取access_token'''
    corpid='wxeecd4f1f44f855da'
    appid='1000018'
    corpsecret='G2dm-9QgDf3uZGGB6ZQ9qVSjq58V4gbfIKwmQ-jQA94'
    url='https://qyapi.weixin.qq.com/cgi-bin/gettoken'
    paras={
        "corpid":corpid,
        "corpsecret":corpsecret
    }
    response=requests.get(url=url,params=paras)
    access_token=response.json()['access_token']
    return access_token

def sendMsg(touser,content):
    '''直接在企业微信号中发送消息'''
    access_token='dBUBkg0a9OSP5c8_mlQV8ZqMpEbMN04RvgIr_8rDpt5kZweUYpMb5Da9_BWS7lxA0GE0ct2AdXAMp5ZkPmeZsveTT7XoMUMwciTIBiM2nai5ArKp75tImlO0qdCb1LXkUo255SMRi_3IBcU30BJNsVo3-BcTmRqAbfzVNdAJypvx6k2iKw0fN14d_vEQkr4jf7YSoC81du9Ah4djrfh3gQ'
    paras={
       "touser" : touser,
       "msgtype" : "text",
       "agentid" : 1000018,
       "text" : {
           "content" : content
       }
    }
    sendurl='https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}'.format(access_token)
    t=requests.post(url=sendurl,json=paras)
    return t.json()
###############
con=connect()
file=fileInfo(r'D:\projects\zfjw\common\readFiles\1.xlsx')
res=file.getFileContent()
L=[]
writeTologs='''insert into LIKAI_MESSAGE_LOG(id,RECEIVER,content,MESSAGE,SENDTIME)
        values (:1,:2,:3,:4,:5)'''
for row in res:
    if row[0].find('内容来自于文件名') < 0:
        user, content, sendtime = row[0], row[1], row[2]
        if user and '2020-02-20' == sendtime.strip():
            # title = setTitle(xxlx)
            t = sendMsg(touser=user, content=content)
            sendtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            L.append((str(uuid.uuid1()), user, content, t['errmsg'], sendtime))
    else:
        pass

if L:
    con.execute(writeTologs, L)
print('send finish!')
