import xmlrpc.client

proxy=xmlrpc.client.ServerProxy("http://localhost:8000/")

def print_grid(arr):
	for i in range(9):
		for j in range(9):
			print(arr[i][j],end=" ")
		print("\n")

def solve_sudoku(arr):
	l=[0,0]
	r=[]
	ans=proxy.find_empty_location(arr,l)
	if(ans[0]==False):
		r.append(True)
		r.append(arr)
		return r
	l=ans[1].copy()
	row=l[0]
	col=l[1]
	for num in range(1,10):
		if(proxy.check_location_is_safe(arr,row,col,num)):
			arr[row][col]=num
			#a=arr.copy()
			res=solve_sudoku(arr)
			arr=res[1].copy()
			if(res[0]==True):
				r.append(True)
				r.append(arr)
				return r
			arr[row][col]=0
	r.append(False)
	r.append(arr)
	return r

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
	res=solve_sudoku(grid)
	if(res[0]==True):
		print_grid(res[1])
	else:
		print("no solution exists")
		print_grid(res[1])
