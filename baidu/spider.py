import json
import os
from urllib.parse import urlencode
import pymongo
import requests
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError
import re
from multiprocessing import Pool
from hashlib import md5
from json.decoder import JSONDecodeError
from config import *
import TEST

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
}
client = pymongo.MongoClient(MONGO_URL, connect=False)
db = client[MONGO_DB]


def get_page_index(offset, keyword):
    add_key1 = str(hex(offset // 16))[2:]
    add_key2 = str(hex((offset % 16)))[2:]
    add_key = add_key1 + add_key2
    data = {
                'tn': 'resultjson_com',
                'ipn': 'rj',
                'ct': '201326592',
                'is': '',
                'fp': 'result',
                'queryWord': keyword,
                'cl': 2,
                'lm': -1,
                'ie': 'utf-8',
                'oe': 'utf-8',
                'adpicid': '',
                'st': -1,
                'z': '',
                'ic': '',
                'word': keyword,
                's': '',
                'se': '',
                'tab': '',
                'width': '',
                'height': '',
                'face': '',
                'istype': '',
                'qc': '',
                'nc': 1,
                'fr': '',
                'pn': offset,
                'rn': 30,
                'gsm': add_key,
                #'1521624543479': ''
    }
    params = urlencode(data)
    base = 'http://image.baidu.com/search/acjson'
    url = base + '?' + params
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        print('Error occurred')
        return None


def download_image(url):
    print('Downloading', url)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            save_image(response.content)
        return None
    except ConnectionError:
        return None


def save_image(content):
    file_name = "{0}.jpg".format(md5(content).hexdigest())
    file_path = os.path.join(os.getcwd(), KEYWORD, file_name)
    print(file_path)
    if not os.path.exists(file_path):
        try:
            with open(file_path, 'wb') as f:
                f.write(content)
                f.close()
        except Exception as a:
            print(a)


def parse_page_index(text):
    try:
        data = json.loads(text)
        if data and 'data' in data.keys():
            for item in data.get('data'):
                yield item.get('objURL')
    except JSONDecodeError:
        pass


def get_page_detail(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # print(response.text)
            return response.text
        return None
    except ConnectionError:
        print('Error occurred')
        return None


def parse_page_detail(html, url):
    soup = BeautifulSoup(html, 'lxml')
    result = soup.select('title')
    title = result[0].get_text() if result else ''
    images_pattern = re.compile('gallery: JSON.parse\("(.*?)"\)', re.S)
    result = re.search(images_pattern, html)
    if result:
        try:
            data = json.loads(result.group(1).replace('\\', ''))
            if data and 'sub_images' in data.keys():
                sub_images = data.get('sub_images')
                images = [item.get('url') for item in sub_images]
                for image in images:
                    download_image(image)
                return {
                    'title': title,
                    'url': url,
                    'images': images
                }
        except JSONDecodeError:
            pass


def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print('Successfully Saved to Mongo', result)
        return True
    return False


def main(offset):
    html = get_page_index(offset, KEYWORD)
    for url in parse_page_index(html):
        try:
            real_url = TEST.decode(url)
            download_image(real_url)
        except AttributeError:
            pass


if __name__ == '__main__':
    pool = Pool()
    groups = ([x * 30 for x in range(GROUP_START, GROUP_END + 1)])
    pool.map(main, groups)
    pool.close()
    pool.join()
