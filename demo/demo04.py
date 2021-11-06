#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @File ：demo04.py
# @Author ：orange
# @Date ：2021/11/1 下午11:04

# 简单的支持携程的HTTP服务器

import re
import socket
import gevent
from gevent import monkey

monkey.patch_all()


def service_clint(new_socket):
    """
    客户段的套接字
    :param new_socket:
    :return:
    """
    # 1. 接受浏览器请求
    request = new_socket.recv(1024)
    print('req_data: ', request.decode('utf-8'))
    # GET /index.html HTTP/1.1
    request_lines = request.decode('utf-8').splitlines()
    print(request_lines[0])
    # 匹配出请求的文件
    ret = re.match(r'[^/]+(/[^ ]*)', request_lines[0])
    file_name = ''
    if ret:
        file_name = ret.group(1)
        if file_name == '/':
            file_name = '/index.html'
    else:
        print('未找到文件')
    # 2. 返回http格式的数据
    # HTTP/1.1 200 OK
    #
    # test demo

    # 读出请求的静态文件放在body中返回给前端
    try:
        f = open('./html' + file_name, 'rb')
        html_content = f.read()
        # http header
        response = 'HTTP/1.1 200 OK\r\n'
        # 空行
        response += '\r\n'
        # http body
        # tcp传输需要编码成字节流
        new_socket.send(response.encode('utf-8'))
        new_socket.send(html_content)
        f.close()
    except Exception as e:
        print('err_msg: ', e)
        response = 'HTTP/1.1 404 NOT FOUND\r\n'
        response += '\r\n'
        response += 'file not found'
        new_socket.send(response.encode('utf-8'))

    # 关闭套接字
    new_socket.close()

def main():
    # 1. 创建套接字
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 2. 绑定端口
    tcp_socket.bind(('', 8899))
    # 3. 监听请求
    tcp_socket.listen(10)
    # 4. 等待客户段的请求
    while True:
        # 处理客户段的请求，返回客户段的套接字和客户端IP
        new_socket, client_addr = tcp_socket.accept()
        gevent.spawn(service_clint, new_socket)
        # 创建子进程时会复制父进程中的资源，new_socket被复制到子进程，父进程中的socket也需要关闭

    # 5. 关闭链接
    tcp_socket()


if __name__ == '__main__':
    print('---服务端开启---')
    main()

