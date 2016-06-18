#! /usr/bin/env python
#coding=utf8
import time

class TaskInfo:
	_id = None
	_name = None
	_title = None
	_url = None
	_type = None
	_total = 0
	_finish_num = 0
	_suc_num = 0
	_speed = None
	_init_num = None
	_status = 0
	_contorl_cmd = 0
	_create_time = time.time()
	_last_update_tme = None
	_start_time = None
	_finish_time = None
	_ordered_num = 0

	# analyse which crawler type be used ,according to the url domain,task type etc
	def parse_crawler_type():
		return 2
		
		
