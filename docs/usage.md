# Usage

## To clone this repository

```bash
git clone https://github.com/allenrobel/ndfc-python.git
```

## Dependencies


### DCNM Ansible Collection

We depend on RestSend(), Sender() and other classes in this repository.

To install:

1. ``cd $HOME/repos`` (or wherever you keep your repositories)
2. ``git clone https://github.com/CiscoDevNet/ansible-dcnm.git``
3. For now, you need to switch to the ``relative-imports`` branch.

```bash
cd $HOME/repos/ansible-dcnm
git switch relative-imports
```

4. Update your PYTHONPATH to include this repository

```bash
export PYTHONPATH=$PYTHONPATH:$HOME/repos/ansible-dcnm
```

With the above in place, imports from this repository will look like the following in your scripts.

```python
from plugins.module_utils.common.rest_send import RestSend
from plugins.module_utils.common.sender_requests import Sender
```

<!---
Commenting this section out until we have replaced the fabric scripts and libraries...

## Fabric Characteristics

The characteristics of the child/site fabrics are as follows (see also the included PDF for a topology).

1. 2 Spine acting as Route Reflectors for all Leaf and Border Gateway
2. 4 Leaf / VTEP (2 VPC pairs using fabric-peering for their virtual peer-link)
3. 2 Border Gateway / VTEP
4. 2 VRF: v1 and v2
5. L3 (ipv4 / ipv6) connectivity between VRF v1 and v2 (import/export of route-targets)
6. L2 connectivity within each VRF
7. OSPF underlay
8. VXLAN/EVPN Replication Mode: Ingress

Spines and Leafs can be added/removed by updating the Common Role Variables described below.

-->


## Python Path

Add this repository's library to your python path.  For example, in .bash_profile or .zprofile

```bash
export PYTHONPATH=${PYTHONPATH}:${HOME}/repos/ndfc-python/lib
```

## Logging configuration

To enable logging, set the following environment variable.

```bash
export NDFC_LOGGING_CONFIG=/path/to/logging_config.json
```

This is a standard Pyton logging configuration file.  There is an example
file in this repository at ``lib/ndfc_python/logging_config.json``

## Running the example scripts

```bash
export PYTHONPATH=${PYTHONPATH}:/path/to/this/repo/ndfc-python/lib
# optional - for Ansible Vault
# export NDFC_PYTHON_CONFIG=/path/to/ndfc-python-settings.yaml
# optional - to enable logging
# export NDFC_LOGGING_CONFIG=/path/to/ndfc-python-logging-config.json

py311) ~ % cd /top/level/directory/of/this/repo/examples
(py311) examples % ./device_info.py --config config_device_info.yaml
```

If you're using Ansible Vault, you'll be prompted for the vault password.

## Ansible Vault
[Usage for Ansible Vault](ansible_vault.md)