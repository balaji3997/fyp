from xmlrpc.server import SimpleXMLRPCServer

def find_empty_location(arr,l):
	res=[]
	for row in range(9):
		for col in range(9):
			if(arr[row][col]==0):
				l[0]=row
				l[1]=col
				res.append(True)
				res.append(l)
				return res
	res.append(False)
	res.append(l)
	return res

def used_in_row(arr,row,num):
	for i in range(9):
		if(arr[row][i] ==num):
			return True
	return False
def used_in_col(arr,col,num):
	for i in range(9):
		if(arr[i][col] == num):
			return True
	return False

def used_in_box(arr,row,col,num):
	for i in range(3):
		for j in range(3):
			if(arr[i+row][j+col]==num):
				return True
	return False

def check_location_is_safe(arr,row,col,num):
	return not used_in_row(arr,row,num) and not used_in_col(arr,col,num) and not used_in_box(arr,row-row%3,col-col%3,num)


server = SimpleXMLRPCServer(("localhost",8000))
print("listening on port 8000")
server.register_function(check_location_is_safe,"check_location_is_safe")
server.register_function(used_in_row,"used_in_row")
server.register_function(used_in_col,"used_in_col")
server.register_function(used_in_box,"used_in_box")
server.register_function(find_empty_location,"find_empty_location")
server.serve_forever()
