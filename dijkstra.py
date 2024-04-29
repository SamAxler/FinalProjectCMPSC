import copy
import heapq
import openrouteservice as ors
from math import radians, sin, cos, sqrt, atan2

class Dijkstra:
    def __init__(self, graph, client):
        self.graph = copy.deepcopy(graph)  #Deep copy
        self.client = client
        
    def find_shortest_path(self, start_coord, end_coord):
        '''
        Find the shortest path from the start_vertex to the end_vertex using Dijkstra's algorithm.

        Args:
            start_coord (tuple): The starting vertex (coordinate) of the path.
            end_coord (tuple): The ending vertex (coordinate) of the path.

        Returns:
            list: List of vertices (coordinates) representing the shortest path from
                  start_vertex to end_vertex.
        '''
        start = tuple(start_coord)
        end = tuple(end_coord)
        if start not in self.graph or end not in self.graph:
            raise ValueError("Start or end coordinate not in graph")

        #Dictionary to store shortest distances
        distances = {vertex: float('inf') for vertex in self.graph}
        distances[start] = 0

        #Priority queue to store vertices to visit
        pq = [(0, start)]
        visited = set()  #Initialize a set to keep track of visited vertices

        while pq:
            current_distance, current_vertex = pq[0]
            heapq.heappop(pq)
            visited.add(current_vertex)
            if current_distance > distances[current_vertex]:
                continue
            for neighbor, _ in self.graph[current_vertex].items():
                if neighbor not in visited:
                    driving_distance = self.calculate_haversine_distance(current_vertex, neighbor)
                    distance = current_distance + driving_distance
                    if distance < distances[neighbor]:
                        distances[neighbor] = distance
                        heapq.heappush(pq, (distance, neighbor))

        #Reconstruct shortest path
        shortest_path = [end]
        while shortest_path[-1] != start:
            current_vertex = shortest_path[-1]
            next_vertex = None
            for neighbor, _ in self.graph[current_vertex].items():
                driving_distance = self.calculate_haversine_distance(current_vertex, neighbor)
                if distances[current_vertex] + driving_distance < distances[neighbor]:
                    distances[neighbor] = distances[current_vertex] + driving_distance
                    next_vertex = neighbor
            if next_vertex is None:
                break
            shortest_path.append(next_vertex)

        #Reverse the path to get it from start to end
        shortest_path.reverse()

        return shortest_path

    
    def calculate_driving_distance(self, start_coord, end_coord):
        '''
        Calculate the driving distance between two coordinates using OpenRouteService.

        Args:
            start_coord (tuple): Latitude and longitude of the starting coordinate.
            end_coord (tuple): Latitude and longitude of the ending coordinate.

        Returns:
            float: Driving distance between the two coordinates in miles.
        '''
        #Convert coordinates to (longitude, latitude) format
        start_lon, start_lat = start_coord
        end_lon, end_lat = end_coord

        #Calculate driving distance using OpenRouteService
        response = self.client.directions(coordinates=[[start_lon, start_lat], [end_lon, end_lat]], profile='driving-car')

        #Extract driving distance from the response (in meters)
        distance_meters = response['routes'][0]['summary']['distance']

        #Convert meters to miles (1 meter = 0.000621371 miles)
        distance_miles = distance_meters * 0.000621371

        return distance_miles
    

    #Haversine distance
    def calculate_haversine_distance(self, start_coord, end_coord):
        '''
        Calculate Haversine Distance

        Args:
            start_coord (tuple):
            end_coord (tuple):

        Returns:
            float: havesine distance between to coordinates in kilometers
        '''
        R = 6371.0

        lat1, lon1 = radians(start_coord[1]), radians(start_coord[0])
        lat2, lon2 = radians(end_coord[1]), radians(end_coord[0])

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c

        return distance


    def visualize_route(self, shortest_path):
        '''
        Visualize the route on a map using the OpenRouteService (ORS) Directions API.

        Args:
            shortest_path (list): List of vertices (coordinates) representing the shortest path.

        Returns:
            dict: Route information obtained from the ORS API.
        '''
        # Convert list of tuples to list of lists (required format for ORS)
        coordinates = [[coord[0], coord[1]] for coord in shortest_path]

        # Make API call to ORS Directions API
        response = self.client.directions(coordinates=coordinates, profile='driving-car')

        return response


'''
sources:
https://brilliant.org/wiki/dijkstras-short-path-finder/
Dijkstras algorithm -
1. https://brilliant.org/wiki/dijkstras-short-path-finder/
Calculate distance (Haversine formula) - 
1. https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
2. https://louwersj.medium.com/calculate-geographic-distances-in-python-with-the-haversine-method-ed99b41ff04b

'''

