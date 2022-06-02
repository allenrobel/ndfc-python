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
        payload['userName'] = self.properties['username']
        payload['userPasswd'] = self.properties['password']
        payload['domain'] = 'DefaultAuth'
        headers = dict()
        headers['Content-Type'] = 'application/json'
        headers['Connection'] = 'keep-alive'

        self.response = requests.post(url, headers=headers, data=json.dumps(payload), verify=False)
        op = json.loads(self.response.text)
        self.auth_token = op["jwttoken"]
        self.bearer_token = 'Bearer {}'.format(self.auth_token)

    def post(self, url, headers, payload):
        # headers = dict()
        # headers['Content-Type'] = 'application/json'
        # headers['Authorization'] = self.bearer_token
        # print('self.url: {}'.format(self.url))
        # print('self.headers: {}'.format(self.headers))
        # print('self.payload: {}'.format(json.dumps(self.payload)))
        self.response = requests.post(url,
                        data=json.dumps(payload),
                        verify=False,
                        headers=headers)
        if self.response.status_code == 200:
            self.log.info('POST succeeded {}'.format(url))
            return
        else:
            self.log.error('Error response from NDFC controller during {}'.format(url))
            self.log.error('self.response {}'.format(self.response.status_code))
            try:
                self.log.info(self.response.reason)
            except:
                self.log.error(self.response.reason)
                self.log.info(self.response.txt)


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
