import os
import netifaces
import psutil
import sys
import shlex
import subprocess
from subprocess import Popen,PIPE,STDOUT
import time

def get_simple_cmd_output(cmd,stderr=STDOUT):
	args=shlex.split(cmd)
	return Popen(args,stdout=PIPE,stderr=stderr).communicate()[0]


filename='sudokusolver.py'
process=subprocess.Popen(['python3',filename])
print("process id:",process.pid)
cmd="ps -p {p_id} -o %cpu".format(p_id=process.pid)
re=str(get_simple_cmd_output(cmd))
print("result:",re)
try:
	#cmd="ps -p {p_id} -o %cpu,%mem,cmd".format(p_id=process.pid)
	process.wait(timeout=15)
	#re=str(get_simple_cmd_output(cmd))
	#print("result:",re)
except subprocess.TimeoutExpired:
	print('timed out killing ',process.pid)
	#re=str(get_simple_cmd_output(cmd))
	#print("result:",re)
	#process.kill()
#re=str(get_simple_cmd_output(cmd))
print('done')

