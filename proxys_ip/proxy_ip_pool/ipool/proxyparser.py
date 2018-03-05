# -*- coding: utf-8 -*-
# @Author: Hobo
# @Date:   2017-12-14 13:05:08
# @Last Modified by:   koosuf
# @Last Modified time: 2018-03-04 23:10:01
import re
import time
import requests
from lxml import etree

'''
---------------内置解析代理iP网站API待选---------------------------
'''


def spider_proxy_0(content):
    '''
    代理网站解析接口
    http://www.xicidaili.com/nn/
    '''
    ips = etree.HTML(content).xpath(
        '//table[contains(@id,"ip_list")]/tr/td[2]/text()')
    ports = etree.HTML(content).xpath(
        '//table[contains(@id,"ip_list")]/tr/td[3]/text()')
    protos = etree.HTML(content).xpath(
        '//table[contains(@id,"ip_list")]/tr/td[6]/text()')
    return ips, ports, protos


def spider_proxy_1(content):
    '''
    http://cn-proxy.com/
    墙外才能获取
    墙外代理,在需要使用的时候使用
    proxy_urls = {'hppt': 'http://127.0.0.1:4411'}
    '''
    ips = etree.HTML(content).xpath(
        '//table[contains(@class,"sortable")]/tbody/tr/td[1]/text()')
    ports = etree.HTML(content).xpath(
        '//table[contains(@class,"sortable")]/tbody/tr//td[2]/text()')
    protos = ['http'] * len(ips)
    return ips, ports, protos


def spider_proxy_2(content):
    '''
    https://www.free-proxy-list.net/
    墙外才能获取
    墙外代理,在需要使用的时候使用
    proxy_urls = {'hppt': 'http://127.0.0.1:4411'}
    '''
    protos = []
    ips = etree.HTML(content).xpath(
        '//*[@id="proxylisttable"]/tbody/tr/td[1]/text()')
    ports = etree.HTML(content).xpath(
        '//*[@id="proxylisttable"]/tbody/tr/td[2]/text()')
    flags = etree.HTML(content).xpath(
        '//*[@id="proxylisttable"]/tbody/tr/td[7]/text()')
    for flag in flags:
        if flag == "yes":
            protos.append("https")
        elif flag == "no":
            protos.append("http")
    return ips, ports, protos


def spider_proxy_3(content):
    '''
    http://www.gatherproxy.com/zh/
    '''
    ips = re.findall(r'"PROXY_IP":"(.*?)"', content, re.S)
    ports = re.findall(r'"PROXY_PORT":"(.*?)"', content, re.S)
    portss = [int(port, 16) for port in ports]
    protos = ['http'] * len(ips)
    return ips, portss, protos


def spider_proxy_4(content):
    '''https://www.nyloner.cn/proxy'''
    import json
    import base64
    import hashlib
    ips = []
    ports = []
    header = {
        'DNT': '1',
        'Host': 'www.nyloner.cn',
        'Referer': 'https://www.nyloner.cn/proxy',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
    }
    page = 0
    limitnum = 15
    while True:
        try:
            page += 1
            timestamp = int(time.time())
            token = str(page) + str(limitnum) + str(timestamp)
            token = hashlib.md5(token.encode()).hexdigest()
            url = "https://www.nyloner.cn/proxy?page={page}&num={num}&token={token}&t={t}".format(
                page=page, num=limitnum, token=token, t=timestamp)
            data = requests.get(url, headers=header, timeout=20).text
            lists = json.loads(data).get('list')
            scHZjLUh1 = base64.decodestring(lists.encode('utf-8'))
            assert len(lists) > 10, "结束！！！"
            key = b'nyloner'
            lenth = len(key)
            schlenth = len(scHZjLUh1)
            code = ''
            for i in range(schlenth):
                coeFYlqUm2 = i % lenth
                code += chr(scHZjLUh1[i] ^ key[coeFYlqUm2])

            code = base64.decodestring(code.encode())
            iplists = eval(code.decode())
            for iplist in iplists:
                ips.append(iplist.get('ip'))
                ports.append(iplist.get('port'))
            time.sleep(2)

        except:
            protos = ['http'] * len(ips)
            return ips, ports, protos


def spider_proxy_5(content):
    '''失效'''
    '''http://www.goubanjia.com/free/index1.shtml'''
    ips = []
    ports = []
    protos = []
    header = {
        'DNT': '1',
        'Host': 'www.goubanjia.com',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://www.goubanjia.com/free/index1.shtml',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
    }
    page = 0
    while True:
        try:
            flag = 0
            page += 1
            url = 'http://www.goubanjia.com/free/index{page}.shtml'.format(
                page=page)
            data = requests.get(url, headers=header, timeout=20).text
            # 遍历子节点
            tbodys = etree.HTML(data).xpath('//tbody')[0]
            for sub in tbodys.iterchildren():
                flag += 1
                iplist = sub.xpath(
                    './td[1]/div[@style]/text() | ./td[1]/span[@style]/text() | ./td[1]/span/text()')[:-1]
                ips.append(''.join(iplist))
                portstr = sub.xpath(
                    './td[1]/span[contains(@class,"port")]/@class')[0]  # ['port GEGEA']
                proto = sub.xpath('./td[3]/a/@title')[0]
                proto = re.findall(r"(https?)|(socks5)", proto)[0]
                protos.append(''.join(proto))
                # 有加密
                num_list = []
                for item in portstr:
                    num = 'ABCDEFGHIZ'.find(item)
                    if num >= 0:
                        num_list.append(str(num))
                port = int("".join(num_list)) >> 0x3
                ports.append(str(port))
            if flag < 15:
                # [print(ip+':'+port+'\n') for ip,port in zip(protos,ips,ports)]
                return ips, ports, protos
            time.sleep(1)
        except Exception as msg:
            print(msg)
            pass


def spider_proxy_6(content):
    '''
    http://www.freeproxylists.net/zh/?c=&pt=&pr=&a%5B%5D=0&a%5B%5D=1&a%5B%5D=2&u=80
    有点难度
    '''
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'Host': 'www.freeproxylists.net',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 Firefox/50.0',
    }
    url = "http://www.freeproxylists.net/zh/?c=&pt=&pr=&a[]=0&a[]=1&a[]=2&u=80"
    data = requests.get(url, headers=header, timeout=20).text
    print(data)
    pass


def nmap(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
    }
    html = ''
    try:
        html = requests.get(url, timeout=80, headers=headers)
        html = html.headers['server']
    except Exception as msg:
        print(msg)
    f = open('./proxyanalysis.txt', 'a')
    print(url, html, file=f)

if __name__ == '__main__':
    # 测试
    # spider_proxy_4(0)
    # spider_proxy_6(0)
    url = 'http://35.199.20.177:80'
    nmap(url)
    print("完成")
