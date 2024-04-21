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

client = ors.Client(key='5b3ce3597851110001cf62483d1d56a31e134c83851721865a6ac5c4')

def find_popup_slice(html):
    '''
    Find the starting and edning index of popup function
    '''

    pattern = "function latLngPop(e)"

    # startinf index
    starting_index = html.find(pattern)

    #
    tmp_html = html[starting_index:]

    #
    found = 0
    index = 0
    opening_found = False
    while not opening_found or found > 0:
        if tmp_html[index] == "{":
            found += 1
            opening_found = True
        elif tmp_html[index] == "}":
            found -= 1

        index += 1

    # determine the edning index of popup function
    ending_index = starting_index + index

    return starting_index, ending_index

def find_variable_name(html, name_start):
    variable_pattern = "var "
    pattern = variable_pattern + name_start

    starting_index = html.find(pattern) + len(variable_pattern)
    tmp_html = html[starting_index:]
    ending_index = tmp_html.find(" =") + starting_index

    return html[starting_index:ending_index]

def custom_code(popup_variable_name, map_variable_name, folium_port):
    return '''
            // custom code

            var markers = [];

            var layerGroup = new L.LayerGroup(),
                    featureGroup = new L.FeatureGroup().addTo(layerGroup);
            var layerControl = new L.control.layers({
            'Main': layerGroup
            //here i need to add new layer control
            }, null, { collapsed: false }).addTo(%s);

            function latLngPop(e) {
                %s
                    .setLatLng(e.latlng)
                    .setContent(`
                        lat: ${e.latlng.lat}, lng: ${e.latlng.lng}
                        <button onClick="
                            fetch('http://localhost:%s', {
                                method: 'POST',
                                mode: 'no-cors',
                                headers: {
                                    'Accept': 'application/json',
                                    'Content-Type': 'application/json'
                                },
                                body: JSON.stringify({
                                    lat: ${e.latlng.lat},
                                    long: ${e.latlng.lng}
                                })
                            });
                            markers.push([${e.latlng.lat},${e.latlng.lng}])
                            %s.removeLayer(layerGroup);
                            %s.removeLayer(layerControl);
                            layerGroup.clearLayers();
                            layerGroup = new L.LayerGroup(),
                                featureGroup = new L.FeatureGroup().addTo(layerGroup);
                            layerControl = new L.control.layers({
                                
                                'Main': layerGroup
                                //here i need to add new layer control
                                }, null, { collapsed: false }).addTo(%s);
                            for(var i = 0;i<markers.length;i++)
                            {
                                L.marker(
                                [markers[i][0], markers[i][1]],
                                {}
                            ).addTo(layerGroup);
                            }
                            %s.addLayer(layerGroup);

                            
                        "> Store Coordinate </button>
                        <button onClick="
                            fetch('http://localhost:%s', {
                                method: 'POST',
                                mode: 'no-cors',
                                headers: {
                                    'Accept': 'application/json',
                                    'Content-Type': 'application/json'
                                },
                                body: JSON.stringify({
                                    lat: ${e.latlng.lat},
                                    long: ${e.latlng.lng}
                                })
                            });
                            markers = [];
                            %s.removeLayer(layerGroup);
                            %s.removeLayer(layerControl);
                            layerGroup.clearLayers();
                            layerGroup = new L.LayerGroup(),
                                featureGroup = new L.FeatureGroup().addTo(layerGroup);
                            layerControl = new L.control.layers({
                                'Main': layerGroup
                                //here i need to add new layer control
                                }, null, { collapsed: false }).addTo(%s);
                            %s.addLayer(layerGroup);


                            
                        "> Clear Map </button>

                        <button onClick="
                            fetch('http://localhost:%s', {
                                method: 'POST',
                                mode: 'no-cors',
                                headers: {
                                    'Accept': 'application/json',
                                    'Content-Type': 'application/json'
                                },
                                body: 'q'
                            });
                        "> Quit </button>
                    `)
                    .openOn(%s);
            }
            // end custom code
    ''' % (map_variable_name,popup_variable_name, folium_port, map_variable_name, map_variable_name, map_variable_name, map_variable_name, folium_port, map_variable_name, map_variable_name, map_variable_name, map_variable_name, folium_port, map_variable_name)

def create_folium_map(map_filepath, center_coord, folium_port):
    # create folium map
    vmap = folium.Map(center_coord, zoom_start=14)

    # add popup
    folium.LatLngPopup().add_to(vmap)

    # store the map to a file
    vmap.save(map_filepath)

    # read ing the folium file
    html = None
    with open(map_filepath, 'r') as mapfile:
        html = mapfile.read()

    # find variable names
    map_variable_name = find_variable_name(html, "map_")
    popup_variable_name = find_variable_name(html, "lat_lng_popup_")

    # determine popup function indicies
    pstart, pend = find_popup_slice(html)

    #folium.Marker(location=list([-75.11176,40.11733]), icon=folium.Icon(color="red")).add_to(vmap)

    # inject code
    with open(map_filepath, 'w') as mapfile:
        mapfile.write(
            html[:pstart] + \
            custom_code(popup_variable_name, map_variable_name, folium_port) + \
            html[pend:]
        )

def open_folium_map(project_url, map_filepath):
    driver = None
    try:
        driver = webdriver.Chrome()
        driver.get(
            project_url + map_filepath
        )

    except Exception as ex:
        print(f"Driver failed to open/find url: {ex}")

    return driver

def close_folium_map(driver):
    try:
        driver.close()
    except Exception as ex:
        pass

class FoliumServer(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        data = post_data.decode("utf-8")
        print(data)
        if data.lower() == 'q':
            raise KeyboardInterrupt("Intended exception to exit webserver")
        
        coords.append(json.loads(data))

        doORSRouting(coords)

        self._set_response()

def listen_to_folium_map(port=3001):
    server_address = ('', port)
    httpd = HTTPServer(server_address, FoliumServer)
    print("Server started")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
    print("Server stopped...")


def doORSRouting(coordins):
    print("COORDS:")
    print(coordins)
    route = client.directions(coordinates=coordins,profile='driving-car',format='geojson')
    #folium.PolyLine(locations=[list(reversed(coord)) for coord in route['features'][0]['geometry']['coordinates']],color = "blue").add_to(vmap)

coords = []
if __name__ == "__main__":
    # create variables

    folium_port = 3001
    map_filepath = "folium-map.html"
    center_coord = [40.11733,-75.11176]
    project_url = "D:\!finalProjectCMPSC\FinalProject\folium-map.html"
    coordinate_filepath = "coords.json"

    # create folium map
    create_folium_map(map_filepath, center_coord, folium_port)
    
    # open the folium map (selenium)
    driver = open_folium_map(project_url, map_filepath)

    # run webserer that listens to sent coordinates
    listen_to_folium_map(port=folium_port)

    # close the folium map
    close_folium_map(driver)

    # print all collected coords
    json.dump(coords, open(coordinate_filepath, 'w'))

    