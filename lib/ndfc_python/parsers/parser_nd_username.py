import argparse

parser_help = "Username for the Nexus Dashboard controller. "
parser_help += "If missing, the environment variable ND_USERNAME "
parser_help += "or Ansible Vault is used. "

parser_nd_username = argparse.ArgumentParser(add_help=False)
optional = parser_nd_username.add_argument_group(title="OPTIONAL ARGS")
optional.add_argument(
    "--nd-username",
    dest="nd_username",
    required=False,
    help=f"{parser_help}",
)
