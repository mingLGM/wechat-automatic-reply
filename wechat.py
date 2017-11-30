import itchat
import requests
# import全部消息类型
from itchat.content import *

header = {
    'Authorization': 'APPCODE 86ae3718e2cb4ccbbebf93b9a79dd748',
}
s = requests.Session();


# 处理文本类消息
# 包括文本、位置、名片、通知、分享
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    # 微信里，每个用户和群聊，都使用很长的ID来区分
    # msg['FromUserName']就是发送者的ID
    # 将消息的类型和文本内容返回给发送者
    itchat.send((getReply(msg['Text']).replace('小i', '晓珂')), msg['FromUserName'])


# 处理多媒体类消息
# 包括图片、录音、文件、视频
@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    # msg['Text']是一个文件下载函数
    # 传入文件名，将文件下载下来
    msg['Text'](msg['FileName'])
    # 把下载好的文件再发回给发送者
    return '暂不支持多媒体文件处理'


# 处理好友添加请求
@itchat.msg_register(FRIENDS)
def add_friend(msg):
    # 该操作会自动将新好友的消息录入，不需要重载通讯录
    itchat.add_friend(**msg['Text'])
    # 加完好友后，给好友打个招呼
    itchat.send_msg('Nice to meet you!', msg['RecommendInfo']['UserName'])


# 处理群聊消息
@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    if msg['isAt']:
        str = msg['Content'].replace('@Claudius', '').replace('@J','')
        itchat.send(getReply(str).replace('小i', 'yourName')+'  '+msg['FromUserName'], msg['FromUserName'])

#发送阿里云获取自动回复
def getReply(msg):
    msg = msg.strip()
    if msg == '':
        return '干嘛?'
    res = s.get(url='http://jisuznwd.market.alicloudapi.com/iqa/query?question=' + msg, headers=header)
    return (eval(res.text)['result']['content'])


# 在auto_login()里面提供一个True，即hotReload=True
# 即可保留登陆状态
# 即使程序关闭，一定时间内重新开启也可以不用重新扫码
itchat.auto_login(True)
itchat.run()
