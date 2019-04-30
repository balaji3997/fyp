import socket
import netifaces

addrs=netifaces.ifaddresses('wlan0')
addrs=list(addrs[netifaces.AF_INET])
addrs=dict(addrs[0])
#ip address   addrs['addr']
while True:
	server= socket.socket(socket.AF_INET,socket.SOCK_DGRAM,socket.IPPROTO_UDP)
	server.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
	server.bind(("",4444))
	data,addr= server.recvfrom(1024)
	data.decode('ascii')
	data=str(data)
	data=list(data.split("'"))
	data=str(data[1])
	print(data)
