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

#print(get_access_token())
def sendMsg(touser,content,title='在线教学温馨提醒',content2='',content3='【广州大学教务处】'):
    '''直接在企业微信号中发送消息'''
    access_token='NfLoDZmU8smTOwFT4qb0uyDLSBBpP76xZW3-cwLdqk6J_yMBiDB2BZQYlGcE08v06tgG-xtuIwNO3eo-Hzw2jskGPDcM9cUu4JD13cenptozhwyAQ_SojE5m9RT535mNVPW53xQCvL8gNJeYjyqAkrrRUZGvZO5xTw_2Y_8Ocauplkc3m0hYgku4tn-Wy1vYPCwID-81i4ozzCOfq0hqhA'
    paras={
       "touser" : touser,
       "msgtype" : "textcard",
       "agentid" : 1000018,
       "textcard" : {
           "title":title,
           "description" : " <div class=\"normal\">"
                          +content+"</div><div class=\"highlight\">"+content2+"</div>",
           "url":'https://www.yuketang.cn/web/?next=/v/index/bindSchool_list'

       }
    }
    sendurl='https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}'.format(access_token)
    t=requests.post(url=sendurl,json=paras)
    return t.json()
###############
con=connect()
file=fileInfo(r'D:\projects\zfjw\common\readFiles\用户信息.xlsx')
res=file.getFileContent()
L=[]
writeTologs='''insert into LIKAI_MESSAGE_LOG(id,RECEIVER,content,MESSAGE,SENDTIME)
        values (:1,:2,:3,:4,:5)'''
for row in res:
    if row[0].find('内容来自于文件名') < 0:
        user, content, sendtime,content2 = row[0], row[1], row[2],row[3]
        if user and '2020-02-21' == sendtime.strip():
            # title = setTitle(xxlx)
            t = sendMsg(touser=user, content=content,content2=content2)
            sendtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            L.append((str(uuid.uuid1()), user, content, t['errmsg'], sendtime))
            print('user={},result={}'.format(user,t['errmsg']))
    else:
        pass

if L:
    con.execute(writeTologs, L)
print('send finish!')
