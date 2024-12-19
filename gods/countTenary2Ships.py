from numba import jit,njit,prange,int32,int8
from rich.progress import track
import numpy as np
from godsNumber import plotBoard,multiplotBoard

@jit
def countP2(pattern):
    possible = 0 
    field = np.zeros((10,10))
    for i in pattern:
        field[i]=1
    for row in range(10):
        #count vertical 
        for col in range(10):
            if col == 9:
                continue 
            if field[row,col] == 0 and field[row,col+1] == 0:
                possible+=1
        #count horizontal 
        if row == 9:
            continue 
        for col in range(10):
            if field[row,col] == 0 and field[row+1,col] ==0:
                possible+=1
    return possible

if __name__ == "__main__":
    patterns = [[(i,j)  for i in range(10) for j in range(10) if  (i+j)%3 == k ] for k in range(3)]

    for idx,i in enumerate(patterns):
        print(idx,countP2(i))
    P = patterns[0]+[(i,j) for i in range(5) for j in range(6)]
    M = np.zeros((10,10))
    print("bollen Formation:",countP2(P))
