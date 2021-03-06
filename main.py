import PySimpleGUI as sg
import os

from API import API
from RSA import RSAService

terminateKeyword = '--GOODBYE--'
encryptKeyword = '--ENCRYPTED--'

class Main:
    def __init__(self):
        self.API = API()
        self.hosting = False
        self.joining = False
        self.waiting = False
        self.receiveMessages = False
        self.receiveMessagesList = []
        self.username = ''
        self.roomLink = ''
        self.id = ''

        # keys
        self.layoutKeys = [
            {'name': '-COL1-', 'keys': [], 'callback': self.mainMenuCB}, # main menu
            {'name': '-COL2-', 'keys': [], 'callback': self.messagesCB}, # messages
            {'name': '-COL3-', 'keys': [], 'callback': None},  # input room id
            {'name': '-COL4-', 'keys': [], 'callback': None},  # input username
            {'name': '-COL5-', 'keys': [], 'callback': self.waitingCB},  # waiting
            {'name': '-COL6-', 'keys': [], 'callback': None}  # settings
        ]

        # main menu -COL1-
        self.layout1 = [
            [sg.Button('Create Room', key=self.registerLayoutKey('-Create Room-', '-COL4-'))],
            [sg.Button('Join Room', key=self.registerLayoutKey('-Join Room-', '-COL4-'))],
            [sg.Button('EXIT')]
        ]

        # messages -COL2-
        self.layout2 = [
            [sg.Text('Username:'), sg.InputText('', use_readonly_for_disable=True, disabled=True, size=(60, 1), key='-USERNAME-'),
             sg.Button('settings', button_color=('SkyBlue1', 'dim gray'), key=self.registerLayoutKey('-SETTINGS_BTN-', '-COL6-'))],
            [sg.Text('Room Link:'), sg.InputText('', use_readonly_for_disable=True, disabled=True, size=(60, 1), key='-ROOMLINK-')],
            [sg.Text('Room ID:'), sg.InputText('', use_readonly_for_disable=True, disabled=True, size=(60, 1), key='-ROOMID-')],
            [sg.Text('Messages:', size=(40, 1))],
            [sg.Output(size=(110, 20), font=('Helvetica 10'), key='-OUT-')],
            [sg.Multiline(size=(70, 5), enter_submits=True, key='-MSG_INPUT-', do_not_clear=True),
            sg.Button('SEND', button_color=(sg.YELLOWS[0], sg.BLUES[0]), bind_return_key=True),
            sg.Button('SEND (Encrypted)', button_color=(sg.YELLOWS[0], sg.BLUES[0]), key='-SEND_ENCRYPTED-'),
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

        # waiting -COL5-
        self.layout5 = [
            [sg.Text('Room Link:'), sg.InputText('', use_readonly_for_disable=True, disabled=True, size=(60, 1), key='-WAITINGROOMLINK-')],
            [sg.Text('Room ID:'), sg.InputText('', use_readonly_for_disable=True, disabled=True, size=(60, 1), key='-WAITINGROOMID-')],
            [sg.Text('Waiting for a user to join...')],
            [sg.Button('Cancel', key=self.registerLayoutKey('-Cancel Waiting-', '-COL1-'))]
        ]

        # settings -COL6-
        self.layout6 = [
            [sg.Text('Your private key:'), sg.Text('Other user\'s public key:', pad=(270, 0))],
            [sg.Multiline('', size=(50, 20), do_not_clear=True, key='-selfPrivateKey-'),
             sg.Multiline('', size=(50, 20), do_not_clear=True, key='-otherPublickey-')],
            [sg.Button('BACK', key=self.registerLayoutKey('-Back Settings-', '-COL2-'), button_color=(sg.YELLOWS[0], sg.GREENS[0]))],
        ]

        # main layout
        self.layout = [
            [
                sg.Column(self.layout1, key=self.layoutKeys[0]['name']),
                sg.Column(self.layout2, visible=False, key=self.layoutKeys[1]['name']),
                sg.Column(self.layout3, visible=False, key=self.layoutKeys[2]['name']),
                sg.Column(self.layout4, visible=False, key=self.layoutKeys[3]['name']),
                sg.Column(self.layout5, visible=False, key=self.layoutKeys[4]['name']),
                sg.Column(self.layout6, visible=False, key=self.layoutKeys[5]['name']),
            ]
        ]


    # callbacks
    def mainMenuCB(self):
        self.hosting = False
        self.joining = False
        self.waiting = False
        self.receiveMessages = False
        self.receiveMessagesList = []


    def messagesCB(self):
        self.receiveMessages = True
        self.window['-USERNAME-'].update(self.username)
        self.window['-ROOMLINK-'].update(self.roomLink)
        self.window['-ROOMID-'].update(self.roomId)


    def waitingCB(self):
        self.waiting = True
        # crete room
        result = self.API.roomCreate()
        self.roomLink = result['link']
        self.roomId = result['room.id']

        # join room
        self.API.roomJoin(self.roomId, self.username)

        self.window['-WAITINGROOMLINK-'].update(self.roomLink)
        self.window['-WAITINGROOMID-'].update(self.roomId)


    def checkIfRoomReady(self):
        result = self.API.roomGet(self.roomId)
        if (len(result.get('room', {}).get('users')) > 1):
            self.waiting = False
            self.switchLayout('-COL2-')


    def refreshMessages(self):
        result = self.API.messageGetAll(self.roomId)

        if (result.get('messages')):
            for message in result.get('messages'):
                messageId = message.get('id')
                if not messageId in self.receiveMessagesList:
                    self.receiveMessagesList.append(messageId)
                    username = message.get('username')
                    message: str = message.get('message')

                    # try to decrypt encrypted message
                    try:
                        if username != self.username and message.startswith(encryptKeyword):
                            selfPrivateKey = self.window['-selfPrivateKey-'].get()
                            message = RSAService.decrypt(selfPrivateKey, message.split(encryptKeyword)[1])
                    except:
                        username = 'SYSTEM:'
                        message = '--THIS MESSAGE IS ENCRYPTED AND CANNOT BE DECRYPTED USING YOUR PRIVATE KEY--'

                    # notice current user if recipient possibly left
                    if message == terminateKeyword:
                        print(f'{username} possibly left the conversation.')
                    else:
                        print(f'{username}: {message}')


    def sendMessage(self, message):
        self.API.messageSend(self.roomId, self.username, message)


    def sendEncryptedMessage(self, message):
        try:
            otherPublicKey = self.window['-otherPublickey-'].get()
            encryptedText = encryptKeyword + RSAService.encrypt(otherPublicKey, message)
            self.API.messageSend(self.roomId, self.username, encryptedText)
        except:
            sg.Popup('There was an error while try to encrypt the message using the public.')


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


    def joinRoom(self, roomId):
        result = self.API.roomJoin(roomId, self.username)
        if result.get('success') == False:
            sg.Popup(result.get('msg'))
            return

        self.roomLink = result['link']
        self.roomId = result['room.id']
        self.switchLayout('-COL2-')


    def run(self):
        self.window = sg.Window('Aice Chat', self.layout, default_button_element_size=(8,2), use_default_focus=False, finalize=True)
        self.window.Element('-OUT-')._TKOut.output.bind("<Key>", lambda e: "break") # make output read-only

        if (os.path.isfile('./private.pem')):
            self.window['-selfPrivateKey-'].update(open('./private.pem').read())

        if (os.path.isfile('./public.pem')):
            self.window['-otherPublickey-'].update(open('./public.pem').read())

        while True:
            event, values = self.window.read(timeout=1000)

            if event in (sg.WIN_CLOSED, 'EXIT'): # quit if exit button or X
                break

            if event == '-Create Room-':
                self.hosting = True

            if event == '-Join Room-':
                self.joining = True

            if event == '-Cancel Waiting-':
                self.waiting = False

            if self.waiting:
                self.checkIfRoomReady()

            if event == '-Back Messages-':
                self.sendMessage(terminateKeyword)
                self.receiveMessages = False
                self.receiveMessagesList = []

            if self.receiveMessages:
                self.refreshMessages()

            layoutName = self.searchEventLayoutName(event)
            if layoutName:
                self.switchLayout(layoutName)

            if event == '-Submit Username-':
                inputUsername = values[1]
                if inputUsername == '':
                    sg.Popup('Username cannot be empty')
                else:
                    self.username = inputUsername
                    if self.hosting:
                        self.switchLayout('-COL5-')
                    elif self.joining:
                        self.switchLayout('-COL3-')

            if event == '-Submit Room ID-':
                inputRoomId = values[0]
                if inputRoomId == '':
                    sg.Popup('Room ID cannot be empty')
                else:
                    self.joinRoom(inputRoomId)

            if event == 'SEND':
                msg = values['-MSG_INPUT-'].rstrip()
                self.window['-MSG_INPUT-'].update('')
                self.sendMessage(msg)

            if event == '-SEND_ENCRYPTED-':
                msg = values['-MSG_INPUT-'].rstrip()
                self.window['-MSG_INPUT-'].update('')
                self.sendEncryptedMessage(msg)

        self.window.close()


if __name__ == "__main__":
    main = Main()
    main.run()
