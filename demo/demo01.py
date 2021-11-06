#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @File ：demo01.py
# @Author ：orange
# @Date ：2021/10/31 下午2:41

# 简单的HTTP服务器，可以接受多个客户段请求，并返回数据

import socket


def service_clint(new_socket):
    """
    客户段的套接字
    :param new_socket:
    :return:
    """
    # 1. 接受浏览器请求
    request = new_socket.recv(1024)
    print('req_data: ', request.decode('utf-8'))
    # 2. 返回http格式的数据
    # HTTP/1.1 200 OK
    #
    # test demo

    # http header
    response = 'HTTP/1.1 200 OK\r\n'
    # 空行
    response += '\r\n'
    # http body
    response += 'test demo'
    # tcp传输需要编码成字节流
    new_socket.send(response.encode('utf-8'))

def main():
    # 1. 创建套接字
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 2. 绑定端口
    tcp_socket.bind(('', 8080))
    # 3. 监听请求
    tcp_socket.listen(10)
    # 4. 等待客户段的请求
    while True:
        # 处理客户段的请求，返回客户段的套接字和客户端IP
        new_socket, client_addr = tcp_socket.accept()
        service_clint(new_socket)
    # 5. 关闭链接
    tcp_socket()


if __name__ == '__main__':
    print('---服务端开启---')
    main()
