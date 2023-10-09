#!/usr/bin/env python
import os
import sys
import dotenv 

dotenv.load_dotenv() 
project_dir = os.getenv("project_dir")

sys.path.append(os.path.join(project_dir))
sys.path.append(os.path.join(project_dir, "wechat"))
sys.path.append(os.path.join(project_dir, "wechat\\libs"))

import wechat_chatbot

if __name__ == '__main__':
    try:
        wechat_chatbot.main()
    except KeyboardInterrupt:
        os._exit(1)