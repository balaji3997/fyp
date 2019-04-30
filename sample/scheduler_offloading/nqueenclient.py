import xmlrpc.client

proxy=xmlrpc.client.ServerProxy("http://localhost:8000/")


def printSolution(board): 
	for i in range(10): 
		for j in range(10): 
			print(board[i][j], end=' ') 
		print()


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

		if(proxy.isSafe(board, i, col)): 
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

#offload=no
def solveNQ(): 
	board = [ [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
			]  
	res=solveNQUtil(board,0)
	if(res[0] == False): 
		print("Solution does not exist")
		return False

	printSolution(res[1]) 
	return True

# driver program to test above function 

if __name__=="__main__":
	solveNQ()