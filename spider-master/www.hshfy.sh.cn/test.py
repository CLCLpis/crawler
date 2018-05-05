#!/usr/bin/env python
# encoding: utf-8
import datetime
import time
import requests
"""
@version: 1.0
@author: Pis
@license: Apache Licence 
@software: PyCharm
@file: test.py
@time: 2018/3/27 19:42
"""

def get_html(url,data):
    '''
    :param url:请求的url地址
    :param data: 请求的参数
    :return: 返回网页的源码html
    '''
    response = requests.get(url,data)
    return response.text


base_url = "http://www.hshfy.sh.cn/shfy/gweb/ktgg_search_content.jsp?"
date_time = datetime.date.fromtimestamp(time.time())
print(date_time)
data = {
    "pktrqks": str(date_time),
    "ktrqjs": str(date_time),
}
print(data)
html = get_html(base_url, data)
print(html)
