import requests
import PySimpleGUI as sg


layout = [
        [ sg.Text("Dashboard") ],
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
        sg.popup(msg)

window.close()