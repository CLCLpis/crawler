import requests
PROXY_POOL_URL = 'http://127.0.0.1:5000/get'
KEYWORD = '风景'
MONGO_URI = 'localhost'
MONGO_DB = 'weixin'
MAX_COUNT = 5


def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None