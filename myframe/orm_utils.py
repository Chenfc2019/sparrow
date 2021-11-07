#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @File ：orm_utils.py
# @Author ：orange
# @Date ：2021/11/7 上午11:27

# 实现一个简单的orm工具
# 参考：https://blog.csdn.net/qq_39466701/article/details/104453202

from myframe.sql_utils import sql_get_data


class Model(type):
    def __new__(cls, name, base, attrs):
        """

        :param name: 类名
        :param base: 父类的名字
        :param attrs: 类属性
        """
        mappings = dict()
        for k, v in attrs.items():
            if isinstance(v, tuple):
                mappings[k] = v

        for k in mappings.keys():
            attrs.pop(k)

        attrs['__mapping__'] = mappings
        attrs['__table__'] = name.lower()

        return type.__new__(cls, name, base, attrs)


class Hero(metaclass=Model):
    id = ('id', 'int')
    name = ('name', 'varchar(30)')
    power = ('power', 'int')

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def save(self):
        field = []
        args = []
        for k, v in self.__mapping__.items():
            if hasattr(self, v[0]):
                field.append(v[0])
            args.append(getattr(self, k, None))

        temp_args = []
        for info in args:
            if isinstance(info, int):
                temp_args.append(str(info))
            elif isinstance(info, str):
                temp_args.append(f"'{info}'")
        sql_text = f"insert into {self.__table__} ({','.join(field)}) values ({','.join(temp_args)});"
        print(sql_text)
        result = sql_get_data(sql_text)
        return result


if __name__ == '__main__':
    hero = Hero(name='orm_add', power=78)
    hero.save()
