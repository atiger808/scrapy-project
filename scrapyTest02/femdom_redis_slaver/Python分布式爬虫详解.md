# Python分布式爬虫详解



**二、修改项目为RedisCrawlSpider爬虫**

1、首先修改爬虫文件

① RedisCrawlSpider修改很简单，首先需要引入RedisCrawlSpider：

```
from scrapy_redis.spiders import RedisCrawlSpider

```

② 将父类中继承的`CrawlSpider`改为继承`RedisCrawlSpider`：

```
class DyttSlaverSpider(RedisCrawlSpider):

```

③ 因为slaver端要从redis数据库中获取爬取的链接信息，所以去掉`allowed_domains()` 和 `start_urls`，并添加`redis_key`

```
redis_key = 'dytt:start_urls'

```

④ 增加`__init__()`方法，动态获取`allowed_domains()`，[理论上要加这个，但是实测加了爬取的时候链接都被过滤了，所以我没加，暂时没发现有什么影响]

```
     def __init__(self, *args, **kwargs):



         domain = kwargs.pop('domain', '')



         self.allowed_domains = filter(None, domain.split(','))



         super(DyttSlaverSpider, self).__init__(*args, **kwargs)
```

2、修改setting文件

① 首先要指定redis数据库的连接参数：

```
REDIS_HOST = '192.168.0.131'



REDIS_PORT = 6379
```

② 指定使用`scrapy-redis`的调度器

```
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

```

③ 指定使用`scrapy-redis`的去重

```
DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'

```

④ 指定排序爬取地址时使用的队列

```
# 默认的 按优先级排序(Scrapy默认)，由sorted set实现的一种非FIFO、LIFO方式。



SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'



# 可选的 按先进先出排序（FIFO）



# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderQueue'



# 可选的 按后进先出排序（LIFO）



# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderStack'
```

⑤ 设置断点续传，也就是不清理redis queues

```
SCHEDULER_PERSIST = True

```

⑥ 默认情况下,`RFPDupeFilter`只记录第一个重复请求。将`DUPEFILTER_DEBUG`设置为`True`会记录所有重复的请求。

```
DUPEFILTER_DEBUG =True

```

⑦ 配置`RedisPipeline`将`item`写入`key`为 `spider.name : items` 的redis的list中，供后面的分布式处理item

```
ITEM_PIPELINES = {



   'dytt_redis_slaver.pipelines.DyttRedisSlaverPipeline': 300,



   'scrapy_redis.pipelines.RedisPipeline': 400



}
```

3、增加爬虫信息字段（可选）

由于会有多个slaver端，所以可加一个爬虫名字的字段和时间字段来区分是哪个爬虫在什么时间爬到的信息。

① item中增加字段

```
    # utc时间



    crawled = scrapy.Field()



    # 爬虫名



    spider = scrapy.Field()
```

② pipelines中新增类：

```
class InfoPipeline(object):



 



    def process_item(self, item, spider):



        #utcnow() 是获取UTC时间



        item["crawled"] = datetime.utcnow()



        # 爬虫名



        item["spider"] = spider.name



        return item
```

③ setting中设置ITEM_PIPELINES

```
ITEM_PIPELINES = {



   'dytt_redis_slaver.pipelines.DyttRedisSlaverPipeline': 300,



   'dytt_redis_slaver.pipelines.InfoPipeline':350,



   'scrapy_redis.pipelines.RedisPipeline': 400



}
```

至此，项目修改完毕，现在可以爬取某一分类下的第一页的电影信息。

以Windows10为slaver端运行一下：

![img](https://img-blog.csdn.net/20181020160653715?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3podXNvbmd6aXll/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

因为请求队列为空，所以爬虫会停下来进行监听，直到我们在Master端给它一个新的连接：

![img](https://img-blog.csdn.net/20181020160703412?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3podXNvbmd6aXll/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

爬虫启动，开始爬取信息：

![img](https://img-blog.csdn.net/2018102016071226?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3podXNvbmd6aXll/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

爬取完成后，项目不会结束，而是继续等待新的爬取请求的到来，爬取结果：

![img](https://img-blog.csdn.net/20181020160725419?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3podXNvbmd6aXll/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

**本章小结：**

本章将一个crawlspider爬虫改为了RedisCrawlSpider爬虫，可以实现分布式爬虫，但是由于数据量较小（只有30条）所以只用了一个slaver端。并且没有去设置代理ip和user-agent，下一章中，针对上述问题，将对项目进行更深一步的修改。

**项目源码：**

```
https://github.com/ZhiqiKou/Scrapy_notes
```