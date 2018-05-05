#!/usr/bin/env python
# encoding: utf-8
"""
@version: 1.0
@author: Pis
@license: Apache Licence 
@software: PyCharm
@file: TEST.py
@time: 2018/3/21 19:04
"""
from urllib.parse import unquote
from config import *

str_table = {
    '_z2C$q': ':',
    '_z&e3B': '.',
    'AzdH3F': '/'
}

char_table = {
    'w': 'a',
    'k': 'b',
    'v': 'c',
    '1': 'd',
    'j': 'e',
    'u': 'f',
    '2': 'g',
    'i': 'h',
    't': 'i',
    '3': 'j',
    'h': 'k',
    's': 'l',
    '4': 'm',
    'g': 'n',
    '5': 'o',
    'r': 'p',
    'q': 'q',
    '6': 'r',
    'f': 's',
    'p': 't',
    '7': 'u',
    'e': 'v',
    'o': 'w',
    '8': '1',
    'd': '2',
    'n': '3',
    '9': '4',
    'c': '5',
    'm': '6',
    '0': '7',
    'b': '8',
    'l': '9',
    'a': '0'
}

# str 的translate方法需要用单个字符的十进制unicode编码作为key
# value 中的数字会被当成十进制unicode编码转换成字符
# 也可以直接用字符串作为value
char_table = {ord(key): ord(value) for key, value in char_table.items()}
# 解码图片URL


def decode(url):
    # 先替换字符串
    for key, value in str_table.items():
        url = url.replace(key, value)
    # 再替换剩下的字符
    return url.translate(char_table)


if __name__ == '__main__':
    # url = "ippr_z2C$qAzdH3FAzdH3Ft42c_z&e3B17tpwg2_z&e3Bv54AzdH3F7rs5w1fAzdH3Ftpj4AzdH3Fda8nadAzdH3F80AzdH3Fda8nad8080dnan_F1Xvy_z&e3Bpi74k_z&e3B0aa_a_z&e3B3rj2"
    # print(decode(url))
    offset = 270
    add_key1 = str(hex(offset // 16))[2:]
    add_key2 = str(hex((offset % 16)))[2:]
    add_key = add_key1 + add_key2
    print(add_key)
    groups = ([x * 30 for x in range(GROUP_START, GROUP_END + 1)])
    for i in groups:
        print(i)
