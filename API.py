import requests
import sys

class API:
    def __init__(self):
        if "--production" in sys.argv:
            self.baseUrl = 'https://aice-chat.herokuapp.com'
        else:
            self.baseUrl = 'http://localhost:4000'


    def _getData(self, req, *args):
        jsonResult = req.json()
        dictResult = {
            'success': jsonResult.get('success'),
            'msg': jsonResult.get('msg'),
        }

        for arg in args:
            if '.' in arg:
                keys = arg.split('.')
                # TODO could be improve to accept infinite . values but 2 will work for now
                dictResult[arg] = jsonResult.get(keys[0], {}).get(keys[1])
                continue

            dictResult[arg] = jsonResult.get(arg) or None

        return dictResult


    def roomCreate(self):
        r = requests.get(f'{self.baseUrl}/room/create')

        return self._getData(r, 'link', 'room.id')


    def roomGetAll(self):
        r = requests.get(f'{self.baseUrl}/room/get')

        return self._getData(r, 'rooms')


    def roomGet(self, roomId):
        r = requests.get(f'{self.baseUrl}/room/get/{roomId}')

        return self._getData(r, 'room')


    def roomJoin(self, roomId, username):
        data = {'username': username}
        r = requests.post(f'{self.baseUrl}/room/join/{roomId}', json=data)

        return self._getData(r, 'room', 'link', 'room.id')


    def messageGetAll(self, roomId):
        r = requests.get(f'{self.baseUrl}/message/get/{roomId}')

        return self._getData(r, 'messages')


    def messageSend(self, roomId, username, message):
        data = {'username': username, 'message': message}
        r = requests.post(f'{self.baseUrl}/message/send/{roomId}', json=data)

        return self._getData(r, 'messages')


if __name__ == "__main__":
    api = API()
    username = 'jane doe'
    # roomCreateRes = api.roomCreate()
    # roomId = roomCreateRes['room.id']
    roomId = 'd45dbf39-e702-4007-a035-8bab3ceb80fd'

    # print(roomCreateRes)
    print(api.roomGetAll())
    print(api.roomGet(roomId))
    print(api.roomJoin(roomId, username))
    print(api.messageGetAll(roomId))
    print(api.messageSend(roomId, username, 'Hello from python2'))
