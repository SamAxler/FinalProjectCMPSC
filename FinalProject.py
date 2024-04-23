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

from DirectedGraph import *

#if terminal command doesn't run use python instead of py

# py -m pip install folium
# py -m pip install openrouteservice
# py -m pip install IPython

client = ors.Client(key='5b3ce3597851110001cf62483d1d56a31e134c83851721865a6ac5c4')

linepoints2 = [
    [-75.11176,40.11733],
    [-75.11933,40.11894],
    [-75.11631,40.12466],
    [-74.8794,40.2248]
]

start = [40.11733,-75.11176]

# visualize the points on a map
m = folium.Map(location=list(start), tiles="cartodbpositron", zoom_start=12)
for coord in linepoints2:
    folium.Marker(location=list(reversed(coord))).add_to(m)
folium.Marker(location=list(start), icon=folium.Icon(color="red")).add_to(m)

lines_group = folium.FeatureGroup(name="Lines").add_to(m)

route = client.directions(coordinates=linepoints2,profile='driving-car',format='geojson')
folium.PolyLine(locations=[list(reversed(coord)) for coord in route['features'][0]['geometry']['coordinates']],color = "blue").add_to(m)
m.save('aee.html')
def auto_open(url):
    webbrowser.open(url, new=2)

auto_open('aee.html')

def main():

    # Prepare paths
    root_folder = pathlib.Path(__file__).parent
    data_folder = root_folder / 'data'
    temp_folder = data_folder / 'temp'
    local_osm_file = data_folder / 'saved_local_osm_data.map'
    output_shp_folder = data_folder / 'output_shp'

    # Download OSM file
    osm_map_file_content = osmp.download_osm(left=-73.4244, bottom=45.4302, right=-73.4010, top=45.4466, cache=True, cacheTempDir=temp_folder.as_posix())

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