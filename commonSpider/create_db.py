import pymysql

# 创建mysql数据库

class CreateDB(object):
    def __init__(self):
        self.conn = pymysql.connect('192.168.43.249', 'develop', 'poo001')
        self.cursor = self.conn.cursor()

    def create_db(self):
        # 创建数据库
        sql = """
        create database if not exists crawl charset=utf8;
        """
        self.cursor.execute(sql)
        self.cursor.close()
        self.conn.close()

    def create_table(self):
        # 创建表
        self.conn = pymysql.connect('192.168.43.249', 'develop', 'poo001', 'crawl')
        self.cursor = self.conn.cursor()
        sql = """
        create table if not exists chengyu (
        id INT auto_increment PRIMARY KEY,
        title VARCHAR(20) NOT NULL UNIQUE,
        pronounce VARCHAR(20),
        paraphrase VARCHAR(200),
        reference VARCHAR(200),
        influence INT,
        link VARCHAR(100)
        )
        """
        self.cursor.execute(sql)
        self.cursor.close()
        self.conn.close()


d = CreateDB()
d.create_db()
d.create_table()
print('ok')