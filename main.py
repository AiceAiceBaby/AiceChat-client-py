import requests
import PySimpleGUI as sg
import json

from API import API

class Main:
    def __init__(self):
        self.API = API()
        self.username = ''
        # keys
        self.layoutKeys = [
            {'name': '-COL1-', 'keys': [], 'callback': None}, # main menu
            {'name': '-COL2-', 'keys': [], 'callback': self.messagesCB}, # messages
            {'name': '-COL3-', 'keys': [], 'callback': None},  # input room id
            {'name': '-COL4-', 'keys': [], 'callback': None}  # input username
        ]

        # main menu -COL1-
        self.layout1 = [
            [sg.Button('Create Room', key=self.registerLayoutKey('-Create Room-', '-COL4-'))],
            [sg.Button('Join Room', key=self.registerLayoutKey('-Join Room-', '-COL3-'))],
            [sg.Button('EXIT')]
        ]

        # messages -COL2-
        self.layout2 = [
            [sg.Text('Username:'), sg.InputText('', use_readonly_for_disable=True, disabled=True, size=(60, 1), key='-USERNAME-')],
            [sg.Text('Room Link:'), sg.InputText('', use_readonly_for_disable=True, disabled=True, size=(60, 1), key='-ROOMLINK-')],
            [sg.Text('Room ID:'), sg.InputText('', use_readonly_for_disable=True, disabled=True, size=(60, 1), key='-ROOMID-')],
            [sg.Text('Messages:', size=(40, 1))],
            [sg.Output(size=(110, 20), font=('Helvetica 10'), key='-OUT-')],
            [sg.Multiline(default_text='hi', size=(70, 5), enter_submits=False, key='-QUERY-', do_not_clear=False),
            sg.Button('SEND', button_color=(sg.YELLOWS[0], sg.BLUES[0]), bind_return_key=True),
            sg.Button('BACK', key=self.registerLayoutKey('-Back Messages-', '-COL1-'), button_color=(sg.YELLOWS[0], sg.GREENS[0]))]
        ]

        # input room id -COL3-
        self.layout3 = [
            [sg.Text('Room ID:')],
            [sg.InputText()],
            [sg.Button('Submit', key='-Submit Room ID-'), sg.Button('Cancel', key=self.registerLayoutKey('-Cancel Room ID-', '-COL1-'))]
        ]

        # input username -COL4-
        self.layout4 = [
            [sg.Text('Username:')],
            [sg.InputText()],
            [sg.Button('Submit', key='-Submit Username-'), sg.Button('Cancel', key=self.registerLayoutKey('-Cancel Username-', '-COL1-'))]
        ]

        # main layout
        self.layout = [
            [
                sg.Column(self.layout1, key=self.layoutKeys[0]['name']),
                sg.Column(self.layout2, visible=False, key=self.layoutKeys[1]['name']),
                sg.Column(self.layout3, visible=False, key=self.layoutKeys[2]['name']),
                sg.Column(self.layout4, visible=False, key=self.layoutKeys[3]['name']),
            ]
        ]


    # callbacks
    def messagesCB(self):
        result = self.API.roomCreate()

        self.window['-USERNAME-'].update(self.username)
        self.window['-ROOMLINK-'].update(result['link'])
        self.window['-ROOMID-'].update(result['room.id'])


    def registerLayoutKey(self, key, layoutName):
        index = self.layoutKeys.index(list(filter(lambda l: l.get('name') == layoutName, self.layoutKeys))[0])

        if key not in self.layoutKeys[index]['keys']:
            self.layoutKeys[index]['keys'].append(key)

        return key


    def switchLayout(self, layoutName):
        for layoutKey in self.layoutKeys:
            self.window[layoutKey['name']].update(visible=False)
            if layoutKey['name'] == layoutName:
                if layoutKey['callback']:
                    layoutKey['callback']()

        self.window[layoutName].update(visible=True)


    def searchEventLayoutName(self, event):
        for layoutKey in self.layoutKeys:
            if event in layoutKey['keys']:
                return layoutKey['name']

        return None


    def run(self):
        self.window = sg.Window('Aice Chat', self.layout, default_button_element_size=(8,2), use_default_focus=False, finalize=False)
        # self.window.Element('-OUT-')._TKOut.output.bind("<Key>", lambda e: "break") # make output read-only

        while True:
            event, values = self.window.read()

            if event in (sg.WIN_CLOSED, 'EXIT'): # quit if exit button or X
                break

            layoutName = self.searchEventLayoutName(event)
            if layoutName:
                self.switchLayout(layoutName)

            if event == '-Submit Username-':
                inputUsername = values[1]
                if inputUsername == '':
                    sg.Popup('Username cannot be empty')
                else:
                    self.username = inputUsername
                    self.switchLayout('-COL2-')

            if event == '-Submit Room ID-':
                inputRoomId = values[0]
                pass

            if event == 'SEND':
                query = values['-QUERY-'].rstrip()
                # EXECUTE YOUR COMMAND HERE
                print('The command you entered was {}'.format(query), flush=True)

        self.window.close()


if __name__ == "__main__":
    main = Main()
    main.run()
