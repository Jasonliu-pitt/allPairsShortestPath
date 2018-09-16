# allPairsShortestPath
find all Pairs Shortest Path using BellmanFord and FloydWarshall
----------------------
Command Line Arguments
----------------------
$python3  allPairsShortestPath.py --algorithm a filename -v

Calculate the shortest path between all pairs of vertices in a graph

positional arguments:
  <filename>            Input file containing graph

optional arguments:
  -h, --help            show this help message and exit
  --algorithm ALGORITHM
                        Algorithm: Select the algorithm to run, default is
                        all. (a)ll, (b)ellman-ford only or (f)loyd-warshall
                        only
  -v, --verbose
  --profile


----------------------
Discussions
----------------------

The python version I used is Python 3.6.0

function BellmanFord(G) 
calculate the shortest distance between any two points, and check if there exists
a negative cycle.

function FloydWarshall(G)
calculate the shortest distance between any two points, and check if there exists
a negative cycle.


function readFile(filename)
Read the data from the text and construct the graph as G=<vertices,edges>,where edge
are formatted as "<source>,<sink>,<weight>".

function matrixEquality(a,b)
Make sure the two method produce the same result.

I used cProfile.runctx to profile the running time, and filename_shortestPaths.txt to save the result.
if the graph doesn't contain a negative cycle, then print"Floyd-Warshall and Bellman-Ford produce the same result"
and save the 2D array of shortest paths between all pairs of vertices. otherwise, print and save"Graph contains negative weight cycle".
