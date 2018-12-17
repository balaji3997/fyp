import sys
li=list(sys.argv)
print("the list of arguments",li)
for i in range(1,len(li)):
	f=open(li[i],'r')
	l=f.readlines()
	s='@profiler.do_profile(follow=[])\n'
	for j,line in enumerate(l):
		if(line.startswith('def')):
			line=s+line
			del l[j]
			l.insert(j,line)
		#print(i,end="")
		print(line,end=" ")
	f.close()
	f=open(li[i],'w')
	f.write('import profiler\n')
	for line in l:
		f.write(line)
	f.close()
