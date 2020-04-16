from AVMOO.ProxyService.ProxyValidator import ProxyValidator
from AVMOO.ProxyService.Proxy import Proxy
import logging
import time
import json
import random


class ProxyHolder:
    Validator = None
    passed_proxies = []
    available_proxies = []
    current_kick_times_flag = 0
    flag_increase_signal = 3
    delay = 1.2

    def __init__(self):
        self.Validator = ProxyValidator(self)

    def has_the_same(self, proxy_dic):
        for pro in self.passed_proxies:
            if pro.ip == proxy_dic["ip"]:
                return True
        return False

    def append_passed_proxies(self, proxy_dic):
        if not self.has_the_same(proxy_dic):
            proxy = Proxy(proxy_dic["ip"], proxy_dic["port"], proxy_dic["type"], self)
            self.passed_proxies.append(proxy)
            self.available_proxies.append(proxy)

    def get_available_count(self):
        logging.info("+++++++++++ still got {} proxies available +++++++++++++".format(len(self.available_proxies)))
        return len(self.available_proxies)

    def check_self(self):
        if self.get_available_count() <= 10:
            self.increase_flag()

    def increase_flag(self):
        logging.info("++++++++++++ increase flag ++++++++++++")
        self.current_kick_times_flag += 1
        for pro in self.passed_proxies:
            if (pro.kick_out_times <= self.current_kick_times_flag) and (pro.baned is not True):
                if not self.available_proxies.__contains__(pro):
                    self.available_proxies.append(pro)
                pro.err_times = 0
                pro.success_times = 0

    def kick_proxy(self, proxy):
        if self.available_proxies.__contains__(proxy):
            self.available_proxies.remove(proxy)
        self.check_self()

    def get_random_one(self):
        if len(self.passed_proxies) == 0:
            return None
        proxy = random.choice(self.passed_proxies)
        return proxy

    def get_one(self):
        time_now = time.time()
        for pro in self.available_proxies:
            if pro.last_request_time > time_now - self.delay:
                continue
            if (pro.kick_out_times <= self.current_kick_times_flag) and (pro.baned is not True):
                time_found = time.time()
                logging.info("search proxy spend {} seconds".format(time_found-time_now))
                return pro
        time_found = time.time()
        logging.warning("search proxy failed spend {} seconds".format(time_found - time_now))
        return None

    def save_proxy(self):
        pros = []
        for pro in self.passed_proxies:
            if (pro.kick_out_times <= self.current_kick_times_flag) and (pro.baned is not True):
                pros.append(pro)
        with open('proxies.json', 'w+') as file:
            json.dump(pros, file)
        logging.info('proxies saved')


if __name__ == "__main__":
    a = ProxyHolder()
    b = a.get_one()
    print(b.to_string())