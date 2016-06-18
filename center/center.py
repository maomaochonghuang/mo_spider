from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from jsonrpc import JSONRPCResponseManager, dispatcher
import socket
import requests
import json,sys,time,copy
import collections,threading,thread
sys.path.append("..")
from utils.jsonrpc_sdk import *
from utils.db_opear import sql_select,sql_update,sql_executemany
from utils.entity_trans import *
from utils.common_func import *
from utils.proxy_client import *

global flag_ser_status # server status of activity , 0:not active,1:on serve,
global flag_finished_status # this task's status of finish , 0:doing ,1:done
flag_ser_status = 0
flag_finished_status = 0

PERSISTENT_PERIOD = 30
REFRESH_MAC_PERIOD = 30 #120 * 60

class CenterManger:
	
	task_info = None 
	local_ip_port = None
	ser_port = None
	order_type = 2 # 1: one by one ,2: sent batchly
	batch_num = 2
	sent_num = 0
	persistent_period = 90  # s
	client_addrs = []
	proxy_addrs = []
	last_persist_time = time.time()
	last_refresh_mac_time = time.time()
	master_ipaddr_port = 'localhost:4000'
	
	
	# load task info from database,DB ,TODO maybe change to become that the taskinfo is delivered by master.py using json
	def load( self,task_id) :
		sql = 'select ' + all_fields_task_info + 'from task_info where id = %d '  % task_id
		rows = sql_select(sql)
		if len(rows) == 1 :
			self.task_info = rows_to_taskinfo(rows[0])

	# 1.init task info,get client ips
	#  refresh_type ,1 : need to refresh client_info ,2: need to refresh proxy info
	#  command_source,0 : period refresh , 1: from master command
	def refresh_mac_info(self, refresh_type = [1,2] ,command_source = 0):
		if not command_source == 1 and not is_over_period(self.last_refresh_mac_time , REFRESH_MAC_PERIOD):
			return
		#self.client_addrs = ["localhost:7001"] #TODO load from DB 
		if 1 in refresh_type:
			sql = 'select ip,port from client_info where status = 1'
			rows = sql_select(sql)
			tmp_client_addrs = []
			for row in rows:
				tmp_client_addrs.append(row[0] + ':' + str(row[1]))
			self.client_addrs = tmp_client_addrs

		if 2 in refresh_type:
			sql = 'select ip,port from proxy_info where status = 1'
			rows = sql_select(sql)
			tmp_proxy_addrs = []
			for row in rows:
				tmp_proxy_addrs.append(row[0] + ':' + str(row[1]))
			self.proxy_addrs = tmp_proxy_addrs
			
		

	def __init__(self,task_id,task_port):
		self.load(task_id)
		self.ser_port = task_port
		#self.local_ip_port = socket.gethostbyname(socket.gethostname()) + ':' +str(task_port)
		self.local_ip_port = "localhost"  + ':' +str(task_port)
		if self.task_info is None or self.task_info._id <= 0 :
			print 'error,start center manger ,id = ', task_id
			return 
		self.refresh_mac_info()
		if self.order_type == 1 and self.batch_num != 1 :
			self.batch_num = 1

	# 1.send the order to proxy (crawler,js view)
	def order(self):
		method = 'ct2cl_order'
		crawler_type = 2
		tmp_headers = {}
		other_conditions = {}
		other_conditions['from_ip_port'] = self.local_ip_port
		need_sent_num = self.task_info._total - self.task_info._suc_num
		tmp_client_addrs = copy.deepcopy(self.client_addrs)
		for client_addr in tmp_client_addrs:
			if need_sent_num <= 0 :
				break
			cur_sent_num = self.batch_num if need_sent_num > self.batch_num else need_sent_num
			param_list = [self.task_info._id,self.task_info._type, crawler_type ,self.task_info._url,cur_sent_num,tmp_headers, other_conditions ]
			ret = jsonrpc_sent(client_addr,method,param_list)
			self.task_info._ordered_num += cur_sent_num
			need_sent_num -= cur_sent_num 
		

	# send http(s) req to proxy
	def proxy(self):
		method = 'ct2cl_proxy'
		crawler_type = 2
		tmp_headers = {}
		other_conditions = {}
		other_conditions['from_ip_port'] = self.local_ip_port
		need_sent_num = self.task_info._total - self.task_info._suc_num
		tmp_proxy_addrs = copy.copy(self.proxy_addrs)
		per_proxy_num = 20
		n = len(tmp_proxy_addrs) / per_proxy_num + 1
		for i in range (0,n):
			if need_sent_num <= 0 :
				break
			start_index = i * per_proxy_num 
			end_index = (i+1) * per_proxy_num
			tmp_cur_proxy_addrs = tmp_proxy_addrs[start_index:end_index]
			cur_count = len(tmp_cur_proxy_addrs)
			if cur_count == 0:
				break 
			cur_sent_num = self.batch_num if need_sent_num > self.batch_num else need_sent_num
			param_list = [self.task_info._id,self.task_info._type, crawler_type ,self.task_info._url,cur_count,tmp_headers, other_conditions ]
			suc_num = batch_proxy_get(self.task_info._url,tmp_cur_proxy_addrs)
			#ret = jsonrpc_sent(client_addr,method,param_list)
			self.task_info._ordered_num += cur_count
			need_sent_num -= cur_count 
			r_dict = {'req_num':cur_count,'suc_num':suc_num}
			self.recv_report(r_dict)
		

	# task excuted ,this class main function
	def run(self):
		print 'run start..........'
		global flag_finished_status 
		if self.task_info._total <= self.task_info._finish_num :
			print 'is enough',self.task_info._total ,self.task_info._finish_num
			flag_finished_status = 1
		else :
			self.order()
			self.proxy()
		self.persistent()
		self.check_task()
		self.refresh_mac_info(command_source = 1)
		print self.client_addrs
		#print self.proxy_addrs
		print 'run end..........'

	def recv_response(self,json_str):
		print 'recv_response',json_str
		json_dict = None
		try :
			json_dict = json.loads(json_str)
		except :
			print 'recv_response json loads error',json_str
			return 
		# 1. OK ,from master
		# 2. OK ,from crawler
		# 3. update ,from crawler
		# 4. command ,from master


	# recv messages from listened port
	def recv_report(self,r_dict):
		print 'recv_response', r_dict
		# 1. update the number of cache
		self.task_info._finish_num += r_dict['req_num']
		self.task_info._suc_num += r_dict['suc_num']
		print 'task_info number ' , self.task_info._ordered_num,self.task_info._finish_num,self.task_info._suc_num
		#self.persistent()

	def persistent(self):
		if not is_over_period(self.last_persist_time , PERSISTENT_PERIOD):
			return 

		sql = 'update task_info set ' + update_task_number_fields % (self.task_info._ordered_num,self.task_info._finish_num,\
			self.task_info._suc_num) + ' where id = ' + str(self.task_info._id)
		ret = sql_update(sql)
		if ret > 0 :
			self.last_persist_time = time.time()
		else:
			print 'update db error',sql
	

	# report the info to master
	def report(self):
		pass

	#TODO
	def check_task(self):
		#1. check contorl info , eg:  
		#TODO 
		#2. check task finish situation
		#2. check if finished , send msg to master
		pass

	# check crawler ??
	def check(self):
		pass
	# cancel all orders that are running by crawlers
	#TODO
	def cancel(self):
		pass

	
class CenterSer():
	task_id = 0
	centerManger = None

	def __init__(self,task_id,task_port):
		self.task_id = task_id
		self.centerManger = CenterManger(task_id,task_port)

	def recv_report(self,r_dict):
		print 'gettttttttttttttt ', r_dict
		self.centerManger.recv_report(r_dict)

	@Request.application
	def application(self,request):
		# Dispatcher is dictionary {<method_name>: callable}
		dispatcher["echo"] = lambda s: s
		dispatcher["cl2ct_report"] = self.recv_report
		print 'revice data',request.data

		response = JSONRPCResponseManager.handle(
			request.data, dispatcher)
		return Response(response.json, mimetype='application/json')

	def server(self,ser_port):
		global flag_ser_status
		print 'CenterSer App will start '
		t = threading.Timer(2.0,self.center_mgr_loop)
		t.start()
		flag_ser_status = 1
		run_simple('localhost', ser_port, self.application)
		flag_ser_status =  0
		print '........................end'

	def center_mgr_loop(self):
		global flag_ser_status
		while flag_ser_status == 1:
			print 'manger ............ '
			self.centerManger.run()
			time.sleep(10)


if __name__ == "__main__":
	print len(sys.argv)
	if len(sys.argv) < 3:
		print 'start center server fail,cause the argv len is ' ,len(sys.argv)
		sys.exit(0)
	if not sys.argv[1].startswith('task_id=') or not sys.argv[2].startswith('task_port=') :
		print 'start center server fail,cause the input argv is error :' ,sys.argv
		sys.exit(0)
	task_id  = int(sys.argv[1].split('=')[1])
	task_port  = int(sys.argv[2].split('=')[1])
	centerServer =  CenterSer(task_id,task_port)
	centerServer.server(task_port)

		


