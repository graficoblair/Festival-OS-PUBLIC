#!/usr/bin/env python3

import folium
from folium.plugins import FloatImage

import os
import base64

class MapManager:

    # POI Icon Colors
    RED = 'red'
    ORANGE = 'orange'
    GREEN = 'green'
    BLUE = 'blue'
    PURPLE = 'purple'
    BLACK = 'black'
    WHITE = 'white'
    GREY = 'gray'
    BEIGE = 'beige'
    # OTHERS: 'darkgreen', 'lightred', 'cadetblue', 'lightgreen', 'pink', 'lightblue', 'darkred',  'darkblue'

    # POI Icon Shapes
    INFO = 'info-sign'
    NAV = 'navigate-circle-outline'
    BOOTH = 'square-outline'
    WARNING = 'warning-sign'
    ARROW_UP = 'arrow-up'
    ARROW_DOWN = 'arrow-down'
    ARROW_LEFT = 'arrow-left'
    ARROW_RIGHT = 'arrow-right'

    # Map Title colors https://leaflet-extras.github.io/leaflet-providers/preview/

    DARK_MODE_1 = 'CartoDB dark_matter'
    DARK_MODE_2 = 'Stadia Alidade_Smooth_Dark'
    LIGHT_MODE_1 = 'CartoDB Positron'

    def __init__(self, center: list, tileTheme: str = DARK_MODE_2, map_rotation: float = 0.0):
        """ Initialize a MapManger object with a center location.
            https://python-visualization.github.io/folium/latest/getting_started.html

            Args:
                center (tuple): The center location of the map.

            Returns:
                None
        """
        self.map = folium.Map(
            location=center,
            zoom_start=20,
            tiles=tileTheme,
            zoom_control=False,
            control_scale=True,
            attributionControl=False
        )

    # Create a function that will be called from the UI
    def handle_clear_map(self):
        self.clear_map()
        self.map.save(f"map_{id(self)}.html")

    def clear_map(self):
        """ Remove all markers, polylines, and overlays from the map
        """
        print("Map cleared!!!")

        # Store the base map tiles
        base_tiles = [child for child in self.map._children.values()
                        if isinstance(child, folium.TileLayer)]

        # Clear all children
        self.map._children = {}

        # Add back only the base tiles
        for tile in base_tiles:
            self.map.add_child(tile)


    def add_marker(self, name: str, location: list, color: str, iconImage: str):
        """ Add a marker with one of the predefined CONSTANT colors and icon image

            Args:
                name (str): The name of the marker.
                location (list): The location of the marker.
                color (str): The color of the marker.
                iconImage (str): The icon image of the marker.

            Returns:
                None
        """
        self.map.add_child(folium.Marker(
            location=location,
            popup=name,
            icon=folium.Icon(color=color, icon=iconImage)
        ))

    def add_path(self, name: str, locations: list, color: str, iconImage: str):
        """ Add a path with one of the predefined CONSTANT colors and icon image
        """
        #print(name)
        self.map.add_child(folium.PolyLine(
            name=name,
            locations=locations,
            popup=None,
            color=color,
            weight=5,
            opacity=0.7,
            icon=folium.Icon(color=color, icon=iconImage),
            tooltip=name
        ))

    def add_image(self, imgURI: str):
        # https://gis.stackexchange.com/questions/458932/leaflet-image-overlay-align-with-pixel-coordinates-on-map
        # https://python-visualization.github.io/folium/latest/user_guide/raster_layers/image_overlay.html
        # Read image file and encode as base64
        print("Adding QR code image")
        with open(imgURI, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")

        # Get the file extension to determine mime type
        file_ext = os.path.splitext(imgURI)[1].lower()
        mime_type = "image/png" if file_ext == ".png" else "image/jpeg" if file_ext in [".jpg", ".jpeg"] else "image/gif"

        # Create data URL
        dataURI = f"data:{mime_type};base64,{encoded_string}"

        FloatImage(dataURI, bottom=5, left=75).add_to(self.map)

    def save_map_to_html(self, map):
        # Save the map to an HTML file
        htmlFile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
        self.map.save(htmlFile)

        return htmlFile
