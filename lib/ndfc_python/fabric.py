import copy
import inspect
import json
import logging

from plugins.module_utils.common.controller_features import ControllerFeatures
from plugins.module_utils.common.exceptions import ControllerResponseError
from plugins.module_utils.common.properties import Properties
from plugins.module_utils.common.results import Results
from plugins.module_utils.fabric.common import FabricCommon
from plugins.module_utils.fabric.create import FabricCreateBulk
from plugins.module_utils.fabric.delete import FabricDelete
from plugins.module_utils.fabric.fabric_details_v2 import FabricDetailsByName
from plugins.module_utils.fabric.fabric_summary import FabricSummary
from plugins.module_utils.fabric.fabric_types import FabricTypes
from plugins.module_utils.fabric.query import FabricQuery
from plugins.module_utils.fabric.replaced import FabricReplacedBulk
from plugins.module_utils.fabric.template_get import TemplateGet
from plugins.module_utils.fabric.update import FabricUpdateBulk
from plugins.module_utils.fabric.verify_playbook_params import VerifyPlaybookParams


def json_pretty(msg):
    """
    Return a pretty-printed JSON string for logging messages
    """
    return json.dumps(msg, indent=4, sort_keys=True)


@Properties.add_rest_send
class Common(FabricCommon):
    """
    Common methods, properties, and resources for all states.
    """

    def __init__(self, params):
        self.class_name = self.__class__.__name__
        self.log = logging.getLogger(f"dcnm.{self.class_name}")
        super().__init__()
        method_name = inspect.stack()[0][3]  # pylint: disable=unused-variable

        self.controller_features = ControllerFeatures()
        self.features = {}
        self._implemented_states = set()

        self.params = params
        # populated in self.validate_input()
        self.payloads = {}

        self.populate_check_mode()
        self.populate_state()
        self.populate_config()

        self.results = Results()
        self.results.state = self.state
        self.results.check_mode = self.check_mode
        self._rest_send = None
        self._verify_playbook_params = VerifyPlaybookParams()

        self.have = {}
        self.query = []
        self.validated = []
        self.want = []

        msg = f"ENTERED Common().{method_name}: "
        msg += f"state: {self.state}, "
        msg += f"check_mode: {self.check_mode}"
        self.log.debug(msg)

    def populate_check_mode(self):
        """
        ### Summary
        Populate ``check_mode`` with the playbook check_mode.

        ### Raises
        -   ValueError if check_mode is not provided.
        """
        method_name = inspect.stack()[0][3]
        self.check_mode = self.params.get("check_mode", None)
        if self.check_mode is None:
            msg = f"{self.class_name}.{method_name}: "
            msg += "check_mode is required."
            raise ValueError(msg)

    def populate_config(self):
        """
        ### Summary
        Populate ``config`` with the playbook config.

        ### Raises
        -   ValueError if:
                -   ``state`` is "merged" or "replaced" and ``config`` is None.
                -   ``config`` is not a list.
        """
        method_name = inspect.stack()[0][3]
        states_requiring_config = {"merged", "replaced"}
        self.config = self.params.get("config", None)
        if self.state in states_requiring_config:
            if self.config is None:
                msg = f"{self.class_name}.{method_name}: "
                msg += "params is missing config parameter."
                raise ValueError(msg)
            if not isinstance(self.config, list):
                msg = f"{self.class_name}.{method_name}: "
                msg += "expected list type for self.config. "
                msg += f"got {type(self.config).__name__}"
                raise ValueError(msg)

    def populate_state(self):
        """
        ### Summary
        Populate ``state`` with the playbook state.

        ### Raises
        -   ValueError if:
                -   ``state`` is not provided.
                -   ``state`` is not a valid state.
        """
        method_name = inspect.stack()[0][3]

        valid_states = ["deleted", "merged", "query", "replaced"]

        self.state = self.params.get("state", None)
        if self.state is None:
            msg = f"{self.class_name}.{method_name}: "
            msg += "params is missing state parameter."
            raise ValueError(msg)
        if self.state not in valid_states:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Invalid state: {self.state}. "
            msg += f"Expected one of: {','.join(valid_states)}."
            raise ValueError(msg)

    def get_have(self):
        """
        ### Summary
        Build ``self.have``, which is a dict containing the current controller
        fabrics and their details.

        ### Raises
        -   ``ValueError`` if the controller returns an error when attempting to
            retrieve the fabric details.

        ### have structure

        ``have`` is a dict, keyed on fabric_name, where each element is a dict
        with the following structure.

        ```python
        have = {
            "fabric_name": "fabric_name",
            "fabric_config": {
                "fabricName": "fabric_name",
                "fabricType": "VXLAN EVPN",
                "etc...": "etc..."
            }
        }
        ```

        """
        method_name = inspect.stack()[0][3]  # pylint: disable=unused-variable
        try:
            self.have = FabricDetailsByName()
            # pylint: disable=no-member
            self.have.rest_send = self.rest_send
            self.have.results = Results()
            self.have.refresh()
            # pylint: enable=no-member
        except ValueError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += "Controller returned error when attempting to retrieve "
            msg += "fabric details. "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error

    def get_want(self) -> None:
        """
        ### Summary
        -   Validate the playbook configs.
        -   Update self.want with the playbook configs.

        ### Raises
        -   ``ValueError`` if the playbook configs are invalid.
        """
        merged_configs = []
        for config in self.config:
            try:
                self._verify_payload(config)
            except ValueError as error:
                raise ValueError(f"{error}") from error
            merged_configs.append(copy.deepcopy(config))

        self.want = []
        for config in merged_configs:
            self.want.append(copy.deepcopy(config))

    def get_controller_features(self) -> None:
        """
        ### Summary

        -   Retrieve the state of relevant controller features
        -   Populate self.features
                -   key: FABRIC_TYPE
                -   value: True or False
                        -   True if feature is started for this fabric type
                        -   False otherwise

        ### Raises

        -   ``ValueError`` if the controller returns an error when attempting to
            retrieve the controller features.
        """
        method_name = inspect.stack()[0][3]
        self.features = {}
        # pylint: disable=no-member
        self.controller_features.rest_send = self.rest_send
        # pylint: enable=no-member
        try:
            self.controller_features.refresh()
        except ControllerResponseError as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += "Controller returned error when attempting to retrieve "
            msg += "controller features. "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error

        for fabric_type in self.fabric_types.valid_fabric_types:
            self.fabric_types.fabric_type = fabric_type
            self.controller_features.filter = self.fabric_types.feature_name
            self.features[fabric_type] = self.controller_features.started


class Deleted(Common):
    """
    ### Summary
    Handle deleted state
    """

    def __init__(self, params):
        self.class_name = self.__class__.__name__
        super().__init__(params)

        self.action = "fabric_delete"
        self.delete = FabricDelete()
        self._implemented_states.add("deleted")

        self.log = logging.getLogger(f"dcnm.{self.class_name}")

        self.fabric_details = FabricDetailsByName()
        self.fabric_summary = FabricSummary()

        msg = "ENTERED Deleted(): "
        msg += f"state: {self.results.state}, "
        msg += f"check_mode: {self.results.check_mode}"
        self.log.debug(msg)

    def commit(self) -> None:
        """
        ### Summary
        delete the fabrics in ``self.want`` that exist on the controller.

        ### Raises

        -   ``ValueError`` if the controller returns an error when attempting to
            delete the fabrics.
        """
        self.get_want()
        method_name = inspect.stack()[0][3]

        msg = f"ENTERED: {self.class_name}.{method_name}"
        self.log.debug(msg)

        # pylint: disable=no-member
        self.fabric_details.rest_send = self.rest_send
        self.fabric_details.results = Results()

        self.fabric_summary.rest_send = self.rest_send
        self.fabric_summary.results = Results()

        self.delete.rest_send = self.rest_send
        self.delete.fabric_details = self.fabric_details
        self.delete.fabric_summary = self.fabric_summary
        self.delete.results = self.results
        # pylint: enable=no-member

        fabric_names_to_delete = []
        for want in self.want:
            fabric_names_to_delete.append(want["FABRIC_NAME"])

        try:
            self.delete.fabric_names = fabric_names_to_delete
        except ValueError as error:
            raise ValueError(f"{error}") from error

        try:
            self.delete.commit()
        except ValueError as error:
            raise ValueError(f"{error}") from error


class Merged(Common):
    """
    ### Summary
    Handle merged state.

    ### Raises

    -   ``ValueError`` if:
        -   The controller features required for the fabric type are not
            running on the controller.
        -   The playbook parameters are invalid.
        -   The controller returns an error when attempting to retrieve
            the template.
        -   The controller returns an error when attempting to retrieve
            the fabric details.
        -   The controller returns an error when attempting to create
            the fabric.
        -   The controller returns an error when attempting to update
            the fabric.
    """

    def __init__(self, params):
        self.class_name = self.__class__.__name__
        super().__init__(params)
        method_name = inspect.stack()[0][3]  # pylint: disable=unused-variable

        self.action = "fabric_create"
        self.log = logging.getLogger(f"dcnm.{self.class_name}")

        self.fabric_details = FabricDetailsByName()
        self.fabric_summary = FabricSummary()
        self.fabric_create = FabricCreateBulk()
        self.fabric_types = FabricTypes()
        self.fabric_update = FabricUpdateBulk()
        self.template = TemplateGet()

        msg = f"ENTERED Merged.{method_name}: "
        msg += f"state: {self.state}, "
        msg += f"check_mode: {self.check_mode}"
        self.log.debug(msg)

        self.need_create = []
        self.need_update = []

        self._implemented_states.add("merged")

    def get_need(self):
        """
        ### Summary
        Build ``self.need`` for merged state.

        ### Raises
        -   ``ValueError`` if:
            -   The controller features required for the fabric type are not
                running on the controller.
            -   The playbook parameters are invalid.
            -   The controller returns an error when attempting to retrieve
                the template.
            -   The controller returns an error when attempting to retrieve
                the fabric details.
        """
        # pylint: disable=too-many-branches
        method_name = inspect.stack()[0][3]
        self.payloads = {}
        for want in self.want:

            fabric_name = want.get("FABRIC_NAME", None)
            fabric_type = want.get("FABRIC_TYPE", None)

            if self.features.get("fabric_type") is False:
                msg = f"{self.class_name}.{method_name}: "
                msg += f"Features required for fabric {fabric_name} "
                msg += f"of type {fabric_type} are not running on the "
                msg += "controller. Review controller settings at "
                msg += "Fabric Controller -> Admin -> System Settings -> "
                msg += "Feature Management"
                raise ValueError(msg)

            try:
                self._verify_playbook_params.config_playbook = want
            except TypeError as error:
                raise ValueError(f"{error}") from error

            try:
                self.fabric_types.fabric_type = fabric_type
            except ValueError as error:
                raise ValueError(f"{error}") from error

            try:
                template_name = self.fabric_types.template_name
            except ValueError as error:
                raise ValueError(f"{error}") from error

            self.template.rest_send = self.rest_send
            self.template.template_name = template_name

            try:
                self.template.refresh()
            except ValueError as error:
                raise ValueError(f"{error}") from error
            except ControllerResponseError as error:
                msg = f"{self.class_name}.{method_name}: "
                msg += "Controller returned error when attempting to retrieve "
                msg += f"template: {template_name}. "
                msg += f"Error detail: {error}"
                raise ValueError(msg) from error

            try:
                self._verify_playbook_params.template = self.template.template
            except TypeError as error:
                raise ValueError(f"{error}") from error

            # Append to need_create if the fabric does not exist.
            # Otherwise, append to need_update.
            if fabric_name not in self.have.all_data:
                try:
                    self._verify_playbook_params.config_controller = None
                except TypeError as error:
                    raise ValueError(f"{error}") from error

                if self.params.get("skip_validation") is False:
                    try:
                        self._verify_playbook_params.commit()
                    except ValueError as error:
                        raise ValueError(f"{error}") from error
                else:
                    msg = f"{self.class_name}.{method_name}: "
                    msg += "skip_validation: "
                    msg += f"{self.params.get('skip_validation')}, "
                    msg += "skipping parameter validation."
                    self.log.debug(msg)

                self.need_create.append(want)

            else:

                nv_pairs = self.have.all_data[fabric_name]["nvPairs"]
                try:
                    self._verify_playbook_params.config_controller = nv_pairs
                except TypeError as error:
                    raise ValueError(f"{error}") from error
                if self.params.get("skip_validation") is False:
                    try:
                        self._verify_playbook_params.commit()
                    except (ValueError, KeyError) as error:
                        raise ValueError(f"{error}") from error
                else:
                    msg = f"{self.class_name}.{method_name}: "
                    msg += "skip_validation: "
                    msg += f"{self.params.get('skip_validation')}, "
                    msg += "skipping parameter validation."
                    self.log.debug(msg)

                self.need_update.append(want)
        # pylint: enable=too-many-branches

    def commit(self):
        """
        ### Summary
        Commit the merged state request.

        ### Raises
        -   ``ValueError`` if:
            -   The controller features required for the fabric type are not
                running on the controller.
            -   The playbook parameters are invalid.
            -   The controller returns an error when attempting to retrieve
                the template.
            -   The controller returns an error when attempting to retrieve
                the fabric details.
            -   The controller returns an error when attempting to create
                the fabric.
            -   The controller returns an error when attempting to update
        """
        method_name = inspect.stack()[0][3]  # pylint: disable=unused-variable
        msg = f"{self.class_name}.{method_name}: entered"
        self.log.debug(msg)

        self.fabric_details.rest_send = self.rest_send
        self.fabric_summary.rest_send = self.rest_send

        self.fabric_details.results = Results()
        self.fabric_summary.results = Results()

        self.get_controller_features()
        self.get_want()
        self.get_have()
        self.get_need()
        self.send_need_create()
        self.send_need_update()

    def send_need_create(self) -> None:
        """
        ### Summary
        Build and send the payload to create fabrics specified in the playbook.

        ### Raises

        -   ``ValueError`` if:
            -   Any payload is invalid.
            -   The controller returns an error when attempting to create
                the fabric.
        """
        method_name = inspect.stack()[0][3]  # pylint: disable=unused-variable
        msg = f"{self.class_name}.{method_name}: entered. "
        msg += f"self.need_create: {json_pretty(self.need_create)}"
        self.log.debug(msg)

        if len(self.need_create) == 0:
            msg = f"{self.class_name}.{method_name}: "
            msg += "No fabrics to create."
            self.log.debug(msg)
            return

        self.fabric_create.fabric_details = self.fabric_details
        self.fabric_create.rest_send = self.rest_send
        self.fabric_create.results = self.results

        try:
            self.fabric_create.payloads = self.need_create
        except ValueError as error:
            raise ValueError(f"{error}") from error

        try:
            self.fabric_create.commit()
        except ValueError as error:
            raise ValueError(f"{error}") from error

    def send_need_update(self) -> None:
        """
        ### Summary
        Build and send the payload to create fabrics specified in the playbook.

        ### Raises

        -   ``ValueError`` if:
            -   Any payload is invalid.
            -   The controller returns an error when attempting to update
                the fabric.
        """
        method_name = inspect.stack()[0][3]  # pylint: disable=unused-variable
        msg = f"{self.class_name}.{method_name}: entered. "
        msg += "self.need_update: "
        msg += f"{json_pretty(self.need_update)}"
        self.log.debug(msg)

        if len(self.need_update) == 0:
            msg = f"{self.class_name}.{method_name}: "
            msg += "No fabrics to update for merged state."
            self.log.debug(msg)
            return

        self.fabric_update.fabric_details = self.fabric_details
        self.fabric_update.fabric_summary = self.fabric_summary
        self.fabric_update.rest_send = self.rest_send
        self.fabric_update.results = self.results

        try:
            self.fabric_update.payloads = self.need_update
        except ValueError as error:
            raise ValueError(f"{error}") from error

        try:
            self.fabric_update.commit()
        except ValueError as error:
            raise ValueError(f"{error}") from error


class Query(Common):
    """
    ### Summary
    Handle query state.

    ### Raises

    -   ``ValueError`` if:
        -   The playbook parameters are invalid.
        -   The controller returns an error when attempting to retrieve
            the fabric details.
    """

    def __init__(self, params):
        self.class_name = self.__class__.__name__
        super().__init__(params)

        self.action = "fabric_query"
        self._implemented_states.add("query")

        self.log = logging.getLogger(f"dcnm.{self.class_name}")
        self.fabric_details = FabricDetailsByName()

        msg = "ENTERED Query(): "
        msg += f"state: {self.state}, "
        msg += f"check_mode: {self.check_mode}"
        self.log.debug(msg)

    def commit(self) -> None:
        """
        ### Summary
        query the fabrics in ``self.want`` that exist on the controller.

        ### Raises

        -   ``ValueError`` if:
            -   Any fabric names are invalid.
            -   The controller returns an error when attempting to
                query the fabrics.
        """
        # pylint: disable=no-member
        self.fabric_details.rest_send = self.rest_send
        self.fabric_details.results = Results()
        # pylint: enable=no-member

        self.get_want()

        fabric_query = FabricQuery()
        fabric_query.fabric_details = self.fabric_details
        # pylint: disable=no-member
        fabric_query.rest_send = self.rest_send
        fabric_query.results = self.results
        # pylint: enable=no-member

        fabric_names_to_query = []
        for want in self.want:
            fabric_names_to_query.append(want["FABRIC_NAME"])
        try:
            fabric_query.fabric_names = copy.copy(fabric_names_to_query)
        except ValueError as error:
            raise ValueError(f"{error}") from error

        try:
            fabric_query.commit()
        except ValueError as error:
            raise ValueError(f"{error}") from error


class Replaced(Common):
    """
    ### Summary
    Handle replaced state.

    ### Raises

    -   ``ValueError`` if:
        -   The controller features required for the fabric type are not
            running on the controller.
        -   The playbook parameters are invalid.
        -   The controller returns an error when attempting to retrieve
            the template.
        -   The controller returns an error when attempting to retrieve
            the fabric details.
        -   The controller returns an error when attempting to create
            the fabric.
        -   The controller returns an error when attempting to update
    """

    def __init__(self, params):
        self.class_name = self.__class__.__name__
        super().__init__(params)
        method_name = inspect.stack()[0][3]  # pylint: disable=unused-variable

        self.action = "fabric_replaced"
        self.log = logging.getLogger(f"dcnm.{self.class_name}")

        self.fabric_details = FabricDetailsByName()
        self.fabric_replaced = FabricReplacedBulk()
        self.fabric_summary = FabricSummary()
        self.fabric_types = FabricTypes()
        self.merged = None
        self.need_create = []
        self.need_replaced = []
        self.template = TemplateGet()
        self._implemented_states.add("replaced")

        msg = f"ENTERED Replaced.{method_name}: "
        msg += f"state: {self.state}, "
        msg += f"check_mode: {self.check_mode}"
        self.log.debug(msg)

    def get_need(self):
        """
        ### Summary
        Build ``self.need`` for replaced state.

        ### Raises
        -   ``ValueError`` if:
            -   The controller features required for the fabric type are not
                running on the controller.
        """
        method_name = inspect.stack()[0][3]
        self.payloads = {}
        for want in self.want:

            fabric_name = want.get("FABRIC_NAME", None)
            fabric_type = want.get("FABRIC_TYPE", None)

            # If fabrics do not exist on the controller, add them to
            # need_create.  These will be created by Merged() in
            # Replaced.send_need_replaced()
            if fabric_name not in self.have.all_data:
                self.need_create.append(want)
                continue

            if self.features.get("fabric_type") is False:
                msg = f"{self.class_name}.{method_name}: "
                msg += f"Features required for fabric {fabric_name} "
                msg += f"of type {fabric_type} are not running on the "
                msg += "controller. Review controller settings at "
                msg += "Fabric Controller -> Admin -> System Settings -> "
                msg += "Feature Management"
                raise ValueError(msg)

            self.need_replaced.append(want)

    def commit(self):
        """
        ### Summary
        Commit the replaced state request.

        ### Raises

        -   ``ValueError`` if:
            -   The controller features required for the fabric type are not
                running on the controller.
        """
        method_name = inspect.stack()[0][3]
        msg = f"{self.class_name}.{method_name}: entered"
        self.log.debug(msg)

        # pylint: disable=no-member
        self.fabric_details.rest_send = self.rest_send
        self.fabric_summary.rest_send = self.rest_send
        # pylint: enable=no-member

        self.fabric_details.results = Results()
        self.fabric_summary.results = Results()

        self.get_controller_features()
        self.get_want()
        self.get_have()
        self.get_need()
        self.send_need_replaced()

    def send_need_replaced(self) -> None:
        """
        ### Summary
        Build and send the payload to modify fabrics specified in the
        playbook per replaced state handling.

        ### Raises

        -   ``ValueError`` if:
            -   Any payload is invalid.
            -   The controller returns an error when attempting to
                 update the fabric.
        """
        method_name = inspect.stack()[0][3]  # pylint: disable=unused-variable
        msg = f"{self.class_name}.{method_name}: entered. "
        msg += "self.need_replaced: "
        msg += f"{json_pretty(self.need_replaced)}"
        self.log.debug(msg)

        if len(self.need_create) != 0:
            self.merged = Merged(self.params)
            # pylint: disable=no-member
            self.merged.rest_send = self.rest_send  # pylint: disable=attribute-defined-outside-init
            self.merged.fabric_details.rest_send = self.rest_send
            self.merged.fabric_summary.rest_send = self.rest_send
            self.merged.results = self.results
            # pylint: disable=no-member
            self.merged.need_create = self.need_create
            self.merged.send_need_create()

        if len(self.need_replaced) == 0:
            msg = f"{self.class_name}.{method_name}: "
            msg += "No fabrics to update for replaced state."
            self.log.debug(msg)
            return

        self.fabric_replaced.fabric_details = self.fabric_details
        self.fabric_replaced.fabric_summary = self.fabric_summary
        # pylint: disable=no-member
        self.fabric_replaced.rest_send = self.rest_send
        # pylint: enable=no-member
        self.fabric_replaced.results = self.results

        try:
            self.fabric_replaced.payloads = self.need_replaced
        except ValueError as error:
            raise ValueError(f"{error}") from error

        try:
            self.fabric_replaced.commit()
        except ValueError as error:
            raise ValueError(f"{error}") from error
