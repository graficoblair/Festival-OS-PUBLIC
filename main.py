#!/usr/bin/env python3.13
# https://github.com/zauberzeug/nicegui/discussions/4068
# https://github.com/WolfgangFahl/nicegui_widgets/blob/f3a31a35d9c6322e4314480489c7242647c5d6d4/ngwidgets/widgets_demo.py#L757
# https://nicegui.io/documentation/leaflet#add_markers_on_click
# https://leaflet-extras.github.io/leaflet-providers/preview/
from nicegui import ui

# Remove default padding
ui.query('body').classes('p-0 m-0')

mapOptions = {
    'zoomControl': False,
    'scrollWheelZoom': True,
    'doubleClickZoom': False,
    'boxZoom': False,
    'keyboard': False,
    'dragging': True,
    'attributionControl': False
}

# Store Points of Interest as GPS locations
pointsOfInterest = [
    {'id':0, 'name': 'Map Center', 'lat': 36.12864437979148, 'long': -115.15153977260387},
    {'id':1, 'name': 'Point A', 'lat': 36.1287, 'long': -115.15153977260387},
    {'id':2, 'name': 'Point B', 'lat': 36.1288, 'long': -115.15153977260387},
    {'id':3, 'name': 'Point C', 'lat': 36.1289, 'long': -115.15153977260387}
]

# Create full-screen container
with ui.element('div').style('position: absolute; top: 0; left: 0; right: 0; bottom: 0; width: 100%; height: 100vh; padding: 0; margin: 0;'):
    map = ui.leaflet(center=(pointsOfInterest[0]['lat'], pointsOfInterest[0]['long']), zoom=17, options=mapOptions).style('width: 100%; height: 100%;')

# Add markers for each point of interest
for point in pointsOfInterest:
    map.marker(latlng=(point['lat'], point['long'])) #.bind_popup(point['name'])

#map.clear_layers()
map.tile_layer(
    url_template='https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png',
    options={
        'maxZoom': 20,
        'zoomControl': False
    }
)

# Run the application
ui.run(native=True, title='ComplexCon Map')
