from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from jsonrpc import JSONRPCResponseManager, dispatcher
import requests
import json,sys,time
import collections,threading,thread
sys.path.append("..")
from utils.db_opear import sql_select,sql_update,sql_executemany
from utils.entity_trans import *
from utils.common_func import *


TASK_CENTER_BASE_PORT = 6000

global flag_ser_status
flag_ser_status = 0

# ready tasks info cache,for paused tasks,loaded tasks
global ready_tasks,running_tasks,paused_tasks,finished_task
ready_tasks = collections.deque(maxlen = 100)
# running tasks info cache 
running_tasks = collections.deque(maxlen = 100)
# paused tasks info cache 
paused_tasks = collections.deque(maxlen = 100) 	
# finished tasks info cache ,for success finish or stoped tasks 
finished_tasks = collections.deque(maxlen = 100)



class MasterManger():
	global ready_tasks,running_tasks,paused_tasks,finished_task
	
	# load task info from database,DB --> ready task queue
	def load( self,status) :
		sql = 'select ' + all_fields_task_info + 'from task_info where status = %d '  % status
		print 'load ...', sql
		rows = sql_select(sql)
		for row in  rows:
			ready_tasks.append(rows_to_taskinfo(row)) 
		print 'ready fun ,ready_tasks' ,len(ready_tasks),'running_tasks',len(running_tasks),'finished_tasks',len(finished_tasks),'paused_tasks',len(paused_tasks)

	# 1 start task info, ready queue --> running queue
	# 2 folk a process (center for specified task) 
	# 3 check process usability 
	# 4 update status to db
	def start(self):
		started_taskid = []
		sql = 'update task_info set status = %d  where status = %d and id = %d '  
		while  len( ready_tasks ) > 0 :
			task = ready_tasks.pop()
			tmp_sql = sql % (1 , 0 , task._id)
			print tmp_sql
			update_num  = sql_update( tmp_sql)
			if update_num == 0 :
				print 'sql update warn ',tmp_sql
				continue
			status , process_id = self. __folk_center_process(task)
			if status == 0 and process_id > 0:
				running_tasks.append(task)	
				started_taskid.append(task._id)
			else :
				tmp_sql = sql % (99 , 1 , task._id)
				update_num  = sql_update( tmp_sql)
				print 'start center error and update to status 99,task.id = ',task._id
		print 'start fun ,ready_tasks' ,len(ready_tasks),'running_tasks',len(running_tasks),'finished_tasks',len(finished_tasks),'paused_tasks',len(paused_tasks)
		print 'started_taskid list' ,started_taskid
		return started_taskid
		

	# 1 read running_task finish num
	# 2 update to DB ,finish num, fail num
	# 3 if success num >= total num ,running --> finished
	# 4 kill process (center for specified task)
	def check_finish(self):
		sql = 'select ' + all_fields_task_info + 'from task_info where status = 1 and total <= suc_num '
		u_sql = 'update task_info set status = 2 where status = 1 and id = %d ' 
		rows = sql_select(sql)
		temp_running_tasks = list(running_tasks )
		for row in  rows:
			task = rows_to_taskinfo(row)
			for temp_task in temp_running_tasks:
				# match the same id of task in cache
				if temp_task._id != task._id :
					continue
				finished_tasks.append(temp_task)
				running_tasks.remove(temp_task)
		print 'check_finish fun ,ready_tasks' ,len(ready_tasks),'running_tasks',len(running_tasks),'finished_tasks',len(finished_tasks),'paused_tasks',len(paused_tasks)
	
	# 1 read running_task finish num,and update info to DB
	# 2 kill process (center for specified task)
	def check_stop(self):
		u_sql = 'update task_info set status = 2 ,finish_time = now() where id = %d'
		while len (finished_tasks) > 0 :
			task = finished_tasks.pop()
			status = self.__kill_process(task)
			tmp_sql = u_sql % task._id 
			update_num = sql_update( tmp_sql )
			if update_num == 0 :
				print 'stop fun','sql update warn ',tmp_sql
				continue
			print 'check_stop fun ,ready_tasks' ,len(ready_tasks),'running_tasks',len(running_tasks),'finished_tasks',len(finished_tasks),'paused_tasks',len(paused_tasks)

	# 1 read running_task finish num,and update info to DB
	# 2 kill process (center for specified task)
	# 3 running --> paused 
	def pause(self, taskid):
		sql = 'select ' + all_fields_task_info + 'from task_info where status = 1 and contorl_cmd = 3 and id = %d ' % int(taskid)
		pass

	# 1 paused -- > running
	def tocontinue(self,taskid):
		sql = 'select ' + all_fields_task_info + 'from task_info where status = 3 and contorl_cmd = 4 and id = %d ' % int(taskid)
		pass

	# 1 paused, running --> stopped
	def stop(self,taskid):
		sql = 'select ' + all_fields_task_info + 'from task_info where status in (1,2) and contorl_cmd = 2 and id = %d ' % int(taskid)
		pass


	# 1 manger all excute task
	def manger(self):
		# load new task
		self.load(status = 0 )
		started_taskids = self.start()
		finished_taskids = self.check_finish()

	# recv messages from listened port
	def recv_response(self,json_str):
		print 'recv_response',json_str
		json_dict = None
		try :
			json_dict = json.loads(json_str)
		except :
			print 'recv_response json loads error',json_str
			return 
		pass
	
	# 1 folk a center process
	def __folk_center_process(self,task_info):
		task_port = TASK_CENTER_BASE_PORT + task_info._id 
		cmd = 'python ../center/center.py task_id=%d task_port=%d  > ../log/center%d.log & ' % (task_info._id ,task_port,task_info._id)
		#TODO folk a center server to remote mac
		#ret  = excute_cmd_by_os(cmd)
		cmd = 'ps -ef|grep center |grep "task_id=%d "| awk \'{print $2}\' ' % task_info._id
		ret , process_id = excute_cmd(cmd)
		if ret == 0 and process_id is not None and process_id.isdigit():
			return ret,process_id
		#output is process id
		return -1,0

	# 1 kill
	def __kill_process(self):
		cmd = 'ps -ef|grep center |grep task_id| awk \'{print $2}\' '
		#status , output = excute_cmd(cmd) #TODO check the specified process id ,and kill it
	

class MasterSer():
	masterManger = MasterManger()

	@Request.application
	def application(self,request):
		# Dispatcher is dictionary {<method_name>: callable}
		dispatcher["echo"] = lambda s: s
		dispatcher["add"] = lambda a, b: a + b
		print 'revice data',request.data

		response = JSONRPCResponseManager.handle(
			request.data, dispatcher)
		return Response(response.json, mimetype='application/json')

	def server(self):
		global flag_ser_status
		print 'MasterSer App will start '
		t = threading.Timer(2.0,self.master_mgr_loop)
		t.start()
		flag_ser_status = 1
		run_simple('localhost', 4000, self.application)
		flag_ser_status =  0
		print '........................end'

	def master_mgr_loop(self):
		global flag_ser_status
		print flag_ser_status
		while flag_ser_status == 1:
			self.masterManger.manger()
			time.sleep(10)
			


if __name__ == "__main__":
	#app_type  = sys.argv[1]
	masterServer =  MasterSer()
	masterServer.server()

		


