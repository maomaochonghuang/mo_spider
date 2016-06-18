import commands,os
import time


def excute_cmd(cmd):
	status = -1 
	output = ""
	try :
		status, output = commands.getstatusoutput(cmd)
	except Exception ,e:
		print 'error',str(t)
		pass
	return status, output

def excute_cmd_by_os(cmd):
	status = -1 
	output = ""
	try :
		os.system(cmd)
		status = 0
	except Exception ,e:
		print 'error',str(t)
		pass
	return  status

def is_over_period(last_time,period):
	differ = time.time() - last_time
	if differ > period :
		return True
	return False

def extract_protocol(url):
	if url is None or len(url) < 5 :
		return 'http'
	tmp_url = url.lower()
	if tmp_url.startswith('http://'):
		return 'http'
	if tmp_url.startswith('https://'):
		return 'https'
	if tmp_url.startswith('ftp://'):
		return 'ftp'
	return 'http'

