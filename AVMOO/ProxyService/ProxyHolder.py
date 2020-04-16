from AVMOO.ProxyService.ProxyValidator import ProxyValidator
from AVMOO.ProxyService.Proxy import Proxy
import logging


class ProxyHolder:
    Provider = None
    Validator = None
    passed_proxies = []
    in_use_proxies = []
    current_kick_times_flag = 0
    flag_increase_signal = 3

    def __init__(self, provider):
        self.Provider = provider
        self.Validator = ProxyValidator(self)

    def has_the_same(self, proxy_dic):
        for pro in self.passed_proxies:
            if pro.ip == proxy_dic["ip"]:
                return True
        return False

    def is_in_use(self, proxy_obj):
        for pro in self.in_use_proxies:
            if pro.ip == proxy_obj.ip:
                return True
        return False

    def append_passed_proxies(self, proxy_dic):
        if not self.has_the_same(proxy_dic):
            proxy = Proxy(proxy_dic["ip"], proxy_dic["port"], proxy_dic["type"], self)
            self.passed_proxies.append(proxy)
            result = self.Provider.add_proxy(proxy)
            self.in_use_proxies.append(proxy)
            # if not self.is_in_use(proxy) and result is True:
            #     self.in_use_proxies.append(proxy)

    def get_available_count(self):
        count = 0
        for pro in self.passed_proxies:
            if (pro.kick_out_times <= self.current_kick_times_flag) and (pro.baned is not True):
                count += 1
        return count

    def check_self(self):
        if self.get_available_count() <= len(self.passed_proxies)/10:
            self.increase_flag()

    def increase_flag(self):
        logging.info("++++++++++++ increase flag ++++++++++++")
        self.current_kick_times_flag += 1
        for pro in self.passed_proxies:
            if (pro.kick_out_times <= self.current_kick_times_flag) and (pro.baned is not True):
                pro.err_times = 0
                pro.success_times = 0
                result = self.Provider.add_proxy(pro)
                if not self.is_in_use(pro) and (result is True):
                    self.in_use_proxies.append(pro)

    def kick_proxy(self, proxy):
        if proxy in self.Provider.proxies:
            self.Provider.remove_proxy(proxy)
        if self.in_use_proxies.__contains__(proxy):
            self.in_use_proxies.remove(proxy)
        pro = self.get_one()
        if pro is not None:
            result = self.Provider.add_proxy(pro)
            if result:
                self.in_use_proxies.append(pro)
        self.check_self()

    def get_one(self):
        for pro in self.passed_proxies:
            if (pro.kick_out_times <= self.current_kick_times_flag) and (pro.baned is not True):
                return pro
        return None
