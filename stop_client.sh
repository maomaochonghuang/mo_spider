ps -ef|grep crawler.py|grep python|awk '{print $2}' |xargs kill
