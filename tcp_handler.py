import socket

def get_client(host, port):
	s = socket.socket()
	s.connect((host, port))
	return s

def send_data(s, message):
	s.send(message.encode("utf-8"))

def recv_data(s):
	data = s.recv(35).decode("utf-8")
	return data

def get_server(host, port):
	s = socket.socket()
	s.bind((host, port))
	s.listen(1)
	c, addr = s.accept()
	return c

