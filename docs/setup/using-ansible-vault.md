# Using Ansible Vault

Most `ndfc-python` scripts now include a `--ansible-vault` command line argument.
When this argument is present, you'll be asked for your vault password, and the
script will read the vault for any of the credentials it needs.

Below is a quick cheat-sheet.

## Installation

``` bash
pip install ansible
```

## Update your Vault with key/values specific to ndfc-python

Next, you'll need to edit your Ansible Vault file to add your Nexus Dashboard Controller
credentials (username, password, login domain) and ip address, as well as the username
and password for your NX-OS switches.  NX-OS credentials are used by, for example,
[reachability.py](https://github.com/allenrobel/ndfc-python/blob/main/examples/reachability.py)
which uses them for switch discovery.

It is recommended (but not mandatory) that you encrypt all passwords.  Below is one way to do this.

### Modify /path/to/your/ansible/vault/file

#### Edit `nd_password` and `nxos_password`

- `nd_password` is the password used to login to the Nexus Dashboard controller.
- `nxos_password` is the password used by Nexus Dashboard to login to NX-OS switches that it manages.

Add `nd_password` and `nxos_password` in encrypted format (or non-encrypted,
if you don't care about security).

To add encrypted passwords, issue the following.

``` bash title="Generate encrypted passwords"
ansible-vault encrypt_string 'mySuperSecretNdfcPassword' --name 'nd_password' >> /path/to/your/ansible/vault/file
echo "" >> /path/to/your/ansible/vault/file
ansible-vault encrypt_string 'mySuperSecretNxosPassword' --name 'nxos_password' >> /path/to/your/ansible/vault/file
echo "" >> /path/to/your/ansible/vault/file
```

`ansible-vault` will prompt you for a vault password, which you'll use to decrypt
these passwords when running the example scripts.

#### Example

``` bash title="Example encrypted password"
% ansible-vault encrypt_string 'mySuperSecretNdfcPassword' --name 'nd_password' >> /path/to/your/ansible/vault/file
New Vault password: 
Confirm New Vault password: 
%
% echo "" >> /path/to/your/ansible/vault/file
% cat /path/to/your/ansible/vault/file
nd_password: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          35313565343034623966323832303764633165386439663133323832383336366362663431366565
          6238373030393562363831616266336464353963393566300a316564663135323263653165393330
          33353935396462663531323437336366653937326234313866623535313431366534363938633834
          6563336634653963320a376364323430316134623430636265383561663631343763646465626365
          36666366333438373537343033393939653830663061623362613439376161626439
% 
```

If you don't care about security, you can add non-encrypted passwords by editing the
file directly. The following are example unencrypted passwords for the Nexus Dashboard
controller and NX-OS devices added to this file:

``` yaml title="Example non-encrypted passwords"
nd_password: mySuperSecretNdfcPassword
nxos_password: mySuperSecretNxosPassword
```

#### Add the domain for Nexus Dashboard Controller login

Change ``nd_domain`` in the same file to the domain associated with the above password
that you're using on Nexus Dashboard.  If the `domain` field is not displayed when you
login to the GUI, then use local, as shown below.

``` yaml title="Example ND domain"
nd_domain: local
```

#### Add usernames for Nexus Dashboard Controller and switches

Change `nd_username` in the same file to the username associated with the above
password that you're using on Nexus Dashboard.

Change `nxos_username` in the same file to the username used to login to your
NX-OS switches.

``` yaml title="Example username credentials"
nd_username: admin
nxos_username: admin
```

#### Add the IPv4 address of your Nexus Dashboard Controller

``` yaml title="Example ipv4 address"
nd_ip4: 192.168.1.1
```

## See also

- [Credentials](./set-credentials.md) for a list of the credential names the scripts expect.
- [Ansible Vault @ docs.ansible.com](https://docs.ansible.com/ansible/latest/vault_guide/vault.html)
  for detailed Ansible Vault installation and usage.
