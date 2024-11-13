import argparse

parser_help = "Username for NX-OS switches. "
parser_help += "If missing, the environment variable NXOS_USERNAME "
parser_help += "or Ansible Vault is used."

parser_nxos_username = argparse.ArgumentParser(add_help=False)
optional = parser_nxos_username.add_argument_group(title="OPTIONAL ARGS")
optional.add_argument(
    "--nxos-username",
    dest="nxos_username",
    required=False,
    default="admin",
    help=f"{parser_help}",
)
