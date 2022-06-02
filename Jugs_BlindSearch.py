from collections import defaultdict
import random as r
import networkx as nx
import matplotlib.pyplot as plt
from numpy import short

class Graph:
    def __init__(self) -> None:
        self.graph = defaultdict(list)

    def addEdge(self, u, v):
        self.graph[u].append(v)

    def BFS(self,s):

        parents={}
        parents[s]=None

        visited = {gi:False for gi in self.graph.keys()}

        queue =[]
        queue.append(s)

        visited[s]=True

        while queue:
            s=queue.pop(0)
            print(s, end= " ")
            for i in self.graph[s]:
                if not visited[i]:
                    queue.append(i)
                    visited[i]=True
                    parents[i]=s
        
        return parents
    
    def DFS(self,s):

        parents={}
        parents[s]=None

        visited = {gi:False for gi in self.graph.keys()}

        queue =[]
        queue.append(s)

        visited[s]=True

        while queue:
            s=queue.pop()
            print(s, end= " ")
            for i in self.graph[s]:
                if not visited[i]:
                    queue.append(i)
                    visited[i]=True
                    parents[i]=s
                    
        return parents
        
    def pathfromOrigin(self, origin, n, parents):
        if origin == n:
            return []

        pathO = [n]
        i = n

        while True:
            i = parents[i]
            pathO.insert(0, i)
            if i == origin:
                return pathO
            
class Jug:
    def __init__(self, capacity, state = 0):
        self.capacity = capacity
        self.state = state
        
    def setState(self, state):
        self.state = state
    
    def getCapacity(self):
        return self.capacity
    
    def getState(self):
        return self.state
    
    def empty(self):
        self.state = 0  
      
    def pour(self, jug):
        if jug.getState() == 0:
            if self.getState() <= jug.getCapacity():
                jug.fill(self.getState())
                self.empty()
            else:
                jug.fill(jug.getCapacity())
                self.fill(self.getState() - jug.getCapacity())
        else:
            if jug.getState() < jug.getCapacity():
                if (self.getState() + jug.getState()) <= jug.getCapacity():
                    jug.fill(self.getState() + jug.getState())
                    self.empty()
                else:
                    permitted = (jug.getCapacity() - jug.getState())
                    leftOver = abs(self.getState() - permitted)
                    jug.fill(jug.getState() + permitted)
                    self.setState(leftOver)
    
    def fill(self, content = None):
        if content is not None:
            self.setState(content)
        else:
            self.setState(self.getCapacity())
            
    def action(self, jug):
        auxEmpty = Jug(self.getCapacity(), self.getState())
        auxPour = Jug(self.getCapacity(), self.getState())
        auxFill = Jug(self.getCapacity(), self.getState())
        auxJug = Jug(jug.getCapacity(), jug.getState())
        
        auxEmpty.empty()
        auxPour.pour(auxJug)
        auxFill.fill()
        
        if self.getCapacity() == 4:
            return [(auxEmpty.getState(), jug.getState()),
                (auxPour.getState(), auxJug.getState()),
                (auxFill.getState(), jug.getState())]
        else:
            return [(jug.getState(), auxEmpty.getState()),
                (auxJug.getState(), auxPour.getState()),
                (jug.getState(), auxFill.getState())]

jugTree = Graph()
G = nx.Graph()

def generateRootChilds(bj, sj, states):
    
    childs = bj.action(sj)
    for child in childs:
        if child not in states and child not in jugTree.graph[states[-1]]:
            jugTree.addEdge(states[-1], child)
            G.add_edge(states[-1], child)
            
    childs = sj.action(bj)
    for child in childs:
        if child not in states and child not in jugTree.graph[states[-1]]:
            jugTree.addEdge(states[-1], child)
            G.add_edge(states[-1], child)

def generateChilds(bj, sj, states, state):
    auxStates = [states[-1]]
    
    for node in jugTree.graph[state]:
        if node[0] == 2:
            jugTree.addEdge(node, state)
            G.add_edge(node, state)
        else:
            auxStates.append(node)
            bj.setState(node[0])
            sj.setState(node[1])
            
            childs = bj.action(sj)
            for child in childs:
                if child not in states and child not in auxStates and child not in jugTree.graph[node]:
                    jugTree.addEdge(node, child)
                    G.add_edge(node, child)
                    
            childs = sj.action(bj)
            for child in childs:
                if child not in states and child not in auxStates and child not in jugTree.graph[node]:
                    jugTree.addEdge(node, child)
                    G.add_edge(node, child)
       
    auxStates.pop(0)
    [states.append(state) for state in auxStates]
    
def execute(bigJugCapacity, shortJugCapacity, initialState = (0,0)):
    states = [initialState]
    bigJug = Jug(bigJugCapacity, initialState[0])
    shortJug = Jug(shortJugCapacity, initialState[1])
                
    generateRootChilds(bigJug, shortJug, states)
    
    for state in states:
        generateChilds(bigJug, shortJug, states, state)
        
def main(args):
    """
    Uso:
    python jug_execution.py simulations bigJugCapacity shortJugCapacity initialState
    Parametros:
    bigJugCapacity: galons of capacity (number)
    shortJugCapacity: galons of capacity (number)
    big jug initial state: 0
    short jug initial state: 0
    Ejemplo:
    python Jugs_BlindSearch.py 4 3 0 0
    """
    answers = []
    bestAnswer = None
    
    if len(args) == 4:
        
        bigJugCapacity = int(args[0])
        shortJugCapacity = int(args[1])
        initialState = tuple((int(args[2]), int(args[3])))
        
        execute(bigJugCapacity, shortJugCapacity, initialState)
        
        # target = (2, 0) or (2, 3)
        target0 = (2, 0)
        target1 = (2, 3)
        
        print("\nBúsqueda anchura: ")
        parentsBFS = jugTree.BFS(initialState)
        print("\n", parentsBFS)
        print("ruta target 0: ", jugTree.pathfromOrigin(initialState, target0, parentsBFS))
        print("ruta target 1: ", jugTree.pathfromOrigin(initialState, target1, parentsBFS))
        
        print("\nBúsqueda profundidad: ")
        parentsDFS = jugTree.DFS(initialState)
        print("\n", parentsDFS)
        print("ruta target 0: ", jugTree.pathfromOrigin(initialState, target0, parentsDFS))
        print("ruta target 1: ", jugTree.pathfromOrigin(initialState, target1, parentsDFS))
        
        plt.figure(figsize=(10,10))
        #Ploting the graph in Kamada Kawai Layout
        nx.draw(G, with_labels=1, node_size=1000,font_size=20)
        plt.savefig("G-KamadaKawai_Layout.png")
        #Saving the figure
        # nx.draw_circular(G, with_labels=1,node_size=1000,font_size=20)
        # plt.savefig("G-Circular_Layout.png")
        
        # for key in jugTree.graph.keys():
        #     print(f"{key}: {jugTree.graph[key]} \n")
        
    else:
        print(main.__doc__)


if __name__ == "__main__":
    import sys
    main(sys.argv[1:])