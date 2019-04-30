import psutil
import time
import os
import os.path
import sys
import math
import shlex
import socket
import subprocess
from datetime import datetime,timedelta
from subprocess import Popen,PIPE,STDOUT
from statistics import mean
from collections import defaultdict
import netifaces
from threading import Thread
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.tree import DecisionTreeClassifier

def randomForest(train_X,train_Y,test_X,treeCount):
	X=train_X[:]
	Y=train_Y[:]
	X_test=test_X[:]
	forest=RandomForestClassifier(treeCount)
	forest.fit(X,Y)
	predictedRF=forest.predict(X_test)
	return predictedRF

def decisiontree(train_X,train_Y,test_X,treedepth):
	X=train_X[:]
	Y=train_Y[:]
	X_test=test_X[:]
	decisiontree=clf_entropy=DecisionTreeClassifier(criterion="entropy",random_state=100,max_depth=treedepth,min_samples_leaf=5)
	decisiontree.fit(X,Y)
	predictedtree=decisiontree.predict(X_test)
	return predictedtree



def secs2hours(secs):
	mm, ss = divmod(secs, 60)
	hh, mm = divmod(mm, 60)
	#return "%d:%02d:%02d" % (hh, mm, ss)
	st=str(hh)+' hours '+str(mm)+' minutes '+str(ss)+' seconds '
	return st

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
	#print("CPU INFORMATION")
	cp=psutil.cpu_times()
	cpu_list.append(psutil.cpu_count())
	cpupercent=psutil.cpu_percent(interval=1,percpu=True)
	cpu_list.append(cpupercent)
	cpufreq=psutil.cpu_freq()
	cpu_list.append(cpufreq.current)
	cpu_list.append(cpufreq.max)
	return cpu_list

def network_details():
	nw_list=[]
	#print("NETWORK BANDWIDTH")
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
			#print("The network speed for the interval ",i-1,":",end="")
			#print('UpLink: {:0.2f} kB/s '.format(ul),end=" ")
			#print('DownLink: {:0.2f} kB/s'.format(dl))
			nw_list.append(ul)
			nw_list.append(dl)
	return nw_list

def get_simple_cmd_output(cmd,stderr=STDOUT):
	args = shlex.split(cmd)
	return Popen(args,stdout=PIPE,stderr=stderr).communicate()[0]

def get_ping_time(host='192.168.43.2'):
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
		#print("The response time to the edge node:",foglatency[:7])
	else:
		pass
		#print("problem finding the latency")
	return foglatency
#rm
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
#rm
def dfsutil(graph,node,dfslist):
	for n in graph[node]:
		if n not in dfslist:
			dfslist.append(n)
			dfsutil(graph,n,dfslist)
#rm
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
	#print("The content of graph:")
	#for dn in m:
		#print(dn,end=":")
		#print(m[dn])
	for node in graph:
		#print("Edge from node:",node)
		for content in graph[node]:
			#print("  to node:",content)

			if(content==node):
				graph[node].remove(content)
	return graph
	'''
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
	'''
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
#rm
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
#rm
def offload_func(f_name):
	fa=open(f_name+'.py','r')
	la=fa.readlines()
	access=0
	fil=open(f_name+'1.py','w')
	for j,line in enumerate(la):
		if(line.startswith('@offload_fog')):
			access=1
		elif(line.startswith('@execute_local') or line.startswith('if __name__')):
			access=0
		elif(access==1):
			if(line.startswith('@offload_fog')):
				continue
			else:
				fil.write(line)
	fa.close()
	fil.close()

def socket_func(f_name):
	s=socket.socket()
	host="192.168.43.28"
	port=5555
	s.connect((host,port))
	name=f_name+'1.py'
	s.send(name.encode('ascii'))
	#s.close()
	#s.connect((host,port))
	f=open(name,'rb')
	l=f.read(1024)
	while(l):
		s.send(l)
		l=f.read(1024)
	f.close()
	s.close()

class ClientThread(Thread):
	def __init__(self,ip,port):
		Thread.__init__(self)
		self.ip=ip
		self.port=port
		print("[+] new server socket thread for "+str(ip)+" "+str(port))

	def run(self):
		data=conn.recv(2048)
		data.decode('ascii')
		e_details.append(str(data))
		print("server received data:",str(data))
		conn.close()


if __name__=='__main__':
	li=list(sys.argv)
	print("the list of programs :",li[1:])
	for i in range(1,len(li)):
		f_name=li[i].split('.')[0]
		f_name=str(f_name)
		fil_name=f_name+'.txt'
		cur_dir=os.getcwd()
		file_list=os.listdir(cur_dir)
		if fil_name not in file_list:
			argf='./pyan.py '+li[i]+' --tgf -n -f '+f_name+'.txt'
			os.system(argf)
		m={}
		graph=defaultdict(list)
		#d_list=gengraph(f_name,graph)
		#d_list=[m[x] for x in d_list]
		graph=gengraph(f_name,graph)
		print("GRAPH")
		print(graph)
		print("MAP")
		print(m)
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
		file_name=f_name+'1.txt'
		if file_name not in file_list:
			argfile='kernprof.py -l '+li[i]+'; python3 -m line_profiler '+li[i]+'.lprof >'+f_name+'1.txt'
			#with PyCallGraph(output=GraphvizOutput()):
			os.system(argfile)
		remannot='python3 rmannot.py '+li[i]
		os.system(remannot)
		
		#e_map={}
		e_map=get_exectime(f_name)
		print("EMAP")
		print(e_map)

		#b_det=battery_details()
		c_det=cpu_details()
		nw_det=network_details()
		#res_det=get_ping_time()
		#fc_det=fogandcloud_details()
	
		#bat_rem_sec=round(float(b_det[0]),2)
		#print("battery rem sec ",bat_rem_sec)
	
		#bat_per=float(b_det[1])
		#print("battery percent ",bat_per)
		print("\n\nPROFILER OUTPUT\n\n")


		cpu_cores=int(c_det[0])
		cpu_util_avg=round(float((float(c_det[1][0])+float(c_det[1][1]))/2),2)
		print("NUMBER OF CPU CORES : ",cpu_cores)
		print("CPU UTILISATION AVERAGE : ",cpu_util_avg)
		print("CPU CURRENT FREQUENCY : ",float(c_det[2]))
		print("CPU MAXIMUM FREQUENCY : ",float(c_det[3]))
		nw_up=round(float(nw_det[0]),2)
		nw_dwn=round(float(nw_det[1]),2)
		#pi_res_time=round(float(res_det),2)/1000.00

		print("NETWORK UPLINK SPEED : ",nw_up)
		print("NETWORK DOWNLINK SPEED : ",nw_dwn)
		#print("EDGE NODE RESPONSE TIME : ",pi_res_time)
	
		#fc_d=fc_det.split(',')
		#print("fog data ",fc_d)

		#f_cpu_cores=fc_d[0].split(':')[-1]
		#print("Number of cpu cores in fog node ",f_cpu_cores)

		#f_cpu_util_avg=float(fc_d[1].split(':')[-1])
		#print("fog node average cpu utilisation ",f_cpu_util_avg)

		#f_cpu_util_avg=float(sum(f_cpu_util_avg)/len(f_cpu_util_avg))
		#f_nw_up=round(float(fc_d[2].split(':')[-1]),2)
		#print("fog node uplink speed ",f_nw_up)
		#f_nw_dwn=round(float(fc_d[3].split(':')[-1]),2)
		#print("fog node downlink speed",f_nw_dwn)
		#cl_res_time=round(float(fc_d[4].split(':')[-1]),2)/1000.00
		#print("cloud response time ",cl_res_time)
		#print(b_det)
		#print(c_det)
		#print(nw_det)
		#print(res_det)
		#print(fc_det)


		#The algorithm for partitioning
		#offload_cloud_list=[]
		

		offload_list=[]
		off=[]
		max_exectime=0.00
		for f in e_map:
			if(float(e_map[f])>max_exectime):
				max_exectime=e_map[f]
				key_func=f
		print(key_func)
		print(type(key_func))
		for x in graph:
			if(str(m[x])==str(key_func)):
				for i in graph[x]:
					offload_list.append(str(m[i]))
					off.append(i)
		for x in off:
			for i in graph[x]:
				offload_list.append(str(m[i]))
		#for x in m:
			#if str(m[x]) in offload_list:

			#for i in graph[x]:
				#if i not in offload_list:
					#offload_list.append(i)
		print("\n\nPARTITIONING OUTPUT\n\n")
		print("THE METHODS IN THE PROGRAM : ")
		total_exec_time=0.0
		for i in e_map:
			print(i)
		print("THE METHODS THAT CAN BE OFFLOADED : ")
		for i in offload_list:
			print(i)
			total_exec_time=total_exec_time+float(e_map[str(i)])
		print("total exec time:",total_exec_time)

		#implementing random forest
		dset='dataset.txt'
		f=open(dset,'r')
		l=f.readlines()
		xtrain=[]
		ytrain=[]
		for i in l[1:]:
			temp=[]
			lis=list(i.split(','))
			#print(lis)
			#lis=list(lis[0].split('\t'))
			#print(lis)
			temp.append(float(lis[0]))
			temp.append(int(lis[1]))
			#temp.append(float(lis[2]))
			#temp.append(float(lis[3]))
			xtrain.append(temp)
			t=str(lis[4]).replace('\n','')
			t=int(t)
			ytrain.append(t)
		f.close()
		#print(xtrain)
		#print("len(xtrain)",len(xtrain))
		#print(ytrain)
		#print("len(ytrain)",len(ytrain))
		loc_exec=float(total_exec_time)
		loc_cpu=int(c_det[2])
		xtest=[]
		xtemp=[]
		xtemp.append(loc_exec)
		xtemp.append(loc_cpu)
		xtest.append(xtemp)
		ytest=[]
		xtrain_np=np.array(xtrain)
		ytrain_np=np.array(ytrain)
		#print("np array x:",xtrain_np)
		#print("np array y:",ytrain_np)
		xtest_np=np.array(xtest)
		#xtest_np.reshape(-1,1)
		ytest_np=np.array(ytest)
		#print("The number of train set :",len(xtrain))
		#print("The train set:",xtest)
		treesCount=3
		predRF=randomForest(xtrain_np,ytrain_np,xtest_np,treesCount)
		print("predicted random forest result")
		print(predRF)
		
		#predRF[0]=0
		if(predRF[0]==0):
			print("local Exec")
			argf='python3 '+str(f_name)+'.py'
			os.system(argf)
			sys.exit()
			pass

		#methodResults(predRF=ytest_np)
		#predtree=decisiontree(xtrain_np,ytrain_np,xtest_np,3)
		#print("decision tree result:")
		#print(predtree)



		'''
		for i,node in enumerate(d_list[1:]):
			local_exec=True
			
			if node in offload_fog_list:
				for n in graph[node]:
					if n not in offload_fog_list:
						putannot(f_name,n,'@offload_fog\n')
						local_exec=False
				continue
			elif(cpu_util_avg>f_cpu_util_avg):
				#if(pi_res_time+(e_map[node]/2)<e_map[node] and(nw_up>float(1.0) and nw_dwn>float(1.0))):
				#if(pi_res_time+(e_map[node]/2)<e_map[node]): #original condition
				if(e_map[node]/2<e_map[node]): #dummy condition
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
		'''
		#function to copy the methods to be offloaded to a new file
		'''
		offload_func(f_name)
		if(len(offload_fog_list)>0):
			socket_func(f_name)
		'''
		addrs=netifaces.ifaddresses('wlan0')
		addrs=list(addrs[netifaces.AF_INET])
		addrs=dict(addrs[0])
		w_cnt=0
		while True:
			e_details=[]
			client=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
			client.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
			client.bind(("",3000))
			msg='broadcast from:'+str(addrs['addr'])
			msg=str(msg)
			client.sendto(msg.encode('ascii'),('192.168.43.255',4444))
			print("message sent")
			client.close()
			tcpip=''
			tcpport=5555
			buffer_size=2048
			tcpserv=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			tcpserv.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
			tcpserv.bind((tcpip,tcpport))
			tcpserv.settimeout(5)
			threads=[]
			tcpserv.listen(4)
			while True:
				try:
					(conn,(ip,port))=tcpserv.accept()
					newthread = ClientThread(ip,port)
					newthread.start()
					threads.append(newthread)
				except socket.timeout as e:
					print("connection over")
					tcpserv.close()
					break
			for t in threads:
				t.join()
			print("edge devices list:",e_details)
			if(len(e_details)==0 and w_cnt<1):
				w_cnt=1
			elif(len(e_details)==0 and w_cnt>0):
				print('local execution ')
				argexec='python3 '+str(f_name)+'.py'
				os.system(argexec)
				sys.exit()
			else:
				break
		reject_list=[]
		if(len(e_details)>1):
			ipdict=dict()
			ip=[]
			for i in e_details:
				temp=str(i.split("'")[-2])
				t=str(temp.split(" ")[0])
				ip.append(t)
				ipdict[t]=list(temp.split(" ")[1:])
			maxdiff=0
			selected='none'
			for i in ip:
				print(i,end="->")
				print(ipdict[i])
				if((float(ipdict[i][2])-float(ipdict[i][1]))>maxdiff):
					maxdiff=float(ipdict[i][2])-float(ipdict[i][1])
					if(selected=='none'):
						selected=i
					else:
						reject_list.append(selected)
						selected=i
				else:
					reject_list.append(i)
			print(selected)
			print(reject_list)
		else:
			if(len(e_details)==1):
				temp=e_details[0]
				temp=str(temp.split("'")[-2])
				temp=str(temp.split(" ")[0])
				selected=temp
			else:
				argl='python3 '+str(f_name)+'.py'
				os.system(argl)
				sys.exit()
				pass #to be updated
				#execute local

		#3rd communication
		cli=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		cliport=8888
		cli.bind(("",cliport))
		local_flag=0
		if(len(e_details)>1 and (float(psutil.cpu_freq().max)-float(psutil.cpu_freq().current))>maxdiff):
			local_flag=1
			reject_list.append(selected)
		for i in reject_list:
			#cli=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
			port=7777
			msg='reject'
			msg=str(msg)
			cli.sendto(msg.encode('ascii'),(i,port))
		#cli=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		if(local_flag==1):
			argf='python3 '+str(f_name)+'.py'
			os.system(argf)
			sys.exit()
		port=7777
		msg='ok'
		msg=str(msg)
		cli.sendto(msg.encode('ascii'),(selected,port))
		data,addr=cli.recvfrom(1024)
		cli.close()
		data=data.decode('ascii')
		if(data=='ok'):
			#send code through tcp
			print("code to be sent")
			client=f_name+'1.py'
			server=f_name+'2.py'
			fname=f_name+'.py'
			ipaddress=selected
			if(len(offload_list)>0):
			
			#writing client file
				f=open(fname,'r')
				l=f.readlines()
				l1='import xmlrpc.client\n'
				l2='proxy=xmlrpc.client.ServerProxy("http://{ip}:8000/")\n'.format(ip=ipaddress)
				l.insert(0,l1)
				l.insert(1,l2)
				access=1
				cnt=0
				for j,line in enumerate(l):
					if(line.startswith('if __name__')):
						access=1
					if(line.startswith('def')):
						for i in offload_list:
							if(line.find(i)!=-1):
								access=0
								cnt=1
								del l[j]
								l.insert(j,'')
								break
						if(cnt!=1):
							access=1
						else:
							cnt=0
					elif(access==1):
						for i in offload_list:
							if(line.find(i)!=-1):
								st='proxy.'+i
								li=line.replace(i,st)
								del l[j]
								l.insert(j,li)
					else:
						del l[j]
						l.insert(j,'')
				f.close()
				f=open(client,'w')
				for line in l:
					f.write(line)
				f.close()

				#writing server file
				f=open(fname,'r')
				l=f.readlines()
				access=0
				cnt=0
				for j,line in enumerate(l):
					if(line.startswith('if __name__')):
						del l[j]
						l.insert(j,'')
						access=0
						continue
					if(line.startswith('def')):
						for i in offload_list:
							if(line.find(i)!=-1):
								access=1
								cnt=1
								break
						if(cnt!=1):
							access=0
							del l[j]
							l.insert(j,'')
						else:
							cnt=0
					elif(access==0):
						del l[j]
						l.insert(j,'')
				f.close()
				f=open(server,'w')
				l1='from xmlrpc.server import SimpleXMLRPCServer\n'
				l.insert(0,l1)
				l2='\nserver = SimpleXMLRPCServer(("",8000))\n'
				l.append(l2)
				for i in offload_list:
					l1='server.register_function({func},"{func}")\n'.format(func=i)
					l.append(l1)
				l1='server.serve_forever()\n'
				l.append(l1)
				for line in l:
					f.write(line)
				f.close()


				s=socket.socket()
				host=ipaddress
				port=9999
				s.connect((host,port))
				name=f_name+'2.py'
				s.send(name.encode('ascii'))
				#s.close()
				#s.connect((host,port))
				f=open(name,'rb')
				l=f.read(1024)
				while(l):
					s.send(l)
					l=f.read(1024)
				f.close()
				s.close()
				print("file sent for execution")
				#added new
				socketcloud=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
				udphost=''
				port=22222
				socketcloud.bind((udphost,port))
				data,addr=socketcloud.recvfrom(1024)
				data=data.decode('ascii')
				print('cloud or ok',data)
				if(data=='cld'):
					fa=open(f_name+'1.py','r')
					la=fa.readlines()
					for j,line in enumerate(la):
						if(line.startswith('proxy')):
							line='proxy=xmlrpc.client.ServerProxy("http://142.93.222.110:8000/")\n'
							del la[j]
							la.insert(j,line)
							break
					fa.close()
					fa=open(f_name+'1.py','w')
					for line in la:
						fa.write(line)
					fa.close()
				#added new
				end_time=time.time()+2
				while True:
					if(time.time()>end_time):
						break
				filename=f_name+'1.py'
				#important code
				arg1='python3 '+str(filename)
				os.system(arg1)
				'''
				process=subprocess.Popen(['python3',filename])
				print("process id:",process.pid)
				cmd="ps -p {p_id} -o %cpu".format(p_id=process.pid)
				re=str(get_simple_cmd_output(cmd))
				print("result:",re)
				try:
					process.wait(timeout=15)
				except subprocess.TimeoutExpired:
					print('timed out killing ',process.pid)
				print('done')
				filename=f_name+'.py'
				process1=subprocess.Popen(['python3',filename])
				print("process1 id:",process.pid)
				cmd="ps -p {p_id} -o %cpu".format(p_id=process1.pid)
				re=str(get_simple_cmd_output(cmd))
				print("result:",re)
				try:
					process1.wait(timeout=15)
				except subprocess.TimeoutExpired:
					print('timed out killing',process1.pid)
				'''