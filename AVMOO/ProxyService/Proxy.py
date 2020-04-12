class Proxy(object):
    ip = ""
    port = 0
    type = "HTTP"
    err_times = 0
    max_err_times = 10

    def __init__(self, ip, port, _type, provider):
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