import json
import requests
import time
import threading
import logging
import queue
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
from AVMOO.ProxyService.ProxySource import XiciProxySource, GlobalProxySource, KuaiProxySource, YunProxySource, \
    QiYunProxySource, XiaoShuProxySource, SixSixProxySource, KaiXinProxySource

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                        'AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/64.0.3282.186 Safari/537.36'}


class ProxyValidator:
    time_span = 30

    good_proxies = []

    Sources = [
        XiciProxySource(),
        GlobalProxySource(),
        KuaiProxySource(),
        YunProxySource(),
        QiYunProxySource(),
        XiaoShuProxySource(),
        SixSixProxySource(),
        KaiXinProxySource()
    ]

    def __init__(self):
        self.MINIMUM = 5
        self._work_thread = threading.Thread(target=self._auto_check, daemon=True)
        self._flag = True
        self._pause = False
        self.add_proxy()
        self._work_thread.start()

    def check(self, proxies):
        self._pause = True
        ths = []
        for ip in proxies:
            t = threading.Thread(target=self._check, args=[ip, ], daemon=True)
            t.start()
            ths.append(t)
        for t in ths:
            t.join()
        self._pause = False
        logging.info("found {} available proxies".format(self.good_proxies))

    def get_good_proxy(self):
        if len(self.good_proxies) == 0:
            return None
            # self.add_proxy()
            # return self.get_good_proxy()
        return self.good_proxies.pop()

    def get_all(self):
        res = self.good_proxies.copy()
        self.good_proxies = []
        return res

    def add_proxy(self):
        results = []
        for source in self.Sources:
            # if isinstance(source, GlobalProxySource):
            results.extend(source.ips)
        self.check(results)
        # return results

    def _auto_check(self):
        while self._flag:
            if not self._pause:
                time.sleep(self.time_span)
                self.add_proxy()

    @classmethod
    def dict2proxy(cls, dic):
        s = dic['type'] + '://' + dic['ip'] + ':' + str(dic['port'])
        return {'http': s, 'https': s}

    def _check(self, ip):
        try:
            pro = self.dict2proxy(ip)
            # print(pro)
            url = 'https://avmask.com/cn/'
            r = requests.get(url, headers=header, proxies=pro, timeout=30)
            print(r)
            r.raise_for_status()
            print(r.status_code, ip['ip'])
        except Exception as e:
            #print(e)
            pass
            # if self.good_proxies.__contains__(ip):
            #     self.good_proxies.remove(ip)
        else:
            if not self.has_the_same(ip):
                self.good_proxies.append(ip)

    def has_the_same(self, ip):
        for pro in self.good_proxies:
            if pro["ip"] == ip["ip"]:
                return True
        return False



if __name__ == "__main__":
    a = ProxyValidator()
    b = a.get_good_proxy()
    print(b)
