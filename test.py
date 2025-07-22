from nicegui import ui

with ui.tabs() as tabs:
    ui.tab('h', label='Home', icon='home')
    ui.tab('a', label='About', icon='info')
with ui.tab_panels(tabs, value='h').classes('w-full'):
    with ui.tab_panel('h'):
        ui.label('Main Content')
    with ui.tab_panel('a'):
        ui.label('Infos')

ui.run(native=True)
