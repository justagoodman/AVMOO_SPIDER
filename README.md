# AVMOO_SPIDER

AVMOO,  番号， scrapy， python, 代理

# 如何白嫖代理？

# ProxyService模块可以在线、动态的检测添加可用代理<br>

ProxySource类本质上是爬虫，爬取主流代理网站的免费代理<br>

ProxyValidator类动态检测来自ProxySource的代理，
将通过验证的代理传递给ProxyHolder<br>

ProxyHolder类保存所有通过验证的代理,调用get_one方法获取一个距离上次使用经过delay秒的可用代理(可能返回None)<br>

Proxy类接受请求信息的反馈，调用good_proxy表示进行了一次成功的请求
调用bad_proxy表示进行了一次失败的请求，Proxy类会定期检测失败率，
剔除质量差的代理

# 如何使用 ?

proxy_holder = ProxyHolder()<br>
proxy = proxy_holder.get_one()<br>

res = requests.get(’https://www.baidu.com‘, proxies=proxy.to_dict())<br>

if res.status != 200:<br>
&nbsp;&nbsp;  proxy.bad_proxy()<br>
else:<br>
&nbsp;&nbsp;  proxy.good_proxy()

# tips

Proxy.to_string() 生成用于scrapy Request的proxy字符串<br>
Proxy.to_dict()   生成用于requests proxies 的字典<br>

ProxyHolder的初始化会初始化所有的ProxySource爬取免费代理再进行一次完整的检测，所以会消耗3-5min的时间<br>

如果要单独使用ProxyService，需要更改 `import` 的路径