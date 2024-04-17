# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import openpyxl
import pymysql


class DBPipeline:
    """链接数据库的"""
    def __init__(self):
        self.conn = pymysql.connect(host="127.0.0.1", port=3306,
                                    user="root", password="root123",
                                    database="movie_demo", charset="utf8mb4")
        self.cursor = self.conn.cursor()
        # 批处理用到
        self.data = []
        ...

    def open_spider(self, spider):
        ...

    def close_spider(self, spider):
        # 写入数据库后要commit提交一下
        # self.conn.commit()
        # 批处理的话要考虑到，爬取完成，数据量未达到100，要在关闭代码的时候再写入数据库一次
        if len(self.data) > 0:
            self.wright_to_db()
        self.conn.close()
        ...

    def process_item(self, item, spider):
        title = item.get("title", "")
        pingfen = item.get("pingfen", "")
        # 等数据爬取完成，统一塞入数据库
        # self.cursor.execute(
        #     'insert into movie_demo (title, pingfen) values (%s, %s)', (title, pingfen))
        # 批处理的话
        self.data.append((title, pingfen))
        if len(self.data) == 100:
            self.wright_to_db()
            self.data.clear()
        return item

    def wright_to_db(self):
        """
        批处理用这个
        """
        self.cursor.execute(
            'insert into movie_demo (title, pingfen) values (%s, %s)', self.data)
        self.conn.commit()


class ExcelPipeline:
    def __init__(self):
        self.wb = openpyxl.Workbook()
        self.ws = self.wb.active
        self.ws.title = "Top250"
        self.ws.append(("标题", "评分"))

    def open_spider(self, spider):
        """
        爬虫开始的时候要干啥
        """
        ...

    def close_spider(self, spider):
        """
        爬虫运行完成保存数据到excel中
        """
        self.wb.save('电影数据.xlsx')

    def process_item(self, item, spider):
        title = item.get("title", "")
        pingfen = item.get("pingfen", "")
        self.ws.append((title, pingfen))
        return item
