# -*- coding: utf-8 -*-
# @Author: Hobo
# @Date:   2017-12-14 13:46:51
# @Last Modified by:   Hobo
# @Last Modified time: 2018-01-19 17:26:21
import os


def update_sq(ips, ports, protos, times):
    '''
    更新squid代理
    '''
    # Squid的配置文件语法
    post_lines = ['never_direct allow all',
                  'forwarded_for off',
                  'via off',
                  'forwarded_for transparent',
                  'request_header_access Via deny all',
                  'request_header_access X-Forwarded-For deny all',
                  'request_header_access From deny all']
    # 将请求转发到父代理 由于有可能有相同ip，而端口不同的代理会报错 加入no-query 后面的语句
    PEER_CONF = "cache_peer {ip} parent {port} 0 no-query weighted-round-robin weight=1 connect-fail-limit=2 allow-miss max-conn=5 name={name}\n"
    # 输入安装squid的路径squid.conf.original直接备份的文件
    with open('D:/Program Files/Squid/etc/squid/squid.conf.original', 'r', encoding='utf-8') as f:
        squid_conf = f.readlines()
    squid_conf.append('\n#>>>>>>>>Cache peer config<<<<<<<<<<\n')
    for index, ip, port, proto in zip(range(len(ips)), ips, ports, protos):
        name = '{}_{}'.format(index, proto)
        item = PEER_CONF.format(ip=ip, port=port, name=name)
        if proto in ['HTTP', 'http']:
            item += 'cache_peer_access {} deny acl_deny_https\n'.format(name)
        elif proto in ['HTTPS', 'https']:
            item += 'cache_peer_access {} deny acl_deny_http\n'.format(name)
        else:
            continue
        squid_conf.append(item)
    with open('D:/Program Files/Squid/etc/squid/squid.conf', 'w') as f:
        f.writelines(squid_conf)
        f.writelines('\n' + '\n'.join(post_lines) + '\n')
    # 重新加载配置文件,需要管理员运行
    print("重启squid加载配置文件！！！")
    assert os.system('squid -k reconfigure') == 0, 'update fail'


def updata_db_sqllite(ips, ports, protos, times):
    import time
    import sqlite3
    '''
    插入sqllite数据库
    '''
    try:
        conn = sqlite3.connect("./proxys.db")
    except:
        print("Error to open database%" % "proxys.db")
    create_tb = '''
    CREATE TABLE IF NOT EXISTS PROXY
    (DATE TEXT,IP TEXT,PORT TEXT,RUN_TIME time);
    '''
    conn.execute(create_tb)
    for _, ip, port, r_time in zip(range(len(ips)), ips, ports, times):
        insert_db_cmd = '''INSERT INTO PROXY (DATE,IP,PORT) VALUES ('%s','%s','%s');
        ''' % (time.strftime("%Y-%m-%d"), ip, port, r_time)
        conn.execute(insert_db_cmd)
    conn.commit()
    conn.close()
