#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @File ：mini_frame.py
# @Author ：orange
# @Date ：2021/11/4 上午8:38

import re
import logging
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
    return re.sub(r'{content}', 'hello', file_content)


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
        write_log(path)
        return url_map[path]()
    write_log(path + ' not found')
    return 'resource not found'


def write_log(log_msg):
    # https://www.cnblogs.com/xianyulouie/p/11041777.html
    # https://www.cnblogs.com/xybaby/p/9197032.html
    # 第一步，创建一个logger
    logger = logging.getLogger()
    # Log等级总开关
    logger.setLevel(logging.INFO)

    # 第二步，创建一个handler，用于写入日志文件
    # log_path = os.path.dirname(os.getcwd()) + '/logs/'
    logfile = './logs/sparrow.log'
    fh = logging.FileHandler(logfile, mode='a')
    # 输出到file的log等级的开关
    fh.setLevel(logging.INFO)

    # 输出到console的log等级的开关
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # 第三步，定义handler的输出格式
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # 第四步，将logger添加到handler里面
    logger.addHandler(fh)
    logger.addHandler(ch)

    # logging.basicConfig函数对日志的输出格式及方式做相关配置
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
    # 由于日志基本配置中级别设置为DEBUG，所以一下打印信息将会全部显示在控制台上
    logging.info(log_msg)
    logging.debug(log_msg)
    logging.warning(log_msg)
    logging.error(log_msg)
    logging.critical(log_msg)