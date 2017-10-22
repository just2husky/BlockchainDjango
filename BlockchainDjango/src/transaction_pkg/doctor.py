#!/usr/bin/python3
# -*- coding: UTF-8 -*-


class Doctor(object):
    """
        记录医生的信息，存储在一个Transaction对象的 content field 中。
    """

    def __init__(self, identifier, name, gender, age, nation, hospital, department, grade):
        """

        :param identifier:
        :param name:
        :param gender:
        :param age:
        :param hospital: 医生所属医院
        :param department: 医生所属科室
        :param grade: 医生等级
        """
        self.identifier = identifier
        self.name = name
        self.gender = gender
        self.age = age
        self.nation = nation
        self.hospital = hospital
        self.department = department
        self.grade = grade
