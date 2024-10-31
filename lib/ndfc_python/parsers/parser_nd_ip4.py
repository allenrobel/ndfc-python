import argparse

parser_help = "IPv4 address for the Nexus Dashboard controller. "
parser_help += "If missing, the environment variable ND_IP4 "
parser_help += "or Ansible Vault is used."

parser_nd_ip4 = argparse.ArgumentParser(add_help=False)
optional = parser_nd_ip4.add_argument_group(title="OPTIONAL ARGS")
optional.add_argument("--nd-ip4", dest="nd_ip4", required=False, help=f"{parser_help}")
