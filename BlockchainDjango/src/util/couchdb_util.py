#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import couchdb
from couchdb.http import ResourceNotFound
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# couchdb的地址
server_addr = 'http://localhost:5984/'


def init_db(db_name):
    """
    连接couchdb，并创建数据库 block_tree，若存在，则先进行删除操作
    :return:
    """
    couch = couchdb.Server(server_addr)
    logger.info("开始删除数据库 " + db_name)
    try:
        couch.delete(db_name)
    except ResourceNotFound:
        logger.info("数据库 " + db_name + " 不存在")
    else:
        logger.info("删除完成")

    logger.info("开始创建数据库 " + db_name)
    new_db = couch.create(db_name)
    logger.info("创建完成")
    return new_db


def get_db(db_name):
    """
    根据db_name返回对应的数据库
    :param db_name:
    :return:
    """
    server = couchdb.Server(server_addr)
    try:
        server[db_name]
    except ResourceNotFound:
        logger.info("数据库" + db_name + "不存在， 开始创建 ...")
        server.create(db_name)
        logger.info("创建完成")

    return server[db_name]


def save(param_db, doc_content):
    """
    将doc_content 的内容存储到数据库 db 中
    :param param_db:
    :param doc_content:
    :return: doc_id 与 rev
    """
    logger.info("开始向数据库写入: " + str(doc_content))
    doc_id, rev = param_db.save(doc_content)
    # param_db['_id'] = doc_content['id']
    logger.info("写入成功")
    return doc_id, rev


if __name__ == "__main__":

    db = init_db('test')
    doc = {'foo': 'bar'}
    arg_doc_id, arg_rev = save(db, doc)
    print("id: " + arg_doc_id)
    doc = db[arg_doc_id]
    print(doc['foo'])
