#! /usr/bin/env python
#coding=utf8
import time
import sys
sys.path.append("..")
from entity.task_info import *

reload(sys)
sys.setdefaultencoding('utf-8')

all_fields_task_info = '`id` ,`name` ,`title` ,`url` ,`type` ,`total`,`finish_num`,`suc_num` ,`speed`,`init_num`,`status` ,`create_time`,`last_update_tme` ,`start_time` ,`finish_time`,`ordered_num`'

update_task_number_fields = '`ordered_num` = %d ,`finish_num` = %d ,`suc_num` = %d  , `last_update_tme`=now()'

def rows_to_taskinfo(row):
	if row is None:
		return None
	info = TaskInfo()
	info._id = row[0]
	info._name = row[1]
	info._title = row[2]
	info._url = row[3]
	info._type = row[4]
	info._total = row[5]
	info._finish_num = row[6]
	info._suc_num = row[7]
	info._speed = row[8]
	info._init_num = row[9]
	info._status = row[10]
	info._create_time = row[11]
	info._last_update_tme = row[12]
	info._start_time = row[13]
	info._finish_time = row[14]
	info._ordered_num = row[15]
	return info
