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



# 初始化微信 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(level=logging.INFO)  # 日志器
msg_queue = Queue()  # 消息队列

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

def get_chat_history(wx_account, num_messages=1000, filepath='tests', filename="msg_0.txt"):
    friends = w.pull_list(pull_type=1)
    selected_friends = [d for d in friends if d['wx_account'] == wx_account] # 选择一个人的聊天记录作为测试
    selected_wx_account = selected_friends[0]['wx_id']
    print(f"选择的好友是{selected_wx_account}")

    # 获取聊天记录
    MSG0 = w.select_db(
    db_name="MSG0.db",
    sql_text=f"select IsSender, CreateTime, StrContent from MSG where StrTalker = '{wx_account}' limit {num_messages}; "
    )

    # 清洗聊天记录，去除xml标签以方便构建prompt
    valid_entries = []
    for item in MSG0:
        content = item['StrContent']
        soup = BeautifulSoup(content, 'html.parser')
        if not soup.find():
            valid_entries.append(item)
    chat_msg = valid_entries
    full_path = os.path.join(project_dir, filepath, filename)
    with open(full_path, "w", encoding='utf-8') as f:
        f.write(str(chat_msg))
    print(wx_account, "的聊天记录已保存到", full_path) 

    time.sleep(3)
    w.logout()
    
# reply message as a GPT chatbot
def reply_to_friends(model="gpt-3.5-turbo-0613"): 
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

    while True:
        msg = msg_queue.get()
        if msg["type"] == 100:
            if msg["is_self_msg"]:
                print("收到了自己发送的消息！")
            else: 
                # 缺少限制条件，应该只回复少量的人，不是回复所有人
                response = gpt.get_friend_chat("user", msg["content"], model=model)
                w.send_text(to_wx=msg["wx_id"], msg=response)
                print('收到了来自', msg["wx_id"], '的消息：', msg["content"])
                time.sleep(2)

def create_wechat_todo(): 
    pass

def main(): 
    reply_to_friends()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        os._exit(1)
