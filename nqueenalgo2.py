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


def solveNQUtil(board, col): 
	# base case: If all queens are placed 
	# then return true 
	r=[]
	if col >= 10: 
		r.append(True)
		r.append(board)
		return r

	# Consider this column and try placing 
	# this queen in all rows one by one 
	for i in range(10): 

		if(isSafe(board, i, col)): 
			# Place this queen in board[i][col] 
			board[i][col] = 1

			# recur to place rest of the queens 
			res=solveNQUtil(board,col+1)
			board=res[1].copy()
			if res[0] == True: 
				r.append(True)
				r.append(board)
				return r

			# If placing queen in board[i][col 
			# doesn't lead to a solution, then 
			# queen from board[i][col] 
			board[i][col] = 0

	# if the queen can not be placed in any row in 
	# this colum col then return false 
	r.append(False)
	r.append(board)
	return r

# This function solves the N Queen problem using 
# Backtracking. It mainly uses solveNQUtil() to 
# solve the problem. It returns false if queens 
# cannot be placed, otherwise return true and 
# placement of queens in the form of 1s. 
# note that there may be more than one 
# solutions, this function prints one of the 
# feasible solutions. 

#offload=no

server = SimpleXMLRPCServer(("",8000))
server.register_function(solveNQUtil,"solveNQUtil")
server.register_function(isSafe,"isSafe")
server.serve_forever()
