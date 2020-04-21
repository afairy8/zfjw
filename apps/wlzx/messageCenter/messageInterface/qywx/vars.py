
###企业微信id
corpid='wxeecd4f1f44f855da'
#消息中心应用秘钥
ids={
    'msgCenter':{
        'corpsecret':'G2dm-9QgDf3uZGGB6ZQ9qVSjq58V4gbfIKwmQ-jQA94',
        'aggentid':1000018,
    },
    'jwxt':{
        'corpsecret':'SXKBGYTdA0lyvV93PJPbZcxPOnrjRwdnd1wc_nMEAsc',
        'aggentid':16
    },
    'xnTz':{
        'corpsecret':'0WAEeSXNxQXrNaz2vmK99XabPTofNhqGzipSWzZbco27L2KgktCcacLsYaDhc6f1',
        'aggentid':5

    }
}

wxapiurls={
    'postMsg':'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}',##发送消息
    'getTxl':'https://qyapi.weixin.qq.com/cgi-bin/user/get',##获取通讯录
    'upLoad':'https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={}N&type={}',##上传素材
    'getAccessToken':'https://qyapi.weixin.qq.com/cgi-bin/gettoken'##获取企业微信access_token
}
