# tor进行匿名访问

tor实现了代理ip,这种方案有很多缺点，比如访问速度很慢，还有就是代理的ip一般都在500个左右。一般我们使用这种方案爬取少量的网页。

- pip install requesocks
      if is_open('https://github.com/shazow/urllib3/pull/68'):  # ;)
          import requesocks as requests
      else:
          import requests
      
      session = requests.session()
      session.proxies = {'http': 'socks5://127.0.0.1:9050',
                         'https': 'socks5://127.0.0.1:9050'}
      resp = session.get('https://api.github.com', auth=('user', 'pass'))
      print(resp.status_code)
      print(resp.headers['content-type'])
      print(resp.text)
- pip install  PySocks
      import socket
      import socks
      import requests
      
      socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
      socket.socket = socks.socksocket
      print(requests.get('http://ifconfig.me/ip').text)

安装tor

- 有浏览器界面
  [下载地址](https://www.torproject.org/dist/torbrowser/7.0.10/torbrowser-install-7.0.10_en-US.exe) 安装好后，这里这里就可以打开了。要注意你可以翻墙，配置我就不说了，网上很多。

- 无浏览器界面
  [下载地址](https://www.torproject.org/dist/torbrowser/7.0.10/tor-win32-0.3.1.8.zip) 这里就下载了核心部件。但是为了好操作。我们还需要下载一个软件[Vidalia](http://fs2.download82.com/software/bbd8ff9dba17080c0c121804efbd61d5/vidalia/vidalia-bridge-bundle-0.2.4.23-0.2.21.exe) 后安装，使用自行**百度** ，
  注意：今后大伙儿需要用 TOR 提供的 SOCKS 代理来上网，端口号如下：
  **9150**（2.3.25版本之后的 Tor Browser Bundle 软件包）
  **9050**（其它的软件包）

- socks转为http|https代理

  这里我选择了MOEW这款软件，因为我正在使用它，把它可以转为**http|https:prot**