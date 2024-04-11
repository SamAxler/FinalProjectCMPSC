import copy
import heapq
import math

class Dijkstra:
    def __init__(self, graph):
        self.graph = copy.deepcopy(graph) #Deep copy
        
    def find_shortest_path(self, start_vertex, end_vertex):
        '''
        Find the shortest path from the start_vertex to the end_vertex using Dijkstra's algorithm.

        Args:
            start_vertex (tuple): The starting coordinate of the path.
            end_vertex (tuple): The ending coordinate of the path.

        Returns:
            list: List of vertices (coordinates) representing the shortest path from
                  start_vertex to end_vertex.
        '''
        
        #initialize distances
        distances = {vertex: float('inf') for vertex in self.graph}
        distances[start_vertex] = 0
        
        #priority queue to store vertices and distances
        pq = [(0, start_vertex)]
        visited = set()  #Initialize a set to keep track of visited vertices

        while pq:
            current_distance, current_vertex = heapq.heappop(pq)
            visited.add(current_vertex)
            if current_distance > distances[current_vertex]:
                continue
            for neighbor, weight in self.graph[current_vertex].items():
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(pq, (distance, neighbor))
           
        #reconstruct shortest path         
        shortest_path = [end_vertex]
        while shortest_path[-1] != start_vertex:
            current_vertex = shortest_path[-1]
            for neighbor, weight in self.graph[current_vertex].items():
                if distances[current_vertex] == distances[neighbor] + weight:
                    shortest_path.append(neighbor)
                    break

        #reverse the path to get it from start to end
        shortest_path.reverse()

        print("Shortest Path:", shortest_path)
        return shortest_path
      
'''
sources:
https://brilliant.org/wiki/dijkstras-short-path-finder/
'''
