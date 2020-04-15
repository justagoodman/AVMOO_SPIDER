from AVMOO.ProxyService.ProxyValidator import ProxyValidator
import random
from AVMOO.ProxyService.Proxy import Proxy
import logging


class ProxyProvider:

    ProxyValidator = ProxyValidator()

    proxies = []

    minimum_proxy = 5

    maximum_proxy = 20

    next_index = 0

    def __init__(self):
        self.get_all()

    def get_all(self):
        pros = self.ProxyValidator.good_proxies
        for pro in pros:
            if pro is not None:
                if self.has_the_same(pro):
                    continue
                self.proxies.append(Proxy(pro["ip"], pro["port"], pro["type"], self))
        # self.dynamic_change_err_times()

    def get_proxy(self, rand=False):
        # while len(self.proxies) < self.minimum_proxy:
        # while len(self.proxies) < self.minimum_proxy:
        #     pro = self.ProxyValidator.get_good_proxy()
        #     if (pro is not None) & (not self.has_the_same(pro)):
        #         self.proxies.append(Proxy(pro["ip"], pro["port"], pro["type"], self))
        #         self.dynamic_change_err_times()
        if len(self.proxies) == 0:
            return Proxy()

        # if len(self.proxies) < self.minimum_proxy:
        #     self.add_proxy()

        if rand:
            proxy = random.choice(self.proxies)
            return proxy
        else:
            return self._next()

    def add_proxy(self):
        if len(self.proxies) >= self.maximum_proxy:
            return
        pro = self.ProxyValidator.get_good_proxy()
        if (pro is not None) & (not self.has_the_same(pro)):
            self.proxies.append(Proxy(pro["ip"], pro["port"], pro["type"], self))
            # self.dynamic_change_err_times()
            logging.info(
                "added proxy {}, still got {} proxies left".format(pro, len(self.proxies)))

    def remove_proxy(self, proxy):
        for pro in self.proxies:
            if pro.ip == proxy.ip:
                self.proxies.remove(pro)
                # self.add_proxy()
                logging.info(
                    "removing proxy {}, still got {} proxies left".format(pro.to_string(), len(self.proxies)))
                break

    def _next(self):
        if self.next_index >= len(self.proxies):
            self.next_index = 0
        proxy = self.proxies[self.next_index]
        self.next_index += 1
        return proxy

    def has_the_same(self, ip):
        for pro in self.proxies:
            if pro.ip == ip["ip"]:
                return True
        return False

    def dynamic_change_err_times(self):
        # if len(self.proxies) < 5:
        #     max_err = 5
        # elif len(self.proxies) < 7:
        #     max_err = 4
        # # elif len(self.proxies) < 15:
        # #     max_err = 5
        # else:
        #     max_err = 3
        max_err = 5
        for pro in self.proxies:
            pro.max_err_times = max_err


if __name__ == "__main__":
    a = ProxyProvider()
    a.get_proxy()
    print(a.get_proxy())
    print(a.get_proxy())
    print(a.get_proxy())
    print(a.get_proxy())
    print(a.get_proxy())
    print("a")