from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from jsonrpc import JSONRPCResponseManager, dispatcher
import requests
import json,sys,time
import collections,threading,thread
sys.path.append("..")
from utils.jsonrpc_sdk import *
from utils.entity_trans import *
from utils.common_func import *
from utils.simple_http_client import *
from entity.constannt import *


global flag_ser_status
flag_ser_status = 0

ser_port = 7000

THREAD_MAX_NUM = 10

task_max_num = 10



class CrawlerBase():

	task_id = None

	proxy_ip_port = None

	from_ip_port = None
	
	cookies = None

	url = None 

	req_num = 0
	
	user_agent = None 

	crawler_type = 0	

	def __init__(self ):
		pass

	def check_paramters_available(self):
		if self.url is None or not self.url.startswith("http"):
			return False
		return True
	
	# simple action , use the python http client to request
	def simple_action(self):
		suc_num = 0
		for i in range (0,self.req_num) :
			text = simple_get(self.url)
			print 'simple action finish ',self.url ,text[:100],'len(text)' ,len(text) if text is not None else '0'
			time.sleep(2)
			if text is not None and  len(text) > 100:#TODO confirm the text availabl and more careful
				suc_num += 1
		result_dict = {'task_id':self.task_id,'req_num':self.req_num,'task_url':self.url,'suc_num':suc_num}
		return result_dict

	# webkit action , use the javascript tools by casperjs 
	def webkit_action():
		pass

	# special action , custom-made codes by site or pattern 
	def webkit_action():
		pass




class LoginCrawler(CrawlerBase):
	crawler_type = 1
	pass

class ViewCrawler(CrawlerBase):
	crawler_type = 2
	# simple action , use the python http client to request
	#def simple_action(self):
	#	return True

class VoteCrawler(CrawlerBase):
	crawler_type = 3
	
	pass

class ShareCrawler(CrawlerBase):
	crawler_type = 4
	pass



class CrawlerManger():
	# save all  base infos of the using tasks
	# the same task ids can't be ordered more than tow times at the same time
	crawler_slave = None
	client_type = 1 
	task_info_map = {}
	def __init__(self,client_type):
		self.client_type = client_type
	
	def dispatch(self, task_id, task_type,crawler_type ,task_url, req_num,add_headers,other_conditions):
		ret_code = RetcodeCl2Ct.OK
		crawl_worker = self.__select_crawler_worker(task_type,crawler_type ,task_url)
		if crawl_worker is None :
			ret_code =RetcodeCl2Ct.WORKER_CHOOSE_ERROR
		else :
			#TODO move to the single functon
			crawl_worker.task_id = task_id
			crawl_worker.url = task_url
			crawl_worker.req_num = req_num
			crawl_worker.add_headers = add_headers
			crawl_worker.feedback_to_addr =  other_conditions['from_ip_port']
			if (threading.active_count() - 1) <= THREAD_MAX_NUM :
				try :
					#TODO name=None, args=(), kwargs={})
					crawl_t = threading.Thread(target=self.work_feedback,kwargs={'worker':crawl_worker})
					crawl_t.start()
				except Exception ,e:
					print 'error' ,str(e)
					ret_code = RetcodeCl2Ct.THREAD_START_ERROR
		return {'ret':ret_code.value}

	# after finish the order of one task ,report to center
	def report(self,remote_ip_port,result_dict):
		method = 'cl2ct_report'
		param_list = [result_dict]
		ret = jsonrpc_sent(remote_ip_port,method,param_list)


	def work_feedback(self,worker):
		r_dict = worker.simple_action()
		self.report(worker.feedback_to_addr,r_dict)

	def send():
		pass
	
	# if task map is not max , ask new task
	#undefined
	def ask():
		pass

	# refer entity.constant by new thread

	# vote pattern ,directly
	def vote_crawl():
		pass
	
	# vote pattern ,webit
	def vote_crawl():
		pass

	def view_crawl():
		pass

	def run(self):
		pass

	def __select_crawler_worker(self,task_type,crawler_type ,task_url):
		if crawler_type == 1 :
			return LoginCrawler()
		elif crawler_type == 2 :
			return ViewCrawler()
		elif crawler_type == 3 :
			return VoteCrawler()
		elif crawler_type == 4 :
			return ShareCrawler()
		return None

class CrawlerSer():
	crawlerManger = None

	def __init__(self,client_type):
		self.crawlerManger = CrawlerManger(client_type)

	#param_list = [task_info._id, crawler_type ,task_info._url,need_sent_num,tmp_headers]	
	def recv_job(self,task_id, task_type,crawler_type ,task_url, req_num,add_headers,other_conditions):
		r_dict = self.crawlerManger.dispatch( task_id, task_type,crawler_type ,task_url, req_num,add_headers,other_conditions)
		return r_dict
	
	
	@Request.application
	def application(self,request):
		# Dispatcher is dictionary {<method_name>: callable}
		dispatcher["echo"] = lambda s: s
		dispatcher["ct2cl_order"] = self.recv_job
		print 'revice data',request.data

		response = JSONRPCResponseManager.handle(
			request.data, dispatcher)
		return Response(response.json, mimetype='application/json')

	def server(self,ser_port):
		global flag_ser_status
		print 'CrawlerSer App will start '
		t = threading.Timer(2.0,self.crawler_mgr_loop)
		t.start()
		flag_ser_status = 1
		run_simple('localhost', ser_port, self.application)
		flag_ser_status =  0
		print '........................end'

	def crawler_mgr_loop(self):
		global flag_ser_status
		print flag_ser_status
		while flag_ser_status == 1:
			print 'manger ............ '
			self.crawlerManger.run()
			time.sleep(10)


if __name__ == "__main__":
        print len(sys.argv)
        if len(sys.argv) < 3:
                print 'start crawler server fail,cause the argv len is ' ,len(sys.argv)
                sys.exit(0)
        if not sys.argv[1].startswith('client_type=') or not sys.argv[2].startswith('port=') :
                print 'start crawler server fail,cause the input argv is error :' ,sys.argv
                sys.exit(0)
        client_type  = int(sys.argv[1].split('=')[1])
        ser_port  = int(sys.argv[2].split('=')[1])
        crawlerServer =  CrawlerSer(client_type)
        crawlerServer.server(ser_port)
