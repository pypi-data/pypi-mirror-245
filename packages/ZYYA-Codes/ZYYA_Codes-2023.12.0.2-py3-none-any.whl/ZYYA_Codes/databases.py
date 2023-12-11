# -*- coding: utf-8 -*-
"""
@Time ： 2023/9/15 19:50
@Auth ： Alan Gong
@File ：databases.py
@IDE ：PyCharm
"""
import pymongo

Client = pymongo.MongoClient(host="122.224.101.242", port=27017)


def authenticate(username, password):
    global Client
    Client = pymongo.MongoClient(host="122.224.101.242", port=27017, username=username, password=password)
    Client.list_database_names()
