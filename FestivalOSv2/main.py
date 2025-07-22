import folium
from nicegui import ui
import os

# https://python-visualization.github.io/folium/latest/getting_started.html
class MapManger:

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

    INFO = 'info-sign'
    WARNING = 'warning-sign'

    ARROW_UP = 'arrow-up'
    ARROW_DOWN = 'arrow-down'
    ARROW_LEFT = 'arrow-left'
    ARROW_RIGHT = 'arrow-right'

    def __init__(self, center: tuple):
        # Create a folium map
        self.map = folium.Map(
            location=center,
            zoom_start=20,
            tiles='CartoDB dark_matter',
            zoom_control=False
        )

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

    def save_map_to_html(self, map):
        # Save the map to an HTML file
        htmlFile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
        self.map.save(htmlFile)

        return htmlFile

if __name__ in {"__main__", "__mp_main__"}:

    complexCon = MapManger((45.5236, -122.6750))
    complexCon.add_marker('Map Center', [45.5236, -122.6750], MapManger.GREY, MapManger.ARROW_UP)
    complexCon.add_marker('POI #1', [45.5236, -122.6755], MapManger.BEIGE, MapManger.ARROW_RIGHT)

    # Remove default padding
    ui.query('body').classes('p-0 m-0')

    # Save the map to an HTML file
    htmlFile = complexCon.save_map_to_html(complexCon)

    # Read the HTML content from the file
    with open(htmlFile, 'r', encoding='utf-8') as f:
        htmlContent = f.read()

    # Create a full-screen container with the HTML content
    ui.add_body_html(htmlContent)

    # Run the application in native OS window instead of browser
    ui.run(native=True, window_size=(1920, 1080), title='ComplexCon Map')
