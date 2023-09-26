'''
总结文章消息
1. 从订阅的公众号获取的文章 
2. 群聊中转发的链接或文章
'''

''' 
读取历史消息，把新消息和历史消息一起喂给chatgpt【gpt_request】，然后使用【gpt_request】返回的数据发送新消息给给我发消息的人，或是创建待办事项。
使用WeChatPYAPI
https://github.com/mrsanshui/WeChatPYAPI
'''

from WeChatPYAPI import WeChatPYApi

import time
import logging
from queue import Queue 
import os
import sys 
from bs4 import BeautifulSoup
import json


# 初始化微信 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
project_dir = "C:\\Users\\Administrator\\Documents\\GitHub\\digital_twin"
logging.basicConfig(level=logging.INFO)  # 日志器
msg_queue = Queue()  # 消息队列

sys.path.append(os.path.join(project_dir, "src"))
import gpt_requests as gpt

def on_message(msg):
    """消息回调，建议异步处理，防止阻塞"""
    print(msg)
    msg_queue.put(msg)


def on_exit(wx_id):
    """退出事件回调"""
    print("微信({})：已退出登录，请重新登录".format(wx_id))


def initailize_wechat(): 
    # 初始化微信
    w = WeChatPYApi(msg_callback=on_message, exit_callback=on_exit, logger=logging)
    errno, errmsg = w.start_wx()
    if errno != 0:
        print(errmsg)
        if errmsg != "当前为调试模式，不需要调用“start_wx”":
            return
    while not w.get_self_info():
        time.sleep(2)
    my_info = w.get_self_info()
    print("登陆成功！")
    # print(my_info)

# 导出每天的公众号文章
def retrieve_official_account_article(): 
    pass 

def main(): 
    pass

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        os._exit(1)
