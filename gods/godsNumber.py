import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


def plotBoard11(mat):
    cmap = ListedColormap(['b', 'w', 'k',"r","g"])
    plt.matshow(mat,extent=[0,11,0,11],cmap=cmap)
    print(mat)
    row_labels = range(11)
    col_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',"J","K"]
    plt.xticks(range(11), col_labels)
    plt.grid(True)
    plt.title(" blue water black hit red ship orange ship hit")
    plt.yticks(range(11), row_labels)
    return plt
def multiplotBoard(mats,dim=10):
    cmap = ListedColormap(['blue',"y", "r" ,"purple"])
    fig,axes = plt.subplots(4,len(mats))
    #fig.title(" blue water black hit red ship orange ship hit")
    #ax.yticks(range(10), row_labels)

    #ax.xticks(range(10), col_labels)
    for ax,mat in zip(axes,mats): 
        ax.imshow(2*mat,extent=[0,10,0,10],cmap=cmap)
        row_labels = range(10)
        col_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',"J"]
        ax.grid(True)
    return plt
def plotBoard(mat,dim=10):
    cmap = ListedColormap(['blue',"y", "r" ,"purple"])
   
    plt.matshow(2*mat,extent=[0,10,0,10],cmap=cmap)
    row_labels = range(10)
    col_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',"J"]
    plt.xticks(range(10), col_labels)
    plt.grid(True)
    plt.title(" blue water black hit red ship orange ship hit")
    plt.yticks(range(10), row_labels)
    return plt
