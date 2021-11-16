#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @File ：request_test.py
# @Author ：orange
# @Date ：2021/11/15 下午10:58

# 测试请求
import json
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

        # 这里有坑，不能用urlencode，它会把参数中的空格转换成+号
        # self.data = bytes(parse.urlencode(data), encoding='utf-8')

        self.data = bytes(parse.quote(self.transfer_dict_to_str(data)), encoding='utf-8')
        self.headers = headers
        self.method = method

    def send_request(self):
        request = Request(url=self.url, data=self.data, headers=self.headers, method=self.method)
        response = urlopen(request)
        print('response: ', response.read().decode('utf-8'))

        pass

    def transfer_dict_to_str(self, param: dict) -> str:
        """
        将字典转换成查询字符串
        :param param:
        :return:
        """
        if not isinstance(param, dict):
            raise ValueError()
        param_list = []
        for key, value in param.items():
            # 暂时不考虑key不是字符串的情况
            if isinstance(value, (list, dict)):
                value = json.dumps(value)
            if isinstance(value, (int, float)):
                value = str(value)
            param_list.append(f'{key}={value}')
        query = '&'.join(param_list)
        return query


if __name__ == '__main__':
    url = 'http://127.0.0.1:8080/ret_json'
    header = {
        'Content-Type': 'text/html',
    }
    param = {
        'name': 'hello world',
        'age': 18,
        'like': 'game'
    }
    req_test = ReqTest(url, headers=header, data=param, method='POST')
    req_test.send_request()


