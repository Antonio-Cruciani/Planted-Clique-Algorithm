import numpy as np
import networkx as nx
import heapq 
import time

#Importing the Graph

fh=open("graph.el", 'rb')
G=nx.read_edgelist(fh)
fh.close()

k = 70

#--------------------------------------

#Defining Heap data structure
# Heap data structure

class Heap(object):
    
    def __init__(self):
          #create a new heap. 
        self._heap = []

    def push(self, priority, item):
        # Push an item with priority into the heap.
        # Priority 0 is the lowest, which means that such an item will
        # be popped last.
        assert priority >= 0
        heapq.heappush(self._heap, (-priority, item))

    def pop(self):
        # Returns the item with lowest priority. 
        item = heapq.heappop(self._heap)[1] # (prio, item)[1] == item
        return item

    def __len__(self):
        return len(self._heap)

    def __iter__(self):
        # Get all elements ordered by desc. priority. 
        return self

    def next(self):
        # Get all elements ordered by their priority (max first). 
        try:
            return self.pop()
        except IndexError:
            raise StopIteration

# -------------------------------------------------------------
# Write on file the planted clique,
# where the first row of the file is the size of the clique
# and from 2nd row to the end there is the nodes of the planted clique

def write_results(solution):
    outF = open("PlantedClique.txt", "w")
    s = map(str, solution) 
    k = [str(len(solution))]
    textList =k+s
    for line in textList:
        outF.write(line)
        outF.write("\n")
    outF.close()    

#Spectral Algorithm without Heap Data structure

def Spectral_Algorithm(G,k):
    start = time.time()

    # Getting the Adjacency matrix of G

    adj =nx.to_numpy_matrix(G)

    # Declaring J the matrix where every coordinate is 1

    J = np.ones(shape=(np.shape(adj)[0],np.shape(adj)[1]))

    # Creating M the matrix that is -(1/2) where in adj there was a 0 
    # and (1/2) where in adj there was a 1

    M = adj-((0.5)*J)

    # Getting eigenvalues and eigenvectors of M

    w,v = np.linalg.eigh(M)

    # Getting the eigenvector of the max eigenvalue (mev)

    mev = v[:,np.shape(adj)[1]-1]
    lista= list()
    lista_abs = list()

    # Loop that get the indices of the nodes (in lista)
    # ad getting the absolute value of the vector coordinates (lista_abs)

    for i in xrange(0,np.shape(adj)[1]-1):        
        lista.append ((v[i,np.shape(adj)[1]-1],i))
        lista_abs.append ((abs(v[i,np.shape(adj)[1]-1]),i))

    # Sorting the abs list 

    sorted_list = sorted(lista_abs,key=lambda x: x[0],reverse = True)
    K =[]
    for i in xrange(0,k):
        K.append(sorted_list[i][1])
    C = []

    # Taking the set of vertices v in V that have at least (3/4)k neighbors in lista_abs

    for i in xrange(0,len(adj)):
        c= 0
        c =adj[i,K].sum()
        if ( (3.0/4.0)*k <= c):
        
            C.append(i)

    print "K-Planted clique nodes \n",C
    print "Dimension of C:",len(C),"\n"
    print "Running time:",(time.time() - start),"\n"
    return C


# Spectral Algorith with Heap datastructure for taking the k-highest abs value

def Spectral_Algorithm_heap(G,k):
    start = time.time()

    # Getting the Adjacency matrix of G

    adj =nx.to_numpy_matrix(G)

    # Declaring J the matrix where every coordinate is 1

    J = np.ones(shape=(np.shape(adj)[0],np.shape(adj)[1]))

    # Creating M the matrix that is -(1/2) where in adj there was a 0 
    # and (1/2) where in adj there was a 1

    M = adj-((0.5)*J)

    # Getting eigenvalues and eigenvectors of M

    w,v = np.linalg.eigh(M)

    # Getting the eigenvector of the max eigenvalue (mev)

    mev = v[:,np.shape(adj)[1]-1]
    lista= list()
    lista_abs = list()
    # Loop that get the indices of the nodes (in lista)
    # ad getting the absolute value of the vector coordinates (lista_abs)

    for i in xrange(0,np.shape(adj)[1]-1):        
        lista.append ((v[i,np.shape(adj)[1]-1],i))
        lista_abs.append ((abs(v[i,np.shape(adj)[1]-1]),i))

    # Creating an Heap

    h = Heap()
    K=[]

    # Pushing values in the Heap

    for i in lista_abs:
        h.push(i[0],i[1])
    i=0

    # Getting the k highest values

    for item in h:
        K.append(item)
        # I know this break is not funny
        if i>=k:
            break 
        i+=1
    C = []

    # Taking the set of vertices v in V that have at least (3/4)k neighbors in lista_abs
    
    for i in xrange(0,len(adj)):
        c= 0
        c =adj[i,K].sum()
        if ( (3.0/4.0)*k <= c):
        
            C.append(i)

    print "K-Planted clique nodes \n",C
    print "Dimension of C:",len(C),"\n"
    print "Running time:",(time.time() - start),"\n"
    return C



#Invoking the Spectral Algorithm without Heap
print "\n Spectral Algorithm without Heap \n"
snoh = Spectral_Algorithm(G,k)



# Write Results on file
print "\n Writing on file \n"
write_results(snoh)
print "\n Done!\n"
    

#Invoking the Spectral Algorithm with Heap 
print "\n Spectral Algorithm with Heap \n"
sheap = Spectral_Algorithm_heap(G,k)



    

