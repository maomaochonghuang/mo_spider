#! /usr/bin/env python
#coding=utf8

import urllib
import urllib2
import time
import sys
import common_func


DEFAULT_TIMEOUT = 30
http_header_accpent = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
http_header_language = 'zh-CN,zh;q=0.8'
http_header_cache_control = 'max-age=0' 
http_header_pc_ua = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36' 
http_header_mobile_ua = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36'

class CasperjsClient():
	proxy_ip = None
	proxy_port = None
	cookies = None
	
	#TODO setup the path of phantomjs
	# https://github.com/emmetio/pyv8-binaries/downloads 
	# execute js or code js in python file ?????????????
	def view(self,url,more_headers={}):
		cmd = '../bin/casperjs.exe ' + js_file 
		try:
			ret ,output = common_func.excute_cmd(cmd)
			#output  is json_str
			# pasre it ,then get everything we want
		except Exception,e:
			print str(e) #TODO
		return None


 
if __name__ == '__main__':

	casperjsClient = CasperjsClient()

	print casperjsClient.get(url)
	
