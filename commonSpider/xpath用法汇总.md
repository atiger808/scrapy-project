众所周知，在设计爬虫时，最麻烦的一步就是对网页元素进行分析，目前流行的网页元素获取的工具有BeautifulSoup，lxml等，而据我使用的体验而言，Scrapy的元素选择器Xpath（结合正则表达式）是其中较为出色的一种（个人认为最好啦，当然只能在Scrapy中使用）功能相对较全、使用较为方便，正因为它的丰富性，有时很多功能会忘记，所以在这里整理好记录下来，方便今后查阅使用。

1. 元素的多级定位与跳级定位

多级定位：依靠html中的多级元素逐步缩小范围response.xpath('//table/tbody/tr/td') //如果知道元素所属的下标可以用下标选择 response.xpath('//table/tbody/tr[1]/td')1234跳级定位：符号“//”表示跳级定位，即对当前元素的所有层数的子元素（不仅是第一层子元素）进行查找，一般xpath的开头都是跳级定位response.xpath('//span//table')1

2. 依靠元素的属性定位

每个html元素都有很多属性，如id、class、title、href、text(href和text往往可以配合正则表达式）等，这些属性往往具有很强的特殊性，结合元素多级定位或跳级定位会更准确高效，下面举几个典型的例子，其他的举一反三

利用class定位response.xpath('//td[@class="mc_content"]')1利用href配合正则表达式定位response.xpath('//a[re:test(@href,"^\/index\.php\?m=News&a=details&id=1&NewsId=\d{1,4}")]')1利用text结合正则表达式定位a=response.xpath('//a[re:test(text(),"\w{4}")]')1

此外，xpath还有对于html元素操作的两个实用的函数（可以用正则表达式代替）——starts-with和contains；

a=response.xpath('//a[starts-with(@title,"注册时间")]') a=response.xpath('//a[contains(text(),"闻")]')123

3. 提取元素或元素的属性值

首先是最基本的extract()函数，提取被定为的元素对象a=response.xpath('//a[contains(text(),"闻")]').extract() //如果被定为的元素对象有多个，可以有用下标指定 a=response.xpath('//a[contains(text(),"闻")]').extract()[1]1234提取元素的属性//提取text a=response.xpath('//a[contains(text(),"闻")]/text()').extract() //获取href a=response.xpath('//a[contains(text(),"闻")]/@href').extract() //获取name a=response.xpath('//a[contains(text(),"闻")]/@name').extract()12345678

此时我们的正则表达式又闲不住了（scrapy自带的函数），可以对提取的元素进行选择

//对href中的部分字符串进行选择 response.xpath('//a[@name="_l_p_n"]/@href').re('\/s.*?list\.htm')12

在这里关于xpath的所有用法基本总结完毕，只是由于xpath是对静态元素进行匹配选择，对于javascript往往束手无策，这时不得不用一个自动化测试工具——selenium，可以实现各种动态事件和静态元素的选择，只是selenium往往比较吃内存，响应时间也比较慢，对于大型的爬虫任务尽量不要使用，毕竟有一些javascript元素是内嵌在网页代码中的，这时候结合万能的正则表达式，xpath往往能够实现。如下：

link = re.search("javascript:goToPage\('(.*?)'", value) //value为包含该段的字符串1

以上

