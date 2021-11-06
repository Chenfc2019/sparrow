#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @File ：mini_frame.py
# @Author ：orange
# @Date ：2021/11/4 上午8:38

import re
from .sql_utils import sql_get_data

url_map = {}


# 带参数的装饰器实现路由功能
def route(path):
    def set_func(func):
        url_map[path] = func
        def call_func(*args, **kwargs):
            return func(*args, **kwargs)
        return call_func
    return set_func


@route('/index')
def index():
    with open('./template/index.html', 'r') as f:
        file_content = f.read()
    sql_text = 'select * from hero;'
    result = sql_get_data(sql_text)
    html = '<table border="1">'
    for info in result:
        html += f'<tr><th>{info[0]}</th><th>{info[1]}</th><th>{info[2]}</th></tr>'
    html += '</table>'
    return re.sub(r'{content}', html, file_content)


@route('/login')
def login():
    with open('./template/login.html', 'r') as f:
        file_content = f.read()
    return file_content


def application(environ, start_response):
    """
    实现uwsgi协议的函数
    :param environ: 字典
    :param start_response: 函数引用
    :return:
    """
    start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
    path = environ.get('path')
    print('path: ', path)

    if path in url_map and callable(url_map[path]):
        return url_map[path]()
    return 'resource not found'