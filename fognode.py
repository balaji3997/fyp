import socket
import psutil
import time
import os
import sys
import shlex
from subprocess import Popen,PIPE,STDOUT

'''
def secs2hours(secs):
	mm,ss = divmod(secs,60)
	hh,mm = divmod(mm,60)
	st=str(hh)+' hours '+str(mm)+' minutes '+str(ss)+' seconds '
	return st

def battery_details():
	battery = psutil.sensors_battery()
	plugged = battery.power_plugged
	percent = str(battery.percent)
	sec = battery.secsleft
	if plugged==False:
		plugged="Not Plugged in"
	else:
		plugged="Plugged in"
	batper=str(percent[0:5]+% | '+plugged)
	if(str(sec)=='BatteryTime.POWER_TIME_UNLIMITED'):
		pass
	else:
		bat_timeleft=secs2hours(sec)
'''

def cpu_details():
	cp=psutil.cpu_times()
	cpu_cores=str(psutil.cpu_count())
	cpu_percent=psutil.cpu_percent(interval=5)
	return str('Cpu cores:'+str(cpu_cores)+','+'Cpu utilisation:'+str(cpu_percent)+',')

def network_details():
	ul=0.0
	dl=0.0
	t0=time.time()
	upload=psutil.net_io_counters(pernic=True)['wlan0'].bytes_sent
	download=psutil.net_io_counters(pernic=True)['wlan0'].bytes_recv
	up_down=(upload,download)
	i=0
	while(i<2):
		i+=1
		last_up_down= up_down
		upload=psutil.net_io_counters(pernic=True)['wlan0'].bytes_sent
		download=psutil.net_io_counters(pernic=True)['wlan0'].bytes_recv
		t1=time.time()
		up_down =(upload,download)
		ul,dl=[(now-last) /(t1-t0) /1000.0 for now,last in zip(up_down,last_up_down)]
		t0=time.time()
		time.sleep(2)
		if(i!=1):
			return str('Uplink:'+str(ul)+','+'Downlink:'+str(dl)+',')

def get_simple_cmd_output(cmd,stderr=STDOUT):
	args=shlex.split(cmd)
	return Popen(args,stdout=PIPE,stderr=stderr).communicate()[0]

def get_ping_time(host='206.189.170.41'):
	host=host.split(':')[0]
	cmd="fping {host} -C 3 -q".format(host=host)
	re=str(get_simple_cmd_output(cmd))
	result=list(re.strip().split(':')[-1].strip().replace("\n'",'').split())
	result[-1]=result[-1].replace("\\n'",'')
	res=[float(x) for x in result if(x!='-')]
	if(len(res)>0):
		return str('Cloud latency:'+str(sum(res)/len(res))[0:7])
	else:
		return str('cloud doesnot respond:'+'999999')


while(True):
	HOST=''
	PORT=4444
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1);
	s.bind((HOST,PORT))
	s.listen(1)
	conn,addr=s.accept()
	output=str(cpu_details()+network_details()+get_ping_time())
	print(output)
	conn.send(output.encode('ascii'))
	conn.close()
	s.close()
