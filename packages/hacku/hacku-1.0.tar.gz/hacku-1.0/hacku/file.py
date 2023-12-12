# coding=utf-8

import hashlib
import os


def file_md5_hash(file_path: str) -> str:
    if not os.path.isfile(file_path):
        print('文件不存在。')
        return ''
    h = hashlib.md5()
    with open(file_path, 'rb') as f:
        b = f.read(8192)
        while b:
            h.update(b)
    return h.hexdigest()
