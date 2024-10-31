import argparse

parser_help = "Password for the Nexus Dashboard controller. "
parser_help += "If missing, the environment variable ND_PASSWORD "
parser_help += "or Ansible Vault is used."

parser_nd_password = argparse.ArgumentParser(add_help=False)
optional = parser_nd_password.add_argument_group(title="OPTIONAL ARGS")
optional.add_argument(
    "--nd-password",
    dest="nd_password",
    required=False,
    help=f"{parser_help}",
)
