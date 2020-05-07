import logging

'''
Proxy对象，表示一个代理
'''


class Proxy(object):
    ip = ""
    port = 0
    type = "HTTP"
    err_times = 0           # 出错的次数
    success_times = 0       # 成功的次数 ， 由调用者提供
    percent_flag = 0.2      # fail / (fail+success) > $percent_flag$ -> remove(self)
    kick_out_times = 0      # 被移除的次数
    ban_per_flag = 0.8      # when per of fails greater than 0.5 , we don't use this proxy anymore
    baned = False           # 是否不再使用
    last_request_time = 0   # 上一次被使用的时间
    pre_success_times = 0
    pre_err_times = 0

    '''
    :param ip    地址
    :param port  端口
    :param type  类型
    :param holder 对该proxy进行管理的 ProxyHolder
    '''
    def __init__(self, ip="127.0.0.1", port="80", _type="HTTP", holder=None):
        if holder is None:
            pass
            raise KeyError("No Holder Provided")
        self.ip = ip
        self.port = port
        self.type = _type
        self.holder = holder

    '''
    通知该对象，进行了一次成功的请求
    '''
    def good_proxy(self):
        self.success_times += 1
        self.check_self()
        # self.err_times = 0

    '''
    通知该对象，进行了一次失败的请求
    '''
    def bad_proxy(self):
        self.err_times += 1
        self.check_self()

    def ban_proxy(self):
        self.baned = True
        self.holder.kick_proxy(self)

    '''
    每进行一次请求就统计失败率，
    如果大于内置的 percent_flag 则剔除该对象，kick_out_times + 1
    如果大于内置的 ban_per_flag 则 baned 设置为 True ，标志该对象不再被使用                
    '''
    def check_self(self):
        if not (self.err_times+self.success_times) % 20 == 0:
            # print("dont check ", self.success_times+self.err_times)
            return
        # print("check ", self.success_times + self.err_times)

        cur_fail_percent = self.current_fail_percent()

        if cur_fail_percent > self.percent_flag:
            self.kick_out_times += 1
            self.holder.kick_proxy(self)
        if cur_fail_percent > self.ban_per_flag:
            logging.warning("this proxy {} will not use anymore ".format(self.to_string()))
            self.ban_proxy()

    '''
    计算当前对象的失败率
    '''
    def current_fail_percent(self):
        if self.pre_success_times+self.pre_err_times == 0:
            if self.err_times+self.success_times == 0:
                per = 0
            else:
                per = self.err_times/(self.success_times+self.err_times)
        else:
            per = self.pre_err_times / (self.pre_err_times + self.pre_success_times)
        self.pre_err_times = self.err_times
        self.pre_success_times = self.success_times
        return per

    '''
    转换为 scrapy proxy 字符串
    '''
    def to_string(self):
        s = self.type.lower() + "://" + self.ip + ":" + str(self.port)
        return s

    '''
    转换为 requests proxy 格式
    '''
    def to_dict(self):
        s = self.type + '://' + self.ip + ':' + str(self.port)
        return {'http': s, 'https': s}


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