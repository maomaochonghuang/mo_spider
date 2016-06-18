#! /usr/bin/env python
#coding=utf8

from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from jsonrpc import JSONRPCResponseManager, dispatcher
import requests
import json,sys
import threading



DEFAULT_TIMEOUT = 10
mutex = threading.Lock()

global jsonrpc_id 
jsonrpc_id = 0

def make_payload() :
	pass

def get_current_id():
	global jsonrpc_id
	current_id = 0
	try :
		mutex.acquire(2)
		jsonrpc_id += 1
		current_id = jsonrpc_id
		mutex.release()
	except Exception ,e:
		#print str(e)
		pass
	return current_id

def jsonrpc_sent(ip_addr_port, method, param_list):
	url = "http://%s/jsonrpc" % (ip_addr_port)
	headers = {'content-type': 'application/json'}
	payload = {
		"method": method,
		"params": param_list,
		"jsonrpc": "2.0",
		"id": get_current_id(),
	}
	print url,payload
	print json.dumps(payload)
	print json.loads(json.dumps(payload))
	response = requests.post(
		url, data=json.dumps(payload), headers=headers).json()
	return response

def test_jsonrpc_sent():
	ip_addr = 'localhost'
	port = 4000
	method ='echo'
	param_list = ['adsfds']
	jsonrpc_sent(ip_addr+":"+str(port),method,param_list)
	

if __name__ == "__main__":
	test_jsonrpc_sent()

