from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from jsonrpc import JSONRPCResponseManager, dispatcher
import requests
import json,sys


@dispatcher.add_method
def foobar(**kwargs):
	return kwargs["foo"] + kwargs["bar"]


@Request.application
def application(request):
	# Dispatcher is dictionary {<method_name>: callable}
	dispatcher["echo"] = lambda s: "ok"
	dispatcher["add"] = lambda a, b: a + b
	resp_dict = {'ret':0}
	print 'revice data',request.data
	print 'revice data',request
	print 'revice data',request.host_url
	print 'revice data',request.host

	response = JSONRPCResponseManager.handle(
		request.data, dispatcher)
	print response.json
	return Response(response.json, mimetype='application/json')

def server():
	run_simple('localhost', 4000, application)


def client():
	url = "http://localhost:4000/jsonrpc"
	url = "http://localhost:6001/jsonrpc"
	headers = {'content-type': 'application/json'}
	# Example echo method
	payload = {
		"method": "add",
		"params": ["echome!","sf"],
		"jsonrpc": "2.0",
		"id": 0,
	}
	response = requests.post(
		url, data=json.dumps(payload), headers=headers).json()
	print type(response)
	print json.dumps(response)
	assert response["result"] == "echome!"
	assert response["jsonrpc"]
	assert response["id"] == 0

if __name__ == "__main__":
	app_type  = sys.argv[1]
	if app_type == 'server':
		server()

	elif app_type == 'client' :
		client()


