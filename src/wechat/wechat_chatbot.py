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
from bs4 import BeautifulSoup
import json

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



def retrieve_chat_history():
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

    friends = w.pull_list(pull_type=1)
    selected_friends = [d for d in friends if d['wx_account'] == 'ljwb_Gww_dang_snghra'] # 选择一个人的聊天记录作为测试
    selected_wx_account = selected_friends[0]['wx_id']
    print(f"选择的好友是{selected_wx_account}")

    # 获取聊天记录 - 这里以周易为例
    MSG0 = w.select_db(
    db_name="MSG0.db",
    sql_text=f"select IsSender, CreateTime, StrContent from MSG where StrTalker = 'wxid_nqi1sx71l54e12' limit 1000; " # 最多1000条聊天记录
    )

    # 清洗聊天记录，去除xml标签以方便构建prompt
    valid_entries = []
    for item in MSG0:
        content = item['StrContent']
        soup = BeautifulSoup(content, 'html.parser')
        if not soup.find():
            valid_entries.append(item)
    # print("valid_entries are ", valid_entries)

    # chat_msg = [item['StrContent'] for item in valid_entries if item['StrContent']]
    chat_msg = valid_entries
    with open("tests/msg_0.txt", "w", encoding='utf-8') as f:
        f.write(str(chat_msg))
    print("聊天记录已保存到tests/msg_0.txt")

    time.sleep(3)
    w.logout()
    


def main(): 
    retrieve_chat_history() 


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        os._exit(1)
