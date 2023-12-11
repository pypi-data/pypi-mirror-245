# -*- coding: utf-8 -*-
import datetime
import pandas
import typing
import chinese_calendar
import os
import configparser
import warnings
import pymongo
from ZYYA_Codes.utils.cons import *


def to_date(
        x: typing.Union[str, datetime.date, datetime.datetime,]
) -> datetime.date:
    """
    将任何格式的时间转化为日期
    :param x: 任何格式的时间
    :return: 日期
    """
    return pandas.to_datetime(x).date()


def get_fridays(
        start: typing.Union[str, datetime.date, datetime.datetime,],
        end: typing.Union[str, datetime.date, datetime.datetime,]
) -> typing.List[datetime.date]:
    """
    获取给定时间段内每周的最后一个交易日
    :param start: 起始日期
    :param end: 终止日期
    :return:
    """
    Calendar = chinese_calendar.get_workdays(to_date(start), to_date(end))
    for date in Calendar.copy():
        if datetime.datetime.weekday(date) > 4:
            Calendar.remove(date)
    Calendar.sort()
    for date in Calendar.copy():
        if date + datetime.timedelta(days=1) in Calendar:
            Calendar.remove(date)
    return Calendar


def set_configs(**kwargs) -> None:
    path = os.path.expanduser("~")
    configfile_path = os.path.join(path, CONFIG_FILENAME)
    config = configparser.ConfigParser()
    config.read(configfile_path, encoding="utf-8")
    data: typing.Dict[str, dict] = {x: {y: z for y, z in config[x].items()} for x in config.sections()}

    Company_ip = kwargs.get("Company_ip", None)
    Tushare_token = kwargs.get("Tushare_token", None)
    MongoDB_port = kwargs.get("MongoDB_port", None)
    MongoDB_username = kwargs.get("MongoDB_username", None)
    MongoDB_password = kwargs.get("MongoDB_password", None)

    def email_info(info) -> typing.Union[typing.Dict[str, str], None]:
        if isinstance(info, dict):
            username = info.get("username", None)
            password = info.get("password", None)
            if username and password:
                return {
                    "username": str(username),
                    "password": str(password),
                }
            else:
                raise ValueError("账户名或密码缺失，请重新输入")
        elif not info:
            return None
        else:
            raise TypeError("邮箱账号密码输入格式有误")

    TYB_email = email_info(kwargs.get("tyb_email_info"))
    YYB_email = email_info(kwargs.get("yyb_email_info"))

    data.update(
        {
            "tushare_token": {
                "token": Tushare_token
            },
            "Company_Info": {
                "host": Company_ip,
                "domain": COMPANY_DOMAIN
            },
            "YYB_Email": YYB_email,
            "TYB_Email": TYB_email,
            "MongoDB": {
                "host": Company_ip,
                "port": MongoDB_port,
                "username": MongoDB_username,
                "password": MongoDB_password
            }
        }
    )
    for section, pairs in data.items():
        if section not in config.sections() and pairs:
            config.add_section(section)
        if pairs and isinstance(pairs, dict):
            for key, value in pairs.items():
                if value and isinstance(value, str):
                    config.set(section, key, value)
                    print(section, key, value)
                elif value and not isinstance(value, str):
                    warnings.warn("'%s==%s==%s' 参数未被录入， 请输入文本格式再次尝试" % (section, key, value))

    file = open(configfile_path, mode="w", encoding="utf-8")
    config.write(file)
    file.close()


def get_configs() -> typing.Dict[str, typing.Dict[str, str]]:
    path = os.path.expanduser("~")
    configfile_path = os.path.join(path, CONFIG_FILENAME)
    config = configparser.ConfigParser()
    config.read(configfile_path, encoding="utf-8")
    return {x: {y: z for y, z in config[x].items()} for x in config.sections()}


def Mongo_Client():
    return pymongo.MongoClient(
        host=get_configs().get("MongoDB", {}).get("host", None),
        port=int(get_configs().get("MongoDB", {}).get("port", None)),
        username=get_configs().get("MongoDB", {}).get("username", None),
        password=get_configs().get("MongoDB", {}).get("password", None),
    )
