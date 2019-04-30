import sys
import os

li=list(sys.argv)
#print("removing annotation for ",li[1:])
for i in range(1,len(li)):
	f=open(li[i],'r')
	l=f.readlines()
	for j,line in enumerate(l):
		if(line.startswith('@profile')):
			del l[j]
		elif(line.startswith('@execute_local')):
			del l[j]
		elif(line.startswith('@offload_fog')):
			del l[j]
		elif(line.startswith('@offload_cloud')):
			del l[j]
		elif(line.startswith('@offload')):
			del l[j]
	f.close()
	f=open(li[i],'w')
	for line in l:
		f.write(line)
	f.close()

