#! /usr/bin/env python
#coding=utf8

import urllib
import urllib2
import cookielib
import time
import sys
import gzip
import StringIO
import  poster.streaminghttp 
import  poster.encode 


DEFAULT_TIMEOUT = 30
http_header_accpent = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
http_header_language = 'zh-CN,zh;q=0.8'
http_header_cache_control = 'max-age=0' 
http_header_pc_ua = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36' 
http_header_mobile_ua = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36'


global simpleHttpClient 
simpleHttpClient = None

class SimpleHttpClient():
	cj = cookielib.LWPCookieJar()
	cookie_support = urllib2.HTTPCookieProcessor(cj)
	opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
	urllib2.install_opener(opener)

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

	

	def get(self,url,more_headers={}):
		tmp_headers = self.__add_headers(more_headers)
		try:
			req = urllib2.Request(url, headers = tmp_headers)
			page = urllib2.urlopen(url=req, timeout=DEFAULT_TIMEOUT) 
			text = page.read()
			page.close()
			return text
		except Exception,e:
			print str(e) #TODO
		return None


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



	def upload_file(url,post_dict,add_headers={}):
	    text = ""
	    poster.streaminghttp.register_openers()
	    tmp_headers = headers
	    tmp_headers.update(add_headers)
	    post_data = urllib.urlencode(post_dict)
	    try:
		params = {'attachFile1': open("upload2.jpg", "rb")}  
		datagen, file_headers = poster.encode.multipart_encode(params)  
		print 'aaaaa1',file_headers ,datagen
		tmp_headers.update(file_headers)
	    
		print 'aaaaa2',file_headers ,datagen
		req = urllib2.Request(url, data = datagen,headers =  file_headers)  
		print file_headers
		try:
		    print 'req\n', "\n".join(datagen)
		    print 'req\n',req.header_items()
		    page = urllib2.urlopen(url = req) 
		    text = page.read()
		    print 'text' ,text
		    page.close()
		except Exception,e:
		    print 'upload_file error ' ,str(e),e
	    except Exception, e:
		print 'upload_file error ' ,str(e)
	    print 'text',text
	    return text


	def unzip_response_data(resp_result):
	    is_gzip = result.headers.get('Content-Encoding')
	    text = ''
	    if is_gzip =='gzip':
		gzip_text = result.read()
		compressedstream = StringIO.StringIO(gzip_text)
		gzipper = gzip.GzipFile(fileobj=compressedstream)
		text = gzipper.read()
		
	    else:
		text = result.read()
	    return text


# the function for public
def simple_get(url,more_headers={}):
	global simpleHttpClient 
	if simpleHttpClient  is None :
		simpleHttpClient = SimpleHttpClient()

	return simpleHttpClient.get(url,more_headers)
		

 
if __name__ == '__main__':

	url = 'http://cn.made-in-china.com/sendInquiry/shrom_KqUmILoAaWVR_KqUmILoAaWVR.html'
	Encoding =  'gzip, deflate'
	Referer= 'http://cn.made-in-china.com/sendInquiry/shrom_KqUmILoAaWVR_KqUmILoAaWVR.html'

	#add_headers = {'Accept-Encoding':Encoding,'Referer':Referer,'Cookie':test_cookies}
	simpleHttpClient = SimpleHttpClient()

	print simpleHttpClient.get(url)
	


