import socket
import netifaces

addrs=netifaces.ifaddresses('wlan0')
addrs=list(addrs[netifaces.AF_INET])
addrs=dict(addrs[0])
#ip address addrs['addr']

client=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
client.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
client.bind(("",3000))
msg='broadcast from:'+str(addrs['addr'])
msg=str(msg)
client.sendto(msg.encode('ascii'),('192.168.43.255',4444))
print("message sent")
client.close()
