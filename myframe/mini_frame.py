#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @File ：mini_frame.py
# @Author ：orange
# @Date ：2021/11/4 上午8:38

def application(environ, start_response):
    """
    实现uwsgi协议的函数
    :param environ: 字典
    :param start_response: 函数引用
    :return:
    """
    start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
    print('path: ', environ.get('path'))
    if environ.get('path') == '/index.py':
        return index()
    elif environ.get('path') == '/login.py':
        return login()
    return 'hello'


def index():
    with open('./template/index.html', 'r') as f:
        file_content = f.read()
    return file_content


def login():
    with open('./template/login.html', 'r') as f:
        file_content = f.read()
    return file_content