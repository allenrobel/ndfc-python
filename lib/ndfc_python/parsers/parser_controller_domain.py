import argparse

parser_help = "Login domain for the Nexus Dashboard controller. "
parser_help += "If missing, the environment variable NDFC_DOMAIN is used. "

parser_controller_domain = argparse.ArgumentParser(add_help=False)
optional = parser_controller_domain.add_argument_group(title="OPTIONAL ARGS")
optional.add_argument(
    "-d", "--domain", dest="controller_domain", required=False, help=f"{parser_help}"
)
