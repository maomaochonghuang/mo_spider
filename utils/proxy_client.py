#! /usr/bin/env python
#coding=utf8

import urllib
import urllib2
import time
import sys
import threadpool
sys.path.append("..")
from utils.common_func import *

DEFAULT_TIMEOUT = 30
http_header_accpent = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
http_header_language = 'zh-CN,zh;q=0.8'
http_header_cache_control = 'max-age=0' 
http_header_pc_ua = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36' 
http_header_mobile_ua = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36'


global proxyClient 
proxyClient = None
global suc_num,url_suc_num
suc_num = 0
url_suc_num = {}

class ProxyClient():

	headers = {"Accept": http_header_accpent,
	  "Accept-Language" : http_header_language,
	  "Cache-Control": http_header_cache_control,
	  "User-Agent": http_header_pc_ua,
	  }

	mobile_headers = {'User-Agent': http_header_mobile_ua,
	'Accept-Charset':'UTF-8','Accept-Encoding':'gzip','Content-Type':'application/x-www-form-urlencoded'}

	def __add_headers(self,more_headers):
		tmp_headers = self.headers
		tmp_headers.update(more_headers)
		return tmp_headers

	def get(self, url,protocol,proxy_ip,proxy_port, timeout=DEFAULT_TIMEOUT, more_headers={}):
		text = ""
		tmp_headers = self.__add_headers(more_headers)
		proxy_handler = urllib2.ProxyHandler({protocol : protocol + '://' + proxy_ip + ':' + str(proxy_port) })
		try:
			proxy_opener = urllib2.build_opener(proxy_handler, urllib2.HTTPHandler)  
			page = proxy_opener.open(url, timeout=timeout) 
			text = page.read()
			page.close()
		except Exception, e:
			print 'error proxy ', proxy_ip,proxy_port,str(e)
			return False
		if text is not None and len (text) > 100:
			return True
		return False

	def get_feedback_full(self, url,protocol,proxy_ip,proxy_port, timeout=DEFAULT_TIMEOUT, more_headers={}):
		ret = self.get( url,protocol,proxy_ip,proxy_port, timeout, more_headers)
		return ret#,[proxy_ip,proxy_port]


	#TODO change to request by proxy
	def post(self,url,post_dict,mre_headers={}):
		tmp_headers = __add_headers(more_headers)
		post_data = urllib.urlencode(post_dict)
		try:
			req = urllib2.Request(url, headers = tmp_headers)
			page = urllib2.urlopen(req,post_data, timeout=DEFAULT_TIMEOUT)
			text = page.read()
			page.close()
			return text
		except Exception,e:
			print str(e)
		return None


def simple_proxy_get(url, proxy_ip, proxy_port, timeout= DEFAULT_TIMEOUT, more_headers={}):
	global proxyClient 
	if proxyClient  is None :
		proxyClient = ProxyClient()
	protocol = extract_protocol(url)
	return proxyClient.get(url,protocol,proxy_ip,proxy_port, timeout = timeout ,more_headers=more_headers)

def do_something(aa,bb,cc=444):
	print 'do_something.............', aa,bb

def fuc_b(request, n):    
	print 'start fuc_bbbbbbbb' ,request,n    
	print 'end fuc_bbbbbbbbb' ,request,n   
	return 'ok funb'

def request_back(request, ret):    
	global suc_num 
	print 'request_back' ,request,ret
	if ret :
		suc_num += 1
	return 

def request_bac2k(request, ret, resp_params):    
	print 'start fuc_bbbbbbbb' ,request,ret, resp_params 
	print 'end fuc_bbbbbbbbb' ,request,ret, resp_params
	return 'ok funb'

def batch_proxy_get(url, proxy_infos, timeout= DEFAULT_TIMEOUT ,more_headers={}):
	global proxyClient ,suc_num 
	if proxyClient  is None :
		proxyClient = ProxyClient()

	if len(proxy_infos) == 0 :
		return 0
	if type(proxy_infos[0]) is str :
		for i in range (0,len(proxy_infos)):
			addr_port = proxy_infos[i].split(':')
			if len(addr_port) != 2 :
				continue
			proxy_infos[i] = (addr_port[0],addr_port[1])
	req_results = []
	thread_num = 2
	protocol = extract_protocol(url)
	#TODO ,add thread pool , and wait all request over
	pool = threadpool.ThreadPool(thread_num)
	req_args = []
	for proxy_info in proxy_infos:
		#argument_map = {'url':url,'protocol':protocol,'proxy_ip':proxy_info[0],'proxy_port':proxy_info[1]}
		req_args.append(([url,protocol,proxy_info[0],proxy_info[1], timeout ,more_headers],{}))
		#req_args.append(argument_map)
	#requests = threadpool.makeRequests(do_something, [([111,222],{})])
	requests = threadpool.makeRequests( proxyClient.get_feedback_full, req_args, request_back)
	[pool.putRequest(req) for req in requests]
	#suc_num += 1	
	#req_results.append((proxy_info[0] + ':' + proxy_info[1],ret))
	pool.wait()
	print 'abbbbbbbbbbbbbbbbbbbbbba'
	pool.dismissWorkers(20, do_join=True)
	resp_sub_num = suc_num
	suc_num = 0
	return resp_sub_num
		
def fuc_a(argv_a,argv_b): 
	print 'start fuc_aaaaaaaaaa', argv_a,argv_b 
	time.sleep(3)   
	print 'end fuc_aaaaaaaaaa' , argv_a,argv_b    
	return 'ok funa'   
	

def main_test():    
	thread_num = 1     
	pool = threadpool.ThreadPool(thread_num)    
	datas = [((),{'argv_b':5,'argv_a':6}),((3,4),{})]    
	reqs = threadpool.makeRequests(fuc_a, datas, fuc_b)    
	[pool.putRequest(req) for req in reqs]    
	pool.wait()    
	pool.dismissWorkers(20, do_join=True)
	pass

def batch_proxy_get2(url, proxy_infos, timeout= DEFAULT_TIMEOUT ,more_headers={}):
	global proxyClient 
	if proxyClient  is None :
		proxyClient = ProxyClient()
	req_results = []
	suc_num = 0
	protocol = extract_protocol(url)
	#TODO ,add thread pool , and wait all request over
	for proxy_info in proxy_infos:
		ret = proxyClient.get(url,protocol,proxy_info[0],proxy_info[1], timeout = timeout ,more_headers=more_headers)
		if ret :
			suc_num += 1	
		req_results.append((proxy_info[0] + ':' + proxy_info[1],ret))
	return suc_num,req_results 
		
 
if __name__ == '__main__':

	url = 'http://cn.made-in-china.com/sendInquiry/shrom_KqUmILoAaWVR_KqUmILoAaWVR.html'
	Encoding =  'gzip, deflate'
	Referer= 'http://cn.made-in-china.com/sendInquiry/shrom_KqUmILoAaWVR_KqUmILoAaWVR.html'

	#add_headers = {'Accept-Encoding':Encoding,'Referer':Referer,'Cookie':test_cookies}
	proxyClient  = ProxyClient()
	proxy_ip = '123.138.89.130'
	proxy_port = '9999'
	proxy_infos = [('123.138.89.130','9999'),('217.117.0.155','3128')]
	#print simple_get(url,proxy_ip,proxy_port)
	print batch_proxy_get(url, proxy_infos)
	#main_test()
	


