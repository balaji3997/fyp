import socket
import netifaces
import psutil
import sys
import shlex
import os
import subprocess
from subprocess import Popen,PIPE,STDOUT
import time

addrs=netifaces.ifaddresses('wlan0')
addrs=list(addrs[netifaces.AF_INET])
addrs=dict(addrs[0])
#ip address addrs['addr']

def cpu_details():
	cpu_list=[]
	cpupercent=psutil.cpu_percent(interval=1)
	cpu_list.append(cpupercent)
	cpufreq=psutil.cpu_freq()
	cpu_list.append(cpufreq.current)
	cpu_list.append(cpufreq.max)
	return cpu_list
'''
def get_simple_cmd_output(cmd,stderr=STDOUT):
	args=shlex.split(cmd)
	return Popen(args,stdout=PIPE,stderr=stderr).communicate()[0]
def get_bandwidth(host):
	cmd="iperf -c {host}".format(host=host)
	re=str(get_simple_cmd_output(cmd))
	re=list(re.split(" "))
	return str(re[-2])
'''

while True:
	print("listening")
	server=socket.socket(socket.AF_INET,socket.SOCK_DGRAM,socket.IPPROTO_UDP)
	server.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
	server.bind(("",4444))
	data,addr=server.recvfrom(1024)
	data.decode('ascii')
	data=str(data)
	data=list(data.split("'"))
	data=str(data[1])
	data=list(data.split(":"))
	data=data[1]
	print(data)
	print("Type:",type(data))
	server.close()
	host=data
	ipadrs=host
	port=5555
	cpu_info=cpu_details()
	out=str(addrs['addr'])+' '+str(cpu_info[0])+' '+str(cpu_info[1])+' '+str(cpu_info[2])
	out=str(out)
	print(out)
	tcpcli=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	tcpcli.connect((host,port))
	tcpcli.send(bytes(out,'ascii'))
	tcpcli.close()
	print("tcp closed")
	print("udp opened")
	server=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	host=''
	port=7777
	server.bind((host,port))
	data,addr=server.recvfrom(1024)
	data=data.decode('ascii')
	if(data=='reject'):
		print("rejected")
		continue
	host=ipadrs
	port=8888
	msg='ok'
	msg=str(msg)
	server.sendto(msg.encode('ascii'),(host,port))
	server.close()
	print("communication ended")
	port=9999
	s=socket.socket()
	host=""
	s.bind((host,port))
	s.listen(5)
	conn,addr=s.accept()
	data=conn.recv(1024)
	data=data.decode('ascii')
	print('file name',data)
	file_name=data
	with open(data,'wb') as f:
		print('file opened')
		while True:
			d=conn.recv(1024)
			if not d:
				break
			f.write(d)
	f.close()
	print('file closed')
	conn.close()
	s.close()
	#added new
	statinfo=os.stat(file_name)
	statinfo=statinfo.st_size
	statinfo=float(statinfo/1000)
	print(statinfo)
	ul=0.00
	dl=0.00
	t0=time.time()
	up_link=psutil.net_io_counters(pernic=True)['wlan0'].bytes_sent
	down_link=psutil.net_io_counters(pernic=True)['wlan0'].bytes_recv
	up_down=(up_link,down_link)
	i=0
	while(i<2):
		i+=1
		last_up_down=up_down
		upload=psutil.net_io_counters(pernic=True)['wlan0'].bytes_sent
		download=psutil.net_io_counters(pernic=True)['wlan0'].bytes_recv
		t1=time.time()
		up_down=(upload,download)
		ul,dl=[(now-last)/(t1-t0)/1000.0 for now ,last in zip(up_down,last_up_down)]
		t0=time.time()
		time.sleep(1)
		if(i!=1):
			up_link=ul
			down_link=dl
	print(up_link)
	print(down_link)
	if(float(statinfo)<up_link and float(statinfo)<down_link):
		da="cld"
		socketcloud=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		host='142.93.222.110'
		port=11111
		name=file_name
		statinfo=os.stat(name)
		statinfo=statinfo.st_size
		statinfo=float(statinfo/1000)
		print('file size ',float(statinfo),end=" ")
		print('kb')
		socketcloud.connect((host,port))
		socketcloud.send(name.encode('ascii'))
		f=open(name,'rb')
		l=f.read(1024)
		while(l):
			
			socketcloud.send(l)
			l=f.read(1024)
		f.close()
		socketcloud.close()

	else:
		da='ok'
	print("da ",da)
	socketcloud=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	udphost=ipadrs
	port=22222
	#socketcloud.bind((udphost,port))
	da=str(da)
	dat=da.encode('ascii')
	socketcloud.sendto(dat,(ipadrs,port))
	socketcloud.close()
	#added new
	#arg1='python3 '+str(file_name)
	#os.system(arg1) #use subprocess module
	if(da=='ok'):
		process=subprocess.Popen(['python3',file_name])
		try:
			print('running in process',process.pid)
			process.wait(timeout=15)
		except subprocess.TimeoutExpired:
			print('timed out -killing ',process.pid)
			process.kill()
		print('done')
	#socketcloud.sendto(dat,(ipadrs,port))
	#socketcloud.close()
