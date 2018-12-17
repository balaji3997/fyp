import psutil
import time
import os
import cProfile
import sys
import math
import shlex
import socket
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput
from datetime import datetime,timedelta
from subprocess import Popen,PIPE,STDOUT
from statistics import mean
from collections import defaultdict
#import mergesortalgo
#import sudokusolver
#import line_profiler


def secs2hours(secs):
	mm, ss = divmod(secs, 60)
	hh, mm = divmod(mm, 60)
	#return "%d:%02d:%02d" % (hh, mm, ss)
	st=str(hh)+' hours '+str(mm)+' minutes '+str(ss)+' seconds '
	return st

#battery details
#@do_profile(follow=[])
def battery_details():
	batt_list=[]
	battery = psutil.sensors_battery()
	plugged = battery.power_plugged
	percent = str(battery.percent)
	sec     = battery.secsleft
	batt_list.append(sec)
	if plugged==False:
		plugged="Not Plugged In"
	else:
		plugged="Plugged In"
	print("BATTERY INFORMATION")
	print(percent[0:5]+'% | '+plugged)
	batt_list.append(percent[0:5])
	batt_list=list(map(float,batt_list))
	#print(type(sec))
	if(str(sec)=='BatteryTime.POWER_TIME_UNLIMITED'):
		pass
	else:
		print("time left ",secs2hours(sec))

	#d=datetime(1,1,1)+timedelta(seconds=sec)
	#print("Time left =",d.hour,"hours",end=" ")
	#print(d.minute," minutes",end=" ")
	#print(d.second," seconds")
	return batt_list

#cpu details
#@do_profile(follow=[])
def cpu_details():
	cpu_list=[]
	print("CPU INFORMATION")
	cp=psutil.cpu_times()
	#cputime=cp.user
	#print("CPU TIME IN USER MODE :",cputime)
	#cputime1=cp.system
	#print("CPU TIME IN KERNEL MODE :",cputime1)
	print("total number of cores",psutil.cpu_count())
	cpu_list.append(psutil.cpu_count())
	cpupercent=psutil.cpu_percent(interval=5,percpu=True)
	print("CPU UTILISATION PERCENT :",cpupercent,"%")
	cpu_list.append(cpupercent)
	return cpu_list

#network details
#@do_profile(follow=[])
def network_details():
	nw_list=[]
	print("NETWORK BANDWIDTH")
	ul=0.00
	dl=0.00
	t0 = time.time()
	upload=psutil.net_io_counters(pernic=True)['wlan0'].bytes_sent
	download=psutil.net_io_counters(pernic=True)['wlan0'].bytes_recv
	up_down=(upload,download)
	i=0
	while(i<2):
		i+=1
		last_up_down = up_down
		upload=psutil.net_io_counters(pernic=True)['wlan0'].bytes_sent
		download=psutil.net_io_counters(pernic=True)['wlan0'].bytes_recv
		t1 = time.time()
		up_down = (upload,download)
		ul, dl = [(now - last) / (t1 - t0) / 1000.0 for now,last in zip(up_down, last_up_down)]
		t0 = time.time()
		#if(dl>0.1 or ul>=0.1):
		time.sleep(2)
		if(i!=1):
			print("The network speed for the interval ",i-1,":",end="")
			print('UpLink: {:0.2f} kB/s '.format(ul),end=" ")
			print('DownLink: {:0.2f} kB/s'.format(dl))
			nw_list.append(ul)
			nw_list.append(dl)
	return nw_list

def get_simple_cmd_output(cmd,stderr=STDOUT):
	args = shlex.split(cmd)
	return Popen(args,stdout=PIPE,stderr=stderr).communicate()[0]

def get_ping_time(host='192.168.43.28'):
	host = host.split(':')[0]
	cmd = "fping {host} -C 3 -q".format(host=host)
	re=str(get_simple_cmd_output(cmd))
	#print(re)
	result = list(re.strip().split(':')[-1].strip().replace("\n'",'').split())
	result[-1]=result[-1].replace("\\n'",'')
	#print(result)
	res = [float(x) for x in result if(x!='-')]
	if(len(res) > 0):
		foglatency=str(sum(res)/len(res))
		print("The response time to the fog node:",foglatency[:7])
	else:
		print("problem finding the latency")
	return foglatency

def fogandcloud_details():
	HOST = '192.168.43.28'
	PORT = 4444
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.connect((HOST,PORT))
	data=s.recv(4096)
	fc_list=data.decode('ascii')
	#print(data.decode('ascii'))
	s.close()
	return fc_list
'''
try:
	from line_profiler import LineProfiler
	def do_profile(follow=[]):
		def inner(func):
			def profiled_func(*args, **kwargs):
				try:
					profiler = LineProfiler()
					profiler.add_function(func)
					for f in follow:
						profiler.add_function(f)
					profiler.enable_by_count()
					return func(*args, **kwargs)
				finally:
					profiler.print_stats()
			return profiled_func
		return inner

except ImportError:
	def do_profile(follow=[]):
		"Helpful if you accidentally leave in production!"
		def inner(func):
			def nothing(*args, **kwargs):
				return func(*args, **kwargs)
			return nothing
		return inner
'''
def dfsutil(graph,node,dfslist):
	for n in graph[node]:
		if n not in dfslist:
			dfslist.append(n)
			dfsutil(graph,n,dfslist)

def gendfs(graph,dfslist):
	node=1
	dfslist.append(node)
	dfsutil(graph,node,dfslist)

def gengraph(f_name,graph):
	gfile=open(f_name+'.txt','r')
	g_graph=gfile.readlines()
	access=0
	for j,line in enumerate(g_graph):
		if(line.startswith('#')):
			access=1
		elif(access==0):
			mt=line.split()
			mt[1]=str(mt[1]).replace('\n','')
			m[int(mt[0])]=mt[1]
		else:
			mtemp=line.split()
			graph[int(mtemp[0])].append(int(mtemp[1]))
	print("The content of graph:")
	for dn in m:
		print(dn,end=":")
		print(m[dn])
	for node in graph:
		print("Edge from node:",node)
		for content in graph[node]:
			print("  to node:",content)

	#print("The contents of graph:",graph)
	print("The content of m:",m)
	print("Generating dfs of the graph:")
	dfslist=[]
	gendfs(graph,dfslist)
	print("The Program flow :")
	for node in dfslist:
		if(node !=dfslist[-1]):
			print(m[node],end="->")
		else:
			print(m[node])
	return dfslist

def get_exectime(f_name):
	exec_map={}
	fil=open(f_name+'1.txt','r')
	li=fil.readlines()
	for j,line in enumerate(li):
		if(line.startswith('Function')):
			#print("fun name: ",line.split()[-4])
			#print("fun time: ",li[j+1].split()[-2])
			exec_map[str(line.split()[-4])]=float(li[j+1].split()[-2])
	#print(exec_map)
	return exec_map

def putannot(f_name,node,s):
	fa=open(f_name+'.py','r')
	la=fa.readlines()
	for j,line in enumerate(la):
		if(line.startswith('def '+node)):
			line=s+line
			del la[j]
			la.insert(j,line)
	fa.close()
	fa=open(f_name+'.py','w')
	for line in la:
		fa.write(line)
	fa.close()

if __name__=='__main__':
	li=list(sys.argv)
	print("the list of programs to profile",li[1:])
	for i in range(1,len(li)):
		f_name=li[i].split('.')[0]
		f_name=str(f_name)
		argf='./pyan.py '+li[i]+' --tgf -n -f '+f_name+'.txt'
		os.system(argf)
		m={}
		graph=defaultdict(list)
		d_list=gengraph(f_name,graph)
		d_list=[m[x] for x in d_list]
		#print("map list outside func: ",m)
		#print("dfs list outside func:",d_list)
		f=open(li[i],'r')
		l=f.readlines()
		s='@profile\n'
		for j,line in enumerate(l):
			if(line.startswith('def')):
				line=s+line
				del l[j]
				l.insert(j,line)
			#print(i,end="")
			#print(line,end=" ")
		f.close()
		f=open(li[i],'w')
		#f.write('import profiler\n')
		for line in l:
			f.write(line)
		f.close()
		argfile='kernprof.py -l '+li[i]+'; python3 -m line_profiler '+li[i]+'.lprof >'+f_name+'1.txt'
		#with PyCallGraph(output=GraphvizOutput()):
		os.system(argfile)
		remannot='python3 rmannot.py '+li[i]
		os.system(remannot)
		#e_map={}
		e_map=get_exectime(f_name)
		print(e_map)

		#with PyCallGraph(output=GraphvizOutput()):
		#	kernprof.py -l sudokusolveralgorithm.py; python3 -m line_profiler sudokusolveralgorithm.py.lprof

		#if __name__=='__main__':
	
		b_det=battery_details()
		c_det=cpu_details()
		nw_det=network_details()
		res_det=get_ping_time()
		fc_det=fogandcloud_details()
	
		bat_rem_sec=round(float(b_det[0]),2)
		#print("battery rem sec ",bat_rem_sec)
	
		bat_per=float(b_det[1])
		print("battery percent ",bat_per)
	
		cpu_cores=int(c_det[0])
		cpu_util_avg=round(float((float(c_det[1][0])+float(c_det[1][1])+float(c_det[1][2])+float(c_det[1][3]))/4),2)
		print("Number of cpu cores ",cpu_cores)
		print("CPU utilisation average ",cpu_util_avg)
	
		nw_up=round(float(nw_det[0]),2)
		nw_dwn=round(float(nw_det[1]),2)
		pi_res_time=round(float(res_det),2)/1000.00
		print("Network download speed ",nw_up)
		print("Network Upload speed ",nw_dwn)
		print("fog node response time ",pi_res_time)
	
		fc_d=fc_det.split(',')
		#print("fog data ",fc_d)

		f_cpu_cores=fc_d[0].split(':')[-1]
		print("Number of cpu cores in fog node ",f_cpu_cores)

		f_cpu_util_avg=float(fc_d[1].split(':')[-1])
		print("fog node average cpu utilisation ",f_cpu_util_avg)

		#f_cpu_util_avg=float(sum(f_cpu_util_avg)/len(f_cpu_util_avg))
		f_nw_up=round(float(fc_d[2].split(':')[-1]),2)
		print("fog node uplink speed ",f_nw_up)
		f_nw_dwn=round(float(fc_d[3].split(':')[-1]),2)
		print("fog node downlink speed",f_nw_dwn)
		cl_res_time=round(float(fc_d[4].split(':')[-1]),2)/1000.00
		print("cloud response time ",cl_res_time)
		#print(b_det)
		#print(c_det)
		#print(nw_det)
		#print(res_det)
		#print(fc_det)


		#The algorithm for partitioning
		offload_cloud_list=[]
		offload_fog_list=[]
		for i,node in enumerate(d_list[1:]):
			local_exec=True
			#for offloading to cloud
			if node in offload_cloud_list:
				for n in graph[node]:
					if n not in offload_cloud_list:
						putannot(f_name,n,'@offload_cloud\n')
						local_exec=False
				continue
			elif(f_nw_dwn>float(1.0) and f_nw_up>float(1.0)):
				if(cl_res_time+pi_res_time+(e_map[node]/3)<e_map[node]):
					offload_cloud_list.append(node)
					putannot(f_name,node,'@offload_cloud\n')
					local_exec=False
					for n in graph[node]:
						if n not in offload_cloud_list:
							putannot(f_name,n,'@offload_cloud\n')
							local_exec=False
						continue
			#for offloading to fog
			if node in offload_fog_list:
				for n in graph[node]:
					if n not in offload_fog_list:
						putannot(f_name,n,'@offload_fog\n')
						local_exec=False
				continue
			elif(cpu_util_avg>f_cpu_util_avg):
				if(pi_res_time+(e_map[node]/2)<e_map[node] and(nw_up>float(1.0) and nw_dwn>float(1.0))):
					offload_fog_list.append(node)
					putannot(f_name,node,'@offload_fog\n')
					local_exec=False
					for n in graph[node]:
						if n not in offload_fog_list:
							putannot(f_name,n,'@offload_fog\n')
							local_exec=False
						continue
			if(local_exec==True):
				putannot(f_name,node,'@execute_local\n')

