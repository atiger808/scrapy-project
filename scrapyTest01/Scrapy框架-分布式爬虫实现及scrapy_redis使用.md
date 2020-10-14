# Scrapy框架-分布式爬虫实现及scrapy_redis使用



## 重点

一、我的机器是Linux系统或者是MacOSX系统，不是Windows

二、区别，事实上，分布式爬虫有几个不同的需求，会导致结构不一样，我举个例子：

1、我需要多台机器同时爬取目标url并且同时从url中抽取数据，N台机器做一模一样的事，通过redis来调度、中转，也就是说它根本没有主机从机之分。

2、我有n台机器负责爬取目标URL，另外有M台机器负责容url中抽取数据，N和M做的事不一样，他们也是通过redis来进行调度和中转，它有主机从机之分。

这里演示的，是第1中，N台机器做一模一样的事。这点大家要搞清楚。

分布式爬虫优点：

> ① 充分利用多台机器的带宽速度爬取数据
>
> ② 充分利用多台机器的IP爬取

通过状态管理器来调度scrapy，就需要改造一下scrapy，要解决两个问题：

> ① request之前是放在内存的，现在两台服务器就需要对队列进行集中管理。
>
> ② 去重也要进行集中管理

## redis安装和命令

参考[菜鸟教程](http://www.runoob.com/redis/redis-install.html)的安装以及命令介绍（由于安装时候是下载压缩包后进行解压再安装，所以会留下压缩包和文件夹。需要找一个指定的文件夹存放这些东西，我的电脑一般是放在home/ranbos/Programe File目录下，打开终端，执行以下命令）

```
$ wget http://download.redis.io/releases/redis-4.0.6.tar.gz
$ tar xzf redis-4.0.6.tar.gz
$ cd redis-4.0.6
$ make

```

这次笔记时候的redis版本是4.0.6。 make完后 redis-4.0.6目录下会出现编译后的redis服务程序redis-server,还有用于测试的客户端程序redis-cli,两个程序位于安装目录 src 目录下，下面启动redis服务：

```
$ cd src
$ ./redis-server

```

就可以看到redis的启动画面了。但是这只是启动服务，如果想输入命令的话，还需要打开另一个终端，同样进入到src目录下，运行./redis-cli命令，才能进入命令交互界面。

### 设置密码

redis是可以匿名访问的，所以需要设置连接密码，在cli窗口通过命令查看密码设置状态：

```
CONFIG get requirepass

```

可以得到一个结果，那就是没有设置密码

```
"requirepass"


```

通过命令设置密码：

```
CONFIG set requirepass "ranbos"

```

再次查看的时候就会提示：

```
(error) NOAUTH Authentication required.


```

需要登录才行，登录的命令是：

```
AUTH "ranbos"


```

只要密码对了，就可以连接上去了。

------

## redis基础知识

redis是一个key-value存储系统，它通常被称为数据结构服务器，因为值（value）可以是 字符串(String), 哈希(Map), 列表(list), 集合(sets) 和 有序集合(sorted sets)等类型。

- Redis支持数据的持久化，可以将内存中的数据保存在磁盘中，重启的时候可以再次加载进行使用。
- Redis不仅仅支持简单的key-value类型的数据，同时还提供list，set，zset，hash等数据结构的存储。
- Redis支持数据的备份，即master-slave模式的数据备份。

### Redis 优势

- 性能极高 – Redis能读的速度是110000次/s,写的速度是81000次/s 。
- 丰富的数据类型 – Redis支持二进制案例的 Strings, Lists, Hashes, Sets 及 Ordered Sets 数据类型操作。
- 原子 – Redis的所有操作都是原子性的，意思就是要么成功执行要么失败完全不执行。单个操作是原子性的。多个操作也支持事务，即原子性，通过MULTI和EXEC指令包起来。
- 丰富的特性 – Redis还支持 publish/subscribe, 通知, key 过期等等特性。

### 基础操作

一些基础操作就根据[菜鸟教程的文章](http://www.runoob.com/redis/redis-intro.html)进行学习吧

------

## 通过scrapy-redis搭建分布式爬虫

在github上搜索[scrapy-redis](https://github.com/rmax/scrapy-redis),里面有具体的文档及介绍。

### ① 安装redis

通过pycharm安装redis

### ② 配置scrapy-redis

根据文档的说明，到settings.py中更改配置，在空白地方新增代码：

```
""" scrapy-redis配置 """
# Enables scheduling storing requests queue in redis.
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# Ensure all spiders share same duplicates filter through redis.
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

```

然后到ITEM_PIPELINES中新增：

```
    # Store scraped item in redis for post-processing. 分布式redispipeline
    'scrapy_redis.pipelines.RedisPipeline': 300,

```

即可完成配置。

但是在写代码的时候跟之前的写法不一样，[文档这里介绍](https://github.com/rmax/scrapy-redis#feeding-a-spider-from-redis)到:

```
from scrapy_redis.spiders import RedisSpider

class MySpider(RedisSpider):
    name = 'myspider'

    def parse(self, response):
        # do stuff
        pass

```

> 在爬虫里面引入scrapy_redis的包，以及在类继承的不能继承scrapy.Spider了，而是继承RedisSpider

还有另外两点

run the spider:

```
scrapy runspider myspider.py
push urls to redis:

```

push urls to redis:

```
redis-cli lpush myspider:start_urls http://google.com
Note

```

要预先放置url在redis当中才行，否则爬虫会一直在等待。

------

## 开始搭建分布式爬虫

### ① 新建项目

为了更好的测试scrapy-redis，需要新建一个项目，但是可以选择之前爬虫的虚拟环境，这样就可以不用重复装那么多外部包了

用pycharm新建ScrapyRedis项目，在选择虚拟环境的时候选择之前jobbole-test那个虚拟环境，路径在C盘Admin用户下的Jobbole-test/Script/python.exe。

### ② 新建scrapy项目

用scrapy startproject ScrapyRedisTest命令来新建项目，建好项目后不着急建工程。

然后到github上下载scrapy-redis（实际上是要用pip安装scrapy-redis外部包）。解压后，复制文件夹下面的src目录下的scrapy_redis放到项目目录下，与项目的Spider目录同级。

接着在spider目录下新建jobbole.py文件，将使用说明里的示例代码粘贴进去,覆盖默认的爬虫类：

```
from scrapy_redis.spiders import RedisSpider

class MySpider(RedisSpider):
    name = 'myspider'

    def parse(self, response):
        # do stuff
        pass

```

由于路径问题，自己改一下：

```
from ..scrapy_redis.spiders import RedisSpider

```

------

## 注意

> 这里复制进来只是为了更好的观察和跟踪代码，实际上是要用Pycharm安装scrapy-redis外部包的，一定要装。

跟踪RedisSpider代码可以发现它是继承了两个类：

```
class RedisSpider(RedisMixin, Spider)

```

scrapy的默认Spider以及对redis操作的RedisMixin。

然后跟踪代码RedisMixin。可以看到它用setup_redis给每个爬虫设置了一个redis的key，方法里面包含：

```
 self.redis_key = settings.get(
                'REDIS_START_URLS_KEY', defaults.START_URLS_KEY,
            )

```

意思就是不同的爬虫会自己设置一个默认的key，可以进行覆盖，也可以让它自动生成。覆盖的方法就是在scrapy-redis包的源码中，路径是

> scrapy-redis\example-project\example\spiders

里面有两个文件：

```
mycrawler_redis.py

myspider_redis.py

```

对应两种不同的爬虫。

这里以myspider.py为例，将jobbole.py的代码改成：

```
from ..scrapy_redis.spiders import RedisSpider


class JobboleSpider(RedisSpider):
    name = 'jobbole'
    allowd_domains = ["blog.jobbole.com"]
    redis_key = 'jobbole:start_urls'
    def parse(self, response):
        # do stuff
        pass

```

现在先放着，看下一个RedisMixin中还有一个方法next_requests:

```
 def next_requests(self):
        """Returns a request to be scheduled or none."""
        use_set = self.settings.getbool('REDIS_START_URLS_AS_SET', defaults.START_URLS_AS_SET)
        fetch_one = self.server.spop if use_set else self.server.lpop
        # XXX: Do we need to use a timeout here?
        found = 0
        # TODO: Use redis pipeline execution.
        while found < self.redis_batch_size:
            data = fetch_one(self.redis_key)
            if not data:
                # Queue empty.
                break
            req = self.make_request_from_data(data)
            if req:
                yield req
                found += 1
            else:
                self.logger.debug("Request not made from data: %r", data)

        if found:
            self.logger.debug("Read %s requests from '%s'", found, self.redis_key)


```

之前的scrapy获取下一个队列next_requests，是从本机Schedule获取的，这里是通过redis获取的。

------

## 准备测试

将之前写的jobbole的逻辑代码拿到这个jobbole中：

```
from scrapy.http import Request
from urllib import parse

from ..scrapy_redis.spiders import RedisSpider


class JobboleSpider(RedisSpider):
    name = 'jobbole'
    allowd_domains = ["blog.jobbole.com"]
    redis_key = 'jobbole:start_urls'

    def parse(self, response):

        """
        逻辑分析
            1.通过抓取下一页的链接，交给scrapy实现自动翻页,如果没有下一页则爬取完成
            2.将本页面的所有文章url爬下，并交给scrapy进行深入详情页的爬取
        """
        node_urls = response.css('#archive .floated-thumb .post-thumb a')
        for node_url in node_urls:
            title_url = node_url.css('::attr(href)').extract_first("")
            title_img = node_url.css('img::attr(src)').extract_first("")
            yield Request(url=parse.urljoin(response.url, title_url), meta={"title_img": title_img},
                          callback=self.parse_detail)

        # 实现下一页的翻页爬取
        next_pages = response.css('.next.page-numbers::attr(href)').extract_first("")  # 在当前列表页获取下一页链接
        if next_pages:
            yield Request(url=parse.urljoin(response.url, next_pages), callback=self.parse)  # 如果存在下一页，则将下一页交给parse自身处理

    def parse_detail(self, response):
        """
        将爬虫爬取的数据送到item中进行序列化
        这里通过ItemLoader加载item
        """
        pass

```

然后根据说明文档，到settings.py中进行配置：

```
ITEM_PIPELINES = {
   'scrapy_redis.pipelines.RedisPipeline': 300,
}

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

""" scrapy-redis配置 """
# Enables scheduling storing requests queue in redis.
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# Ensure all spiders share same duplicates filter through redis.
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

```

也就是将scrapy_redis的item_pipeline、scheduler、dupefilter_class配置进来，并且关闭robots协议设置

为了调试，需要在项目写一个main.py文件，里面的代码跟之前的一样：

```
import os,sys
from scrapy.cmdline import execute

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy","crawl","jobbole"])

```

保存即可运行，这时候如果redis之前有设置登录密码的话，是会报错的。这里可以用命令，到redis里面取消登录密码，到redis/src目录下打开终端：

```
./redis-cli

```

进入redis命令终端：

```
config get requirepass   

```

查看是否有密码，如果结果显示：

```
1) "requirepass"
2) "ranbos"

```

那就说明requirepass对应的密码是ranbos，要取消就输入命令：

```
config set requirepass ''

```

即可。这时候保存运行，发现爬虫启动了，但是没有开始爬取，是因为scrapy_redis现在的start_urls是从redis里面取的，所以在redis里面设置key :

```
redis-cli lpush jobbole:start_urls http://blog.jobbole.com/all-posts

```

也就是在redis中设置一个Jobbole的初始url，这样爬虫开始爬取的时候就会取这个url开始，如果没有则报错。

然后在jobbole.py的paser方法和paser_detail方法里面打断点，以便调试。

Debug运行，发现可以运行了，也正确的进入了paser方法和paser_detail方法里面。其他操作跟之前的jobbole爬虫一模一样即可。

------

## 观察过程

为了更好的观察过程，需要在scrapy-redis源码包

```
[项目jobbole-test\Lib\site-packages\scrapy_redis\scheduler.py]

```

中的next_request方法里面：

```
        request = self.queue.pop(block_pop_timeout)

```

这句代码打一个断点，然后恢复断点继续(继续才会从redis里面取starturls，它的取值方法是pop，所以取完后redis是不会有这条记录的)，等程序运行到parse里面的时候，断点暂停，不要点继续，在暂停的时候到redis中用命令查看：

```
 redis-cli keys *

```

就会得到这些数据：

```
1) "myKey"
2) "jobbole:dupefilter"
3) "jobbole:requests"
4) "runoobkey"
5) "mykey"


```

之前的那些是我插入的，真正的是：

```
2) "jobbole:dupefilter"
3) "jobbole:requests"

```

凡是在spider(这里是jobbole爬虫)中用yield出去的记录，都通过scheduler.py里面的enqueue_request方法发push送到这jobbole:requests里面记录着，然后jobbole:dupefilter是个过滤器里面记录的是指纹。

通过命令：

```
redis-cli zrangebyscore jobbole:requests 0 100

```

可以看到redis里面存储的requests数据，这样爬虫发送的所有请求都会在requests中存有记录，分布式爬虫通过里面的记录和dupefilter里面的指纹实现的去重，不会造成交叉重复爬取。

------

## 远程redis

既然它是一个分布式爬虫，就会存在多个服务器。但是负责去重和调度的只能是其中1个服务器，其他的都根据它的redis来抽取request。主要的机器一般叫做master，其他的机器称为slave。

### 数据库密码连接

之前有提到过，redis可以是不用密码的，但是这显然很危险。还是要根据命令设定好密码。但是如果设定好密码后，爬虫不进行配置就会报错。那如何进行密码配置呢（基于单机情况），在settings.py中新增配置：

```
REDIS_PARAMS ={
    'password': 'ranbos',
}

```

就是这么简单，保存后运行即可。

### 远程服务器redis

如果是远程服务器上面的redis是如何连接的呢？

- 还好有台阿里云服务器，在上面根据之前的redis安装方法将它安装上，然后设置好密码。
- 在阿里云服务器安全配置规则里面把6379端口打开
- （有可能需要将bind地址从127.0.0.1改成0.0.0.0）这个我忘了
- 在本地settings配置中新增配置即可
  新增的配置代码为：

```
# 指定redis数据库的连接参数
REDIS_HOST = "59.110.xxx.xxx"
REDIS_PORT = "6379"
REDIS_PARAMS ={
    'password': 'ranbospider',  # 服务器的redis对应密码
}

```

然后开启爬虫，再用命令在服务器的redis上把start_urls添加进去：

```
lpush jobbole:start_urls http://blog.jobbole.com/all-posts


```

就完成了scrapy及远程服务器的连接设置。（多个sleva连接master都可以这么设置）

### 动态配置

在动态配置知识中，可以通过在具体的spider里面重载custom_settings来实现动态配置。这里的redis同样适合动态配置，现将setting里面之前写的配置注释掉，到具体的spider代码中（这里用jobbole演示）：

```
class JobboleSpider(RedisSpider):
    name = 'jobbole'
    allowd_domains = ["blog.jobbole.com"]
    redis_key = 'jobbole:start_urls'

    custom_settings = {
        # 指定redis数据库的连接参数
        'REDIS_HOST':"59.110.xxx.xxx",
        'REDIS_PORT':"6379",
        'REDIS_PARAMS': {
            'password': 'ranbospider',
        },
    }
    def parse(self, response):
        pass

```

同样可以实现远程redis，而且还可以根据不同的爬虫设定不同的服务器地址、配置。

### 小知识

在我们测试的时候，手动停止爬虫（爬虫自动爬取完毕是finish），手动停止是killed。待下次开启爬虫测试的时候，它总是会再爬取几条信息。

原因是上一次手动关闭爬虫，但request队列里面还有记录，所以打开它就会爬完上次的数据。然后就进入等待阶段，等待我用命令将start_urls添加到redis里面。

------

## 去重源码讲解

在源码包里面有：

```
dupefilter.py

```

文件，它的功能主要是去重。它的源码里面用到的方法与scrapy的源码和功能基本上是一致的：

```
    def __init__(self, server, key, debug=False):
 
        self.server = server
        self.key = key
        self.debug = debug
        self.logdupes = True

```

在初始化的时候就自动连接了server，而这个server 在from_settings方法里面生成，跟踪代码可以发现它是自动连接到redis的，而且把key也传到了dupefilter里面。

然后看到request_seen方法：

```
def request_seen(self, request):

    fp = self.request_fingerprint(request)
        # This returns the number of values added, zero if already exists.
        added = self.server.sadd(self.key, fp)
        return added == 0

```

意思是会根据request生成一个指纹，然后把指纹添加到redis中，如果成功则返回1，如果失败则返回0。返回0代表里面已经有一个相同的指纹了。

> 这样就完成了去重的任务

------

打开源码包里面的pipelines.py，里面有一个RedisPipeline类。首先，它的入口是from_settings方法，里面也有一句代码：

```
            'server': connection.from_settings(settings),

```

这个server指向的也是上面介绍的那个server，也就是我们的redis。

接着看process_item方法，这里面这是pipelines里面的重要方法，数据传到pipeline都会经过process_item的处理

```
    def process_item(self, item, spider):
        return deferToThread(self._process_item, item, spider)

```

它调用了deferToThread方法(一个异步化的方法)，放到另外一个线程中去做。然后它还调用了_process_item方法：

```
    def _process_item(self, item, spider):
        key = self.item_key(item, spider)
        data = self.serialize(item)
        self.server.rpush(key, data)
        return item

```

它首先调用spider的name去redis中找到对应的变量，然后通过rpush放置到队列的队尾。

------

源码包里面还有个queue.py文件

里面有几个类要讲解一下

FifoQueue 就是先进先出的有序队列