#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @File ：testdeno.py
# @Author ：orange
# @Date ：2021/10/31 下午2:31


# 简单的多进程服务器HTTP服务器

import re
import sys
import socket
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
import threading
from urllib import parse

from myframe import mini_frame


class Server(object):
    def __init__(self, port=8080):
        # 1. 创建套接字
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 防止端口被占用
        # 2. 绑定端口
        self.tcp_socket.bind(('', port))
        # 3. 监听请求
        self.tcp_socket.listen(10)
        print(f'server start with: 127.0.0.1:{port}')
        self.status = None
        self.headers = None
        self.th_pool = ThreadPoolExecutor(max_workers=3)

    def service_clint(self, new_socket):
        """
        客户段的套接字
        :param new_socket:
        :return:
        """
        # 1. 接受浏览器请求
        request = new_socket.recv(1024)
        req_data = request.decode('utf-8')
        # print('req_data: ', req_data.splitlines())
        # GET /index.html HTTP/1.1
        if not req_data:
            return
        request_lines = req_data.splitlines()
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

        file_type = file_name.split('.')
        if len(file_type) == 2 and file_type[1] in ['html', 'css', 'js']:
            # 2. 返回http格式的数据
            # 读出请求的静态文件放在body中返回给前端
            try:
                f = open('./template' + file_name, 'rb')
                html_content = f.read()
                print('html_content: ', html_content)
                # http header
                response = 'HTTP/1.1 200 OK\r\n'
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
        else:
            # 非静态请求，将请求转发到框架处理
            env = dict()
            env['path'] = file_name

            # 解析请求头和参数信息
            query_dict, header_dict = self.parse_param(request_lines, env)
            env['headers'] = header_dict
            env['query_dict'] = query_dict

            # 将请求转发给框架处理
            body = mini_frame.application(env, self.set_response_header)

            header = f'HTTP/1.1 {self.status}\r\n'
            for info in self.headers:
                header += f"{info[0]}:{info[1]}\r\n"

            header += '\r\n'
            response = header + body
            new_socket.send(response.encode('utf-8'))

        # 关闭套接字
        new_socket.close()

    def parse_param(self, request, env: dict) -> tuple:
        # request 为列表 ['POST /ret_json HTTP/1.1', 'Accept-Encoding: identity', 'Content-Length: 45', 'Host: 127.0.0.1:8080', 'User-Agent: Python-urllib/3.7', 'Content-Type: text/html', '', 'name%3Dhello%20world%26age%3D18%26like%3Dgame']
        # 列表最后一个元素是请求数据
        # 请求方法
        first_item = request[0].split(' ')
        method = first_item[0]
        env['method'] = method

        # 参数字典
        query_dict = {}
        # 判断请求方法，GET请求从URL提取参数，POST请求从body中提取参数
        if method == 'GET':
            url_params = first_item[1].split('?')[1].split('&')
            env['path'] = first_item[1].split('?')[0]
            for param in url_params:
                key, value = param.split('=')
                query_dict[key] = value
        elif method == 'POST':
            params_list = parse.unquote(request[-1]).split('&')
            for param in params_list:
                if not param and '=' in param:
                    key, value = param.split('=')
                    query_dict[key] = value
        else:
            pass

        # 请求头信息
        header_dict = {}
        for info in request[1:-2]:
            key, value = info.split(': ')
            header_dict[key] = value
        return query_dict, header_dict

    def set_response_header(self, status, headers):
        self.status = status
        self.headers = headers

    def run(self):
        # 4. 等待客户段的请求
        while True:
            # 处理客户段的请求，返回客户段的套接字和客户端IP
            new_socket, client_addr = self.tcp_socket.accept()
            # 使用线程池来处理请求
            self.th_pool.submit(self.service_clint, new_socket)
        self.th_pool.shutdown()

        #     p = multiprocessing.Process(target=self.service_clint, args=(new_socket, ))
        #     p.start()
        #     # 创建子进程时会复制父进程中的资源，new_socket被复制到子进程，父子进程中的new_socket只向同一个对象，
        #     # 只有当父子都关闭之后，new_socket的引用计数变为0才会被回收
        #     new_socket.close()
        #
        # # 5. 关闭链接
        # tcp_socket()


def main():
    input_args = sys.argv
    port = 8080
    if len(input_args) == 2:
        port = input_args[1]
    try:
        port = int(port)
    except Exception as e:
        print('输入端口号有误')
        raise ValueError

    server = Server(port)
    server.run()


if __name__ == '__main__':
    main()




