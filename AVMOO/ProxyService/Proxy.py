import logging


class Proxy(object):
    ip = ""
    port = 0
    type = "HTTP"
    err_times = 0
    max_err_times = 5

    def __init__(self, ip="127.0.0.1", port="80", _type="HTTP", provider=None):
        self.ip = ip
        self.port = port
        self.type = _type
        self.provider = provider

    def good_proxy(self):
        self.err_times = 0

    def bad_proxy(self):
        self.err_times += 1
        if self.err_times > self.max_err_times:
            self.provider.remove_proxy(self)

    def to_string(self):
        s = self.type + "://" + self.ip + ":" + str(self.port)
        return s


if __name__ == "__main__":
    a = Proxy()
    print(a.to_string())
    a = []
    import random
    b = random.choice(a)
    print(b)