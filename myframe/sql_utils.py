#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @File ：sql_utils.py
# @Author ：orange
# @Date ：2021/11/6 下午7:24

import sys
from pymysql import *
import config


# SQL工具
class SqlUtil(object):
    def __init__(self):
        mysql_config = config.mysql_config
        self.conn = connect(host=mysql_config.host, port=mysql_config.port, user=mysql_config.user,
                       password=mysql_config.password, database=mysql_config.db_name)

    def execute_sql(self, sql_text):
        cursor = self.conn.cursor()
        count = cursor.execute(sql_text)
        result = cursor.fetchall()
        self.conn.commit()
        cursor.close()
        self.conn.close()
        return result


def sql_get_data(sql_text):
    if not sql_text:
        return []
    sql_util = SqlUtil()
    result = sql_util.execute_sql(sql_text)
    return result


if __name__ == '__main__':
    result = sql_get_data("insert into hero (name,power) values ('util_add',59);")
    print(result)
