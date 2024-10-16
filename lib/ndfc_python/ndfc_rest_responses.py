#!/usr/bin/env python
import json


class NdfcRestServer:
    """
    A rudimentary REST response server.
    """

    def __init__(self):
        pass

    @staticmethod
    def ndfc_fabric_inventory():
        """
        ### Summary
        Return JSON response for ndfcFabricInventory
        """
        return json.dumps(
            {
                "fabricName": "DCNM",
                "fabricId": "1",
                "fabricNodes": [
                    {
                        "nodeId": "101",
                        "nodeType": "spine",
                        "nodeRole": "spine",
                        "nodeModel": "N9K-C9336C-FX2",
                        "nodeSerialNumber": "SAL2034L7ZK",
                        "nodeName": "DCNM-SPINE-1",
                        "nodeIpAddress": "10.1.1.1",
                        "nodeMacAddress": "00:00:00:00:00:01",
                        "nodeVersion": "11.3(1)",
                        "nodeUptime": "1 day, 2:03:04",
                    }
                ],
            }
        )


ndfc = NdfcRestServer()
inventory = json.loads(ndfc.ndfc_fabric_inventory())
print(inventory["fabricName"])
