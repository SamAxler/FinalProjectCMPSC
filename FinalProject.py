
import folium
import openrouteservice as ors
import math

coords = [
    [-75.11176, 40.11733],
    [-75.11933,40.11894]

]
start = [-75.11176, 40.11733]

# visualize the points on a map
m = folium.Map(location=list(reversed([-75.11176, 40.11733])), tiles="cartodbpositron", zoom_start=12)
for coord in coords:
    folium.Marker(location=list(reversed(coord))).add_to(m)
folium.Marker(location=list(reversed(start)), icon=folium.Icon(color="red")).add_to(m)
m