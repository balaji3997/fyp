import shlex
from subprocess import Popen,PIPE,STDOUT

def get_simple_cmd_output(cmd, stderr=STDOUT):
	"""
	Execute a simple external command and get its output.
	"""
	args = shlex.split(cmd)
	return Popen(args, stdout=PIPE, stderr=stderr).communicate()[0]

def get_ping_time(host='192.168.43.28'):
	host = host.split(':')[0]
	cmd = "fping {host} -C 3 -q".format(host=host)
	# result = str(get_simple_cmd_output(cmd)).replace('\\','').split(':')[-1].split() if x != '-']
	re=str(get_simple_cmd_output(cmd))
	print(re)
	result = list(re.strip().split(':')[-1].strip().replace("\n'",'').split())
	#.replace("\n'",'').replace("-",'-1').split()
	result[-1]=result[-1].replace("\\n'",'')
	print(result)
	res = [float(x) for x in result if(x!='-')]
	if(len(res) > 0):
		#return sum(res) / len(res)
		print(str(sum(res)/len(res)))
	else:
		print("problem finding the latency")
		#return 999999

'''
def main():
	# sample hard code for test
	#host = 'google.com'
	host='192.168.43.28'
	#host='206.189.170.41'
	r=str(get_ping_time(host))
	if(r=='999999'):
		print("problem finding the latency")
	else:
		print(r[0:7])
	#host = 'besparapp.com'
	#print([host, get_ping_time(host)])
if __name__=='__main__':
	main()
'''
get_ping_time()
