import argparse

parser_help = "Password for the Nexus Dashboard controller. "
parser_help += "If missing, the environment variable ND_PASSWORD is used. "

parser_controller_password = argparse.ArgumentParser(add_help=False)
optional = parser_controller_password.add_argument_group(title="OPTIONAL ARGS")
optional.add_argument(
    "--nd-password",
    dest="controller_password",
    required=False,
    help=f"{parser_help}",
)
