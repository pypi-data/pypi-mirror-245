# coding=utf-8

import random
import socket
import struct


def gen_random_ip(rand_list):
    """
    从指定的CIDR地址段内随机生成IP
    @rand_list: [xx.xx.xx.xx/x]
    """
    str_ip = rand_list[random.randint(0, len(rand_list) - 1)]
    str_ip_addr = str_ip.split('/')[0]
    str_ip_mask = str_ip.split('/')[1]
    ip_addr = struct.unpack('>I', socket.inet_aton(str_ip_addr))[0]
    mask = 0x0
    for i in range(31, 31 - int(str_ip_mask), -1):
        mask = mask | (1 << i)
    ip_addr_min = ip_addr & (mask & 0xffffffff)
    ip_addr_max = ip_addr | (~mask & 0xffffffff)
    return socket.inet_ntoa(struct.pack('>I', random.randint(ip_addr_min, ip_addr_max)))


def is_valid_ip(ip):
    try:
        # 尝试将 IP 地址转换为二进制格式
        socket.inet_aton(ip)
        return True
    except:
        # 转换失败说明 IP 地址不合法
        return False
