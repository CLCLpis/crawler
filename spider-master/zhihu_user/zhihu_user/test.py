#!/usr/bin/env python
# encoding: utf-8
"""
@version: 1.0
@author: Pis
@license: Apache Licence 
@software: PyCharm
@file: test.py
@time: 2018/3/25 22:28
"""
start_user = "excited-vczh"
user_query = "allow_message, is_followed, is_following, is_org, is_blocking, employments, answer_count, follower_count, articles_count, gender,badge[?(type=best_answerer)].topics"


# 这里把查询的参数单独存储为user_query,user_url存储的为查询用户信息的url地址
user_url = "https://www.zhihu.com/api/v4/members/{user}?include={include}"

print(user_url.format(user=start_user, include=user_query))
