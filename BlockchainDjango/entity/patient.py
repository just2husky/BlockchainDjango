#!/usr/bin/python3
# -*- coding: UTF-8 -*-


class Patient(object):
    """
    记录病人的信息，存储在一个Transaction对象的 content field 中。
    """

    def __init__(self, identifier, name, gender, age, nation, born_loc, address):
        """
        初始化类成员
        :param identifier: 病人的ID，如身份证等
        :param name:
        :param gender:
        :param age:
        :param nation:
        :param born_loc: 出生地
        :param address:
        """
        self.identifier = identifier
        self.name = name
        self.gender = gender
        self.age = age
        self.nation = nation
        self.born_loc = born_loc
        self.address = address
