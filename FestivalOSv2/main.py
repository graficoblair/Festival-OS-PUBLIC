#!/usr/bin/env python3
import os
from nicegui import ui, app

from POI import POI
import HtmlTemplates
from QRCodeGenerator import QRCodeGenerator
from AdjacencyMatrix import AdjacencyMatrix
from MapManager import MapManager

# Define Points of Interests (POIs) and Navigation Points (NavPoints)
POIs = [POI("X Booth",    [36.13380377382386, -115.16006196791938], MapManager.GREEN, MapManager.BOOTH, "https://maps.app.goo.gl/2uirM7PpF6wbEQt17"),
        POI("Y Booth",    [36.13383071098152, -115.1595662756256], MapManager.GREEN, MapManager.BOOTH, "TODO"),
        POI("Z Booth",    [36.134429439262066, -115.15938110982675], MapManager.GREEN, MapManager.BOOTH, "TODO")]

NavPoints = [POI("Map Center",         [36.133829539262066, -115.15938110982675], MapManager.BLUE,  MapManager.NAV,  "https://maps.app.goo.gl/NT6877j8AMKvC6sn7"),
                POI("TouchScreen 1",      [36.13364679503148, -115.15954672395739], MapManager.RED,   MapManager.INFO, "TODO"),
                POI("Navigation Point 1", [36.1336969539697, -115.16000331291477], MapManager.BLACK, MapManager.NAV, "TODO")]

TOUCHSCREEN_RUNNING_CODE = NavPoints[1].id

complexCon = MapManager(NavPoints[0].location)

# Register an API endpoint that calls the clear_map function
@app.get('/api/clear_map')
def api_clear_map():
    complexCon.clear_map()

    return {"status": "success"}


@app.get('/api/add_qr_code')
def add_qr_code():
    qr = QRCodeGenerator(NavPoints[0].googleMapUrl)
    imgURI = qr.generate()
    complexCon.add_image(imgURI)

    # Save the updated map to HTML
    complexCon.save_map_to_html(complexCon)


@app.get('/api/navigate_to/{poi_id}')
def navigate_to(poi_id: int):
    print(f"Directions from {NavPoints[1].name} to {POIs[poi_id].name}")
    path = adjMatrix.find_path(NavPoints[1].id, POIs[poi_id].id)
    #path = adjMatrix.find_path(1, POIs[poi_id].id)

    locations = []
    for id in path:
        for point in POIs:
            if point.id == id:
                locations.append(point.location)
            else:
                for point in NavPoints:
                    if point.id == id:
                        locations.append(point.location)

    complexCon.add_path(f"Directions from {NavPoints[1].name} to {POIs[poi_id].name}", locations, MapManager.RED, MapManager.INFO)

    complexCon.save_map_to_html(complexCon)


@app.get('/index.html')
def serve_map():
    # Simply return the current map file
    htmlFile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
    with open(htmlFile, 'r', encoding='utf-8') as f:
        map_html = f.read()

    # Return the map HTML directly
    from fastapi.responses import HTMLResponse
    return HTMLResponse(content=map_html)


if __name__ in {"__main__", "__mp_main__"}:

    ui.dark_mode().enable()

    adjMatrix = AdjacencyMatrix(POIs, NavPoints)

    lastIdUsed = 0
    for i, poi in enumerate(POIs):
        poi.id = i
        complexCon.add_marker(poi.name, poi.location, poi.color, poi.iconImage)
        lastIdUsed = i


    nextId = lastIdUsed + 1
    for i, navPoint in enumerate(NavPoints):
        navPoint.id = nextId + i
        complexCon.add_marker(navPoint.name, navPoint.location, navPoint.color, navPoint.iconImage)

    adjMatrix.define_adjacency_matrix()

    # Add QR code to the map
    #qr = QRCodeGenerator(NavPoints[0].googleMapUrl)
    #imgURI = qr.generate()
    #complexCon.add_image(imgURI)

    # Save the map to an HTML file and add to NiceGUI
    htmlFile = complexCon.save_map_to_html(complexCon)

    # Read the HTML content from the file
    with open(htmlFile, 'r', encoding='utf-8') as f:
        mapHTML = f.read()

    # Wrap the map HTML in a div with that ID
    #wrapped_map_html = f"""
    #<div id="map-frame" class="map-container" style="width: 100%; height: 100%; position: absolute; top: 0; left: 0; z-index: 0;">
    #    {mapHTML}
    #</div>
    #"""

    #modified_map_html = mapHTML.replace('<div class="folium-map"', '<div id="map-frame" class="folium-map"')

    # Use an iframe to display the map - this completely isolates the map HTML
    map_frame_html = f"""
    <div style="width: 100%; height: 100%; position: absolute; top: 0; left: 0; z-index: 0;">
        <iframe id="map-frame" src="/{os.path.basename(htmlFile)}"
                style="width: 100%; height: 100%; border: none;"></iframe>
    </div>
    """

    # Add map htmlContent
    #ui.add_body_html(mapHTML)
    ui.add_body_html(map_frame_html)

    # Create a full-screen container for the HTML content
    ui.add_head_html(HtmlTemplates.styleHTML)
    ui.add_head_html(HtmlTemplates.smooth_reload_script)

    # Register JavaScript function to capture clicks and communicate with Python
    ui.add_body_html(HtmlTemplates.clearMapButtonHTML)
    ui.add_body_html(HtmlTemplates.addQRcodeImageHTML)
    ui.add_body_html(HtmlTemplates.booth0HTML)
    ui.add_body_html(HtmlTemplates.booth1HTML)
    ui.add_body_html(HtmlTemplates.booth2HTML)

    # Run the application in native OS window instead of browser
    ui.run(native=True, title='ComplexCon Map', fullscreen=False)
