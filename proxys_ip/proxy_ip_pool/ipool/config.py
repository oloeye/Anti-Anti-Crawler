# -*- coding: utf-8 -*-
# @Author: Hobo
# @Date:   2017-12-14 11:55:14
# @Last Modified by:   koosuf
# @Last Modified time: 2018-03-04 23:05:59

from proxyparser import *
from insertapi import *


# 这里添加自己的适配配置
config = {
    'async_num': 80,       # 协程池数
    'updata_time': 20,     # 20分钟后更新并在这个时间段进行也抓取的账号循环验证
    'insert': update_sq,   # 存储代理的接口
    'check_url': 'http://www.baidu.com/',  # 测试的网站地址
    'check_word': '百度',  # 判断代理是否可用测试网站的关键字
    'parsingApis': [
        {
            'iter_n': [1, 3],
            'url': 'http://www.xicidaili.com/nn/{iter_n}',  # proxy 网站
            'func': spider_proxy_0,                     # 解析接口函数
            # 代理爬取或者是需要翻墙
            'proxy': {'http': 'http://127.0.0.1:10582', 'https': 'https://127.0.0.1:10582'},
            'sleep': 3                                  # 防止被禁 不设置为不等待
        },
        {
            'url': 'http://cn-proxy.com/',
            'func': spider_proxy_1,
            'proxy': {'http': 'http://127.0.0.1:10582', 'https': 'https://127.0.0.1:10582'},
            'sleep': 1
        },
        {
            'url': 'https://www.free-proxy-list.net/',
            'func': spider_proxy_2,
            'proxy': {'http': 'http://127.0.0.1:10582', 'https': 'https://127.0.0.1:10582'},
            'sleep': 1
        },
        {
            'url': 'http://www.gatherproxy.com/zh/',
            'func': spider_proxy_3,
        },
        {
            'url': 'https://www.nyloner.cn/proxy',
            'func': spider_proxy_4,
        },
        # {
        #     'url': 'http://www.goubanjia.com/free/index1.shtml',
        #     'func': spider_proxy_5,
        #     'proxy': {'http': 'http://127.0.0.1:10582', 'https': 'https://127.0.0.1:10582'},
        # }
    ]

}
