import logging


class Proxy(object):
    ip = ""
    port = 0
    type = "HTTP"
    err_times = 0
    success_times = 0
    percent_flag = 0.3    # fail / (fail+success) > $percent_flag$ -> remove(self)
    kick_out_times = 0
    ban_per_flag = 0.8      # when per of fails greater than 0.5 , we don't use this proxy anymore
    baned = False

    def __init__(self, ip="127.0.0.1", port="80", _type="HTTP", holder=None):
        if holder is None:
            pass
            # raise KeyError("No Holder Provided")
        self.ip = ip
        self.port = port
        self.type = _type
        self.holder = holder

    def good_proxy(self):
        self.success_times += 1
        self.check_self()
        # self.err_times = 0

    def bad_proxy(self):
        self.err_times += 1
        self.check_self()

    def check_self(self):
        if not (self.err_times+self.success_times) % 10 == 0:
            # print("dont check ", self.success_times+self.err_times)
            return
        # print("check ", self.success_times + self.err_times)

        if self.current_fail_percent() > self.percent_flag:
            self.kick_out_times += 1
            self.holder.kick_proxy(self)
        if self.current_fail_percent() > self.ban_per_flag:
            logging.warning("this proxy {} will not use anymore ".format(self))
            self.baned = True

    def current_fail_percent(self):
        per = self.err_times / (self.err_times+self.success_times)
        return per

    def to_string(self):
        s = self.type + "://" + self.ip + ":" + str(self.port)
        return s


if __name__ == "__main__":
    a = Proxy()
    b = 10
    for i in range(0,100):
        a.good_proxy()
    a = {"name":1,"li":2}
    a.pop("s")
    # a = Proxy()
    # print(a.to_string())
    # a = []
    # import random
    # b = random.choice(a)
    # print(b)