"""
Name: ndfc.py
Description:

Methods to login to an NDFC controller and perform get, post,
delete operations.

Example usage:

# Login to an NDFC controller
from ndfc_python.log import Log
from ndfc_python.ndfc import NDFC

log = Log('example_log', 'INFO', 'DEBUG') # INFO to screen, DEBUG to file
ndfc = NDFC()
ndfc.username = "my_username"
ndfc.password = "my_password"
ndfc.ip4 = nc.ndfc_ip
ndfc.logger = log
ndfc.login()
"""
import json
import sys

import requests
import urllib3

OUR_VERSION = 106


class NdfcRequestError(Exception):
    """
    Use for any uncaught errors associated with NDFC REST API requests
    See, for example, NDFC().delete()
    """


class NDFC:
    """
    Methods to login to an NDFC controller and perform get, post, put,
    and delete operations.

    Usage:

    from ndfc_python.log import Log
    from ndfc_python.ndfc import NDFC

    logger = Log('example_log', 'INFO', 'DEBUG')
    ndfc = NDFC()
    ndfc.username = "my_username"
    ndfc.password = "my_password"
    ndfc.ip4 = nc.ndfc_ip
    ndfc.log = logger
    ndfc.login()
    """

    def __init__(self):
        self.lib_version = OUR_VERSION
        self.requests_timeout = 20
        self.headers = {}
        self.response = None
        self.auth_token = None
        self.bearer_token = None
        self.properties_set = set()
        self.properties_set.add("username")
        self.properties_set.add("password")
        self.properties_set.add("ip4")
        self.properties_set.add("logger")
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
        login to an NDFC controller
        """
        for key, value in self.properties.items():
            if value is None:
                msg = f"exiting. Set property {key} before calling login."
                # can't use logger here since it may not be set yet
                print(msg)
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
        response = json.loads(self.response.text)
        if "jwttoken" not in response:
            msg = "Exiting. Response missing jwttoken in response. "
            msg += "Check password or username?"
            self.logger.error(msg)
            self._log_error(self.url_login, "POST")
            sys.exit(1)
        self.auth_token = response["jwttoken"]
        self.bearer_token = f"Bearer {self.auth_token}"

    def make_headers(self):
        """
        return auth and content-type request headers expected by the NDFC
        """
        self.headers = {}
        self.headers["Authorization"] = self.bearer_token
        self.headers["Content-Type"] = "application/json"
        return self.headers

    def _log_error(self, url, request_type):
        """
        Boilerplate error log to corral this in one place.
        """
        msg = f"{request_type} response from NDFC controller during {url}"
        msg += f" response.status_code: {self.response.status_code}"
        self.logger.error(msg)
        try:
            msg = (
                f"response.reason: {self.response.reason}"
                f" response.text: {self.response.text}"
            )
            self.logger.error(msg)
        except ValueError as exception:
            msg = f"Error while logging response for {url}. "
            msg += f"Exception detail {exception}"
            self.logger.error(msg)
        except AttributeError as exception:
            msg = f"Error while logging response for {url}. "
            msg += f"Exception detail {exception}"
            self.logger.error(msg)

    def get(self, url, headers=None, params=None, verify=False):
        """
        Send a GET request to an NDFC controller and set self.response
        Return True if response.status_code == 200
        Else return False
        """
        if headers is None:
            headers = {}
        if params is None:
            params = {}
        request_type = "GET"
        try:
            self.response = requests.get(
                url,
                params=params,
                timeout=self.requests_timeout,
                verify=verify,
                headers=headers,
            )
        except requests.ConnectTimeout as exception:
            msg = f"Exiting. Timed out connecting to {url} "
            msg += f"Exception detail: {exception}"
            self.logger.error(msg)
            sys.exit(1)
        except requests.ConnectionError as exception:
            msg = f"Exiting. Unable to connect to {url} "
            msg += f"Exception detail: {exception}"
            self.logger.error(msg)
            sys.exit(1)
        if self.response.status_code != 200:
            msg = f"status {self.response.status_code} for {request_type} "
            msg += f"url {url}"
            raise NdfcRequestError(msg)
        self.logger.debug(f"{request_type} succeeded {url}")
        return self.response.json()

    def post(self, url, headers, payload=None):
        """
        Send a POST request to an NDFC controller and set self.response
        raise NdfcRequestError if status_code is anything other than 200s
        exit with error on any exceptions from requests.
        """
        if payload is None:
            payload: dict[str, str] = {}
        request_type = "POST"
        try:
            self.response = requests.post(
                url,
                data=json.dumps(payload),
                timeout=self.requests_timeout,
                verify=False,
                headers=headers,
            )
        except requests.ConnectTimeout as exception:
            msg = f"Exiting. Timed out connecting to {url} "
            msg += f"Exception detail: {exception}"
            self.logger.error(msg)
            sys.exit(1)
        except requests.ConnectionError as exception:
            msg = f"Exiting. Unable to connect to {url} "
            msg += f"Exception detail: {exception}"
            self.logger.error(msg)
            sys.exit(1)
        if self.response.status_code != 200:
            msg = f"status_code {self.response.status_code} "
            msg += f"for {request_type} url {url}"
            raise NdfcRequestError(msg)
        self.logger.debug(f"{request_type} succeeded {url}")
        return True

    def put(self, url, headers, payload=None):
        """
        Send a PUT request to an NDFC controller and set self.response
        raise NdfcRequestError if anything other than 200 response is received
        Exit on any requests connection errors
        """
        request_type = "PUT"
        try:
            self.response = requests.put(
                url,
                data=json.dumps(payload),
                timeout=self.requests_timeout,
                verify=False,
                headers=headers,
            )
        except requests.ConnectTimeout as exception:
            msg = f"Exiting. Timed out connecting to {url} "
            msg += f"Exception detail: {exception}"
            self.logger.error(msg)
            sys.exit(1)
        except requests.ConnectionError as exception:
            msg = f"Exiting. Unable to connect to {url} "
            msg += f"Exception detail: {exception}"
            self.logger.error(msg)
            sys.exit(1)
        if self.response.status_code != 200:
            msg = f"Status {self.response.status_code} during {request_type}"
            raise NdfcRequestError(msg)

    def delete(self, url, headers):
        """
        Send a DELETE request to an NDFC controller and set self.response
        raise NdfcRequestError if NDFC response code is anything other than 200
        Exit on any caught error from the requests module.
        """
        request_type = "DELETE"
        try:
            params = {}
            params["url"] = url
            params["timeout"] = self.requests_timeout
            params["verify"] = False
            params["headers"] = headers
            self.response = requests.delete(**params)
        except requests.exceptions.InvalidSchema as exception:
            msg = f"Exiting. error connecting to {url} "
            msg += f"Exception detail: {exception}"
            self.logger.error(msg)
            sys.exit(1)
        except requests.ConnectTimeout as exception:
            msg = f"Exiting. Timed out connecting to {url} "
            msg += f"Exception detail: {exception}"
            self.logger.error(msg)
            sys.exit(1)
        except requests.ConnectionError as exception:
            msg = f"Exiting. Unable to connect to {url} "
            msg = f"Exception detail: {exception}"
            self.logger.error(msg)
            sys.exit(1)
        if self.response.status_code != 200:
            self._log_error(url, request_type)
            msg = f"request response {self.response}"
            raise NdfcRequestError(msg)
        msg = f"{request_type} succeeded {url} response {self.response}"
        self.logger.debug(msg)

    @property
    def logger(self):
        """
        return the current logger instance
        """
        return self.properties["logger"]

    @logger.setter
    def logger(self, param):
        # TODO: add verification
        self.properties["logger"] = param

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
            self.logger.error(
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
