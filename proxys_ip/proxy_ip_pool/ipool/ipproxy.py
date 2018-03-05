# -*- coding: utf-8 -*-
# @Author: koosuf
# @Date:   2017-12-13 20:56:13
# @Last Modified by:   koosuf
# @Last Modified time: 2018-03-04 21:34:45
import time
import schedule
import requests
import telnetlib
from config import *
from gevent import monkey
from gevent.pool import Pool
from gevent.queue import Queue
from requests.adapters import HTTPAdapter
monkey.patch_all()


class Proxyser(object):
    """docstring for Proxy"""

    def __init__(self):
        super(Proxyser, self).__init__()
        self.proxys = set()
        self.async_num = 5
        self.proxies = []
        self.url_funcs = {}
        self.pool = Pool(5)
        self.inputQ = Queue()
        self.outputQ = Queue()
        self.config = config
        self.session = requests.session()

    def tasks(self, func, *t):
        self.pool.spawn(func, *t)

    def register(self, api):
        '''
        注册解析函数
        :param:url 抓取的目标网址
        :param:func 解析函数
        :param:proxy 获取ip代理网站代理
        :retrun 无
        '''
        num = api.get('iter_n', 0)
        if num:
            for n in range(num[0], num[1]):
                url = api.get('url').format(iter_n=n)
                self.url_funcs[url] = api
        else:
            url = api.get('url')
            self.url_funcs[url] = api

    def getContent(self, url):
        header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36'
            '(KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
        }
        self.session.mount('http://', HTTPAdapter(max_retries=3))
        resp = self.session.get(url, proxies=self.url_funcs[url].get(
            'proxy', {}), headers=header, timeout=8)
        if resp.status_code == 200:
            # 利用requests 自带的编码检查模块检测编码
            resp.encoding = None
            ips, ports, protos = self.url_funcs[resp.url]['func'](resp.text)
            self.inputQ.put_nowait(
                {'ips': ips, 'ports': ports, 'protos': protos})
        time.sleep(self.url_funcs[url].get('sleep', 0))

    def check_config(self):
        '''检查配置'''
        if not self.config['parsingApis']:
            print("[!]请注册解析配置PS:config.py中)！！！")
            exit(-1)
        for api in self.config['parsingApis']:
            self.register(api)
        self.goai_url = config.get('check_url', "")
        self.goai_word = config.get('check_word', "")
        self.async_num = self.config.get('async_num')
        self.up_data = self.config.get('insert')
        self.up_time = self.config.get('updata_time')

    def check_proxy(self, ip, port, proto):
        '''验证代理'''
        try:
            telnetlib.Telnet(ip, port=port, timeout=20)
            start = time.time()
            resp = requests.get(url=self.goai_url, proxies={
                                '{proto}': '{proto}://{ip}:{port}'.format(proto=proto, ip=ip, port=port)}, timeout=20)
            resp.encoding = None
            resp.raise_for_status()
            assert self.goai_word in resp.text, "不包含关键字"
            t = time.time() - start
        except Exception as msg:
            print("[x]connect failed- proxy={proto}': '{proto}://{ip}:{port} speed={t}".format(
                proto=proto, ip=ip, port=port, t=0), str(msg))
        else:
            print("[v]connect success proxy={proto}': '{proto}://{ip}:{port} speed={t}".format(
                proto=proto, ip=ip, port=port, t=t))
            self.proxys.add((ip, port, proto))
            self.outputQ.put_nowait(
                {'ip': ip, 'port': port, 'proto': proto, 'time': t})

    def insert_api(self):
        ips = []
        ports = []
        protos = []
        times = []
        while not self.outputQ.empty():
            proxy = self.outputQ.get()
            ips.append(proxy.get('ip'))
            ports.append(proxy.get('port'))
            protos.append(proxy.get('proto'))
            times.append(proxy.get('time'))
        self.up_data(ips, ports, protos, times)

    def updata_time(self, func):
        '''
        更新频率设置
        :param:func  需要定时运行的函数
        :param:time_m time_m分钟后 运行函数
        '''
        # sleep_m分钟获取一批新IP
        schedule.every(self.up_time).minutes.do(func)
        while True:
            schedule.run_pending()
            # 这里可以添加测试代理代码
            merge = sorted(list(self.proxys), key=lambda x: x[-1])
            for index, (ip, port, proto) in enumerate(merge):
                self.tasks(self.check_proxy, ip, port, proto)
            if self.pool.join():
                self.insert_api()
            time.sleep(180)

    def run(self):
        self.proxys.clear()
        self.check_config()
        # 这里一定要注意，协程池没有满是不执行的，有时候需要动态调整
        self.pool = Pool(len(self.url_funcs) - 1)
        [self.tasks(self.getContent, url)for url in self.url_funcs.keys()]
        self.pool.join()
        while True:
            if not self.inputQ.empty():
                proxys = self.inputQ.get()
                ips = proxys.get('ips')
                ports = proxys.get('ports')
                protos = proxys.get('protos')
                self.pool = Pool(self.async_num)
                for ip, port, proto in zip(ips, ports, protos):
                    self.tasks(self.check_proxy, ip, port, proto.lower())
            elif self.pool.join():
                self.insert_api()
                return
            else:
                continue
        self.shutdown()

    def shutdown(self):
        self.pool.kill()


if __name__ == '__main__':
    proxyer = Proxyser()
    proxyer.run()
    proxyer.updata_time(proxyer.run)
