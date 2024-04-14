import copy

class Stack:

    def __init__(self):
        self.items = []

    def isEmpty(self):
        if self.size() == 0:
            return True
        return False

    def push(self, item): #Add an item to the stack
        self.items.append(item)

    def pop(self): #Removes and returns the element on the top of the stack
        return self.items.pop(self.size() - 1)

    def peek(self): #Returns the element at the top of the stack without popping (removing) it.
        return self.items[self.size() - 1]

    def size(self):
        return len(self.items)

    def printout(self):
        return self.items


class Queue:

    def __init__(self):
        self.items = []

    def isEmpty(self):
        if self.size() == 0:
            return True
        return False

    def enqueue(self, item): #Put a new element in the back of the line (simply putting it at end of list)
        self.items.append(item)

    def dequeue(self): #Pops the first element in index 1
        return self.items.pop(0)

    def size(self):
        return len(self.items)

    def printout(self):
        return self.items


#Separating Stacks/Queues from Graphs

class Graph:

    def __init__(self,aGraph):
        self.graph = copy.deepcopy(aGraph) #Deep copy.

    #Function to generate the list of all edges

    #This function generates a list of all connections between each vertex, also known as edges.
    def generate_edges(self):
        edges = []
        for node in self.graph: #This for loop traverses our dictionary
            for neighbour in self.graph[node]: #This for loop finds each connection present between our dictionary keys
                edges.append((node, neighbour)) #This will add each connection

        return edges

    # Function to calculate isolated nodes of a given graph
    def find_isolated_nodes(self):
        """ returns a list of isolated nodes. """
        isolated = []
        for node in self.graph: #This loop traverses our dictionary
            if not self.graph[node]: #If there is nothing found, the node is isolated (no connections). This happens even if something
                #else connected to it, without the node itself connecting to anything, however.
                isolated += node
        return isolated


    #Function to find a path from a start vertex to an end vertex
    def find_path(self, start_vertex, end_vertex, path=None):
        """ find a path from start_vertex to end_vertex in graph """
        if path == None:
            path = []
        path = path + [start_vertex] #We start with the first vertex
        if start_vertex == end_vertex: #If the start and end are the same, it returns itself
            return path
        if start_vertex not in self.graph: #If the start doesn't exist, we return None
            return None
        for vertex in self.graph[start_vertex]: #For loop goes through each connection in the start vertex
            if vertex not in path: #We add the vertex found if it's not in the path
                extended_path = self.find_path(vertex,end_vertex,path) #We recurse, using the new start and same end goal.
                if extended_path: #This if statement occurs if a valid path has been found (if start_vertex==end_vertex)!
                    return extended_path #Since the layer returned, we return everything (the finished path).
        return None

    # The algorithm uses an important technique called backtracking: it tries each possibility in turn until it finds a solution.

    # Function to find all the paths between a start vertex to an end vertex

    def find_all_paths(self, start_vertex, end_vertex, path=[]):
        """ find all paths from start_vertex to
            end_vertex in graph """
        path = path + [start_vertex] #Path starts with the start vertex
        if start_vertex == end_vertex: #If the start equals the end, it returns and the iterations continue from the recursion point
            return [path]
        if start_vertex not in self.graph: #If the start is invalid, we return nothing
            return []
        paths = [] #All valid paths
        for vertex in self.graph[start_vertex]: #We traverse through each connection in the start
            if vertex not in path: #If the visited vertex is not in the path, we add it and go further below
                extended_paths = self.find_all_paths(vertex,end_vertex,path) #This recurses and changes the start to the new vertex
                for p in extended_paths: #If a return is hit (because a valid path is found) then it is appended to paths
                    #and the above for loop continues, to search for more paths.
                    paths.append(p)
        return paths #After the for loop, we return all paths detected.

    '''
    A graph is said to be connected if every pair of vertices in the graph is connected. 
    The example graph on the right side is a connected graph.
    It possible to determine with a simple algorithm whether a graph is connected:
    Choose an arbitrary node x of the graph G as the starting point
    Determine the set A of all the nodes which can be reached from x.
    If A is equal to the set of nodes of G, the graph is connected; otherwise it is disconnected.
    '''
    #  Function to check if a graph is a connected graph.

    def is_connected(self, vertices_encountered=None,start_vertex=None):
        """ determines if the graph is connected """
        if vertices_encountered is None: #We initialize vertices_encountered
            vertices_encountered = set()
        vertices = list(self.graph.keys())  # "list" necessary in Python 3
        if not start_vertex: #If start vertex is none we pick the first key in the dictionary
            # choose a vertex from graph as a starting point
            start_vertex = vertices[0]
        vertices_encountered.add(start_vertex) #We encountered the start
        if len(vertices_encountered) != len(vertices): #This is basically saying that if the graph is connected,
        # all vertices must be encountered, no matter where we start from.
        #For right now, it isn't, so we keep encountering this statement until it is true.
            for vertex in self.graph[start_vertex]: #We run through each vertex's connections
                if vertex not in vertices_encountered: #If the vertex found is not encountered yet
                    if self.is_connected(vertices_encountered, vertex): #We recurse and change the start to the new vertex
                        return True
                #If the vertex is in vertices_encountered, the program returns quickly and the for loop resumes.
        else: #The trues keep cascading and eventually this returns on the final run if the encounters = the total number of vertices
            return True
        return False #Otherwise, false is returned as the last run.

    def do_bfs(self,value=None):

        if value is None or self.graph.get(value) is None: #If the start is invalid or nothing, we initialize it to the first key
            value = list(self.graph.keys())[0]

        marked = [] #Marks visited nodes
        cue = Queue() #This queue processes each node added when adjacents are found (Queue had to be imported. It works, trust)

        for i in self.graph.get(value): #Basically, we enqueue each thing connected to the first node.
            cue.enqueue(i)
        marked.append(value) #We append the starting node

        while len(marked) < len(self.graph.keys()): #This runs until the length is equal to the number of keys (all nodes visited)

            while not cue.isEmpty(): #If the queue named cue has entries, we need to visit them

                yesAppend = False #This flag ensures only one thing is appended for each run that adds neighbors.
                newvalue = cue.dequeue() #New value is the front of the queue that neighbors and stuff are scanned for

                for i in self.graph.get(newvalue): #We traverse the connections found for each node

                    if newvalue not in marked: #If the key is not marked, we enqueue each neighbor
                        cue.enqueue(i)
                        yesAppend = True #In the end, this key will be marked.

                    else:
                        pass

                if len(self.graph.get(newvalue)) == 0 and newvalue not in marked: #If there are no connections (the previous for loop
                    #was skipped) then this ensures the isolated node is added.
                    yesAppend = True

                if yesAppend: #We add the encountered node, after enqueueing all of its potential neighbors
                    marked.append(newvalue)

            for x in self.graph.keys(): #AFTER THE QUEUE IS EMPTY, we check for missing nodes and enqueue it (because if the
                #length of marked is not equal to all keys, we missed a node) the loop then restarts and the queue isn't empty,
                #so that restarts.
                if x not in marked:
                    cue.enqueue(x)
                    break #break the for loop so it doesn't keep runnning if a non-marked entry is found

        return marked

    def do_dfs(self,value=None):

        if value is None or self.graph.get(value) is None:
            value = list(self.graph.keys())[0]

        marked = [] #Marks visited nodes
        stick = Stack() #This stack processes each node added when adjacents are found (Stack had to be imported. It works, trust x 2)

        stick.push(value) #Push the first node

        while len(marked) < len(self.graph.keys()): #Similar logic to bfs, except this goes down the chain then starts backing up
            #when neighbors run out

            while not stick.isEmpty():

                hit = False

                for i in self.graph.get(stick.peek()): #The top of the stack is peeked and its connections are as well in this loop
                    if stick.peek() not in marked: #If for some reason the node isn't marked despite being visited
                        marked.append(stick.peek())
                    if i not in marked: #If a connection isn't found in marked, we append it
                        #then push it onto the stack to look for neighbors
                        marked.append(i)
                        stick.push(i)
                        hit = True
                        break

                if not hit: #If nothing is found, we pop the stack (which happens if nodes that already exist are found).
                    stick.pop()

            for x in self.graph.keys(): #This only runs if not all nodes have been visited yet (the big while loop)
                if x not in marked: #We traverse the keys.
                    stick.push(x) #We push this then break the for loop to start another go around if we find this isolated node
                    break

        return marked
		
'''
    references:
    https://www.python-course.eu/graphs_python.php
    https://www.python.org/doc/essays/graphs/
    test
    
'''
