
import socket

UDP_IP = "172.29.27.189"
UDP_PORT = 8888

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

while True:
	data, addr = sock.recvfrom(1024)
	print("received message: %s" %data)
	dataList = data.decode("utf-8").split(" ")
	print("touch: " + dataList[1])
	print("light: " + dataList[0])	
