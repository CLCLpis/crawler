from urllib.parse import urlencode
import pymongo
import requests
from lxml.etree import XMLSyntaxError
from requests.exceptions import ConnectionError
from pyquery import PyQuery as pq
from config import *

client = pymongo.MongoClient(MONGO_URI)
db = client[MONGO_DB]

base_url = 'http://weixin.sogou.com/weixin?'

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'ABTEST=0|1521815375|v1; IPLOC=CN4201; SUID=895524774A42910A000000005AB50F4F; SUID=895524773020910A000000005AB50F4F; SUV=00810B84772455895AB50F4FFDEE4538; weixinIndexVisited=1; SUIR=78A4D586F2F499E4B1298B4AF21708CF; ppinf=5|1521818327|1523027927|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTo4OkRyYWdvbnplfGNydDoxMDoxNTIxODE4MzI3fHJlZm5pY2s6ODpEcmFnb256ZXx1c2VyaWQ6NDQ6bzl0Mmx1TC10VlVlMjhzVllRVnFwQ3V6N1p1VUB3ZWl4aW4uc29odS5jb218; pprdig=kweZlnuE-ShwTws9lJKbcDYI2rma0xPGmLRp8fRXSknb6mkgHB02HIvRXZ3x6tjeUV_dO3BoRst2o5opRsXeVygIVuCsMLj0eJNg228fHNzj_OZKRd1oW75DLvI2QAnesYe5PXNuT6K9ssQlFZbkqy9YQntwBveG3bGv7284heY; sgid=24-34182383-AVq1GtdYo9gicTqr1MAT0WJc; SNUID=EC31401264610C73225C254C650B9116; ppmdig=152185808200000022bb0b7c1cd64c402af1daaa748cbe3f; sct=4; JSESSIONID=aaa02yn6ysdUq7GhzEOiw',
    'Host': 'weixin.sogou.com',
    'Referer': 'http://weixin.sogou.com/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36',
}


proxy = ''
my_count = 0


def get_html(url, count=1):
    print('Crawling', url)
    print('Trying Count', count)
    global proxy
    global my_count
    if count >= MAX_COUNT:
        print('Tried Too Many Counts')
        return None
    try:
        if proxy:

            proxies = {
                'http': 'http://' + proxy
            }
            print('crawler with header: ' + proxy)
            response = requests.get(url, allow_redirects=False, headers=headers, proxies=proxies)
        else:
            response = requests.get(url, allow_redirects=False, headers=headers)
        print(response.status_code)
        if response.status_code == 200:
            my_count += 1
            if my_count >= 10:
                proxy = get_proxy()
                my_count = 0
            print('my_count: ' + str(my_count))
            return response.text
        if response.status_code == 302:
            # Need Proxy
            print('302')
            proxy = get_proxy()
            if proxy:
                print('Using Proxy', proxy)
                return get_html(url)
            else:
                print('Get Proxy Failed')
                return None
    except ConnectionError as e:
        print('Error Occurred', e.args)
        proxy = get_proxy()
        count += 1
        return get_html(url, count)


def get_index(keyword, page):
    data = {
        'query': keyword,
        'type': 2,
        'page': page
    }
    queries = urlencode(data)
    url = base_url + queries
    html = get_html(url)
    return html


def parse_index(html):
    doc = pq(html)
    items = doc('.news-box .news-list li .txt-box h3 a').items()
    for item in items:
        yield item.attr('href')


def get_detail(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None


def parse_detail(html):
    try:
        doc = pq(html)
        title = doc('.rich_media_title').text()
        content = doc('.rich_media_content').text()
        date = doc('#post-date').text()
        nickname = doc('#js_profile_qrcode > div > strong').text()
        wechat = doc('#js_profile_qrcode > div > p:nth-child(3) > span').text()
        return {
            'title': title,
            'content': content,
            'date': date,
            'nickname': nickname,
            'wechat': wechat
        }
    except XMLSyntaxError:
        return None


def save_to_mongo(data):
    if db['articles'].update_one({'title': data['title']}, {'$set': data}, True):
        print('Saved to Mongo', data['title'])
    else:
        print('Saved to Mongo Failed', data['title'])


def main():
    for page in range(1, 101):
        html = get_index(KEYWORD, page)
        if html:
            article_urls = parse_index(html)
            for article_url in article_urls:
                article_html = get_detail(article_url)
                if article_html:
                    article_data = parse_detail(article_html)
                    print(article_data)
                    if article_data:
                        save_to_mongo(article_data)


if __name__ == '__main__':
    main()
