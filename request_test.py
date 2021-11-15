#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @File ：request_test.py
# @Author ：orange
# @Date ：2021/11/15 下午10:58

# 测试请求

from urllib.request import Request, urlopen
from urllib import parse


# url = 'http://127.0.0.1:8080/ret_json'
# header = {
#     'Content-Type': 'text/html',
# }
# param = {
#     'name': 'hello world'
# }
# data = bytes(parse.urlencode(param), encoding='utf-8')
# request = Request(url=url, data=data, headers=header, method='POST')
# response = urlopen(request)
# print(response.read().decode('utf-8'))


class ReqTest():
    def __init__(self, url, data={}, headers={}, method='GET'):
        self.url = url
        self.data = bytes(parse.urlencode(data), encoding='utf-8')
        self.headers = headers
        self.method = method

    def send_request(self):
        request = Request(url=self.url, data=self.data, headers=self.headers, method=self.method)
        response = urlopen(request)
        print(response.read().decode('utf-8'))
        pass


if __name__ == '__main__':
    url = 'http://127.0.0.1:8080/ret_json'
    header = {
        'Content-Type': 'text/html',
    }
    param = {
        'name': 'hello world'
    }
    req_test = ReqTest(url, headers=header, data=param, method='POST')
    req_test.send_request()


