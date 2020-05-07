import requests
import time
import threading
import logging
from .ProxySource import XiciProxySource, GlobalProxySource, KuaiProxySource, YunProxySource, \
    QiYunProxySource, XiaoShuProxySource, SixSixProxySource, KaiXinProxySource, JiSuProxySource

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                        'AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/64.0.3282.186 Safari/537.36'}
'''
代理检验类，定时进行基本的检验，将通过的代理传递给 ProxyHolder 
'''


class ProxyValidator:

    ProxyHolder = None

    time_span = 30  # 检测间隔

    Sources = [
        XiciProxySource(),
        GlobalProxySource(),
        KuaiProxySource(),
        YunProxySource(),
        QiYunProxySource(),
        XiaoShuProxySource(),
        SixSixProxySource(),
        KaiXinProxySource(),
        JiSuProxySource()
    ]

    # :param holder :: {ProxyHolder}  Proxy管理类
    def __init__(self, holder):
        self.ProxyHolder = holder
        self.MINIMUM = 5
        self._work_thread = threading.Thread(target=self._auto_check, daemon=True)
        self._flag = True
        self._pause = False
        self.add_proxy()
        self._work_thread.start()

    '''
    :param proxies :: { dict }  要进行检查的字典 
    '''
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

    # 从 Source 中取得proxy :: {dict} 进行验证
    def add_proxy(self):
        results = []
        for source in self.Sources:
            # if isinstance(source, GlobalProxySource):
            results.extend(source.ips)
        self.check(results)
        # return results

    # 线程的运行任务，定时执行
    def _auto_check(self):
        while self._flag:
            if not self._pause:
                time.sleep(self.time_span)
                self.add_proxy()

    @classmethod
    def dict2proxy(cls, dic):
        s = dic['type'] + '://' + dic['ip'] + ':' + str(dic['port'])
        return {'http': s, 'https': s}

    # 检验函数，通过proxy向目标网站请求，得到正确响应则添加到ProxyHolder
    def _check(self, ip):
        try:
            pro = self.dict2proxy(ip)
            # print(pro)
            # url = 'https://www.baidu.com/'
            url = 'https://avmoo.host/cn'
            r = requests.get(url, headers=header, proxies=pro, timeout=30)
            # print(r)
            r.raise_for_status()
            # print(r.status_code, ip['ip'])
        except Exception as e:
            pass
            # logging.info("check proxy {} err:{}".format(ip, e))
        else:
            logging.info("found proxy {}".format(ip))
            self.ProxyHolder.append_passed_proxies(ip)


if __name__ == "__main__":
    a = ProxyValidator()

    print(a)
