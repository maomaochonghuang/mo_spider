ps -ef|grep master.py|awk '{print $2}' |xargs kill
