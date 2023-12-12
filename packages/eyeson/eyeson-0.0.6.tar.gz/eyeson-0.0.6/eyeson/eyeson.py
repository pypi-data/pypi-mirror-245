import requests
import sys
import json
from urllib.parse import urlparse, parse_qs

BASE_URL = 'https://api.eyeson.team'


class EyesonClient:
    """Http client for connecting to Eyeson"""

    def __init__(self, access_key=None, room_details=None, api_key=None, base_url=BASE_URL, debug=False):
        self.base_url = base_url
        self.debug = debug
        self.session = requests.session()
        self.access_key = access_key
        self.room_details = room_details
        self.api_key = api_key
        # self.users = []

    def __debug(self, string):
        if self.debug:
            if type(string) == dict:
                print(json.dumps(string))
            else:
                print(string)

    def __get(self, resource, params=None, auth=False):

        headers = None
        caller = sys._getframe(1).f_code.co_name
        url = self.base_url + resource
        self.__debug('GET: ' + url)
        if (auth):
            headers = {"Authorization": self.api_key}
        r = self.session.get(url, params=params, verify=False, headers=headers)
        status = r.status_code
        self.__debug('Return status: ' + str(status))
        value = r.json()
        self.__debug('Return body: \n')
        self.__debug(value)
        return value

    def __post(self, resource, payload=None, data=None, files=None, auth=False):
        headers = None
        caller = sys._getframe(1).f_code.co_name
        url = self.base_url + resource
        self.__debug('POST: ' + url)
        self.__debug('Request:')
        self.__debug(payload)
        if (auth):
            headers = {"Authorization": self.api_key}
        r = self.session.post(url, params=payload,
                              verify=False, files=files, headers=headers)
        status = r.status_code
        self.__debug('Return status: ' + str(status))
        value = r.text
        self.__debug('Return body: \n')
        self.__debug(value)
        return value

    def __delete(self, resource, payload=None, data=None, files=None, auth=False):
        headers = None
        caller = sys._getframe(1).f_code.co_name
        url = self.base_url + resource
        self.__debug('DELETE: ' + url)
        self.__debug('Request:')
        self.__debug(payload)
        if (auth):
            headers = {"Authorization": self.api_key}
        r = self.session.delete(url, json=payload, data=data,
                                verify=False, files=files, headers=headers)
        status = r.status_code
        self.__debug('Return status: ' + str(status))
        # value = r.json()
        # self.__debug('Return body: \n')
        # self.__debug(value)
        return None

    def __patch(self, resource, payload=None, data=None, files=None, auth=False):
        headers = None
        caller = sys._getframe(1).f_code.co_name
        if self.is_allowed(caller):
            url = self.base_url + resource
            self.__debug('PATCH: ' + url)
            self.__debug('Request:')
            self.__debug(payload)
            if (auth):
                headers = {"Authorization": self.api_key}
            r = self.session.patch(url, json=payload, data=data,
                                   verify=False, files=files, headers=headers)
            status = r.status_code
            self.__debug('Return status: ' + str(status))
            value = r.json()
            self.__debug('Return body: \n')
            self.__debug(value)
            return value
        else:
            self.__debug('Unathorized operation: ' + caller)
            return {'Error 403': 'Unauthorized for ' + caller}


    # Initialize room or connect to existing room

    @classmethod
    def get_version(cls):
        #TODO:  Not currently implemented
        print("printing help")

    @classmethod
    def get_room(cls, access_key, base_url=BASE_URL, debug=True, api_key=None):
        """
            Return an instance with the current room set to the given access key.
        """
        client = cls(access_key=access_key, base_url=base_url, debug=debug)
        room_details = client.get_room_details()
        client.room_details = room_details
        return client

    @classmethod
    def register_guest(cls, url, debug=True):
        parsed_url = urlparse(url)
        guest_token = parse_qs(parsed_url.query)['guest'][0]
        print(guest_token)
        client = cls(debug=debug)
        t1 = client.join_guest(guest_token)
        client.room_details = json.loads(client.join_guest(guest_token))
        client.access_key = client.room_details['access_key']
        return client


    @classmethod
    def create_room(cls, username, api_key, custom_params={}, base_url=BASE_URL, debug=False):
        """
            Create a new room.
        """
        headers = {"Authorization": api_key}
        params = {'user[name]': username,
                  'user[id]': username,
                  'id': 'room1',
                  'options[layout]': 'custom',
                  'options[sfu_mode]': 'disabled',
                  'options[cupythostom_fields][virtual_background]': True,
                  # 'options[widescreen]': True,
                  'options[custom_fields][virtual_background_allow_guest]': True
                  }

        params = {**params, **custom_params}


        response = requests.post(base_url + '/rooms', headers=headers, params=params)
        if (response.status_code == 201):
            print('Success:')
            json_response = json.loads(response.text)
            print('GUI: ' + json_response['links']['gui'])
            print('Guest: ' + json_response['links']['guest_join'])
            print('Access Key: ' + json_response['access_key'])

        client = cls(access_key=json_response['access_key'], room_details=json_response, api_key=api_key, base_url=base_url, debug=debug)
        return client


    def authenticate(self, api_key):
        """
            Authentication method required to set the API key for secure operations.
        """

        self.api_key = api_key


    # Authenticated methods

    def get_webhooks(self):
        """
            Get all webhooks.  Needs authentication.
        """
        return self.__get('/webhooks', auth=True)

    def create_webhook(self, url, types=None):
        """
            Create a new webhook.  Needs authentication.
        """
        params = {"url": url,
                  "types": types}

        return self.__post('/webhooks', params, auth=True)

    def get_rooms(self):
        """
            Get all active roome by the current API user.  Needs authentication.
        """
        return self.__get('/rooms', auth=True)

    def get_recordings(self):
        """
            Get all recordings captured by the current API user.  Needs authentication.
        """
        return self.__get('/rooms/' + self.access_key + '/recordings', auth=True)

    # response = requests.post(BASE_URL + '/guests/' + guest_token + '?name=' + user)


    # Room methods that only need access token


    def join_guest(self,guest_token, username='Guest'):
        return self.__post('/guests/' + guest_token + '?name=' + username)


    def get_room_details(self):
        """
        Receive details of the current room.
        """
        room_details = self.__get('/rooms/' + self.access_key)

        print('debugging room details')
        self.room_details = room_details
        return room_details

    def broadcast_message(self, content, type='chat'):
        """
        Broadcast data messages to all users of a meeting.
        """
        params = {
            'type': 'chat',
            'content': content
        }

        return self.__post('/rooms/' + self.access_key + '/messages', params)

    def change_layout(self, layout_type='auto', layout_name='six', users=[], map=None):
        """
        Set the layout of the current room.
        """
        params = {
            'layout': layout_type,
            'name': layout_name,
            'users[]': users,
            'map': json.dumps(map)
        }
        return self.__post('/rooms/' + self.access_key + "/layout", params)

    def image_overlay(self, url=None, z_index=1):
        """
            Set the foreground (z=1) or bakground (z=-1) overlay for the current meeting from a PNG url.
        """
        params = {
            'url': url,
            'z-index': z_index
        }

        return self.__post('/rooms/' + self.access_key + "/layers", params)

    def local_image_overlay(self, filename=None, z_index=1):
        """
            Set the foreground (z=1) or bakground (z=-1) overlay for the current meeting from a PNG file.
        """
        params = {
            'z-index': z_index
        }

        return self.__post('/rooms/' + self.access_key + "/layers", params, files={'file': open(filename, 'rb')})


    def bytes_image_overlay(self, bytes=None, z_index=1):
        """
            Set the foreground (z=1) or bakground (z=-1) overlay for the current meeting from a bufferedReader object..
        """
        params = {
            'z-index': z_index
        }

        return self.__post('/rooms/' + self.access_key + "/layers", params, files={'file': bytes})

    def text_overlay(self, title, content):
        """
            Creates a text box to overlay in the current meeting.
        """
        params = {
            'insert[title]': title,
            'insert[content]': content
        }

        return self.__post('/rooms/' + self.access_key + "/layers", params)

    def delete_layers(self, z):
        """
            Removes a foreground or background in the current meeting (z=1 -> foreground, z=-1 -> background)
        """
        return self.__delete('/rooms/' + self.access_key + '/layers/' + str(z))

    def playback(self, url=None, name=None, play_id=None, replacement_id=None, loop_count=0):
        """
            Adds a video (from a public URL) to show in the current meeting.
        """

        params = {
            'playback[url]': url,
            'playback[name]': name,
            'playback[play_id]': play_id,
            'playback[replacement_id]': replacement_id,
            'playback[loop_count]': loop_count
        }

        return self.__post('/rooms/' + self.access_key + "/playbacks", params)


    def create_snapshot(self):
        """
            Creates a snapshot of the current meeting. Snapshots are saved in Eyesons cloud storage and can be downloaded from there.
        """
        return self.__post('/rooms/' + self.access_key + "/snapshot")
