#N = 4
'''
import xmlrpc.client

proxy=xmlrpc.client.ServerProxy("http://localhost:8000/")
'''
  
# A utility function to print solution matrix sol 
def printSolution( sol ): 
      
    for i in sol: 
        for j in i: 
            print(str(j) + " ", end="") 
        print("") 
  
# A utility function to check if x,y is valid 
# index for N*N Maze 
def isSafe( maze, x, y ): 
      
    if x >= 0 and x < 4 and y >= 0 and y < 4 and maze[x][y] == 1: 
        return True
      
    return False
  
""" This function solves the Maze problem using Backtracking.  
    It mainly uses solveMazeUtil() to solve the problem. It  
    returns false if no path is possible, otherwise return  
    true and prints the path in the form of 1s. Please note 
    that there may be more than one solutions, this function 
    prints one of the feasable solutions. """
      
# A recursive utility function to solve Maze problem 
def solveMazeUtil(maze, x, y, sol): 
    res=[]
    result=[]
    #if (x,y is goal) return True 
    if x == 3 and y == 3: 
        sol[x][y] = 1
        res.append(True)
        res.append(sol)
        return res
          
    # Check if maze[x][y] is valid 
    if isSafe(maze, x, y) == True: 
        # mark x, y as part of solution path 
        sol[x][y] = 1
          
        # Move forward in x direction
        result=solveMazeUtil(maze,x+1,y,sol) 
        print(result[0])
        if result[0] == True:
            res.append(True)
            res.append(sol) 
            return res
              
        # If moving in x direction doesn't give solution  
        # then Move down in y direction
        result=solveMazeUtil(maze,x,y+1,sol) 
        if result[0] == True:
            res.append(True)
            res.append(sol) 
            return res
          
        # If none of the above movements work then  
        # BACKTRACK: unmark x,y as part of solution path 
        sol[x][y] = 0
        res.append(False)
        res.append(sol)
        return res

def solveMaze( maze ): 
      
    # Creating a 4 * 4 2-D list 
    sol = [ [ 0 for j in range(4) ] for i in range(4) ] 
    res=[]
    result=[]
    result=solveMazeUtil(maze,0,0,sol)  
    if result[0]== False: 
        print("Solution doesn't exist"); 
        res.append(False)
        res.append(sol)
        return res
      
    res.append(True)
    res.append(sol)
    return res

  
# Driver program to test above function 
if __name__ == "__main__": 
    # Initialising the maze 
    maze = [ [1, 0, 0, 0], 
             [1, 1, 0, 1], 
             [0, 1, 0, 0], 
             [1, 1, 1, 1] ] 
    res=[]           
    res=solveMaze(maze)
    if(res[0]==True):
        printSolution(res)
     