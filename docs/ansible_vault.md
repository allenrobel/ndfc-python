# Ansible Vault

ndfc-python can be modified to work with Ansible Vault, per below.

## Ansible Python Libraries

If you want to use Ansible Vault with ndfc-python, install Ansible.

### Example

```bash
pip install ansible
```

## Config File

To use these scripts and libraries with Ansible Vault, you'll need to update a common settings
file and set the environment variable ``NDFC_PYTHON_CONFIG`` to point to it.  For example,
if you want your settings to be located in $HOME/ndfc-python-settings.yaml, then set:

```bash
export NDFC_PYTHON_CONFIG=$HOME/ndfc-python-settings.yaml
```

And edit this file to contain:

```yaml
---
ansible_vault: '/path/to/your/ansible/vault/file'
```

## Update your Vault with key/values specific to ndfc-python

Next, you'll need to edit your Ansible Vault file to add your Nexus Dashboard Controller
credentials (username, password, and login domain) and ip address.

We may also require the username and password for your switches in the future,
so you might want to add this as well.

```bash
/path/to/your/ansible/vault/file 
```

It is recommended (but not mandatory) that you encrypt all passwords.  Below is one way to do this.

### Modify /path/to/your/ansible/vault/file

#### Edit ``ansible_password`` (password for NDFC controller) and ``device_password`` (password for NX-OS switches)

Add ``ansible_password`` and ``device_password`` in encrypted format (or non-encrypted,
if you don't care about security).  These are the passwords you use to login to your
ND/NDFC Controller, and NX-OS switches, respectively.

To add encrypted passwords for the ND/NDFC controller and NX-OS devices,
issue the following from this repository's top-level directory.

```bash
ansible-vault encrypt_string 'mySuperSecretNdfcPassword' --name 'ansible_password' >> /path/to/your/ansible/vault/file
echo "" >> /path/to/your/ansible/vault/file
ansible-vault encrypt_string 'mySuperSecretNxosPassword' --name 'device_password' >> /path/to/your/ansible/vault/file
echo "" >> /path/to/your/ansible/vault/file
```

ansible-vault will prompt you for a vault password, which you'll use to decrypt
these passwords when running the example scripts.

Example:

```bash
% ansible-vault encrypt_string 'mySuperSecretNdfcPassword' --name 'ansible_password' >> /path/to/your/ansible/vault/file
New Vault password: 
Confirm New Vault password: 
%
% echo "" >> /path/to/your/ansible/vault/file
% cat /path/to/your/ansible/vault/file
ansible_password: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          35313565343034623966323832303764633165386439663133323832383336366362663431366565
          6238373030393562363831616266336464353963393566300a316564663135323263653165393330
          33353935396462663531323437336366653937326234313866623535313431366534363938633834
          6563336634653963320a376364323430316134623430636265383561663631343763646465626365
          36666366333438373537343033393939653830663061623362613439376161626439
% 
```

If you don't care about security, you can add a non-encrypted password by editing the
file directly. The following are example unencrypted passwords for the ND/NDFC controller
and NX-OS devices added to this file:

```yaml
ansible_password: mySuperSecretNdfcPassword
device_password: mySuperSecretNxosPassword
```

#### Add the domain for Nexus Dashboard Controller login

Change ``nd_domain`` in the same file to the domain associated with the above password
that you're using on ND/NDFC.  If the "domain" field is not displayed when you login to
the GUI, then use local, as shown below.

```yaml
nd_domain: local
```

#### Add usernames for Nexus Dashboard Controller and switches

Change ``ansible_user`` in the same file to the username associated with the above
password that you're using on ND/NDFC.

Change ``device_username`` in the same file to the username used to login to your
NX-OS switches.

Example:

```yaml
ansible_user: voldomort
device_username: admin
```

#### Add the ip address of your Nexus Dashboard Controller

```yaml
ndfc_ip: 192.168.1.1
```
