from .ProxyValidator import ProxyValidator
from .Proxy import Proxy
import logging
import time
import json
import sys

sys.setrecursionlimit(2000)

'''
管理和分发Proxy
'''


class ProxyHolder:
    Validator = None
    passed_proxies = []      # 所有通过初步验证的 proxy :: {Proxy}
    available_proxies = []   # 可用的 proxy :: {Proxy}
    current_kick_times_flag = 0  # kick_out_times 小于或等于该值的 proxy :: {Proxy} 被视为可用

    '''
    初始化一个Validator
    '''
    def __init__(self, delay=1.2):
        self.Validator = ProxyValidator(self)
        self.delay = delay  # 目标网站可以正常访问的最小delay

    # 判断 passed_proxies 是否已经存在相同的 IP
    def has_the_same(self, proxy_dic):
        for pro in self.passed_proxies:
            if pro.ip == proxy_dic["ip"]:
                return True
        return False

    # 由 Validator 调用
    # 添加一个proxy，传入一个proxy字典 -> {"ip":xxx,"port":xxx,"type":"http/https"}
    def append_passed_proxies(self, proxy_dic):
        if not self.has_the_same(proxy_dic):
            proxy = Proxy(proxy_dic["ip"], proxy_dic["port"], proxy_dic["type"], self)
            self.passed_proxies.append(proxy)
            self.available_proxies.append(proxy)

    # 获取可用 proxy 的数目，日志输出，debug 或 测试 使用
    def get_available_count(self):
        logging.info("+++++++++++ still got {} proxies available +++++++++++++".format(len(self.available_proxies)))
        return len(self.available_proxies)

    # 如果可用 proxy 数目太少，增加 current_kick_times_flag
    def check_self(self):
        if self.get_available_count() <= 10:
            self.increase_flag()

    # 增加 current_kick_times_flag ，将之前被剔除但没有被禁止的 proxy 再次放入 available_proxies
    # 重置这些再次使用的 proxy 的请求记录（err_times, success_times）
    def increase_flag(self):
        logging.warning("++++++++++++ increase flag ++++++++++++")
        self.current_kick_times_flag += 1
        for pro in self.passed_proxies:
            if (pro.kick_out_times <= self.current_kick_times_flag) and (pro.baned is not True):
                if not self.available_proxies.__contains__(pro):
                    self.available_proxies.append(pro)
                pro.err_times = 0
                pro.success_times = 0
                pro.pre_err_times = 0
                pro.pre_success_times = 0

    # 由 proxy :: {Proxy} 实例调用，移除自身
    # 从 available_proxies 移除 proxy
    # 每次移除都检查可用的 proxy 数目
    def kick_proxy(self, proxy):
        if self.available_proxies.__contains__(proxy):
            self.available_proxies.remove(proxy)
        self.check_self()

    # 面向使用者的接口，返回一个 proxy
    # 这个 proxy 距离上次被使用至少经过了 self.delay 秒
    # 如果一次遍历没有发现可用的 proxy 则返回None
    def get_one(self, pre_time=0.0):
        time_now = time.time()
        if len(self.available_proxies) == 0:
            time_found = time.time()
            logging.warning("search proxy failed spend {} seconds".format(time_found - time_now + pre_time))
            return None
        for pro in self.available_proxies:
            if pro.last_request_time > time_now - self.delay:
                continue
            if (pro.kick_out_times <= self.current_kick_times_flag) and (pro.baned is not True):
                time_found = time.time()
                logging.info("search proxy spend {} seconds".format(time_found-time_now+pre_time))
                return pro
        time.sleep(0.01)
        time_found = time.time()
        # logging.warning("search proxy not found spend {} seconds".format(time_found - time_now))
        return self.get_one(pre_time=(time_found - time_now + pre_time))

    # 将质量较高的 proxy 保存起来
    # 可以在 spider_closed 信号中调用
    def save_proxy(self):
        pros = []
        for pro in self.passed_proxies:
            if (pro.kick_out_times <= self.current_kick_times_flag) and (pro.baned is not True):
                pros.append({"ip": pro.ip, "port": pro.port, "type": pro.type})
        with open('.proxies.json', 'w+') as file:
            json.dump(pros, file, indent=4)
        logging.info('proxies saved')


if __name__ == "__main__":
    a = ProxyHolder()
    b = a.get_one()
    print(b.to_string())