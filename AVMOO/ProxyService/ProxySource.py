import json
import requests
import time
from bs4 import BeautifulSoup as Soup
import threading
import logging
import random
import re
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                        'AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/64.0.3282.186 Safari/537.36'}


'''
每次提供一百个左右proxy，应用缓存机制
每次网络请求结束后，记录当前时间作为更新时间，
定期开启线程更新proxy，每个源的更新时间不同
'''


class ProxySource(object):
    base_url = ""

    _ips = []

    time_span = 60*30

    def __init__(self):
        self._flag = True  # 线程停止信号
        self._work_thread = threading.Thread(target=self._work, daemon=True)
        self.get_proxies(page_count=4)
        self._work_thread.start()

    @property
    def ips(self):
        return self._ips

    def get_proxies(self, **kwargs):
        res = []
        index = 1
        while len(res) < 100:
            result = self.parse_page(index)
            res.extend(result)
            index += 1
            time.sleep(1)
            if index > 20:
                break
        self._ips = res

    def parse_page(self, index):
        url = self.base_url.format(index)
        results = []
        try:
            res = requests.get(url, headers=header, timeout=1)
        except:
            return []
        soup = Soup(res.text, features='html.parser')
        items = soup.find_all('tr')[1:]
        for item in items:
            tds = item.find_all('td')
            # 从对应位置获取ip，端口，类型
            ip, port, _type = tds[0].text, int(tds[1].text), tds[3].text.lower()
            results.append({'ip': ip, 'port': port, 'type': _type})
        return results

    def _work(self):
        while self._flag:
            time.sleep(self.time_span)
            self.get_proxies(page_count=5)


class KuaiProxySource(ProxySource):
    base_url = "https://www.kuaidaili.com/free/intr/{}"

    def __init__(self):
        ProxySource.__init__(self)

    # def get_proxies(self, **kwargs):
    #     # if "page_count" not in kwargs.keys():
    #     #     raise KeyError("not enough keys")
    #     # page_count = kwargs['page_count']
    #     res = []
    #     index = 1
    #     while len(res) < 100:
    #         url = self.base_url + "/" + str(index)
    #         result = self.parse_page(url)
    #         res.extend(result)
    #         index += 1
    #         time.sleep(1)
    #     self.ips = res

    # def parse_page(self, index):
    #     url = self.base_url + "/" + str(index)
    #     results = []
    #     res = requests.get(url)
    #     soup = Soup(res.text, features='html.parser')
    #     items = soup.find_all('tr')[1:]
    #     for item in items:
    #         tds = item.find_all('td')
    #         # 从对应位置获取ip，端口，类型
    #         ip, port, _type = tds[0].text, int(tds[1].text), tds[3].text.lower()
    #         results.append({'ip': ip, 'port': port, 'type': _type})
    #     return results


class XiciProxySource(ProxySource):
    base_url = "http://www.xicidaili.com"

    genre_options = {
        "高匿": '/nn',
        "普通": '/nt',
        "HTTP": '/wt',
        "HTTPS": '/wn',
    }

    def __init__(self):
        ProxySource.__init__(self)

    def get_proxies(self, **kwargs):
        # if "page_count" not in kwargs.keys() | "genre" not in kwargs.keys():
        #     raise KeyError("not enough keys")
        # page_count = kwargs["page_count"]
        # genre = kwargs["genre"]
        res = []
        index = 1
        while len(res) < 100:
            key = list(self.genre_options.keys())
            key_use = random.choice(key)
            result = self.parse_genre_page(key_use, index)
            res.extend(result)
            index += 1
            if index > 20:
                break
            time.sleep(3)
        self._ips = res

    def parse_page(self, url):
        results = []
        try:
            res = requests.get(url, headers=header, timeout=1)
        except:
            return []
        soup = Soup(res.text, features='html.parser')
        items = soup.find_all('tr')[1:]

        for item in items:
            tds = item.find_all('td')
            # 从对应位置获取ip，端口，类型
            ip, port, _type = tds[1].text, int(tds[2].text), tds[5].text.lower()
            results.append({'ip': ip, 'port': port, 'type': _type})
        return results

    def parse_genre_page(self, genre, index):
        url = self.base_url + self.genre_options[genre] + '/' + str(index)
        results = self.parse_page(url)
        return results


class GlobalProxySource(ProxySource):
    base_url = "https://ip.jiangxianli.com/?page={}"
    # base_url = "https://ip.jiangxianli.com/api/proxy_ip"

    def __init__(self):
        ProxySource.__init__(self)

    # def get_proxies(self, **kwargs):
    #     # if "page_count" not in kwargs.keys():
    #     #     raise KeyError("not enough keys")
    #     # page_count = kwargs["page_count"]
    #     self.ips = []
    #     for i in range(1, page_count+1):
    #         ip = self.parse_page(self.base_url.format(i))
    #         self.ips.extend(ip)
    #         time.sleep(3)
    #     return self.ips

    # def parse_page(self, index):
    #     url = self.base_url.format(index)
    #     results = []
    #     res = requests.get(url, headers=header)
    #     soup = Soup(res.text, features='html.parser')
    #     items = soup.find_all('tr')[1:]
    #     for item in items:
    #         tds = item.find_all('td')
    #         # 从对应位置获取ip，端口，类型
    #         ip, port, _type = tds[0].text, int(tds[1].text), tds[3].text.lower()
    #         results.append({'ip': ip, 'port': port, 'type': _type})
    #     return results


class YunProxySource(ProxySource):
    base_url = "http://www.ip3366.net/?stype=1&page={}"

    def __init__(self):
        ProxySource.__init__(self)

    # def get_proxies(self, **kwargs):
    #     if "page_count" not in kwargs.keys():
    #         raise KeyError("not enough keys")
    #     self.ips = []
    #     page_count = kwargs["page_count"]
    #     for i in range(1, page_count + 1):
    #         ip = self.parse_page(self.base_url.format(i))
    #         self.ips.extend(ip)
    #         time.sleep(3)
    #     return self.ips

    # def parse_page(self, index):
    #     url = self.base_url.format(index)
    #     results = []
    #     res = requests.get(url, headers=header)
    #     soup = Soup(res.text, features='html.parser')
    #     items = soup.find_all('tr')[1:]
    #     for item in items:
    #         tds = item.find_all('td')
    #         # 从对应位置获取ip，端口，类型
    #         ip, port, _type = tds[0].text, int(tds[1].text), tds[3].text.lower()
    #         results.append({'ip': ip, 'port': port, 'type': _type})
    #     return results


class QiYunProxySource(ProxySource):
    base_url = "https://www.7yip.cn/free/?action=china&page={}"

    # def get_proxies(self, **kwargs):
    #     if "page_count" not in kwargs.keys():
    #         raise KeyError("not enough keys")
    #     self.ips = []
    #     page_count = kwargs["page_count"]
    #     for i in range(1, page_count + 1):
    #         ip = self.parse_page(self.base_url.format(i))
    #         self.ips.extend(ip)
    #         time.sleep(3)
    #     return self.ips

    # def parse_page(self, index):
    #     url = self.base_url.format(index)
    #     results = []
    #     res = requests.get(url, headers=header)
    #     soup = Soup(res.text, features='html.parser')
    #     items = soup.find_all('tr')[1:]
    #     for item in items:
    #         tds = item.find_all('td')
    #         # 从对应位置获取ip，端口，类型
    #         ip, port, _type = tds[0].text, int(tds[1].text), tds[3].text.lower()
    #         results.append({'ip': ip, 'port': port, 'type': _type})
    #     return results


class XiaoShuProxySource(ProxySource):
    base_url = "http://www.xsdaili.com"

    time_span = 60*60

    def __init__(self):
        ProxySource.__init__(self)

    def get_proxies(self, **kwargs):
        res = self.parse_page(self.base_url)
        self._ips = res

    def parse_page(self, url):
        results = []
        try:
            res = requests.get(url, headers=header, timeout=5)
        except:
            return []
        soup = Soup(res.text, features='html.parser')
        items = soup.find_all(class_='title')
        index = 0
        while len(results) < 100:
            url = self.base_url+items[index].find_all('a')[0].get('href')
            try:
                item_res = requests.get(url, timeout=5)
            except:
                continue
            soup_item = Soup(item_res.text, features='html.parser')
            re_pattern = '\d*.\d*.\d*.\d*:\d*@\w*'
            cont = soup_item.find_all(class_="cont")[0].text
            res_tem = re.findall(re_pattern, cont)
            for ip in res_tem:
                ip_port = ip.split('@')[0]
                _type = ip.split('@')[1].lower()
                ip = ip_port.split(":")[0]
                port = ip_port.split(":")[1]
                results.append({'ip': ip, 'port': port, 'type': _type})
            index += 1
            time.sleep(3)
        return results




if __name__ == "__main__":
    a = QiYunProxySource()

    print(a.ips)