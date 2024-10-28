import argparse

parser_help = "Absolute path to an Ansible Vault. "
parser_help += "e.g. /home/myself/.ansible/vault. "

parser_ansible_vault = argparse.ArgumentParser(add_help=False)
optional = parser_ansible_vault.add_argument_group(title="OPTIONAL ARGS")
optional.add_argument(
    "-v",
    "--ansible-vault",
    dest="ansible_vault",
    required=False,
    default=None,
    help=f"{parser_help}",
)
