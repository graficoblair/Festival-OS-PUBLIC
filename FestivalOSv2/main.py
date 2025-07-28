#!/usr/bin/env python3
import types
from nicegui import ui
from POI import POI
from QRCodeGenerator import QRCodeGenerator
from AdjacencyMatrix import AdjacencyMatrix
from MapManager import MapManager


# Create HTML for a button that calls a JavaScript function
buttonHTML = """
    <button id="clear-map-btn" style="
        position: absolute;
        top: 10px;
        right: 10px;
        z-index: 999;
        background-color: white;
        border: 2px solid #ccc;
        border-radius: 5px;
        padding: 5px 10px;
        font-weight: bold;
        cursor: pointer;">
        Clear Map
    </button>

    <script>
        document.getElementById('clear-map-btn').onclick = function() {
            // This calls back to Python
            window.parent.postMessage({'type': 'clear_map'}, '*');
        }
    </script>
    """

styleHTML="""
    <style>
        body {
            margin: 0;
            padding: 0;
            overflow: hidden;
        }
        /* Hide scrollbars */
        ::-webkit-scrollbar {
            display: none;
        }
        html, body {
            scrollbar-width: none;
            -ms-overflow-style: none;
        }
    </style>
    """

if __name__ in {"__main__", "__mp_main__"}:
    complexCon = MapManager((45.5236, -122.6750))

    # Define Points of Interests (POIs) and Navigation Points (NavPoints)
    POIs = [POI("X Booth",    [45.5239, -122.6755], MapManager.GREEN, MapManager.BOOTH, "TODO"),
            POI("Y Booth",    [45.5242, -122.6759], MapManager.GREEN, MapManager.BOOTH, "TODO"),
            POI("Z Booth",    [45.5239, -122.6765], MapManager.GREEN, MapManager.BOOTH, "TODO")]

    NavPoints = [POI("Map Center",         [45.5236, -122.6750], MapManager.BLUE,  MapManager.NAV,  "https://maps.app.goo.gl/6KYesGps9J3xgzvp6"),
                 POI("TouchScreen 1",      [45.5236, -122.6755], MapManager.RED,   MapManager.INFO, "TODO"),
                 POI("Navigation Point 1", [45.5236, -122.6759], MapManager.BLACK, MapManager.NAV, "TODO")]

    adjMatrix = AdjacencyMatrix(POIs, NavPoints)

    lastIdUsed = 0
    for i, poi in enumerate(POIs):
        poi.id = i
        complexCon.add_marker(poi.name, poi.location, poi.color, poi.iconImage)
        lastIdUsed = i
        print(lastIdUsed)

    nextId = lastIdUsed + 1
    for i, navPoint in enumerate(NavPoints):
        navPoint.id = nextId + i
        print(navPoint.id)
        complexCon.add_marker(navPoint.name, navPoint.location, navPoint.color, navPoint.iconImage)

    adjMatrix.define_adjacency_matrix()


    path = adjMatrix.find_path(POIs[0].id, POIs[2].id)
    locations = []
    for point in POIs:
        for id in path:
            if point.id == id:
                locations.append(point.location)
            else:
                for point in NavPoints:
                    if point.id == id:
                        locations.append(point.location)

    complexCon.add_path(f"Directions from {POIs[0].name} to {POIs[1].name}", locations, MapManager.RED, MapManager.INFO)

    # Generate QR code
    offsetQR = [0.0, 0.0005]
    qrSize = 0.00025
    corner1 = [NavPoints[0].lat - (qrSize/2) + offsetQR[0], NavPoints[0].long - (qrSize/2) + offsetQR[1]]  #[36.127712, -115.149861]
    corner2 = [NavPoints[0].lat + (qrSize/2) + offsetQR[0], NavPoints[0].long + (qrSize/2) + offsetQR[1]]  #[36.129182, -115.154580]
    qr = QRCodeGenerator(NavPoints[0].googleMapUrl)
    imgURI = qr.generate()
    complexCon.add_image(imgURI, corner1, corner2)

    # Save the map to an HTML file and add to NiceGUI
    htmlFile = complexCon.save_map_to_html(complexCon)

    # Read the HTML content from the file
    with open(htmlFile, 'r', encoding='utf-8') as f:
        mapHTML = f.read()

    # Create a full-screen container for the HTML content
    ui.add_head_html(styleHTML)
    # Add map htmlContent
    ui.add_body_html(mapHTML)
    # Register JavaScript function to capture clicks and communicate with Python
    ui.add_body_html(buttonHTML) #ui.add_body_html('Clear Map', on_click=lambda: complexCon.clear_map())

    # Run the application in native OS window instead of browser
    ui.run(native=True, title='ComplexCon Map', fullscreen=True)
