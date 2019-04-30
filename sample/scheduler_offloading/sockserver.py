import socket
import threading
import socketserver
import time
l=[]
class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
	
	def handle(self):
		data=str(self.request.recv(1024),'ascii')
		cur_thread=threading.current_thread()
		print(data)
		l.append(data)

class ThreadedTCPServer(socketserver.ThreadingMixIn,socketserver.TCPServer):
	pass

HOST=""
PORT=9999

server=ThreadedTCPServer((HOST,PORT),ThreadedTCPRequestHandler)
with server:
	server_thread=threading.Thread(target=server.serve_forever)
	server_thread.daemon=True
	server_thread.start()
	server.settimeout(5)
	server.serve_forever()


print("outside server kill")
print("ip address:",l)
