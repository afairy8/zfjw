import requests
from requests_toolbelt import MultipartEncoder
def get_access_token(corpsecret='G2dm-9QgDf3uZGGB6ZQ9qVSjq58V4gbfIKwmQ-jQA94'):
    '''获取access_token'''
    corpid='wxeecd4f1f44f855da'
    #appid='1000018'
    #corpsecret='G2dm-9QgDf3uZGGB6ZQ9qVSjq58V4gbfIKwmQ-jQA94'
    url='https://qyapi.weixin.qq.com/cgi-bin/gettoken'
    paras={
        "corpid":corpid,
        "corpsecret":corpsecret
    }
    response=requests.get(url=url,params=paras)
    access_token=response.json()['access_token']
    return access_token

def sendMsg(touser,content,title,access_token,url,type='textcard',media_id=''):
    '''直接在企业微信号中发送消息'''
    if type=='textcard':
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
    elif type=='file':
        paras={
           "touser" : touser,
           "msgtype" : "file",
           "agentid" : 1000018,
            "file": {
                "media_id": media_id
            },
            "safe":1
        }
        sendurl = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}'.format(access_token)
        t = requests.post(url=sendurl, json=paras)
        return t.json()
    else:
        pass
###############

def getTxl():
    ###需要使用教务系统应用
    txlUrl='https://qyapi.weixin.qq.com/cgi-bin/user/get'
    access_token=get_access_token('SXKBGYTdA0lyvV93PJPbZcxPOnrjRwdnd1wc_nMEAsc')
    params={
        "access_token":access_token,
        "userid":'103667'
    }
    data=requests.get(url=txlUrl,params=params)
    txl=data.json()
    #print(type(txl))
    return txl
# def uploadMedias(type='file',filename=''):
#     '''上传素材'''
#     access_token=get_access_token('SXKBGYTdA0lyvV93PJPbZcxPOnrjRwdnd1wc_nMEAsc')
#     # params={
#     #     "access_token":access_token,
#     #     "type":type
#     # }
#     url='https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={}N&type={}'.format(access_token,type)
#     m = MultipartEncoder(
#         fields={
#             filename: ('file', open(filename, 'rb'), 'text/plain')
#         },
#     )
#     data={
#         "media":filename
#     }
#     r = requests.post(url=url, data=m, headers={'Content-Type': 'multipart/form-data'})
#     # print(r)
#     # print(r.text['media_id'])
#     return r.text['media_id']
#     # t=requests.post(url=url,data=params)
#getTxl()
def qywxInterface(touser,tit,content,url='https://cas.gzhu.edu.cn/cas_server/login'):
    access_token=get_access_token()
    if tit is None:
        tit='教务消息'
    t= sendMsg(touser=touser,title=tit,content=content,access_token=access_token,url=url)
    t['MESSAGE']=t['errmsg']
    return t


# #media_id=uploadMedias(filename=r"D:\projects\zfjw\common\readFiles\media.pdf")
# media_id='3zGujlhkNMIk06h2kCzjqXwhAcPIq_oYny3IwTRPt9hCCpxpz8xMvSA1djHEs-PYs'
# content1='''
# 1.现在微信上传的《2019-2020学年第二学期下半学期本科教学实施方案》是教务处拟提出的初步讨论稿，学校还没有确定毕业班和非毕业班学生返校时间。请各学院一定要通知到每一位学生，不再转发相关的消息。
# 2.请通知全体老师和本科学生，本学期在第9周（即4+4周在线教学)之后，继续实施在线教学以及毕业班学生论文的在线指导，请按相关工作预案和要求，抓好在线课堂教学和论文指导的各个环节，确保教学质量。 【广州大学教务处  2020年4月20日】（联系人：教务处 何贯峰 联系电话：18928873430）
# '''



# def sendMsg2(touser, content, title, access_token, url):
#     paras = {
#         "touser": touser,
#         "msgtype": "textcard",
#         "agentid": 1000018,
#         "textcard": {
#             "title": title,
#             "description": "<div class=\"highlight\">" + content + "</div>",
#             "url": url
#
#         }
#     }
#     sendurl = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}'.format(access_token)
#     t = requests.post(url=sendurl, json=paras)
#     return t.json()


# print(get_access_token())
# for user in ['103667']:
# #     #t=sendMsg(touser=user,type='file',media_id=media_id,access_token=get_access_token(),content='',title='',url='')
# #     t=sendMsg2(touser=user,content=content1,title='广州大学关于继续实施在线教学的紧急通知',access_token=get_access_token(),url='http://www.gzhu.edu.cn/')
# #     print(t)