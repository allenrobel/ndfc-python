import argparse

parser_help = "Login domain for the Nexus Dashboard controller. "
parser_help += "If missing, the environment variable ND_DOMAIN or Ansible Vault is used. "

parser_nd_domain = argparse.ArgumentParser(add_help=False)
optional = parser_nd_domain.add_argument_group(title="OPTIONAL ARGS")
optional.add_argument("--nd-domain", dest="nd_domain", required=False, help=f"{parser_help}")
