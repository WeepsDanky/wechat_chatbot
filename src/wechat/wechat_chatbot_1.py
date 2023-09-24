"""
读取历史消息，把新消息和历史消息一起喂给chatgpt【gpt_request】，然后使用【gpt_request】返回的数据发送新消息给给我发消息的人，或是创建待办事项。
使用WeChatPYAPI
https://github.com/mrsanshui/WeChatPYAPI

"""

from WeChatPYAPI import WeChatPYApi

import time
import logging
from queue import Queue 
import os
import openai


# 当前目录路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


logging.basicConfig(level=logging.INFO)  # 日志器
msg_queue = Queue()  # 消息队列


def on_message(msg):
    """消息回调，建议异步处理，防止阻塞"""
    print(msg)
    msg_queue.put(msg)


def on_exit(wx_id):
    """退出事件回调"""
    print("微信({})：已退出登录，请重新登录".format(wx_id))


def main():

    # 实例化api对象【要多开的话就实例化多个《WeChatPYApi》对象】
    w = WeChatPYApi(msg_callback=on_message, exit_callback=on_exit, logger=logging)

    # 启动微信【调试模式可不调用该方法】
    errno, errmsg = w.start_wx()
    # errno, errmsg = w.start_wx(path=os.path.join(BASE_DIR, "login_qrcode.png"))  # 保存登录二维码
    if errno != 0:
        print(errmsg)
        if errmsg != "当前为调试模式，不需要调用“start_wx”":
            return

    # 这里需要阻塞，等待获取个人信息
    while not w.get_self_info():
        time.sleep(2)

    my_info = w.get_self_info()
    print("登陆成功！")
    print(my_info)

    # 拉取列表（好友/群/公众号等）第一次拉取可能会阻塞，可以自行做异步处理
    # 好友列表：pull_type = 1
    # 群列表：pull_type = 2
    # 公众号列表：pull_type = 3
    # 其他：pull_type = 4
    lists = w.pull_list(pull_type=1)
    print(lists)

    # Mirror the message to the file helper
    history_msg = [0]
    while True: 
        # 处理消息回调
        msg = msg_queue.get()   
        if msg["msg_type"] == 1 and msg["content"] != history_msg[-1]:
            content = msg["content"]
            w.send_text(to_wx="filehelper", msg=content)
            history_msg.append(content)
            
            print(history_msg[-1])
            time.sleep(5) 



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        os._exit(1)

