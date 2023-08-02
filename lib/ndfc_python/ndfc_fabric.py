"""
Name: ndfc_fabric.py
Description: superclass inherited by the other fabric classes in this repo
"""
import sys

from ndfc_python.ndfc import NdfcRequestError

OUR_VERSION = 103


class NdfcFabric:
    """
    superclass inherited by the other fabric classes in this repo.

    Requires one parameter; an instance of NDFC() (see ndfc.py
    in this directory)

    Example usage:

    from ndfc_python.log import Log
    from ndfc_python.ndfc import NDFC

    log = Log('example_log', 'INFO', 'DEBUG') # INFO to screen, DEBUG to file
    ndfc = NDFC()

    class MyNewNdfcFabricType(NdfcFabric):
        def __init__(self, ndfc):
            super().__init__(ndfc)
        etc...

    TODO: Need a delete() method
    """

    def __init__(self, ndfc):
        self.lib_version = OUR_VERSION
        self.class_name = __class__.__name__
        self.ndfc = ndfc
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

    def _init_nv_pairs_default(self):
        """
        Initialize a dictionary containing default values for nv pairs
        """
        self._nv_pairs_default = {}

    def _init_ndfc_params(self):
        """
        This is used to build the payload in self.create()
        and also verified in self._final_verification()
        """
        self._ndfc_params = self._ndfc_params_default
        for item in self._ndfc_params_mandatory_set:
            self._ndfc_params[item] = ""

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
            self.ndfc.verify_boolean(param)
        except TypeError as err:
            msg = f"exiting. {caller}, not expected type. {err}"
            self.ndfc.log.error(msg)
            sys.exit(1)

    def verify_rp_count(self, param, caller=""):
        """
        verify rp_count conforms to NDFC's expectations
        """
        if param in self.valid["rp_count"]:
            return
        msg = f"exiting. {caller}, expected an integer with value in: "
        msg += f"{self.valid['rp_count']}. Got {param}"
        raise ValueError(msg)

    def verify_rp_mode(self, param, caller=""):
        """
        verify rp_mode conforms to NDFC's expectations
        """
        if param in self.valid["rp_mode"]:
            return
        msg = f"exiting. {caller}, expected string with value in: "
        msg += f"{self.valid['rp_mode']}. Got {param}"
        raise ValueError(msg)

    def verify_rr_count(self, param, caller=""):
        """
        verify rr_count conforms to NDFC's expectations
        """
        if param in self.valid["rr_count"]:
            return
        msg = f"exiting. {caller}, expected an integer with value in: "
        msg += f"{self.valid['rr_count']}. Got {param}"
        raise ValueError(msg)

    def verify_stp_root_option(self, param, caller=""):
        """
        verify stp_root_option conforms to NDFC's expectations
        """
        if param in self.valid["stp_root_option"]:
            return
        msg = f"exiting. {caller}, expected string with value in: "
        msg += f"{self.valid['stp_root_option']}. Got {param}"
        raise ValueError(msg)

    def _get_fabric_info(self):
        """
        populate self.fabric_info with information about all fabrics on
        the NDFC

        populate set self.fabric_names with the names of
        all fabrics on the NDFC
        """
        url = self.ndfc.url_control_fabrics
        try:
            self.fabric_info = self.ndfc.get(url, self.ndfc.make_headers())
        except NdfcRequestError as err:
            self.ndfc.log.error(f"error: {err}")
            sys.exit(1)
        for item in self.fabric_info:
            if "fabricName" in item:
                self.fabric_names.add(item["fabricName"])

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
            msg = f"error creating fabric {self.fabric_name} "
            msg += f"error detail: {err}"
            self.ndfc.log.error(f"exiting. {msg}")
            sys.exit(1)

    def config_save(self):
        """
        Send validated POST request to the NDFC config-save endpoint.
        """
        if self.fabric_name is None:
            msg = "exiting. Set instance.fabric_name before calling "
            msg += "instance.config_save()."
            self.ndfc.log.error(msg)
            sys.exit(1)
        if self.ndfc.bearer_token is None:
            msg = "exiting. Call ndfc_instance.login() before calling "
            msg += "confg_save()"
            self.ndfc.log.error(msg)
            sys.exit(1)
        url = f"{self.ndfc.url_control_fabrics}/{self.fabric_name}/config-save"
        self.ndfc.post(url, self.ndfc.make_headers(), {})
        self.ndfc.log.info(f"{self.fabric_name}: config_save complete.")

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
