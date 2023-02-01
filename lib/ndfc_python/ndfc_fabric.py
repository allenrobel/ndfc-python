"""
Name: ndfc_fabric.py
Description: superclass inherited by the other fabric classes in this repo
"""
import sys

OUR_VERSION = 100


class NdfcFabric:
    """
    superclass inherited by the other fabric classes in this repo

    Example usage:


    TODO: Need a delete() method
    """

    def __init__(self, ndfc):
        self.lib_version = OUR_VERSION
        self.class_name = __class__.__name__
        self.ndfc = ndfc

        self._init_properties_set()
        self._init_properties_mandatory_set()
        self._init_nv_pairs_default()
        self._init_nv_pairs_set()
        self._init_nv_pairs_mandatory_set()
        self._init_properties_default()
        self._init_properties()
        self._init_nv_pairs()

    def _init_properties_set(self):
        """
        Initialize a set containing all properties
        """
        self.properties_set = set()
        self.properties_set.add("fabricName")
        self.properties_set.add("templateName")

    def _init_properties_mandatory_set(self):
        """
        Initialize a set containing mandatory properties
        """
        self.properties_mandatory_set = set()
        self.properties_mandatory_set.add("fabricName")

    def _init_nv_pairs_default(self):
        """
        Initialize default values for nv pairs
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

    def _init_properties_default(self):
        """
        Initialize default properties (currently there are no default properties)
        """
        self.properties_default = {}

    def _init_properties(self):
        """
        Initialize all properties
        """
        self.properties = {}
        for param in self.properties_set:
            if param in self.properties_default:
                self.properties[param] = self.properties_default[param]
            else:
                self.properties[param] = ""

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

    def create(self):
        """
        Create a fabric
        """
        self._preprocess_properties()
        self._final_verification()
        if self.ndfc.bearer_token is None:
            self.ndfc.log.error('exiting. Please call ndfc_instance.login() before calling confg_save()')
            sys.exit(1)

        url = f"{self.ndfc.url_control_fabrics}"

        self.properties["nvPairs"] = self._nv_pairs
        self.ndfc.post(url, self.ndfc.make_headers(), self.properties)


    def config_save(self):
        if self.fabric_name is None:
            self.ndfc.log.error(f"exiting. Set instance.fabric_name before calling instance.config_save().")
            sys.exit(1)
        if self.ndfc.bearer_token is None:
            self.ndfc.log.error('exiting. Please call ndfc_instance.login() before calling confg_save()')
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
        return self.properties["fabric_name"]

    @fabric_name.setter
    def fabric_name(self, param):
        self.properties["fabric_name"] = param
