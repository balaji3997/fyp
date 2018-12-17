def get_exectime(f_name):
	exec_map={}
	fil=open(f_name+'1.txt','r')
	li=fil.readlines()
	for j,line in enumerate(li):
		if(line.startswith('Function')):
			#print("fun name: ",line.split()[-4])
			#print("fun time: ",li[j+1].split()[-2])
			exec_map[str(line.split()[-4])]=float(li[j+1].split()[-2])
	print(exec_map)

f_name='nqueenalgo'
get_exectime(f_name)
