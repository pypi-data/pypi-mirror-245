# coding=utf-8

from urllib.parse import quote

import requests
from bs4 import BeautifulSoup
from loguru import logger

from hacku import UA


def get_url_from_search(query, proxy_url):
    proxies = {
        'http': proxy_url,
        'https': proxy_url
    }
    # 爬取网页html源码
    query = query.replace(' ', '+')
    url = 'https://google.com/search?q={q}&num=100'.format(q=quote(query, safe="+"))
    logger.info(url)
    response = requests.get(url, headers={"User-Agent": UA.get_random_user_agent()}, proxies=proxies)
    results = []
    if response.status_code == 200:
        # 使用BeautifulSoup解析html对象，并使用正则表达式查找目标内容
        html = BeautifulSoup(response.text, 'html.parser')
        for item in html.find_all('a'):
            s = item.get('href')
            if '/url?q=' not in s or '.google.' in s:
                continue
            u = s.split('/url?q=')[1].split('&sa=')[0]
            results.append(u)
    else:
        logger.error('Request Failed!')
    return results
