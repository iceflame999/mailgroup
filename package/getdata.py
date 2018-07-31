#!/usr/bin/env python
# coding=utf-8
'''
调用mysql数据库
'''

import pymysql

def getgroup():
    group = []
    db = pymysql.connect("连接信息")
    cursor = db.cursor()
    sql = "select group_id,group_name from `group`;"
    cursor.execute(sql)
    cur1 = cursor.fetchone()
    while cur1:
        group.append((cur1[0],cur1[1]))
        cur1 = cursor.fetchone()
    db.close()
    return group

def addgroup(groupname, groupid):
    db = pymysql.connect("连接信息")
    cursor = db.cursor()
    sql = "insert into `group` values('"+ groupid + "','" + groupname+"');"
    cursor.execute(sql)
    db.commit()
    db.close()
    return 1

def delgroup(groupid):
    db = pymysql.connect("连接信息")
    cursor = db.cursor()
    sql = "delete from `group` where group_id='" + groupid + "';"
    cursor.execute(sql)
    db.commit()
    sql = "delete from admin where group_id='" + groupid + "';"
    cursor.execute(sql)
    db.commit()
    db.close()
    return 1


def getadmin(username):
    admin = []
    username = username + "邮箱域名"
    db = pymysql.connect("连接信息")
    cursor = db.cursor()
    sql = "select group_id,group_admin from admin where group_admin = '" + username + "';"
    cursor.execute(sql)
    cur1 = cursor.fetchone()
    while cur1:
        admin.append(cur1[0])
        cur1 = cursor.fetchone()
    db.close()
    return admin

def addadmin(groupid,username):
    username = username
    db = pymysql.connect("连接信息")
    cursor = db.cursor()
    sql = "insert into admin values('"+ groupid + "','" + username +"');"
    print(sql)
    cursor.execute(sql)
    db.commit()
    db.close()
    return 1

def deladmin(groupid,username):
    db = pymysql.connect("连接信息")
    cursor = db.cursor()
    sql = "delete from admin where group_id = '" + groupid + "' and group_admin = '"+ username+ "';"
    cursor.execute(sql)
    db.commit()
    db.close()
    return 1