import pathlib
import xml.etree.ElementTree as ET
import osm as osmp
from collections import defaultdict
import sys
import matplotlib.pyplot as plt
from math import radians, sin, cos, sqrt, atan2
import networkx as nx


######
root_folder = pathlib.Path(__file__).parent / '..'
root_folder = root_folder.resolve()
sys.path.append(root_folder.as_posix())
#
data_folder = root_folder / 'data'
temp_folder = data_folder / 'temp'
local_osm_file = data_folder / 'saved_local_osm_data.map'
output_shp_folder = data_folder / 'output_shp'
######


class Digraph:
    def __init__(self):
        self.graph = defaultdict(dict)

    def add_edge(self, source, destination, weight=None):
        self.graph[source][destination] = weight

    def edges(self):
        return [(source, destination) for source in self.graph for destination in self.graph[source]]

    def __str__(self):
        result = ""
        for node in self.graph:
            for neighbor in self.graph[node]:
                result += f"{node} -> {neighbor}\n"
        return result

def parse_osm(osm_file_content):
    nodes = {}
    ways = []
    oneway_ways = set()  # Set to store IDs of one-way streets

    root = ET.fromstring(osm_file_content)

    for node in root.findall('.//node'):
        node_id = node.attrib['id']
        lat = float(node.attrib['lat'])
        lon = float(node.attrib['lon'])
        nodes[node_id] = (lat, lon)

    for way in root.findall('.//way'):
        way_nodes = []
        oneway = False
        for tag in way.findall('tag'):
            if tag.attrib['k'] == 'oneway' and tag.attrib['v'] == 'yes':
                oneway = True
                break
        for nd in way.findall('nd'):
            way_nodes.append(nd.attrib['ref'])
        ways.append(way_nodes)
        if oneway:
            oneway_ways.add(way_nodes[0])

    return nodes, ways, oneway_ways

def construct_graph(nodes, ways, oneway_ways):
    graph = Digraph()
    for way in ways:
        if oneway_ways and way[0] not in oneway_ways:
            way.reverse()  # Reverse the way for bidirectional streets
        for i in range(len(way) - 1):
            source = way[i]
            destination = way[i + 1]
            distance = haversine_distance(nodes[source][1], nodes[source][0], nodes[destination][1], nodes[destination][0])
            if not oneway_ways or way[0] not in oneway_ways:
                # Add edge in both directions for bidirectional streets or when oneway_ways is not specified
                graph.add_edge(source, destination, weight=distance)
                graph.add_edge(destination, source, weight=distance)
            else:
                # Add edge in the specified direction for one-way streets
                graph.add_edge(source, destination, weight=distance)
    return graph

def print_edges_with_weights(graph):
        for source in graph.graph:
            for destination, weight in graph.graph[source].items():
                print(f"Edge: {source} -> {destination}, Weight: {weight}")

def haversine_distance(lon1, lat1, lon2, lat2):
    # Convert latitude and longitude from degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = 6371000 * c  
    return distance





