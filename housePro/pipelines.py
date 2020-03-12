# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class HouseproPipeline(object):
    def process_item(self, item, spider):
        # print(item)
        return item


class beikePipeline(object):

    conn = None
    cursor = None

    def open_spider(self, spider):
        self.conn = pymysql.connect(host='localhost',port=3306,db='jobdata',user='root',password='')
        print(self.conn)
    def process_item(self, item, spider):


        self.cursor = self.conn.cursor()
        try:
            with self.cursor as cursor:
                #查询是否重复的语句
                searchSql = """select distinct houseCode from tb_beike where houseCode = '%s'"""
                cursor.execute(searchSql%item['houseCode'])
                result = cursor.fetchone()
                #如果为空，表示没有查询到重复的信息
                if result is None:
                    insertSql = """insert into tb_beike(title, location, price, houseCode,longlatitude, pageNum) values (%s,%s,%s,%s,%s,%s)"""
                    #再次提交插入语句
                    cursor.execute(
                    insertSql,(item['title'],item['location'],item['price'],item['houseCode'],item['longlatitude'],item['page']))
                    self.conn.commit()
                    print("数据添加成功")
                else:
                    print("数据已存在%s:%s"%(item['title'],item['houseCode']))
        # 这里就是判断，如果有异常，就打印异常，然后回滚事物。否则就直接提交
        except Exception as e:
            print(e)
            self.conn.rollback()

        return item

    def close_spider(self,spider):
        self.conn.close()
        self.cursor.close()