#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @File ：client.py
# @Author ：orange
# @Date ：2021/10/31 下午4:43

# tcp的客户端

import socket


def main(num):
    # 1. 创建套接字
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 2. 链接服务器
    tcp_socket.connect(('127.0.0.1', 8080))
    # 3. 发送消息
    tcp_socket.send(f'我是客户端{num}'.encode('utf-8'))
    # 4. 接收信息
    tcp_recv = tcp_socket.recv(1024)
    print('接收信息：' + tcp_recv.decode('utf-8'))
    # 5. 关闭套接字
    tcp_socket.close()


if __name__ == '__main__':
    for num in range(5):
        main(num)
