import time
import json
import folium
from selenium import webdriver
import subprocess
from IPython.display import display, HTML
import openrouteservice as ors
import math
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from dijkstra import Dijkstra

from DirectedGraph import *

#if terminal command doesn't run use python instead of py

# py -m pip install folium
# py -m pip install openrouteservice
# py -m pip install IPython
# py -m pip install selenium

'''
This file:

    1. Downloads a .osm file (creates cache)
    2. Parses the file 
    3. Creates a DiGraph
    4. plots graph on matplotlib
    5. ...

'''
linepoints2 = [
    [-75.11176,40.11733],
    [-75.11933,40.11894],
    [-75.11631,40.12466],
    [-74.8794,40.2248]
]

start = [40.11733,-75.11176]

def main():

    # Prepare paths
    root_folder = pathlib.Path(__file__).parent
    data_folder = root_folder / 'data'
    temp_folder = data_folder / 'temp'
    local_osm_file = data_folder / 'saved_local_osm_data.map'
    output_shp_folder = data_folder / 'output_shp'

    # Download OSM file (Currently a 3 block radius around Penn State Abington)
    osm_map_file_content = osmp.download_osm(left=-75.1206, bottom=40.1096, right=-75.1000, top=40.1209, cache=True, cacheTempDir=temp_folder.as_posix())

    nodes, ways, oneway_ways = parse_osm(osm_map_file_content)
    graph = construct_graph(nodes, ways, oneway_ways)

    # 2 options to print graph:
    # print_edges_with_weights(graph)
    print(graph)


    # Convert Digraph to networkx graph
    nx_graph = nx.DiGraph()
    nx_graph.add_edges_from(graph.edges())


    # Display graph on matplotlib 
    nx.draw(nx_graph, with_labels=True)
    plt.show()

if __name__ == "__main__":
    main()
