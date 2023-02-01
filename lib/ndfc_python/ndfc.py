"""
Name: ndfc.py
Description: Methods to login to an NDFC controller and perform get, post, delete operations.

Example usage:

# Login to an NDFC controller
from ndfc_python.log import Log
from ndfc_python.ndfc import NDFC

log = Log('example_log', 'INFO', 'DEBUG') # INFO to screen, DEBUG to file
ndfc = NDFC(log)
ndfc.username = "my_username"
ndfc.password = "my_password"
ndfc.ip4 = nc.ndfc_ip
ndfc.login()
"""
import json
import sys
import requests
import urllib3
from ndfc_python.common import Common

OUR_VERSION = 102


class NDFC(Common):
    """
    Methods to login to an NDFC controller and perform get, post, delete operations
    """

    def __init__(self, log):
        super().__init__(log)
        self.lib_version = OUR_VERSION

        self.requests_timeout = 20
        self.response = None
        self.auth_token = None
        self.bearer_token = None

        self.properties_set = set()
        self.properties_set.add("username")
        self.properties_set.add("password")
        self.properties_set.add("ip4")
        self.init_properties()

    def init_properties(self):
        """
        initialize all properties to None
        """
        self.properties = {}
        for param in self.properties_set:
            self.properties[param] = None

    def login(self):
        """
        login to an NDFC controllerf
        """
        for key, value in self.properties.items():
            if value is None:
                self.log.error(f"Exit. Set property {key} before calling login.")
                sys.exit(1)
        urllib3.disable_warnings()
        payload = {}
        payload["userName"] = self.username
        payload["userPasswd"] = self.password
        payload["domain"] = "DefaultAuth"
        headers = {}
        headers["Content-Type"] = "application/json"
        headers["Connection"] = "keep-alive"

        self.response = requests.post(
            self.url_login,
            headers=headers,
            data=json.dumps(payload),
            timeout=self.requests_timeout,
            verify=False,
        )
        resp = json.loads(self.response.text)
        if "jwttoken" not in resp:
            self.log.error(
                f"Exit. Response missing jwttoken. Check password or username?  Response: {resp}"
            )
            sys.exit(1)
        self.auth_token = resp["jwttoken"]
        self.bearer_token = f"Bearer {self.auth_token}"


    def make_headers(self):
        self.headers = {}
        self.headers["Authorization"] = self.bearer_token
        self.headers["Content-Type"] = "application/json"
        return self.headers


    def _log_error(self, url, request_type):
        self.log.error(f"{request_type} response from NDFC controller during {url}")
        self.log.error(f"response.status_code: {self.response.status_code}")
        try:
            self.log.error(f"response.reason: {self.response.reason}")
            self.log.error(f"response.text: {self.response.text}")
        except Exception as general_exception:
            self.log.error(
                f"Unable to log response.reason or response.text from NDFC for {url}"
            )
            self.log.error(f"Exception detail: {general_exception}")


    def get(self, url, headers={}, params={}, verify=False):
        """
        Send a GET request to an NDFC controller
        """
        request_type = 'GET'
        self.response = requests.get(
            url,
            params=params,
            timeout=self.requests_timeout,
            verify=verify,
            headers=headers,
        )
        if self.response.status_code == 200:
            self.log.info(f"{request_type} succeeded {url}")
            return
        self._log_error(url, request_type)


    def post(self, url, headers, payload):
        """
        Send a POST request to an NDFC controller
        """
        request_type = 'POST'
        self.response = requests.post(
            url,
            data=json.dumps(payload),
            timeout=self.requests_timeout,
            verify=False,
            headers=headers,
        )
        if self.response.status_code == 200:
            self.log.info(f"{request_type} succeeded {url}")
            return
        self._log_error(url, request_type)


    def put(self, url, headers, payload):
        """
        Send a PUT request to an NDFC controller
        """
        request_type = "PUT"
        self.response = requests.put(
            url,
            data=json.dumps(payload),
            timeout=self.requests_timeout,
            verify=False,
            headers=headers,
        )
        if self.response.status_code == 200:
            self.log.info(f"{request_type} succeeded {url}")
            return
        self._log_error(url, request_type)


    def delete(self, url, headers):
        """
        Send a DELETE request to an NDFC controller
        """
        request_type = 'DELETE'
        self.response = requests.delete(
            url, timeout=self.requests_timeout, verify=False, headers=headers
        )
        if self.response.status_code == 200:
            self.log.info(f"{request_type} succeeded {url}")
            return
        self._log_error(url, request_type)


    @property
    def username(self):
        """
        return the current username
        """
        return self.properties["username"]

    @username.setter
    def username(self, param):
        self.properties["username"] = param


    @property
    def password(self):
        """
        return the current password
        """
        return self.properties["password"]

    @password.setter
    def password(self, param):
        self.properties["password"] = param


    @property
    def ip4(self):
        """
        return the current NDFC controller IP
        """
        return self.properties["ip4"]

    @ip4.setter
    def ip4(self, param):
        self.properties["ip4"] = param


    @property
    def url_base(self):
        """
        Return the base URL for the NDFC controller
        """
        if self.ip4 is None:
            self.log.error(
                "Exit. Set instance.i4 before calling NDFC() url properties."
            )
        return f"https://{self.ip4}"

    @property
    def url_login(self):
        """
        Return the login URL for the NDFC controller
        """
        return f"{self.url_base}/login"


    @property
    def url_api_v1(self):
        """
        Return the V1 API URL for the NDFC controller
        """
        return f"{self.url_base}/appcenter/cisco/ndfc/api/v1"


    @property
    def url_control_fabrics(self):
        """
        Return the fabric control API URL for the NDFC controller
        """
        return f"{self.url_api_v1}/lan-fabric/rest/control/fabrics"


    @property
    def url_top_down_fabrics(self):
        """
        Return the top down fabric URL for the NDFC controller
        """
        return f"{self.url_api_v1}/lan-fabric/rest/top-down/fabrics"


    @property
    def url_control_policies_switches(self):
        """
        Return the fabric control API URL for the NDFC controller
        """
        return f"{self.url_api_v1}/lan-fabric/rest/control/policies/switches"
