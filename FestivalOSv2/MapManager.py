#!/usr/bin/env python3

import folium
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

    def __init__(self, center: tuple, tileTheme: str = 'CartoDB dark_matter'):
        """ Initialize a MapManger object with a center location.
            https://python-visualization.github.io/folium/latest/getting_started.html
            https://leaflet-extras.github.io/leaflet-providers/preview/

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
            attributionControl= False
        )

    def clear_map(self):
            self.map.clear_layers()

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

    def remove_path(self, name: str):
        """
        Remove a path (polyline) from the map by its name.

        Args:
            name (str): The name of the polyline to remove
        """
        print(f"Removing path: {name}")
        def remove_path(self, name: str):
            """
            Remove a path (polyline) from the map by its name.

            Args:
                name (str): The name of the polyline to remove
            """
            # Find and remove the polyline with the given name
            layers_to_remove = []

            for layer in self.map._children.values():
                if hasattr(layer, 'name') and layer.name == name:
                    layers_to_remove.append(layer.get_name())

            for layer_name in layers_to_remove:
                self.map._children.pop(layer_name)



    def add_image(self, imgURI: str, cornerNW: list, cornerSE: list ):
        # https://gis.stackexchange.com/questions/458932/leaflet-image-overlay-align-with-pixel-coordinates-on-map
        # https://python-visualization.github.io/folium/latest/user_guide/raster_layers/image_overlay.html
        # Read image file and encode as base64
        with open(imgURI, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")

        # Get the file extension to determine mime type
        file_ext = os.path.splitext(imgURI)[1].lower()
        mime_type = "image/png" if file_ext == ".png" else "image/jpeg" if file_ext in [".jpg", ".jpeg"] else "image/gif"

        # Create data URL
        dataURI = f"data:{mime_type};base64,{encoded_string}"


        img = folium.raster_layers.ImageOverlay(
            name="QR Code",
            image=dataURI,
            bounds=[cornerNW, cornerSE],
            opacity=0.6,
            interactive=False,
            cross_origin=False,
            zindex=1,
        )
        img.add_to(self.map)
        folium.LayerControl().add_to(self.map)

    def save_map_to_html(self, map):
        # Save the map to an HTML file
        htmlFile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
        self.map.save(htmlFile)

        return htmlFile
