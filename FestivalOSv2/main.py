#!/usr/bin/env python3

from nicegui import ui
import qrcode
import os
from POI import POI
from AdjacencyMatrix import AdjacencyMatrix
from MapManager import MapManager

class QRCodeGenerator:

    def __init__(self, data):
        self.data = data

    def generate(self):
        qr = qrcode.QRCode(
            version=2,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(self.data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save("QR_code.png")

        currentDir = os.path.dirname(os.path.abspath(__file__))
        imagePath = os.path.join(currentDir, 'QR_CODE.png')
        imgURI = 'https://maps.lib.utexas.edu/maps/historical/newark_nj_1922.jpg' #f"file://{imagePath}" # 'https://drive.google.com/file/d/1mqIKAF13UkoVmjosC6bCc_c06DR_qXSC'
        print(f"Corner 1: {corner1} & Corner 2: {corner2} using img: {imgURI}")

        return imgURI

if __name__ in {"__main__", "__mp_main__"}:
    complexCon = MapManager((45.5236, -122.6750))
    #ui.timer(complexCon.clear_map(), interval=60)

    # Define Points of Interests (POIs) and Navigation Points (NavPoints)
    POIs = [POI("X Booth",    [45.5239, -122.6755], MapManager.GREEN, MapManager.BOOTH),
            POI("Y Booth",    [45.5239, -122.6759], MapManager.GREEN, MapManager.BOOTH),
            POI("Z Booth",    [45.5239, -122.6765], MapManager.GREEN, MapManager.BOOTH)]

    NavPoints = [POI("Map Center", [45.5236, -122.6750], MapManager.BLUE, MapManager.NAV),
                 POI("TouchScreen 1", [45.5236, -122.6750], MapManager.RED, MapManager.INFO),
                 POI("Navigation Point 1", [45.5236, -122.6755], MapManager.BLACK, MapManager.NAV)]

    adjMatrix = AdjacencyMatrix(POIs, NavPoints)
    matrixIndex = [POIs[0], POIs[1], NavPoints[0], NavPoints[1], NavPoints[2]]

    # Update POI IDs and add markers and poly path to map
    lastIdUsed = 0
    for i, poi in enumerate(POIs):
        poi.id = i
        complexCon.add_marker(poi.name, poi.location, poi.color, poi.iconImage)
        lastIdUsed = i

    for i, navPoint in enumerate(NavPoints):
        navPoint.id = lastIdUsed + i
        complexCon.add_marker(navPoint.name, navPoint.location, navPoint.color, navPoint.iconImage)


    path = adjMatrix.find_path(POIs[0], POIs[1])
    complexCon.add_path(f"Directions from {path[0].name} to {path[-1].name}", path, MapManager.RED, MapManager.INFO)


    # Generate QR code on map
    data = "https://example.com"
    #TODO mapZoomLevel = complexCon.get_zoom_level()
    offsetQR = [0.0, 0.0005]
    qrSize = 0.0005
    corner1 = [NavPoints[0].lat - (qrSize/2) + offsetQR[0], NavPoints[0].long - (qrSize/2) + offsetQR[1]]  #[36.127712, -115.149861]
    corner2 = [NavPoints[0].lat + (qrSize/2) + offsetQR[0], NavPoints[0].long + (qrSize/2) + offsetQR[1]]  #[36.129182, -115.154580]
    qr = QRCodeGenerator(data)
    imgURI = qr.generate()
    complexCon.add_image(imgURI, corner1, corner2)


    # Save the map to an HTML file and add to NiceGUI
    htmlFile = complexCon.save_map_to_html(complexCon)

    # Read the HTML content from the file
    with open(htmlFile, 'r', encoding='utf-8') as f:
        htmlContent = f.read()


    # Register the Python function to be called when the map is clicked
    #ui.run_javascript(handle_map_click, 100)
    def handle_map_click(e):
        lat = e.args['lat']
        lng = e.args['lng']
        ui.notify(f"Map clicked at: {lat}, {lng}")
        # You can add more functionality here, like finding the nearest POI

    # Register JavaScript function to capture clicks and communicate with Python
    ui.add_head_html("""
    <style>
        body {
            margin: 0;
            padding: 0;
            overflow: hidden;
        }
        .leaflet-container {
            width: 100vw;
            height: 100vh;
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
    <script>
        // Function to set up map click event after the map is loaded
        function setupMapClickEvent() {
            // Wait for the map to be available in the DOM
            const checkMapInterval = setInterval(() => {
                const map = window._map || window.map;
                if (map) {
                    clearInterval(checkMapInterval);

                    // Add click event listener to the map
                    map.on('click', function(e) {
                        // Send click event data to Python
                        window.notifyPyMapClick({
                            lat: e.latlng.lat,
                            lng: e.latlng.lng
                        });
                    });
                }
            }, 100);
        }

        // Call the setup function when the document is ready
        if (document.readyState === 'complete') {
            setupMapClickEvent();
        } else {
            window.addEventListener('load', setupMapClickEvent);
        }
    </script>
    """)

    # Create a full-screen container with the HTML content
    ui.add_body_html(htmlContent)

    # Run the application in native OS window instead of browser
    ui.run(native=True, title='ComplexCon Map', fullscreen=True) #TODO Remove scroll bar window_size=(1920, 1080),
