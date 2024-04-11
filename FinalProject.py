import folium
import subprocess
from IPython.core.display import display, HTML
import openrouteservice as ors
import math
import webbrowser

coords = [
    [40.11733,-75.11176],
    [40.11894,-75.11933],
    [40.12466,-75.11631]

]

line_points = [
    [40.11733,-75.11176],
    [40.11894,-75.11933],
    [40.12466,-75.11631]
              ]


start = [40.11733,-75.11176]

# visualize the points on a map
m = folium.Map(location=list(start), tiles="cartodbpositron", zoom_start=12)
for coord in coords:
    folium.Marker(location=list(coord)).add_to(m)
folium.Marker(location=list(start), icon=folium.Icon(color="red")).add_to(m)

lines_group = folium.FeatureGroup(name="Lines").add_to(m)
lines_group.add_child(folium.PolyLine(locations=line_points, weight=3,color = 'blue'))

m
m.save('aee.html')


def auto_open(url):
    webbrowser.open(url, new=2)


auto_open('aee.html')

