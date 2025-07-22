#!/usr/bin/env python3.13
# https://leafmap.org/get-started/#leafmap-modules
# https://github.com/zauberzeug/nicegui/discussions/4068
# https://github.com/WolfgangFahl/nicegui_widgets/blob/f3a31a35d9c6322e4314480489c7242647c5d6d4/ngwidgets/widgets_demo.py#L757
# https://nicegui.io/documentation/leaflet#add_markers_on_click
# https://leaflet-extras.github.io/leaflet-providers/preview/
# https://developer.what3words.com/tutorial/python#usage
import os
from nicegui import ui
from pathlib import Path

class POI:

    def __init__(self, id, name, lat, long):
        self.id = id
        self.name = name
        self.lat = lat
        self.long = long
        self.content = '''  <svg viewBox="0 0 200 200" width="100" height="100" xmlns="http://www.w3.org/2000/svg">
                            <circle cx="100" cy="100" r="78" fill="#ffde34" stroke="black" stroke-width="3" />
                            <circle cx="80" cy="85" r="8" />
                            <circle cx="120" cy="85" r="8" />
                            <path d="m60,120 C75,150 125,150 140,120" style="fill:none; stroke:black; stroke-width:8; stroke-linecap:round" />
                            </svg> '''

    def find_point_of_interest(self, name: str):
        for poi in MapManager.POIs:
            if poi.name == name:
                return poi.id

        return None


class MapManager:

    POIs = [POI(0, 'Map Center', 36.1286, -115.1515),
            POI(1, 'Point A',    36.1287, -115.1516),
            POI(2, 'Point B',    36.1288, -115.1517),
            POI(3, 'Point C',    36.1289, -115.1518),
            POI(4, 'Point D', 36.1290, -115.1519)]

    mapOptions = {
        'zoomControl': False,
        'scrollWheelZoom': True,
        'doubleClickZoom': False,
        'boxZoom': False,
        'keyboard': False,
        'dragging': True,
        'attributionControl': False
    }


    def __init__(self):
        self.map = ui.leaflet(center=(MapManager.POIs[0].lat, MapManager.POIs[0].long), zoom=17, options=MapManager.mapOptions).style('width: 100%; height: 100%;')
        self.points = []

    def clear_map(self, map):
        map.clear_layers()

    def set_markers(self, map, points):

        for point in points:
            mark = map.marker(latlng=(point.lat, point.long))
            for point in points:
                js_icon = 'L.icon({iconUrl: "https://leafletjs.com/examples/custom-icons/leaf-red.png", iconSize: [38, 95], iconAnchor: [22, 94]})'
                mark.run_method(':setIcon', js_icon)

    def add_vector_layer(self, map, location: tuple, shape:str, radius: int, color: str):
        map.generic_layer(
            name=shape,
            args=[location, {'color': color, 'radius': radius}]
        )

    def add_image(self, map, imgURL: str, latBounds: list, longBounds: list ):
        # https://gis.stackexchange.com/questions/458932/leaflet-image-overlay-align-with-pixel-coordinates-on-map
        map.image_overlay(
            url=imgURL,
            bounds=[latBounds, longBounds],
            options={'opacity': 0.8}
            #name=imgURL
        )

    def add_video_overlay(self, map):
        # 'https://labs.mapbox.com/bites/00189/'
        # 'https://www.mapbox.com/bites/00188/patricia_nasa.webm'
        map.video_overlay(
            url='https://www.mapbox.com/bites/00188/patricia_nasa.webm',
            bounds=[[32, -130], [13, -100]],
            options={'opacity': 0.5, 'autoplay': True, 'playsInline': True},
        )
        
    def open_html_info(self):
        """Open the HTML information file in a new window"""
        html_path = Path(__file__).parent / 'sample.html'
        if html_path.exists():
            with open(html_path, 'r') as f:
                html_content = f.read()
            # Create a new window for the HTML content
            with ui.window(title='ComplexCon Information'):
                ui.html(html_content).style('width: 100%; height: 100%;')
        else:
            ui.notify(f'HTML file not found: {html_path}', color='negative')



if __name__ in {"__main__", "__mp_main__"}:

    # Remove default padding
    ui.query('body').classes('p-0 m-0')
    
    # Create container for controls at the bottom
    controls_container = ui.element('div').style('position: absolute; bottom: 10px; left: 10px; z-index: 1000;')
    with controls_container:
        ui.button('Show Info', on_click=lambda: complexConMap.open_html_info()).style('background-color: #ffde34; color: black;')

    # Create full-screen container
    with ui.element('div').style('position: absolute; top: 0; left: 0; right: 0; bottom: 0; width: 100%; height: 100vh; padding: 0; margin: 0;'):
        complexConMap = MapManager()
        complexConMap.set_markers(complexConMap.map, MapManager.POIs)
        
    ui.timer(1.0, lambda: complexConMap.set_markers(complexConMap.map, MapManager.POIs))

        #complexConMap.map.on('ready', lambda e: complexConMap.set_markers(complexConMap.map, MapManager.POIs))
        #complexConMap.clear_map(complexConMap.map)

        #complexConMap.add_vector_layer(complexConMap.map, complexConMap.map.center, 'circle', 50, 'green')
        #complexConMap.add_video_overlay(complexConMap.map)
        #complexConMap.clear_map(complexConMap.map)

        # POI(0, 'Map Center', 36.12864437979148, -115.15153977260387)
        corner1 = [36.127712, -115.149861] #= [(MapManager.POIs[0].lat) - 0.001, (MapManager.POIs[0].long) - 0.001]
        corner2 = [36.129182, -115.154580] # = [(MapManager.POIs[0].lat) + 0.001, (MapManager.POIs[0].long) + 0.001]

        #'https://maps.lib.utexas.edu/maps/historical/newark_nj_1922.jpg'
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, 'LasVegasMap.png')
        img = f"file://{image_path}" # 'https://drive.google.com/file/d/1mqIKAF13UkoVmjosC6bCc_c06DR_qXSC'
        print(f"Corner 1: {corner1} & Corner 2: {corner2} using img: {img}")
        #complexConMap.add_image(complexConMap.map, img, corner1, corner2)

        complexConMap.map.tile_layer(
            url_template='https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png',
            options={
                'maxZoom': 20,
                'zoomControl': False
            }
        )

    # Run the application in native OS window instead of browser
    ui.run(native=True, window_size=(1920, 1080), title='ComplexCon Map')
