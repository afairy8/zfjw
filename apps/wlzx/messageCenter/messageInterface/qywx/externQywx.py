import requests
from apps.wlzx.messageCenter.messageInterface.qywx import vars
import os
from requests_toolbelt import MultipartEncoder
def get_access_token(corpsecret=vars.ids['msgCenter']['corpsecret']):
    '''获取access_token'''
    url=vars.wxapiurls['getAccessToken']
    paras={
        "corpid":vars.corpid,
        "corpsecret":corpsecret
    }
    response=requests.get(url=url,params=paras)
    access_token=response.json()['access_token']
    return access_token

def uploadFiles(access_token='',filename=''):
    '''上传临时素材，始终提示invalid access_token,但是在网页上则没有提示'''
    suffix=os.path.split(filename)[-1].split('.')[-1]
    if suffix.lower() in ['png','jpg','jpeg']:
        type='image'
    elif suffix.lower() in ['pdf','docx','doc','xlsx','xls']:
        type='file'
    else:
        type=None
    if type:
        pass
        # url=vars.wxapiurls['upLoad'].format(access_token,type)
        # # files=MultipartEncoder(
        # #     {"media":('u.pdf',open(filename, 'rb'),'application/octet-stream')}
        # # )
        # # # files=[('media', ('u.pdf', open(filename, 'rb'), 'text/plain'))]
        # # headers={
        # #     'Content-Type':'application/octet-stream'
        # # }
        # files={"meida":("u.pdf",open(filename, 'rb'))}
        # headers={"Content-type":'application/octet-stream'}
        # r=requests.post(url=url,files=files,headers=headers)
        # print(r.json())
        # print(r)


def sendMsg(touser,content,title,access_token,url,type='textcard',media_id=''):
    '''发送消息'''
    params={
        "touser":touser,
        'agentid':1000018,
        "msgtype":type
    }
    if type.lower()=='textcard':
        params["textcard"]={
            'title':title,
            'description':"<div class=\"highlight\">"+content+"</div>",
            'url':url
        }
    elif type.lower()=='file':
        params["file"]={
            "media_id":media_id
        }
        params["safe"]:1
    else:
        pass
    sendurl=vars.wxapiurls['postMsg'].format(access_token)
    print(sendurl)
    r=requests.post(url=sendurl,json=params)
    return r.json()


# access_token=get_access_token()
# # print(sendMsg(
# #     touser='103667',
# #     content='测试',
# #     title='测试',
# #     access_token=access_token,
# #     url='http://www.gzhu.edu.cn'
# # ))
#
# uploadFiles(
#     access_token,
#     filename=r'D:\projects\zfjw\common\readFiles\media.pdf'
# )
# # print(get_access_token(vars.ids['msgCenter']['corpsecret']))