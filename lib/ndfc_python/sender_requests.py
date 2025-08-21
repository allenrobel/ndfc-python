#
# Copyright (c) 2024 Cisco and/or its affiliates.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import, division, print_function

__metaclass__ = type
__author__ = "Allen Robel"

import copy
import inspect
import json
import logging
from collections import deque
from os import environ

try:
    import requests

    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    import urllib3

    HAS_URLLIB3 = True
except ImportError:
    HAS_URLLIB3 = False

if HAS_REQUESTS is False:
    msg_outer = "requests is not installed. "
    msg_outer += "install with e.g. pip install requests"
    raise ImportError(msg_outer)

if HAS_URLLIB3 is False:
    msg_outer = "urllib3 is not installed. "
    msg_outer += "install with e.g. pip install urllib3"
    raise ImportError(msg_outer)


class Sender:
    """
    ### Summary
    An injected dependency for ``RestSend`` which implements the
    ``sender`` interface.  Responses are retrieved using Python
    requests library.

    ### Raises
    -   ``ValueError`` if:
            -   ``path`` is not set.
            -   ``password`` is not set.
            -   ``domain`` is not set.
    -   ``TypeError`` if:
            -   ``payload`` is not a ``dict``.
            -   ``response`` is not a ``dict``.

    ### Default values
    -   ``domain``: "local"
    -   ``username``: "admin"

    ### Usage
    Credentials and NDFC server IP can be set using environment
    variables.  For example:

    ```bash
    export ND_USERNAME="my_username"
    export ND_PASSWORD="my_password"
    export ND_DOMAIN="local"
    export ND_IP4="10.1.1.1"
    export ND_IP6="2001:db8::1"
    ```

    Setting credentials through the following class properties overrides
    the environment variables:

    - domain
    - ip4
    - ip6
    - password
    - username

    ```python
    from ansible_collections.cisco.dcnm.plugins.module_utils.common.sender_requests import \
        Sender

    sender = Sender()
    # Uncomment to override environment variables
    # sender.domain = "local"
    # If both ip4 and ip6 are set, ip4 is used.
    # sender.ip4 = "10.1.1.1"
    # sender.ip6 = "2001:db8::1"
    # sender.password = "my_password"
    # sender.username = "my_username"
    sender.login()
    try:
        rest_send = RestSend()
        rest_send.sender = sender
    except (TypeError, ValueError) as error:
        handle_error(error)
    # etc...
    # See rest_send_v2.py for RestSend() usage.
    ```
    """

    def __init__(self):
        self.class_name = self.__class__.__name__
        self._implements = "sender_v1"

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.log = logging.getLogger(f"ndfc_python.{self.class_name}")

        self.TIMEOUT = 10  # seconds

        self._domain = environ.get("ND_DOMAIN", "local")
        self._headers = None
        self._history_rc = deque(maxlen=50)
        self._history_path = deque(maxlen=50)
        self._ip4 = environ.get("ND_IP4", None)
        self._ip6 = environ.get("ND_IP6", None)
        self._jwttoken = None
        self._last_rc = None
        self._logged_in = False
        self._password = environ.get("ND_PASSWORD", None)
        self._path = None
        self._payload = None
        self._rbac = None
        self._response = None
        self._timeout = self.TIMEOUT
        self._token = None
        self.last_url = None
        self.return_code = None
        self.url = None
        self._username = environ.get("ND_USERNAME", "admin")
        self._verb = None
        

    def _verify_commit_parameters(self):
        """
        ### Summary
        Verify that required parameters are set prior to calling ``commit()``

        ### Raises
        -   ``ValueError`` if ``verb`` is not set
        -   ``ValueError`` if ``path`` is not set
        """
        method_name = inspect.stack()[0][3]
        if self.ip4 is None and self.ip6 is None:
            msg = f"{self.class_name}.{method_name}: "
            msg += "ip4 or ip6 must be set before calling commit()."
            raise ValueError(msg)
        if self.path is None:
            msg = f"{self.class_name}.{method_name}: "
            msg += "path must be set before calling commit()."
            raise ValueError(msg)
        if self.verb is None:
            msg = f"{self.class_name}.{method_name}: "
            msg += "verb must be set before calling commit()."
            raise ValueError(msg)

    def commit(self):
        """
        Send the REST request to the controller

        ### Raises
            -   ``ValueError`` if:
                    -   ``path`` is not set.
                    -   ``verb`` is not set.

        ### Properties read
            -   ``verb``: HTTP verb e.g. GET, POST, PUT, DELETE
            -   ``path``: HTTP path e.g. http://controller_ip/path/to/endpoint
            -   ``payload`` Optional HTTP payload

        ## Properties written
            -   ``response``: raw response from the controller
        """
        method_name = inspect.stack()[0][3]
        caller = inspect.stack()[1][3]
        method_name = inspect.stack()[0][3]
        msg = f"{self.class_name}.{method_name}: "
        msg += f"Caller: {caller}, ENTERED"
        self.log.debug(msg)

        try:
            self._verify_commit_parameters()
        except ValueError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += "Not all mandatory parameters are set. "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error
        self.get_url()
        msg = f"{self.class_name}.{method_name}: "
        msg += f"caller: {caller}.  "
        msg += f"Calling requests with: "
        msg += f"verb {self.verb}, "
        msg += f"path {self.path}, "
        msg += f"url {self.url}, "
        try:
            if self.payload is None:
                self.log.debug(msg)
                msg = f"self.timeout: {self.timeout}"
                self.log.debug(msg)
                response = requests.request(self.verb, self.url, headers=self.get_headers(), verify=False, timeout=self.timeout)
            else:
                msg_payload = copy.copy(self.payload)
                if "userPasswd" in msg_payload:
                    msg_payload["userPasswd"] = "********"
                msg += ", payload: "
                msg += f"{json.dumps(msg_payload, indent=4, sort_keys=True)}"
                self.log.debug(msg)
                msg = f"self.timeout: {self.timeout}"
                self.log.debug(msg)
                response = requests.request(
                    self.verb,
                    self.url,
                    headers=self.get_headers(),
                    data=json.dumps(self.payload),
                    verify=False,
                    timeout=self.timeout,
                )
        except requests.exceptions.ConnectionError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg = "Error connecting to the controller. "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error
        self._payload = None
        self.gen_response(response)

    def get_headers(self):
        """Get the headers to include in the request.

        Returns:
            dict: The headers to include in the request.
        """
        headers = {}
        headers["Cookie"] = f"AuthCookie={self.token}"
        headers["AuthCookie"] = self.token
        headers["Content-Type"] = "application/json"
        headers["Authorization"] = self.token
        return copy.copy(headers)

    def get_host(self):
        """
        Returns the server IP address to use based on the values
        of ip4 and ip6.
        """
        method_name = inspect.stack()[0][3]
        if self.ip4 is not None:
            return self.ip4
        if self.ip6 is not None:
            return self.ip6
        msg = f"{self.class_name}.{method_name}: "
        msg += "ip4 or ip6 must be set before calling "
        msg += f"{self.class_name}.commit()"
        self.log.debug(msg)
        raise ValueError(msg)

    def get_url(self):
        """Get the URL to use for the request.

        Raises:
            ValueError: If the path is not set.
        """
        method_name = inspect.stack()[0][3]
        if self.path is None:
            msg = f"{self.class_name}.{method_name}: "
            msg += "call Sender.path before calling "
            msg += f"{self.class_name}.commit()"
            self.log.debug(msg)
            raise ValueError(msg)
        if self.path[0] == "/":
            self.url = f"https://{self.get_host()}{self.path}"
        else:
            self.url = f"https://{self.get_host()}/{self.path}"
        msg = f"{self.class_name}.{method_name}: "
        msg += f"Set url to {self.url}"
        self.log.debug(msg)

    def add_history_rc(self, x):
        """Add a return code to the history.

        Args:
            x (int): The return code to add.
        """
        self._history_rc.appendleft(x)

    def add_history_path(self):
        """Add a request path to the history."""
        self._history_path.appendleft(self.url)

    def update_status(self):
        """
        Update the status of the sender.
        """
        self.last_rc = self.return_code
        self.last_url = self.url
        self.add_history_rc(self.return_code)
        self.add_history_path()

    def gen_response(self, response):
        """
        Generate a response dictionary from the requests response object.
        """
        method_name = inspect.stack()[0][3]
        # set the token to the value of Set-Cookie in the
        # response headers (if present)
        token = response.headers.get("Set-Cookie", None)
        if token is not None:
            token = token.split("=")[1]
            token = token.split(";")[0]
            self.token = token
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Set new token to {self.token}"
            self.log.debug(msg)

        response_dict = {}
        self.return_code = response.status_code
        response_dict["RETURN_CODE"] = response.status_code
        try:
            response_dict["DATA"] = json.loads(response.text)
        except json.JSONDecodeError:
            data = {}
            data["INVALID_JSON"] = response.text
            response_dict["DATA"] = data
        response_dict["MESSAGE"] = response.reason
        response_dict["METHOD"] = response.request.method
        response_dict["REQUEST_PATH"] = response.url
        self.response = copy.deepcopy(response_dict)

    def login(self):
        """
        Log in to the server.
        """
        if self.logged_in is True:
            return
        _raise = False
        msg = ""
        if self.username is None:
            msg = "call Sender.username before calling Sender.login()"
            _raise = True
        if self.password is None:
            msg = "call Sender.password before calling Sender.login()"
            _raise = True
        if self.domain is None:
            msg = "call Sender.domain before calling Sender.login()"
            _raise = True
        if _raise is True:
            if msg != "":
                self.log.debug(msg)
                raise ValueError(msg)
            msg = "Unknown error.  Check if all mandatory fields are set."
            raise ValueError(msg)
        self.logged_in = "Pending"
        self.path = "/login"
        self.get_url()
        payload = {}
        payload["userName"] = self.username
        payload["userPasswd"] = self.password
        payload["domain"] = self.domain
        self.payload = copy.copy(payload)
        headers = {}
        headers["Content-Type"] = "application/json"
        self.headers = copy.copy(headers)
        self.verb = "POST"
        self.commit()
        self.update_token()
        self.logged_in = True

    def update_token(self):
        """
        Update the authentication token.
        """
        method_name = inspect.stack()[0][3]
        msg = f"{self.class_name}.{method_name}: "
        msg += "ENTERED"
        self.log.debug(msg)
        try:
            self.token = self.response["DATA"]["jwttoken"]
            self.jwttoken = self.response["DATA"]["jwttoken"]
            self.rbac = self.response["DATA"]["rbac"]
        except KeyError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += "Unable to parse token from response: "
            msg += f"{self.response}"
            self.log.debug(msg)
            raise ValueError(msg) from error

    def refresh_login(self):
        """
        Refresh the login session.
        """
        method_name = inspect.stack()[0][3]
        msg = f"{self.class_name}.{method_name}: "
        msg += "ENTERED"
        self.log.debug(msg)
        self.path = "/refresh"
        self.get_url()
        payload = {}
        payload["userName"] = self.username
        payload["userPasswd"] = self.password
        payload["domain"] = self.domain
        self.payload = payload
        headers = {}
        headers["Content-Type"] = "application/json"
        headers["Cookie"] = f"AuthCookie={self.jwttoken}"
        headers["Authorization"] = self.token
        self.headers = headers
        self.commit()
        self.update_token()

    @property
    def domain(self):
        """
        The domain to use for the request.

        Raises:
            ValueError: If the domain is not set.
        """
        if self._domain is None:
            raise ValueError("Domain is not set.")
        return self._domain

    @domain.setter
    def domain(self, value):
        self._domain = value

    @property
    def headers(self):
        """
        The headers to use for the request.

        Raises:
            ValueError: If the headers are not set.
        """
        if self._headers is None:
            raise ValueError("Headers are not set.")
        return self._headers

    @headers.setter
    def headers(self, value):
        self._headers = value

    @property
    def history_pretty_print(self):
        """
        Get a pretty-printed string of the request history.
        """
        msg = ""
        msg += "History (last 50 calls, most recent on top)\n"
        msg += f'{"RESULT_CODE":<11} {"Path":<70}\n'
        msg += f'{"-" * 11:<11} {"-" * 70:<70}\n'
        self.log.debug(msg)
        for rc, path in zip(self.history_rc, self.history_path):
            msg = f"{rc:<11} {path:<70}"
            self.log.debug(msg)

    @property
    def history_rc(self):
        """
        Get the history of return codes.
        """
        return list(self._history_rc)

    @property
    def history_path(self):
        """
        Get the history of request paths.
        """
        return list(self._history_path)

    @property
    def implements(self):
        """
        ### Summary
        The interface implemented by this class.

        ### Raises
        None
        """
        return self._implements

    @property
    def ip4(self):
        """
        The IPv4 address to use for the request.

        Raises:
            ValueError: If the IPv4 address is not set.
        """
        if self._ip4 is None:
            raise ValueError("IPv4 address is not set.")
        return self._ip4

    @ip4.setter
    def ip4(self, value):
        self._ip4 = value

    @property
    def ip6(self):
        """
        The IPv6 address to use for the request.

        Raises:
            ValueError: If the IPv6 address is not set.
        """
        if self._ip6 is None:
            raise ValueError("IPv6 address is not set.")
        return self._ip6

    @ip6.setter
    def ip6(self, value):
        self._ip6 = value

    @property
    def jwttoken(self):
        """
        The JWT token to use for the request.
        """
        return self._jwttoken

    @jwttoken.setter
    def jwttoken(self, value):
        self._jwttoken = value

    @property
    def last_rc(self):
        """
        Get the last return code.
        """
        return self._last_rc

    @last_rc.setter
    def last_rc(self, value):
        self._last_rc = value

    @property
    def logged_in(self):
        """
        Check if the user is logged in.
        """
        return self._logged_in

    @logged_in.setter
    def logged_in(self, value):
        self._logged_in = value

    @property
    def password(self):
        """
        The password to use for the request.

        Raises:
            ValueError: If the password is not set.
        """
        if self._password is None:
            raise ValueError("Password is not set.")
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    @property
    def path(self):
        """
        Endpoint path for the REST request.

        ### Raises
        None

        ### Example
        ``/appcenter/cisco/ndfc...etc...``
        """
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    @property
    def payload(self):
        """
        Return the payload to send to the controller

        ### Raises
        -   ``TypeError`` if value is not a ``dict``.
        """
        return self._payload

    @payload.setter
    def payload(self, value):
        method_name = inspect.stack()[0][3]
        if not isinstance(value, dict) and not isinstance(value, list):
            msg = f"{self.class_name}.{method_name}: "
            msg += f"{method_name} must be a list or dict. "
            msg += f"Got type {type(value).__name__}, "
            msg += f"value {value}."
            raise TypeError(msg)
        self._payload = value

    @property
    def rbac(self):
        """
        Get the RBAC (Role-Based Access Control) settings.
        """
        return self._rbac

    @rbac.setter
    def rbac(self, value):
        self._rbac = value

    @property
    def response(self):
        """
        ### Summary
        The response from the controller.

        ### Raises
        -   ``TypeError`` if value is not a ``dict``.

        -   getter: Return a copy of ``response``
        -   setter: Set ``response``
        """
        return copy.deepcopy(self._response)

    @response.setter
    def response(self, value):
        method_name = inspect.stack()[0][3]
        if not isinstance(value, dict):
            msg = f"{self.class_name}.{method_name}: "
            msg += f"{method_name} must be a dict. "
            msg += f"Got type {type(value).__name__}, "
            msg += f"value {value}."
            raise TypeError(msg)
        self._response = value

    @property
    def timeout(self):
        """
        Get the timeout value for the request.
        """
        return self._timeout

    @timeout.setter
    def timeout(self, value):
        self._timeout = value

    @property
    def username(self):
        """
        The username to use for the request.

        Raises:
            ValueError: If the username is not set.
        """
        if self._username is None:
            raise ValueError("Username is not set.")
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    @property
    def verb(self):
        """
        The HTTP verb to use for the request.

        Raises:
            ValueError: If the verb is not set.
        """
        if self._verb is None:
            raise ValueError("HTTP verb is not set.")
        return self._verb

    @verb.setter
    def verb(self, value):
        self._verb = value

    @property
    def token(self):
        """
        The JWT token to use for the request.
        """
        return self._jwttoken

    @token.setter
    def token(self, value):
        self._jwttoken = value
