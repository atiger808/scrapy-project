#coding=utf-8
import requests #请求模块
from lxml import etree #解析模块
#import re #正则表达式(备用)
#import os #操作访问系统的模块（此处用于创建文件夹）
#import xlsxwriter #操作xls文件
import pymysql #操作数据库模块
#import smtplibfrom email.mime.text
#import MIMEText #此模块可以用于发送正文
#from email.mime.multipart import MIMEMultipart #此模块用于发送带附件的邮件
#from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED, FIRST_COMPLETED
import time
from queue import Queue
from threading import Thread
import threading





class comSpider(object):
    """docstring for comSpider"""
    def __init__(self):
        super(comSpider, self).__init__()
        self.headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
        self.url_head='http://detail.zol.com.cn'
        #url队列
        self.url_queue=Queue()
        #单个页面队列
        self.page_queue=Queue()
        #数据队列
        self.data_queue=Queue()


    def addurl_queue(self):
        L1=[]
        home_url='http://detail.zol.com.cn/notebook_index/subcate16_list_1.html'
        home_data=requests.get(home_url,headers=self.headers).text
        home_html = etree.HTML(home_data)
        brand_url=home_html.xpath('//*[@id="J_ParamBrand"]/a/@href')
        for x in range(len(brand_url)):
            brand_data=requests.get('http://detail.zol.com.cn'+brand_url[x],headers=self.headers).text
            brand_html= etree.HTML(brand_data)
            page_url=brand_html.xpath('//*[@id="J_PicMode"]/li/a/@href')
            L1=L1+page_url
#        print(L1)
        for i in range(len(L1)):
            self.url_queue.put(self.url_head+L1[i])


    def addpage_queue(self):
        url=self.url_queue.get()
#        print(url)
        resp=requests.get(url,headers=self.headers)
        self.page_queue.put(resp.text)
        self.url_queue.task_done()


    def adddata_queue(self):
        page=self.page_queue.get()
#        print(page)
        page_html=etree.HTML(page)
        name=page_html.xpath('/html/body/div/h1/text()')
#        for i in range(len(name)):
#            name=name[i]
#            name.encode('utf-8')
#        name_list=list(name)
#        print(name)
        price=page_html.xpath('/html/body/div/div/div/div/span/b[2]/text()')
#        for i in range(len(price)):
#           price=price[i]
#            price.encode('utf-8')
#        price_list=list(price)
        parameter=page_html.xpath('/html/body/div/div/div/div/ul/li/p/text()')
#        for i in range(len(parameter)):
#            parameter=parameter[i]
#            parameter.encode('utf-8')
#        parameter_list=list(parameter)

        data=name+price+parameter
        data=[str(i)for i in data]
#        print(type(data[0]),type(data[1]),type(data[2]),type(data[3]),type(data[4]),type(data[5]),type(data[6]),type(data[7]),type(data[8]),type(data[9]),)
        self.data_queue.put(data)
        self.page_queue.task_done()

    def sava_mysql(self):
        data=self.data_queue.get()
        print(data)
        db=pymysql.connect(host='localhost', user='root', password='XXXXXXXX', port=3306, db='comeputerdata')
        cursor= db.cursor()
#        time.sleep(2)
#        sql1=sql='''CREATE TABLE IF NOT EXISTS com_chart(Brand VARCHAR(255) NOT NULL,Price INT NOT NULL,ScreenSize VARCHAR(255) NOT NULL,ScreenResolution VARCHAR(255) NOT NULL,CPUmodel VARCHAR(255) NOT NULL,Core VARCHAR(255) NOT NULL,GPU VARCHAR(255) NOT NULL,MemoryCapacity VARCHAR(255) NOT NULL,BatteryLife VARCHAR(255) NOT NULL,Endurance VARCHAR(255) NOT NULL,PRIMARY KEY (Brand))'''
#        cursor.execute(sql1)
        time.sleep(2)
        sql2='''INSERT INTO com_chart(Brand,Price,ScreenSize,ScreenResolution,CPUmodel,Core,GPU,MemoryCapacity,BatteryLife,Endurance)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
#        try:
        cursor.execute(sql2,data)
        db.commit()
#        except:
#            print('数据写入失败')
#            db.rollback()
        db.close()
        self.data_queue.task_done()


    def run(self):
        list1=[]
        list2=[]
        list3=[]
        # 开启线程执行上面的几个方法
        url_t=threading.Thread(target=self.addurl_queue)
        # url_t.setDaemon(True)
        url_t.start()
        for i in range(500):
            t=Thread(target=self.addpage_queue())
            list1.append(t)
            t.start()

        for i in range(500):
            t=Thread(target=self.adddata_queue())
            list2.append(t)
            t.start()

        for i in range(500):
            t=Thread(target=self.sava_mysql())
            list3.append(t)
            t.start()
#        self.run_use_more_task(self.adddata_queue, 2)
#        self.run_use_more_task(self.sava_mysql, 2)
        # 使用队列join方法,等待队列任务都完成了才结束
#        self.url_queue.join()
#        self.page_queue.join()
#        self.data_queue.join()

        for t in list1:
            t.join()

        for t in list2:
            t.join()

        for t in list3:
            t.join()

if __name__ == '__main__':
    qbs=comSpider()
    qbs.run()

