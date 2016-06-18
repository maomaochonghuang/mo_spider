import socket


class Server():
	
	s = None
	port = 0

	def __init__(self, addr, port):
		self.s = self.socket.socket( socket.AF_INET, socket.SOCK_STREAM)


	def listen(self)
		s.connect(("www.mcmillan-inc.com", self.port))



	def connect(self, host, port):
		self.sock.connect((host, port))


	def send(self, msg):
		totalsent = 0
		while totalsent < MSGLEN:
			sent = self.sock.send(msg[totalsent:])
			if sent == 0:
				raise RuntimeError("socket connection broken")
			totalsent = totalsent + sent

	def receive(self):
		chunks = []
		bytes_recd = 0
		while bytes_recd < MSGLEN:
			chunk = self.sock.recv(min(MSGLEN - bytes_recd, 2048))
			if chunk == '':
				raise RuntimeError("socket connection broken")
			chunks.append(chunk)
			bytes_recd = bytes_recd + len(chunk)
		return ''.join(chunks)
