#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @File ：orm_utils.py
# @Author ：orange
# @Date ：2021/11/7 上午11:27

# 实现一个简单的orm工具
# 参考：https://blog.csdn.net/qq_39466701/article/details/104453202

from myframe.sql_utils import sql_get_data


class ModelMetaclass(type):
    def __new__(cls, name, base, attrs):
        """
        在init方法前调用
        :param name: 类名
        :param base: 父类的名字
        :param attrs: 类属性
        """
        mappings = dict()
        for k, v in attrs.items():
            if isinstance(v, tuple):
                mappings[k] = v

        # {
        #     'id': ('id', 'int'),
        #     'name': ('name', 'varchar(30)'),
        #     'power': ('power', 'int')
        # }

        # 删除子类的属性
        for k in mappings.keys():
            attrs.pop(k)

        attrs['__mapping__'] = mappings
        attrs['__table__'] = name.lower()

        return type.__new__(cls, name, base, attrs)


class Model(metaclass=ModelMetaclass):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def save(self):
        """
        保存一条数据
        :return:
        """
        field = []
        args = []
        for k, v in self.__mapping__.items():
            # 只添加实例中传入的字段
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

    def query_by_id(self, id):
        """
        根据ID查询记录
        :return:
        """
        sql_text = f"select * from {self.__table__} where id = {id};"
        result = sql_get_data(sql_text)
        if len(result) > 1:
            raise Exception
        result = result[0]
        self.id = result[0]
        self.name = result[1]
        self.power = result[2]


    def update_by_id(self, id):
        """
        根据id更新记录
        :param filter:
        :return:
        """
        field_list = []
        for k, v in self.__mapping__.items():
            # 只添加实例中传入的字段
            if hasattr(self, v[0]):
                field_list.append(f"{k}={getattr(self, k)}")

        sql_text = f"update {self.__table__} set {','.join(field_list)} where id = {id};"
        print(sql_text)
        result = sql_get_data(sql_text)


class Hero(Model):
    id = ('id', 'int')
    name = ('name', 'varchar(30)')
    power = ('power', 'int')


if __name__ == '__main__':
    # hero = Hero(name='orm_11ha', power=78)
    # hero.save()
    # hero.update_by_id(2)

    her02 = Hero()
    her02.query_by_id(1)
    print(her02)
