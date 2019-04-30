import xmlrpc.client
proxy=xmlrpc.client.ServerProxy("http://192.168.43.28 0.2 600.0 1200.0:8000/")
def print_grid(arr):
	for i in range(9):
		for j in range(9):
			print(arr[i][j],end=" ")
		print("\n")

if __name__=="__main__":
	grid=[[0 for x in range(9)] for y in range(9)]
	grid=[[3,0,6,5,0,8,4,0,0],
		[5,2,0,0,0,0,0,0,0],
		[0,8,7,0,0,0,0,3,1],
		[0,0,3,0,1,0,0,8,0],
		[9,0,0,8,6,3,0,0,5],
		[0,5,0,0,9,0,6,0,0],
		[1,3,0,0,0,0,2,5,0],
		[0,0,0,0,0,0,0,7,4],
		[0,0,5,2,0,6,3,0,0]]
	res=proxy.solve_sudoku(grid)
	if(res[0]==True):
		print_grid(res[1])
	else:
		print("no solution exists")
		print_grid(res[1])

