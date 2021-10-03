import requests
import PySimpleGUI as sg
import json


layout = [
        [ sg.Text("Dashboard") ],
        [ sg.Text("Data: ", size=(53, 5), key="-DATA-") ],
        [ sg.Button("Create Room") ]
    ]

# Create the window
window = sg.Window("Aice Chat", layout, size=(500, 300))

# Create an event loop
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break;

    if event == "Create Room":
        r = requests.get('http://localhost:3000/room/create')
        msg = r.json()['msg']
        window['-DATA-'].update("DATA: " + json.dumps(r.json()))
        sg.popup(msg)

window.close()