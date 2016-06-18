#! /usr/bin/env python
#coding=utf8
import time
import MySQLdb
import sys

db_host = "127.0.0.1"
db_user = "root"
db_passwd = "123456"
db_name = "mo_spider"
reload(sys)
sys.setdefaultencoding('utf-8')

def sql_select(sql):
    conn=MySQLdb.connect(host=db_host,user=db_user,passwd=db_passwd,db=db_name,charset="utf8")  
    cursor = conn.cursor() 
    n = cursor.execute(sql) 
    rows = cursor.fetchall() 
    cursor.close() 
    conn.close()
    return rows

    
def sql_update(sql):
    conn=MySQLdb.connect(host=db_host,user=db_user,passwd=db_passwd,db=db_name,charset="utf8")  
    cursor = conn.cursor() 
    n = cursor.execute(sql) 
    conn.commit()
    cursor.close() 
    conn.close()
    return n

def sql_executemany(sql,entitys):
    conn=MySQLdb.connect(host=db_host,user=db_user,passwd=db_passwd,db=db_name,charset="utf8")  
    cursor = conn.cursor() 
    n = cursor.executemany(sql,entitys) 
    conn.commit()
    cursor.close() 
    conn.close()
    return n

