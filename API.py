import requests
import json

class API:
    def __init__(self):
        self.baseUrl = 'http://localhost:3000'


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


    def roomGet(self, id):
        r = requests.get(f'{self.baseUrl}/room/get/{id}')

        return self._getData(r, 'room')


    def roomJoin(self, id, username):
        data = {'username': username}
        r = requests.post(f'{self.baseUrl}/room/join/{id}', json=data)

        return self._getData(r, 'room')


    def messageGetAll(self, id, username):
        data = {'username': username}
        r = requests.get(f'{self.baseUrl}/message/get/{id}', json=data)

        return self._getData(r, 'messages')


    def messageSend(self, id, username):
        data = {'username': username, 'message': 'Hello from python'}
        r = requests.post(f'{self.baseUrl}/message/send/{id}', json=data)

        return self._getData(r, 'messages')


if __name__ == "__main__":
    api = API()
    # roomId = '3e650f2a-2615-4be8-b992-96273e172e32'
    # username = 'jane doe'

    # print(api.roomCreate())
    # print(api.roomGetAll())
    # print(api.roomGet(roomId))
    # print(api.roomJoin(roomId, username))
    # print(api.messageGetAll(roomId, username))
    # print(api.messageSend(roomId, username))
