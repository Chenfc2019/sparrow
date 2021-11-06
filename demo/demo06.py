#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @File ：demo06.py
# @Author ：orange
# @Date ：2021/11/4 下午9:39

import sys
import re

# 程序运行时传递参数

if __name__ == '__main__':
    print('sys: ', sys.argv)
    # 默认输入格式
    default_input = 'python manage.py runserver 127.0.0.1:6000 myframe:appliction'
    input_args = sys.argv
    if len(input_args) == 1:
        input_args = default_input.split(' ')[3:]
    else:
        input_args = input_args[2:]
    print('---', input_args)
    ret = re.match(r'(([\d]{1,3}\.){3}[\d]{1,3}|0):[\d]+', input_args[0])
    if not ret:
        print('输入参数格式有误')
    host = input_args[0].split(':')[0]
    if host == '0':
        host = '0.0.0.0'
    port = input_args[0].split(':')[1]
    frame = input_args[1].split(':')[0]
    application = input_args[1].split(':')[1]
    # 没传参数就以默认值运行
    print(f'host:{host}, port:{port}, frame:{frame}, app:{application}')
