#!/usr/bin/env python3.13
# https://github.com/zauberzeug/nicegui/discussions/4068
# https://github.com/WolfgangFahl/nicegui_widgets/blob/f3a31a35d9c6322e4314480489c7242647c5d6d4/ngwidgets/widgets_demo.py#L757

# https://leaflet-extras.github.io/leaflet-providers/preview/
from nicegui import ui

# Remove default padding
ui.query('body').classes('p-0 m-0')

mapOptions = {
    'zoomControl': False,
    'scrollWheelZoom': False,
    'doubleClickZoom': False,
    'boxZoom': False,
    'keyboard': False,
    'dragging': True,
    'attributionControl': False
}

# Create full-screen container
with ui.element('div').style('position: absolute; top: 0; left: 0; right: 0; bottom: 0; width: 100%; height: 100vh; padding: 0; margin: 0;'):
    map2 = ui.leaflet(center=(36.12864437979148, -115.15153977260387), zoom=17, options=mapOptions).style('width: 100%; height: 100%;')
map2.clear_layers()
map2.tile_layer(
    url_template='https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png',
    options={
        'maxZoom': 20,
        'zoomControl': False
    }
)

ui.run(native=True)
