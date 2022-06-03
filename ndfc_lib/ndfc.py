import json
import requests
import urllib3
from ndfc_lib.common import Common
class NDFC(Common):
    def __init__(self, log):
        super().__init__(log)

        self.properties_set = set()
        self.properties_set.add('username')
        self.properties_set.add('password')
        self.properties_set.add('ip')
        self.init_properties()

    def init_properties(self):
        self.properties = dict()
        for p in self.properties_set:
            self.properties[p] = None

    def login(self):
        for p in self.properties:
            if self.properties[p] == None:
                self.log.error('Exiting. Please set property {} before calling login.'.format(p))
                exit(1)
        urllib3.disable_warnings()
        url = 'https://{}/login'.format(self.ip)
        payload = dict()
        payload['userName'] = self.username
        payload['userPasswd'] = self.password
        payload['domain'] = 'DefaultAuth'
        headers = dict()
        headers['Content-Type'] = 'application/json'
        headers['Connection'] = 'keep-alive'

        self.response = requests.post(url, headers=headers, data=json.dumps(payload), verify=False)
        op = json.loads(self.response.text)
        self.auth_token = op["jwttoken"]
        self.bearer_token = 'Bearer {}'.format(self.auth_token)

    def get(self, url, headers):
        self.response = requests.get(url,
                        verify=False,
                        headers=headers)
        if self.response.status_code == 200:
            self.log.debug('GET succeeded {}'.format(url))
            return self.response.json()
        else:
            self.log.error('exiting. GET error response from NDFC controller during {}'.format(url))
            self.log.error('response.status_code: {}'.format(self.response.status_code))
            try:
                self.log.info('response.reason: {}'.format(self.response.reason))
                self.log.info('response.text: {}'.format(self.response.text))
            except:
                self.log.error('Unable to log response.reason or response.text from NDFC controller for {}'.format(url))
            exit(1)
    def post(self, url, headers, payload):
        self.response = requests.post(url,
                        data=json.dumps(payload),
                        verify=False,
                        headers=headers)
        if self.response.status_code == 200:
            self.log.info('POST succeeded {}'.format(url))
            return
        else:
            self.log.error('exiting. POST error response from NDFC controller during {}'.format(url))
            self.log.error('response.status_code: {}'.format(self.response.status_code))
            try:
                self.log.info('response.reason: {}'.format(self.response.reason))
                self.log.info('response.text: {}'.format(self.response.text))
            except:
                self.log.error('Unable to log response.reason or response.text from NDFC controller for {}'.format(url))
            exit(1)

    def delete(self, url, headers):
        self.response = requests.delete(url,
                        verify=False,
                        headers=headers)
        if self.response.status_code == 200:
            self.log.info('DELETE succeeded {}'.format(url))
            return
        else:
            self.log.error('exiting. DELETE error response from NDFC controller during {}'.format(url))
            self.log.error('response.status_code: {}'.format(self.response.status_code))
            try:
                self.log.info('response.reason: {}'.format(self.response.reason))
                self.log.info('response.text: {}'.format(self.response.text))
            except:
                self.log.error('Unable to log response.reason or response.text from NDFC controller for {}'.format(url))
            exit(1)

    @property
    def username(self):
        return self.properties['username']
    @username.setter
    def username(self, x):
        self.properties['username'] = x

    @property
    def password(self):
        return self.properties['password']
    @password.setter
    def password(self, x):
        self.properties['password'] = x

    @property
    def ip(self):
        return self.properties['ip']
    @ip.setter
    def ip(self, x):
        self.properties['ip'] = x
