import copy
import inspect
import json
import logging
from typing import Any

from plugins.module_utils.common.merge_dicts_v2 import MergeDicts
from plugins.module_utils.common.properties import Properties
from plugins.module_utils.common.results import Results
from plugins.module_utils.image_policy.create import ImagePolicyCreateBulk
from plugins.module_utils.image_policy.delete import ImagePolicyDelete
from plugins.module_utils.image_policy.image_policies import ImagePolicies
from plugins.module_utils.image_policy.payload import Config2Payload
from plugins.module_utils.image_policy.query import ImagePolicyQuery
from plugins.module_utils.image_policy.replace import ImagePolicyReplaceBulk
from plugins.module_utils.image_policy.update import ImagePolicyUpdateBulk


@Properties.add_rest_send
class Common:
    """
    Common methods for all states
    """

    def __init__(self, params) -> None:
        self.class_name = self.__class__.__name__
        method_name = inspect.stack()[0][3]

        self.log = logging.getLogger(f"dcnm.{self.class_name}")
        self.params: dict[Any, Any] = params

        self.state = self.params.get("state", None)
        self.check_mode = self.params.get("check_mode", None)

        if self.state not in ["deleted", "merged", "overridden", "query", "replaced"]:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Invalid state ({self.state}) in params."
            raise ValueError(msg)

        if self.check_mode not in [False, True]:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"Invalid check_mode ({self.check_mode}) in params."
            raise ValueError(msg)

        self.config = self.params.get("config", {}).get("config", None)

        msg = f"{self.class_name}.{method_name}: "
        msg += f"self.config: {self.config}"
        self.log.debug(msg)

        self.results = Results()
        self.results.check_mode = self.check_mode

        self._rest_send = None

        self.want: list[Any] = []
        self.have = ImagePolicies()

        msg = f"ENTERED {self.class_name}().{method_name}: "
        msg += f"check_mode: {self.check_mode}"
        self.log.debug(msg)

    def get_want(self) -> None:
        """
        # Summary

        Modify the configurations in self.want["config"] by converting them
        to payloads to more easily compare them to self.have (the current image
        policies on the controller).

        # Raises

        `ValueError` if:
            - `Config2Payload` raises `ValueError`
        """
        method_name = inspect.stack()[0][3]

        for config in self.config:
            payload = Config2Payload()
            payload.config = config
            payload.params = self.params
            try:
                payload.commit()
            except ValueError as error:
                msg = f"{self.class_name}.{method_name}: "
                msg += "Error while converting config to payload. "
                msg += f"Error detail: {error}"
                self.log.error(msg)
                print(msg)
            self.want.append(payload.payload)

    def get_have(self) -> None:
        """
        Caller: main()

        self.have consists of the current image policies on the controller
        """
        method_name = inspect.stack()[0][3]
        msg = f"ENTERED {self.class_name}.{method_name}"
        self.log.debug(msg)

        self.have = ImagePolicies()
        # pylint: disable=no-member
        self.have.results = self.results  # type: ignore[attr-defined]
        self.have.rest_send = self.rest_send  # type: ignore[attr-defined]
        self.have.refresh()
        # pylint: enable=no-member


class Deleted(Common):
    """
    Handle deleted state
    """

    def __init__(self, params):
        self.class_name = self.__class__.__name__
        method_name = inspect.stack()[0][3]

        try:
            super().__init__(params)
        except (TypeError, ValueError) as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += "Error during super().__init__(). "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error

        if not isinstance(self.config, list):
            msg = f"{self.class_name}.{method_name}: "
            msg += "Expected list of dict for params.config. "
            msg += f"Got {type(self.config).__name__}"
            raise TypeError(msg)

        self.delete = ImagePolicyDelete()

        msg = f"ENTERED {self.class_name}().{method_name}: "
        msg += f"state: {self.state}, "
        msg += f"check_mode: {self.check_mode}"
        self.log.debug(msg)

    def commit(self) -> None:
        """
        If config is present, delete all policies in self.want that exist on the controller
        If config is not present, delete all policies on the controller
        """
        method_name = inspect.stack()[0][3]
        msg = f"ENTERED {self.class_name}.{method_name}: "
        msg += f"state: {self.state}, "
        msg += f"check_mode: {self.check_mode}"
        self.log.debug(msg)

        # pylint: disable=no-member
        if self.rest_send is None:  # type: ignore[attr-defined]
            msg = f"{self.class_name}.{method_name}: "
            msg += f"rest_send must be set before calling {method_name}."
            raise ValueError(msg)
        # pylint: enable=no-member

        self.results.state = self.state
        self.results.check_mode = self.check_mode

        self.delete.policy_names = self.get_policies_to_delete()
        self.delete.results = self.results
        # pylint: disable=no-member
        self.delete.rest_send = self.rest_send  # type: ignore[attr-defined]
        # pylint: enable=no-member
        self.delete.params = self.params
        self.delete.commit()

    def get_policies_to_delete(self) -> list[str]:
        """
        Return a list of policy names to delete

        -   In config is present, return list of image policy names
            in self.want.
        -   If want["config"] is not present, return ["delete_all_image_policies"],
            which ``ImagePolicyDelete()`` interprets as "delete all image
            policies on the controller".
        """
        method_name = inspect.stack()[0][3]
        msg = f"{self.class_name}.{method_name}: "
        msg += f"self.config: {self.config}"
        self.log.debug(msg)

        # if self.config is None:
        #     return ["delete_all_image_policies"]
        self.get_want()
        policy_names_to_delete = []
        for want in self.want:
            policy_names_to_delete.append(want["policyName"])
        return policy_names_to_delete


class Overridden(Common):
    """
    ### Summary
    Handle overridden state

    ### Raises
    -   ``ValueError`` if:
            -   ``Common().__init__()`` raises ``TypeError`` or ``ValueError``.
    """

    def __init__(self, params):
        self.class_name = self.__class__.__name__
        method_name = inspect.stack()[0][3]

        try:
            super().__init__(params)
        except (TypeError, ValueError) as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += "Error during super().__init__(). "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error

        if not isinstance(self.config, list):
            msg = f"{self.class_name}.{method_name}: "
            msg += "Expected list of dict for params.config. "
            msg += f"Got {type(self.config).__name__}"
            raise TypeError(msg)

        self.delete = ImagePolicyDelete()
        self.merged = Merged(params)
        self.replaced = Replaced(params)

        msg = f"ENTERED {self.class_name}().{method_name}: "
        msg += f"state: {self.state}, "
        msg += f"check_mode: {self.check_mode}"
        self.log.debug(msg)

    def commit(self) -> None:
        """
        ### Summary
        -   Delete all policies on the controller that are not in self.want
        -   Instantiate`` Merged()`` and call ``Merged().commit()``
        """
        method_name = inspect.stack()[0][3]
        msg = f"ENTERED {self.class_name}.{method_name}: "
        msg += f"state: {self.state}, "
        msg += f"check_mode: {self.check_mode}"
        self.log.debug(msg)

        self.results.state = self.state
        self.results.check_mode = self.check_mode

        self.get_want()
        self.get_have()

        msg = f"{self.class_name}.{method_name}: "
        msg += "self.want: "
        msg += f"{json.dumps(self.want, indent=4, sort_keys=True)}"
        self.log.debug(msg)

        msg = f"{self.class_name}.{method_name}: "
        msg += "self.have.all_policies: "
        msg += f"{json.dumps(self.have.all_policies, indent=4, sort_keys=True)}"
        self.log.debug(msg)

        self._delete_policies_not_in_want()
        # pylint: disable=no-member
        # pylint: disable=attribute-defined-outside-init
        self.replaced.rest_send = self.rest_send  # type: ignore[attr-defined]
        # pylint: enable=no-member
        # pylint: enable=attribute-defined-outside-init
        self.replaced.results = self.results
        self.replaced.commit()

    def _delete_policies_not_in_want(self) -> None:
        """
        ### Summary
        Delete all policies on the controller that are not in self.want
        """
        method_name = inspect.stack()[0][3]
        want_policy_names = set()
        for want in self.want:
            want_policy_names.add(want["policyName"])

        policy_names_to_delete = []
        for policy_name in self.have.all_policies:
            msg = f"{self.class_name}.{method_name}: "
            msg += f"policy_name: {policy_name}"
            self.log.debug(msg)
            if policy_name not in want_policy_names:
                msg = f"{self.class_name}.{method_name}: "
                msg += f"Appending to policy_names_to_delete: {policy_name}"
                self.log.debug(msg)
                policy_names_to_delete.append(policy_name)

        msg = f"{self.class_name}.{method_name}: "
        msg += f"policy_names_to_delete: {policy_names_to_delete}"
        self.log.debug(msg)

        if len(policy_names_to_delete) == 0:
            return

        self.results.state = self.state
        self.results.check_mode = self.check_mode
        self.delete.policy_names = policy_names_to_delete
        self.delete.results = self.results
        # pylint: disable=no-member
        self.delete.rest_send = self.rest_send  # type: ignore[attr-defined]
        # pylint: enable=no-member
        self.delete.params = self.params
        self.delete.commit()


class Merged(Common):
    """
    # Summary

    Handle merged state

    # Raises

    -   ``ValueError`` if:
        -   ``params`` is missing ``config`` key.
        -   ``commit()`` is issued before setting mandatory properties
    """

    def __init__(self, params):
        self.class_name = self.__class__.__name__
        method_name = inspect.stack()[0][3]

        try:
            super().__init__(params)
        except (TypeError, ValueError) as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += "Error during super().__init__(). "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error

        if not isinstance(self.config, list):
            msg = f"{self.class_name}.{method_name}: "
            msg += "Expected list of dict for params.config. "
            msg += f"Got {type(self.config).__name__}"
            raise TypeError(msg)

        self.create = ImagePolicyCreateBulk()
        self.update = ImagePolicyUpdateBulk()

        # new policies to be created
        self.need_create = []
        # existing policies to be updated
        self.need_update = []

        self.need = []
        self.state = "merged"

        msg = f"ENTERED {self.class_name}().{method_name}: "
        msg += f"state: {self.state}, "
        msg += f"check_mode: {self.check_mode}"
        self.log.debug(msg)

    def get_need(self):
        """
        # Summary

        Build self.need for merged state

        # Description

        -   Populate self.need_create with items from self.want that are
            not in self.have
        -   Populate self.need_update with updated policies.  Policies are
            updated as follows:
                -   If a policy is in both self.want amd self.have, and they
                    contain differences, merge self.want into self.have,
                    with self.want keys taking precedence and append the
                    merged policy to self.need_update.
                -   If a policy is in both self.want and self.have, and they
                    are identical, do not append the policy to self.need_update
                    (i.e. do nothing).
        """
        method_name = inspect.stack()[0][3]
        msg = f"ENTERED {self.class_name}.{method_name}: "
        msg += f"state: {self.state}, "
        msg += f"check_mode: {self.check_mode}"
        self.log.debug(msg)

        for want in self.want:
            self.have.policy_name = want.get("policyName")

            # Policy does not exist on the controller so needs to be created.
            if self.have.policy is None:
                self.need_create.append(copy.deepcopy(want))
                continue

            # The policy exists on the controller.  Merge want parameters with
            # the controller's parameters and add the merged parameters to the
            # need_update list if they differ from the want parameters.
            have = copy.deepcopy(self.have.policy)
            merged, needs_update = self._merge_policies(have, want)

            if needs_update is True:
                self.need_update.append(copy.deepcopy(merged))

    def commit(self) -> None:
        """
        Commit the merged state requests
        """
        method_name = inspect.stack()[0][3]
        msg = f"ENTERED {self.class_name}.{method_name}: "
        msg += f"state: {self.state}, "
        msg += f"check_mode: {self.check_mode}"
        self.log.debug(msg)

        # pylint: disable=no-member
        if self.rest_send is None:  # type: ignore[attr-defined]
            msg = f"{self.class_name}.{method_name}: "
            msg += f"rest_send must be set before calling {method_name}."
            raise ValueError(msg)
        # pylint: enable=no-member

        self.results.state = self.state
        self.results.check_mode = self.check_mode

        self.get_want()
        self.get_have()
        self.get_need()
        self.send_need_create()
        self.send_need_update()

    def _prepare_for_merge(self, have: dict, want: dict) -> tuple[dict[Any, Any], dict[Any, Any]]:
        """
        ### Summary
        -   Remove fields in "have" that are not part of a request payload i.e.
            imageName and ref_count.
        -   The controller returns "N9K/N3K" for the platform, but it expects
            "N9K" in the payload.  We change "N9K/N3K" to "N9K" in have so that
            the compare works.
        -   Remove all fields that are not set in both "have" and "want"
        """
        # Remove keys that the controller adds which are not part
        # of a request payload.
        for key in ["imageName", "ref_count", "platformPolicies"]:
            have.pop(key, None)

        # Change "N9K/N3K" to "N9K" in "have" to match the request payload.
        if have.get("platform", None) == "N9K/N3K":
            have["platform"] = "N9K"

        return (have, want)

    def _merge_policies(self, have: dict, want: dict) -> tuple[dict[Any, Any], bool]:
        """
        ### Summary
        Merge the parameters in want with the parameters in have.
        """
        method_name = inspect.stack()[0][3]
        (have, want) = self._prepare_for_merge(have, want)

        # Merge the parameters in want with the parameters in have.
        # The parameters in want take precedence.
        try:
            merge = MergeDicts()
            merge.dict1 = have
            merge.dict2 = want
            merge.commit()
        except (TypeError, ValueError) as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += "Error during MergeDicts(). "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error
        merged = copy.deepcopy(merge.dict_merged)

        needs_update = False

        if have != merged:
            needs_update = True

        return (merged, needs_update)

    def send_need_create(self) -> None:
        """
        ### Summary
        Create the policies in self.need_create

        """
        self.create.results = self.results
        self.create.payloads = self.need_create
        # pylint: disable=no-member
        self.create.rest_send = self.rest_send  # type: ignore[attr-defined]
        # pylint: enable=no-member
        self.create.params = self.params
        self.create.commit()

    def send_need_update(self) -> None:
        """
        ### Summary
        Update the policies in self.need_update

        """
        self.update.results = self.results
        self.update.payloads = self.need_update
        # pylint: disable=no-member
        self.update.rest_send = self.rest_send  # type: ignore[attr-defined]
        # pylint: enable=no-member
        self.update.params = self.params
        self.update.commit()


class Query(Common):
    """
    Handle query state
    """

    def __init__(self, params):
        self.class_name = self.__class__.__name__
        method_name = inspect.stack()[0][3]

        try:
            super().__init__(params)
        except (TypeError, ValueError) as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += "Error during super().__init__(). "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error

        if not isinstance(self.config, list):
            msg = f"{self.class_name}.{method_name}: "
            msg += "Expected list of dict for params.config. "
            msg += f"Got {type(self.config).__name__}"
            raise TypeError(msg)

        self.image_policies = None
        self.query = None

        msg = f"ENTERED {self.class_name}().{method_name}: "
        msg += f"state: {self.state}, "
        msg += f"check_mode: {self.check_mode}"
        self.log.debug(msg)

    def commit(self) -> None:
        """
        query the fabrics in self.want that exist on the controller
        """
        method_name = inspect.stack()[0][3]
        msg = f"ENTERED {self.class_name}.{method_name}: "
        msg += f"state: {self.state}, "
        msg += f"check_mode: {self.check_mode}"
        self.log.debug(msg)

        self.results.state = self.state
        self.results.check_mode = self.check_mode

        self.get_want()

        if len(self.want) == 0:
            msg = f"{self.class_name}.{method_name}: "
            msg += "Nothing to query."
            print("msg")
            return

        policy_names_to_query = set()
        for want in self.want:
            policy_names_to_query.add(want["policyName"])

        self.image_policies = ImagePolicies()
        # pylint: disable=no-member
        self.image_policies.rest_send = self.rest_send  # type: ignore[attr-defined]
        # pylint: enable=no-member
        self.image_policies.results = self.results

        self.query = ImagePolicyQuery()
        self.query.image_policies = self.image_policies
        self.query.params = self.params
        self.query.policy_names = list(policy_names_to_query)
        # pylint: disable=no-member
        self.query.rest_send = self.rest_send  # type: ignore[attr-defined]
        # pylint: enable=no-member
        self.query.results = self.results
        self.query.commit()


class Replaced(Common):
    """
    Handle replaced state
    """

    def __init__(self, params):
        self.class_name = self.__class__.__name__
        method_name = inspect.stack()[0][3]

        try:
            super().__init__(params)
        except (TypeError, ValueError) as error:
            msg = f"{self.class_name}.{method_name}: "
            msg += "Error during super().__init__(). "
            msg += f"Error detail: {error}"
            raise ValueError(msg) from error

        if not isinstance(self.config, list):
            msg = f"{self.class_name}.{method_name}: "
            msg += "Expected list of dict for params.config. "
            msg += f"Got {type(self.config).__name__}"
            raise TypeError(msg)

        self.replace = ImagePolicyReplaceBulk()

        msg = f"ENTERED {self.class_name}().{method_name}: "
        msg += f"state: {self.state}, "
        msg += f"check_mode: {self.check_mode}"
        self.log.debug(msg)

    def commit(self) -> None:
        """
        Replace all policies on the controller that are in want
        """
        self.results.state = self.state
        self.results.check_mode = self.check_mode

        self.get_want()
        self.get_have()

        self.replace.params = self.params
        self.replace.payloads = self.want
        self.replace.rest_send = self.rest_send  # type: ignore[attr-defined]
        self.replace.results = self.results
        self.replace.commit()
