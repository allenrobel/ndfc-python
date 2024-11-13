import argparse

parser_help = "Password for NX-OS switches. "
parser_help += "If missing, the environment variable NXOS_PASSWORD "
parser_help += "or Ansible Vault is used."

parser_nxos_password = argparse.ArgumentParser(add_help=False)
optional = parser_nxos_password.add_argument_group(title="OPTIONAL ARGS")
optional.add_argument(
    "--nxos-password",
    dest="nxos_password",
    required=False,
    default="foo",
    help=f"{parser_help}",
)
