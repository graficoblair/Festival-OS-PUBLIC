# At the top of your main.py file
map_update_handlers = []

# Create a function to register handlers
def register_map_update_handler(handler):
    map_update_handlers.append(handler)

# Create a function to notify all handlers
def notify_map_update(html_content):
    for handler in map_update_handlers:
        handler(html_content)

# In your main UI setup code
def setup_ui():
    # Create a container for the map that can be updated
    map_container = ui.html().classes('w-full h-full')

    # Initial map content
    with open(htmlFile, 'r', encoding='utf-8') as f:
        map_container.content = f.read()

    # Register a handler to update the map
    def update_map(html_content):
        map_container.content = html_content

    register_map_update_handler(update_map)

# Updated API endpoint
@app.get('/api/add_qr_code')
def add_qr_code():
    qr = QRCodeGenerator(NavPoints[0].googleMapUrl)
    imgURI = qr.generate()
    complexCon.add_image(imgURI)

    htmlFile = complexCon.save_map_to_html(complexCon)

    with open(htmlFile, 'r', encoding='utf-8') as f:
        updated_map_html = f.read()

    # Notify UI to update
    notify_map_update(updated_map_html)

    return {"status": "success"}
