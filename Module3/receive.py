

import socket

UDP_IP = "172.29.131.160"
UDP_PORT = 8888

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

while True:
	data, addr = sock.recvfrom(1024)
	print("received message: %s" %data)
	dataList = data.decode("utf-8").split(" ")
	print("hall: " + dataList[0])
	print("touch: " + dataList[1])	
	print("x: " + dataList[2])
	print("y: " + dataList[3])
	print("z: " + dataList[4])
