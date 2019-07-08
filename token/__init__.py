#_*_coding:utf-8_*_
# Author       : ToughLama@gmail.com
# Created      : 2019-06-28 15:39
# Filename     : __init__.py.py
# IDE          : PyCharm


import requests
from requests import exceptions
import json
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)


class ZabbixException(Exception):
    pass

class Zabbix(object):

   __options = {
        'zabbix_url': 'protocol://(zabbix server ipaddress)',
        'zabbix_username': '(zabbix auth username)',
        'zabbix_password': '(zabbix auth passowrd'
    }
   __client = None
   def __init__(self, **kwargs):
        if len(kwargs) != 3:
            raise ZabbixException('You must specify a zabbix_url, zabbix_username, zabbix_password as keyword arguments')
        else:
            if 'zabbix_url' in kwargs.keys():
                self.__zabbix_url = kwargs['zabbix_url'] + '/api_jsonrpc.php'
            else:
                raise ZabbixException('You need to specify a zabbix_url as keyword argument')
            if 'zabbix_username' in kwargs.keys():
                self.__zabbix_username = kwargs['zabbix_username']
            else:
                raise ZabbixException('You need to specify a zabbix_username as keyword argument')
            if 'zabbix_password' in kwargs.keys():
                self.__zabbix_password = kwargs['zabbix_password']
            else:
                raise ZabbixException('You need to specify a zabbix_password as keyword argument')
            self.__auth_body = {
                    "jsonrpc": "2.0",
                    "method": "user.login",
                    "params": {
                        "user": self.__zabbix_username,
                        "password": self.__zabbix_password
                    },
                    "id": 1,
                    "auth": None
            }
            self.auth__header = {
                    'Content-Type': 'application/json'
            }
            try:
                self.__client = requests.post(url=self.__zabbix_url, data=json.dumps(self.__auth_body), headers=self.auth__header, timeout=5)
            except (exceptions.HTTPError, exceptions.ConnectionError, exceptions.ConnectTimeout,
                    exceptions.InvalidURL, exceptions.SSLError, exceptions.InvalidProxyURL, exceptions.ProxyError) as e:
                raise ZabbixException('Error: {} occurred, please check'.format(e))

   def get_auth_id(self):
       if 'result' not in  json.loads(self.__client.text):
           raise ZabbixException('Error: {}'.format(json.loads(self.__client.text)['error']['data']))
       else:
           return json.loads(self.__client.text)['result']


# if __name__  == "__main__":
#     url = 'http://10.174.1.10'
#     username = 'Admin'
#     password = 'HUv9oQ82bmZRDWEI'
#     obj = Zabbix(zabbix_url=url, zabbix_username=username, zabbix_password=password)
#     print obj.get_auth_id()


