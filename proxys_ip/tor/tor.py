# -*- coding: utf-8 -*-
# @Author: Hobo
# @Date:   2017-11-27 09:51:13
# @Last Modified by:   Hobo
# @Last Modified time: 2017-11-27 10:20:22

import socket
import socks
import requests

# *这里的端口根据自己的设置
socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9150)
socket.socket = socks.socksocket
# http://ifconfig.me/ip | http://www.httpbin.org/ip
print(requests.get('http://ifconfig.me/ip').text)
print(requests.get('http://www.httpbin.org/ip').text)