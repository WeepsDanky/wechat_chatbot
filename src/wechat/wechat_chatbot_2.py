''' 
相同功能，但是使用wxpy库实现 
'''

import wxpy
import requests 
from bs4 import BeautifulSoup

def retrieve_chat_history():
    bot = wxpy.Bot()
    print('Login successful!') 

    #friend chat history 
    friend = wxpy.bot.search('friend')[0]
    print(friend)
    print('Friend found!') 

    friend_chat_history = friend.get_history()
    for msg in friend_chat_history: 
        print(msg.text)
    
    #group chat history 
    group = wxpy.bot.search('group')[0] 
    print(group) 
    print('Group found!') 

    group_chat_history = group.get_history() 
    for msg in group_chat_history: 
        print(msg.text) 
    
    #公众号聊天记录 
    mp = wxpy.bot.search('公众号')[0].mp 
    response = requests.get(mp.url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    for item in soup.select('.history .message'): 
        print(item.text)

retrieve_chat_history() 