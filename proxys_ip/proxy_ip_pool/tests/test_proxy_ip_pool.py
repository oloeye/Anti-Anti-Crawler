# -*- coding: utf-8 -*-
# @Author: Hobo
# @Date:   2017-11-01 15:03:35
# @Last Modified by:   Hobo
# @Last Modified time: 2018-01-19 17:24:05


import sys
import datetime
import unittest

from lxml import etree
from ipool.IPPool import getProxys


class Proxy_test(unittest.TestCase):
    '''
    测试类
    '''

    def setUp(self):
        print(self.get_head_info())

    def tearDown(self):
        print(self.get_head_info())

    def get_head_info(self):
        try:
            raise Exception
        except:
            f = sys.exc_info()[2].tb_frame.f_back
        return '%s, %s, %s, %s, ' % (str(datetime.time()), f.f_code.co_filename, f.f_code.co_name, str(f.f_lineno))

    def test_init(self):
        # 数据库是本地保存路径
        getProxys("proxy.db")

    def test_addapi(self):
        # 添加解析接口(内置一个解析api)
        obj = getProxys("proxy.db")
        obj.load_func("http://www.xicidaili.com/nn/", spider_proxy_0)
        obj.load_func("https://www.free-proxy-list.net/", spider_proxy_2)

    def test_updatedb(self):
        # 获取数据更新数据库并检测数据库里面的代理ip
        obj = getProxys("proxy.db")
        obj.update_db()

    def test_getip(self):
        # 提取数据库里面的代理ip数据，num代表获取代理ip个数 test_urls满足目标网址测试列表
        obj = getProxys("proxy.db")
        ip, port, Proxies = obj.getProxyIP(
            num=10, test_urls=["http://www.baidu.com"])
        self.assertEqual(len(Proxies), 10)

    def test_isalive(self):
        # 检测代理IP的有效性
        obj = getProxys("proxy.db")
        flage = obj.isAlive("22.18.42.2", "90")
        self.assertEqual(flage, True)


def spider_proxy_0(content):
    '''
    http://www.xicidaili.com/nn/
    代理网站解析接口
    '''
    ip = etree.HTML(content).xpath(
        '//table[contains(@id,"ip_list")]/tr/td[2]/text()')
    port = etree.HTML(content).xpath(
        '//table[contains(@id,"ip_list")]/tr/td[3]/text()')
    return ip, port


def spider_proxy_2(content):
    '''
    代理网站解析接口
    https://www.free-proxy-list.net/
    '''
    ip = etree.HTML(content).xpath(
        '//*[@id="proxylisttable"]/tbody/tr[1]/td[1]/text()')
    port = etree.HTML(content).xpath(
        '//*[@id="proxylisttable"]/tbody/tr[1]/td[2]/text()')
    return ip, port

if __name__ == '__main__':
    unittest.main()
