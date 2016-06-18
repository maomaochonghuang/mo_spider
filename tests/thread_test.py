import json,sys,time
import Queue,threading

def thread_master(thread_number):
    global count, mutex
    threadname = threading.currentThread().getName()
 
    for x in xrange(0, int(thread_number)):
        mutex.acquire()
        count = count + 1
        mutex.release()
        print threadname, x, count
        time.sleep(1)

def hello_by_timer():
	print 'hello world'

'''if __name__ == "__main__":
	#app_type  = sys.argv[1]
	global count, mutex
	threads = []
	count = 1
	num = 4 
	mutex = threading.Lock()
	for x in range(0, num):
		threads.append(threading.Thread(target=thread_master, args=(10,)))
	for t in threads:
		t.start()
	for t in threads:
		t.join()  
 
	print 'end ...........' '''

		
if __name__ == "__main__":
	t = threading.Timer(5.0, hello_by_timer)
	t.start()
