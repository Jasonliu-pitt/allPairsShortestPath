import argparse
import os
import re
import cProfile

# Command line arguments
parser=argparse.ArgumentParser(description='Calculate the shortest path between all pairs of vertices in a graph')
parser.add_argument('--algorithm',default='a',\
    help='Algorithm: Select the algorithm to run, default is all. (a)ll, (b)ellman-ford only or (f)loyd-warshall only')
parser.add_argument('-v','--verbose',action='store_true')
parser.add_argument('--profile',action='store_true')
parser.add_argument('filename',metavar='<filename>',help='Input file containing graph')

graphRE=re.compile("(\\d+)\\s(\\d+)")
edgeRE=re.compile("(\\d+)\\s(\\d+)\\s(-?\\d+)")

vertices=[]
edges=[]

def BellmanFord(G):
    pathPairs=[]
    
    #Initialize the pathPairs
    for source in G[0]:
        pathPairs.append([float('inf')]*len(G[0]))
        pathPairs[source][source]=0
                                  
    #Relaxation
    for source in G[0]:
        flag = True
        for i in G[0]:
            if flag:
                flag = False
            else:
                break
            for u,v,w in G[1]:
                if w != float("inf") and pathPairs[source][v-1] > pathPairs[source][u-1] + int(w):
                    pathPairs[source][v-1] = pathPairs[source][u-1] + int(w)
                    flag = True
                    
    #Check negative cycle
    for source in G[0]:
         for u,v,w in G[1]:
                if pathPairs[source][v-1] > pathPairs[source][u-1] + int(w):
                    return False
    # The pathPairs list will contain the 2D array of shortest paths between all pairs of vertices 
    # [[w(1,1),w(1,2),...]
    #  [w(2,1),w(2,2),...]
    #  [w(3,1),w(3,2),...]
    #   ...]
    return pathPairs

def FloydWarshall(G):
    pathPairs=[[float('inf') for i in G[0]] for j in G[0]]

    #Initialize the pathPairs
    for source in G[0]:
        pathPairs[source][source] = 0
    for u,v,w in G[1]:
        pathPairs[u-1][v-1] = w

    #Relaxation
    for k in G[0]:
        for i in G[0]:
            for j in G[0]:
                pathPairs[i][j] = min(pathPairs[i][j],pathPairs[i][k]+pathPairs[k][j])
       
    #Check negative cycle
    for source in G[0]:
         for u,v,w in G[1]:
                if pathPairs[source][v-1] > pathPairs[source][u-1] + int(w):
                    return False
    # The pathPairs list will contain the 2D array of shortest paths between all pairs of vertices 
    # [[w(1,1),w(1,2),...]
    #  [w(2,1),w(2,2),...]
    #  [w(3,1),w(3,2),...]
    #   ...]
    return pathPairs

def readFile(filename):
    global vertices
    global edges
    # File format:
    # <# vertices> <# edges>
    # <s> <t> <weight>
    # ...
    inFile=open(filename,'r')
    line1=inFile.readline()
    graphMatch=graphRE.match(line1)
    if not graphMatch:
        print(line1+" not properly formatted")
        quit(1)
    vertices=list(range(int(graphMatch.group(1))))
    edges=[]
    for line in inFile.readlines():
        line = line.strip()
        edgeMatch=edgeRE.match(line)
        if edgeMatch:
            source=edgeMatch.group(1)
            sink=edgeMatch.group(2)
            if int(source) > len(vertices) or int(sink) > len(vertices):
                print("Attempting to insert an edge between "+source+" and "+sink+" in a graph with "+vertices+" vertices")
                quit(1)
            weight=edgeMatch.group(3)
            #save edges formatted as “<source> <sink> <weight>” 
            edges.append([int(source),int(sink),int(weight)])
    G = (vertices,edges)
    return G

def matrixEquality(a,b):
    if len(a) == 0 or len(b) == 0 or len(a) != len(b): return False
    if len(a[0]) != len(b[0]): return False
    for i,row in enumerate(a):
        for j,value in enumerate(b):
            if a[i][j] != b[i][j]:
                return False
    return True


def main(filename,algorithm):
    G=readFile(filename)
    pathPairs = []
    # G is a tuple containing a list of the vertices, and a list of the edges
    # in the format ((source,sink),weight)
    if algorithm == 'b' or algorithm == 'B':
        # TODO: Insert timing code here
        pathPairs = BellmanFord(G)
        cProfile.runctx('BellmanFord(G)',{'BellmanFord':BellmanFord,'G':G},None)
        if pathPairs != True:
            print("Graph contains negative weight cycle")
    if algorithm == 'f' or algorithm == 'F':
        # TODO: Insert timing code here
        pathPairs = FloydWarshall(G)
        cProfile.runctx('FloydWarshall(G)',{'FloydWarshall':FloydWarshall,'G':G},None)
        if pathPairs != True:
            print("Graph contains negative weight cycle")
    if algorithm == 'a':
        print('running both')
        pathPairsBellman = BellmanFord(G)
        pathPairsFloyd = FloydWarshall(G)
        cProfile.runctx('BellmanFord(G)',{'BellmanFord':BellmanFord,'G':G},None)
        cProfile.runctx('FloydWarshall(G)',{'FloydWarshall':FloydWarshall,'G':G},None)
        pathPairs = pathPairsBellman
        if pathPairsBellman == False and  pathPairsFloyd == False:
            print("Graph contains negative weight cycle")
            with open(os.path.splitext(filename)[0]+'_shortestPaths.txt','w') as f:
                f.write("Graph contains negative weight cycle")
        else:
            if matrixEquality(pathPairsBellman,pathPairsFloyd):
                print('Floyd-Warshall and Bellman-Ford produce the same result')
            with open(os.path.splitext(filename)[0]+'_shortestPaths.txt','w') as f:
                for row in pathPairs:
                    for weight in row:
                        f.write(str(weight)+' ')
                    f.write('\n')

if __name__ == '__main__':
    args=parser.parse_args()
    main(args.filename,args.algorithm)
