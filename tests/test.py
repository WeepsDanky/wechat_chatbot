# -*- coding: utf-8 -*-
import requests
import time
import json


# 目标url
url = "https://mp.weixin.qq.com/cgi-bin/appmsg"

# 使用Cookie，跳过登陆操作

headers = {
  "Cookie": "bizuin=3878837828; Path=/; Expires=Mon, 02-Oct-2023 09:02:26 GMT; Secure; HttpOnly; data_bizuin=3878837828; Path=/; Expires=Mon, 02-Oct-2023 09:02:26 GMT; Secure; HttpOnly; data_ticket=K//9es21FFV/J4hJcL6OtLo5StjRCp097EPRixyxvWD3tkkD1G9MEwWMP5d84CW4; Path=/; Expires=Mon, 02-Oct-2023 09:02:26 GMT; Secure; HttpOnly; rand_info=CAESIAcspiEY5ghy0PAZkGEKWuDufemOVvn3vnXFESkYp43V; Path=/; Expires=Mon, 02-Oct-2023 09:02:26 GMT; Secure; HttpOnly; slave_bizuin=3878837828; Path=/; Expires=Mon, 02-Oct-2023 09:02:26 GMT; Secure; HttpOnly; slave_sid=V0F5SlJiMFN6cWtIR3hOSDBIN1B6c3NoZVBXeXdPb2RwQVZDZWU4Mjg5UjRVWGVNX3ZJSldRWG5yNkpUS1Jha1J1d1BHSExkQTVReVJFQlFIQ2tMVVJTUkJQOU5PYklHMFBVYWxfVGxlemNqbklydmVVQTFhMFBjTFZwdGJKOVpTS0NabHUzV0JlUVBQOWl2; Path=/; Expires=Mon, 02-Oct-2023 09:02:26 GMT; Secure; HttpOnly; slave_user=gh_1d23d0b9153a; Path=/; Expires=Mon, 02-Oct-2023 09:02:26 GMT; Secure; HttpOnly",
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
}

"""
需要提交的data
以下个别字段是否一定需要还未验证。
注意修改yourtoken,number
number表示从第number页开始爬取，为5的倍数，从0开始。如0、5、10……
token可以使用Chrome自带的工具进行获取
fakeid是公众号独一无二的一个id，等同于后面的__biz
"""
data = {
    "token": "yourtoken",
    "lang": "zh_CN",
    "f": "json",
    "ajax": "1",
    "action": "list_ex",
    "begin": "0",
    "count": "5",
    "query": "",
    "fakeid": "QbitAI",
    "type": "9",
}

# 使用get方法进行提交
content_json = requests.get(url, headers=headers, params=data).json()
# 返回了一个json，里面是每一页的数据
for item in content_json["app_msg_list"]:
    # 提取每页文章的标题及对应的url
    print(item)