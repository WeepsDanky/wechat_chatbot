# digital_twin

## How to deploy locally? 

1. run ```pip install -r requirement.txt ``` to get all dependent python modules.
2. run ```python run_app.py``` 




## Module Description 


1. ```wechat_chatbot.py``` 处理所有与wechat的交互
2. ```wechat_article_bot.py``` 处理微信公众号和相关文章。先分开测试，完成之后可以和```wechat_chatbot.py``` 融合。
3. ```gpt_requests.py``` 处理所有发往OPENAI的请求，此处可以修改prompt来让功能更加多样化
4. ```stupid_requests.py``` 那些有意思的但是不想做的功能

## Features to be added
1. 收到消息后创建To Do List
2. 用RSSHub抓取微信公众号文章，让微信公众号的推送更加可读