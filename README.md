# ndfc-python

This repository contains Python classes and example scripts for interacting
with Cisco's Nexus Dashboard Fabric Controller (NDFC) via its REST API.

We've moved our documentation to GitHub Pages

[https://allenrobel.github.io/ndfc-python/](https://allenrobel.github.io/ndfc-python/)

However a basic quick start guide to this repository follows, intended for those who
have not yet installed the Cisco DCNM Ansible collection.

The ndfc-python repository shares Python code with the DCNM Ansible collection,
so this collection is a dependency.  Note, we do not use anything related
to Ansible.  ndfc-python is, as the name implies, pure Python.

## 1. Create a $HOME/repos directory into which we'll clone ndfc-python

```bash
mkdir $HOME/repos
```

## 2. Clone the ndfc-python repository

```bash
cd $HOME/repos
git clone https://github.com/allenrobel/ndfc-python.git
```

## 3. Clone the ansible-dcnm repository

We want this repository to follow the standard Ansible path structure.

```bash
cd $HOME/repos
mkdir ansible
mkdir ansible/collections
mkdir ansible/collections/ansible_collections
mkdir ansible/collections/ansible_collections/cisco
cd ansible/collections/ansible_collections/cisco
git clone https://github.com/CiscoDevNet/ansible-dcnm.git
# We need to rename the resulting directory from ansible-dcnn to dcnm
mv ansible-dcnm dcnm
```

## 4. Install Python if it is not already installed

[python.org Downloads](https://www.python.org/downloads/)

## 5. Create a virtual environment

```bash
cd $HOME/repos/ndfc-python
python -m venv .venv --prompt ndfc-python
```

## 6. Source the virtual environment

- `source .venv/bin/activate`

```bash
arobel@AROBEL-M-G793 ndfc-python % source .venv/bin/activate
(ndfc-python) AROBEL-M-G793%
```

## 7. Install uv

```bash
pip install uv
```

## 8. Use uv to install the other dependencies

```bash
uv sync
```

## 9. Install the Nexus Dashboard (aka DCNM) Ansible collection

```bash
uv sync
```

## 10. Set required environment variables

```bash
# Edit $HOME/repos/ndfc-python/env/02-nd
# Change the following to match your environment
# ND_IP4=<your Nexus Dashboard IPv4 address>
# ND_USERNAME=<your Nexus Dashboard username, typically admin>
# ND_PASSWORD=<your Nexus Dashboard password for ND_USERNAME>
# NXOS_USERNAME=<The username of your Nexus switches, typically admin>
# NXOS_PASSWORD=<The password of your Nexus switches associated with NXOS_USERNAME>
#
# NOTE: For better security, follow the steps at Github Pages link at the top of this file.
#
# Once 02-nd.sh is edited, source the env.sh file

source $HOME/repos/ndfc-python/env/env
```

## 11. Optionally, enable logging

```bash
export NDFC_LOGGING_CONFIG=$HOME/repos/ndfc-python/lib/ndfc_python/logging_config.json
```

## 11. Run one of the scripts. Let's try the login script

```bash
cd $HOME/repos/ndfc-python
source .venv/bin/activate
source env/env
cd examples
./login.py
```
