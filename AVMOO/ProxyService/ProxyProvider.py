from AVMOO.ProxyService.ProxyHolder import ProxyHolder
import random
import logging


class ProxyProvider:

    ProxyHolder = None

    max_proxies = 40

    proxies = []

    next_index = 0

    def __init__(self):
        self.ProxyHolder = ProxyHolder(self)

    def get_proxy(self, rand=False):
        if len(self.proxies) == 0:
            return None

        if rand:
            proxy = random.choice(self.proxies)
            return proxy
        else:
            return self._next()

    def add_proxy(self, proxy):
        # if len(self.proxies) >= self.max_proxies:
        #     return False
        if self.proxies.__contains__(proxy):
            return False
        self.proxies.append(proxy)
        logging.info(
                "added proxy {}, still got {} proxies left".format(proxy, len(self.proxies)))
        return True

    def remove_proxy(self, proxy):
        self.proxies.remove(proxy)
        logging.info(
                    "removing proxy {}, still got {} proxies left".format(proxy, len(self.proxies)))

    def _next(self):
        if self.next_index >= len(self.proxies):
            self.next_index = 0
        proxy = self.proxies[self.next_index]
        self.next_index += 1
        return proxy


if __name__ == "__main__":
    a = ProxyProvider()
    a.get_proxy()
    print(a.get_proxy())
    print(a.get_proxy())
    print(a.get_proxy())
    print(a.get_proxy())
    print(a.get_proxy())
    print("a")