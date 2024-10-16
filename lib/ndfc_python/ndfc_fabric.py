"""
Name: ndfc_fabric.py
Description: superclass inherited by the other fabric classes in this repo
"""

import sys

from ndfc_python.log import log
from ndfc_python.ndfc import NdfcRequestError
from ndfc_python.validations import Validations

OUR_VERSION = 105


class NdfcFabric:
    """
    superclass inherited by the other fabric classes in this repo.

    Example usage:

    from ndfc_python.log import log
    from ndfc_python.ndfc import NDFC
    from ndfc_python.ndfc_credentials import NdfcCredentials
    from ndfc_python.ndfc_fabric import NdfcFabric

    # INFO to screen, DEBUG to file
    logger = log('example_log', 'INFO', 'DEBUG')
    nc = NdfcCredentials()
    ndfc = NDFC()
    ndfc.log = logger
    ndfc.domain = nc.nd_domain
    ndfc.username = nc.username
    ndfc.password = nc.password
    ndfc.login()

    class MyNewNdfcFabricType(NdfcFabric):
        def __init__(self):
            super().__init__()
        etc...

    fabric = MyNewNdfcFabricType()
    fabric.logger = logger
    fabric.ndfc = ndfc
    etc...

    TODO: Need a delete() method
    """

    def __init__(self):
        self.lib_version = OUR_VERSION
        self.class_name = __class__.__name__

        self.validations = Validations()

        # properties not passed to NDFC
        # order is important for these three
        self._internal_properties = {}
        self._init_default_logger()
        self._init_internal_properties()

        # See self._get_fabric_info()
        self.fabric_info = {}
        # See self._get_fabric_info()
        self.fabric_names = set()
        # These initialize the property names and values
        # Note, these are NOT NDFC parameter names. See
        # _init_ndfc_params_* for those
        self._init_properties_default()
        self._init_properties_set()
        self._init_properties_mandatory_set()

        self._init_ndfc_params_default()
        self._init_ndfc_params_set()
        self._init_ndfc_params_mandatory_set()
        # order is important.  This needs to go last
        self._init_ndfc_params()

        self._init_nv_pairs_default()
        self._init_nv_pairs_set()
        self._init_nv_pairs_mandatory_set()

        self._init_properties()
        self._init_nv_pairs()

        # dictionary, keyed on property name, containing
        # valid values for properties whose values are a
        # list of specific choices.
        self.valid = {}
        self.valid["dhcp_ipv6_enable"] = {"DHCPv4"}
        self.valid["fabric_interface_type"] = {"p2p", "unnumbered"}
        self.valid["link_state_routing"] = {"is-is", "ospf"}
        self.valid["macsec_algorithm"] = {"AES_128_CMAC", "AES_256_CMAC"}
        self.valid["macsec_cipher_suite"] = {
            "GCM-AES-XPN-256",
            "GCM-AES-128",
            "GCM-AES-256",
            "GCM-AES-XPN-128",
        }
        self.valid["rp_count"] = {2, 4}
        self.valid["rr_count"] = {2, 4}
        self.valid["rp_mode"] = {"asm", "bidir"}
        self.valid["stp_root_option"] = {"mst", "rpvst+", "unmanaged"}

    def _init_default_logger(self):
        """
        This logger will be active if the user hasn't set self.logger
        """
        self.logger = log("ndfc_fabric_log")

    def _init_internal_properties(self):
        self._internal_properties["logger"] = self.logger
        self._internal_properties["ndfc"] = None

    def _init_properties_default(self):
        """
        Initialize default properties
        """
        self._properties_default = {}

    def _init_properties_set(self):
        """
        Initialize a set containing all properties
        """
        self._properties_set = set()
        self._properties_set.add("fabricName")
        self._properties_set.add("templateName")

    def _init_properties_mandatory_set(self):
        """
        Initialize a set containing mandatory properties
        """
        self._properties_mandatory_set = set()
        self._properties_mandatory_set.add("fabricName")

    def _init_properties(self):
        """
        Initialize all properties
        """
        self._properties = {}
        for param in self._properties_set:
            if param in self._properties_default:
                self._properties[param] = self._properties_default[param]
            else:
                self._properties[param] = ""

    def _init_ndfc_params_default(self):
        """
        Initialize default properties
        """
        self._ndfc_params_default = {}

    def _init_ndfc_params_set(self):
        """
        Initialize a set containing all properties
        """
        self._ndfc_params_set = set()
        self._ndfc_params_set.add("fabricName")
        self._ndfc_params_set.add("templateName")

    def _init_ndfc_params_mandatory_set(self):
        """
        Initialize a set containing mandatory properties
        """
        self._ndfc_params_mandatory_set = set()
        self._ndfc_params_mandatory_set.add("fabricName")

    def _init_ndfc_params(self):
        """
        This is used to build the payload in self.create()
        and also verified in self._final_verification()
        """
        self._ndfc_params = self._ndfc_params_default
        for item in self._ndfc_params_mandatory_set:
            self._ndfc_params[item] = ""

    def _init_nv_pairs_default(self):
        """
        Initialize a dictionary containing default values for nv pairs
        """
        self._nv_pairs_default = {}

    def _init_nv_pairs_set(self):
        """
        Initialize a set containing all nv pairs
        """
        self._nv_pairs_set = set()

    def _init_nv_pairs_mandatory_set(self):
        """
        Initialize a set containing mandatory nv pairs
        """
        self._nv_pairs_mandatory_set = set()

    def _init_nv_pairs(self):
        """
        Set all nv_pairs params to default initially.
        User can override these through the exposed properties.
        """
        self._nv_pairs = {}
        for param in self._nv_pairs_set:
            if param in self._nv_pairs_default:
                self._nv_pairs[param] = self._nv_pairs_default[param]
            else:
                self._nv_pairs[param] = ""

    def _preprocess_properties(self):
        """
        Align the properties to the expectations of NDFC
        Override this in subclasses
        """

    def _ndfc_verification(self):
        try:
            self.validations.verify_ndfc(self.ndfc)
        except (AttributeError, TypeError) as err:
            msg = f"exiting. {err}"
            self.logger.error(msg)
            sys.exit(1)

    def _final_verification(self):
        """
        Any final verifications go here
        Override this in subclasses
        """

    def verify_boolean(self, param, caller=""):
        """
        If param is boolean, return.
        Else, exit with error message including caller.
        """
        try:
            self.validations.verify_boolean(param)
        except TypeError as err:
            msg = f"exiting. {caller}, not expected type. {err}"
            self.logger.error(msg)
            sys.exit(1)

    def _get_fabric_info(self):
        """
        populate self.fabric_info with information about all fabrics on
        the NDFC

        populate set self.fabric_names with the names of
        all fabrics on the NDFC
        """
        self._ndfc_verification()
        url = self.ndfc.url_control_fabrics
        try:
            self.fabric_info = self.ndfc.get(url, self.ndfc.make_headers())
        except NdfcRequestError as err:
            msg = f"exiting. {err}"
            self.logger.error(msg)
            sys.exit(1)
        for item in self.fabric_info:
            if "fabricName" in item:
                self.fabric_names.add(item["fabricName"])

    def fabric_exists(self, fabric_name):
        """
        Return True if fabric_name exists on the NDFC
        Return False otherwise
        """
        self._get_fabric_info()
        if fabric_name in self.fabric_names:
            return True
        return False

    def create(self):
        """
        Create a fabric

        raise ValueError if bearer_token is not provided
        """
        self._preprocess_properties()
        self._final_verification()
        if self.ndfc.bearer_token is None:
            msg = "exiting. Please call ndfc_instance.login() "
            msg += "before calling confg_save()"
            raise ValueError(msg)

        url = f"{self.ndfc.url_control_fabrics}"

        self._properties["nvPairs"] = self._nv_pairs
        try:
            self.ndfc.post(url, self.ndfc.make_headers(), self._properties)
        except NdfcRequestError as err:
            msg = f"exiting. error creating fabric {self.fabric_name} "
            msg += f"error detail: {err}"
            self.logger.error(msg)
            sys.exit(1)

    def config_save(self):
        """
        Send validated POST request to the NDFC config-save endpoint.
        """
        self._ndfc_verification()
        if self.fabric_name is None:
            msg = "exiting. Set instance.fabric_name before calling "
            msg += "instance.config_save()."
            self.logger.error(msg)
            sys.exit(1)
        if self.ndfc.bearer_token is None:
            msg = "exiting. Call ndfc_instance.login() before calling "
            msg += "confg_save()"
            self.logger.error(msg)
            sys.exit(1)
        url = f"{self.ndfc.url_control_fabrics}/{self.fabric_name}/config-save"
        self.ndfc.post(url, self.ndfc.make_headers(), {})

    # properties that are not passed to NDFC
    @property
    def logger(self):
        """
        return/set the current logger instance
        """
        return self._internal_properties["logger"]

    @logger.setter
    def logger(self, param):
        self._internal_properties["logger"] = param

    @property
    def ndfc(self):
        """
        return/set the current ndfc instance
        """
        return self._internal_properties["ndfc"]

    @ndfc.setter
    def ndfc(self, param):
        self._internal_properties["ndfc"] = param

    # top_level properties
    @property
    def fabric_name(self):
        """
        return the current fabric_name
        """
        return self._properties["fabric_name"]

    @fabric_name.setter
    def fabric_name(self, param):
        self._properties["fabric_name"] = param
