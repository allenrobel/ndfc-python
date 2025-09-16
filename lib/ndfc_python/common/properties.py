from plugins.module_utils.common.rest_send_v2 import RestSend
from plugins.module_utils.common.results import Results


class Properties:
    """
    # Summary

    Common properties used in the ndfc-python repository
    """

    def __init__(self):
        self._rest_send = None
        self._results = None

    @property
    def rest_send(self) -> RestSend:
        """
        rest_send: An instance of RestSend
        """
        return self._rest_send

    @rest_send.setter
    def rest_send(self, value: RestSend):
        self._rest_send = value

    @property
    def results(self) -> Results:
        """
        results: An instance of Results
        """
        return self._results

    @results.setter
    def results(self, value: Results):
        self._results = value
