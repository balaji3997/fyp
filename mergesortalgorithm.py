from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput



def merge(arr,l,m,r):
	n1=int(m-l+1)
	n2=int(r-m)
	
	L=[0]*(n1)
	R=[0]*(n2)
	
	for i in range(0,n1):
		L[i]=arr[l+i]
	
	for j in range(0,n2):
		R[j]=arr[m+1+j]
	i=0
	j=0
	k=l

	while(i<n1 and j<n2):
		if(L[i] <=R[j]):
			arr[k]=L[i]
			i+=1
		else:
			arr[k]=R[j]
			j+=1
		k+=1

	while(i<n1):
		arr[k]=L[i]
		i+=1
		k+=1

	while(j<n2):
		arr[k]=R[j]
		j+=1
		k+=1



def mergeSort(arr,l,r):
	if(l<r):
		m=int((l+(r-1))/2)
		mergeSort(arr,l,m)
		mergeSort(arr,m+1,r)
		merge(arr,l,m,r)

if __name__=="__main__":
	arr=[12,11,13,5,6,7]
	n=int(len(arr))
	print("given array is\n")
	for i in range(n):
		print(arr[i],end=" ")
	with PyCallGraph(output=GraphvizOutput()):
		mergeSort(arr,0,n-1)
	print("\n Sorted array\n")
	for i in range(n):
		print(arr[i],end=" ")
	print("\n")
