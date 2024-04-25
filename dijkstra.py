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
            start_vertex (tuple): The starting vertex (coordinate) of the path.
            end_vertex (tuple): The ending vertex (coordinate) of the path.

        Returns:
            list: List of vertices (coordinates) representing the shortest path from
                  start_vertex to end_vertex.
        '''
        
        print("Finding shortest path from ", start_vertex, " to ", end_vertex)
        
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
            print("Current shortest path:", shortest_path)
            current_vertex = shortest_path[-1]
            next_vertex = None
            for neighbor, weight in self.graph[current_vertex].items():
                print("Checking neighbor:", neighbor)
                if distances[current_vertex] + weight < distances[neighbor]:
                    distances[neighbor] = distances[current_vertex] + weight
                    next_vertex = neighbor
            if next_vertex is None:
                break
            shortest_path.append(next_vertex)
            print("Updated shortest path:", shortest_path)


        #reverse the path to get it from start to end
        shortest_path.reverse()


        print("Shortest Path:", shortest_path)
        return shortest_path
            

def calculate_distance(coord1, coord2):
    '''
    Calculate the distance between two coordinates using the Haversine formula.

    Args:
        coord1 (tuple): Latitude and longitude of the first coordinate in degrees.
        coord2 (tuple): Latitude and longitude of the second coordinate in degrees.

    Returns:
        float: Distance between the two coordinates in meters.
    '''
    
    #Haversine formula to calculate distance between coordinates
    R = 6371000 #Earths radius in meters
    lat1, lon2 = coord1
    lat2, lon1 = coord2
    latitude_radians1 = math.radians(lat1)
    latitude_radians2 = math.radians(lat2)
    latitude_difference_radians = math.radians(lat2 - lat1)
    longitude_difference_radians = math.radians(lon2 - lon1)
    
    a = math.sin(latitude_difference_radians / 2) * math.sin(latitude_difference_radians / 2) + math.cos(latitude_radians1) * math.cos(latitude_radians2) * math.sin(longitude_difference_radians / 2) * math.sin(longitude_difference_radians / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = R * c
    return distance

'''
sources:

Dijkstras algorithm -
1. https://brilliant.org/wiki/dijkstras-short-path-finder/

Calculate distance (Haversine formula) - 
1. https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
2. https://louwersj.medium.com/calculate-geographic-distances-in-python-with-the-haversine-method-ed99b41ff04b

'''
