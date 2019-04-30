from xmlrpc.server import SimpleXMLRPCServer
import time
def evenorodd(n):
	if(n%2==1):
		return True
	else:
		return False

def is_even(n):
    return evenorodd(n)

server = SimpleXMLRPCServer(("localhost", 8000))
print("Listening on port 8000...")
server.register_function(is_even, "is_even")
server.register_function(evenorodd,"evenorodd")
server.serve_forever()

