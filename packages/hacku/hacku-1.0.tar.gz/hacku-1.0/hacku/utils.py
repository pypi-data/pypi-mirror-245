# coding=utf-8

import time

import requests
from loguru import logger

from hacku import UA


def datetime2int(time_str, fmt='%Y-%m-%d %H:%M:%S') -> int:
    try:
        if time_str:
            return int(time.mktime(time.strptime(time_str, fmt)))
    except Exception as e:
        logger.error(e)
    return 0


def parse_json_path(json_obj: dict, json_path: str):
    """
    用json path的语法从json字符串中提取数据
    :param json_obj:
    :param json_path:
    :return:
    """
    try:
        key_list = json_path.split('.')
        for k in key_list:
            if isinstance(json_obj, dict):
                json_obj = json_obj.get(k, '')
            elif isinstance(json_obj, list):
                json_obj = json_obj[int(k)]
        return json_obj
    except Exception as e:
        logger.error(e)
        return None


def query_es_by_sql(es_url, auth, sql, proxy_url) -> list:
    """

    :param es_url: ES服务器地址，格式：http://xx.xx.xx.xx:9200
    :param auth: 认证参数，格式：（username, password)
    :param sql:
    :param proxy_url:
    :return:
    """
    try:
        proxies = {
            'http': proxy_url,
            'https': proxy_url
        }
        body = {
            "query": sql
        }
        header = {
            'User-Agent': UA.get_random_user_agent()
        }
        r = requests.post(f"{es_url}/_sql?format=json", headers=header, json=body, proxies=proxies, auth=auth).json()
        return r['rows']
    except Exception as e:
        logger.opt(exception=True).error(e)

    return []


def has_chinese(strs) -> bool:
    """
    是否包含中文字符
    :param strs:
    :return:
    """
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False
