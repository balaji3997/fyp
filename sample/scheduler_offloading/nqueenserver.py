from xmlrpc.server import SimpleXMLRPCServer


def isSafe(board, row, col): 

	# Check this row on left side 
	for i in range(col): 
		if board[row][i] == 1: 
			return False

	# Check upper diagonal on left side 
	for i,j in zip(list(range(row,-1,-1)), list(range(col,-1,-1))): 
		if board[i][j] == 1: 
			return False

	# Check lower diagonal on left side 
	for i,j in zip(list(range(row,10,1)), list(range(col,-1,-1))): 
		if board[i][j] == 1: 
			return False

	return True




server = SimpleXMLRPCServer(("localhost",8000))
print("listening on port 8000")
#server.register_function(solveNQUtil,"solveNQUtil")
server.register_function(isSafe,"isSafe")
server.serve_forever()