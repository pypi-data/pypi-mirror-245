# coding=utf-8
import csv
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


def save_json_to_csv(json_data, csv_file):
    # 打开CSV文件并创建写入器
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        # 遍历JSON数据的每个对象
        for obj in json_data:
            # 提取对象的键作为CSV文件的标题行
            headers = list(obj.keys())
            # 写入标题行
            writer.writerow(headers)
            # 写入数据行
            writer.writerow(obj.values())
