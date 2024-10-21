import argparse

help = "Password for the Nexus Dashboard controller. "
help += "If missing, the environment variable NDFC_PASSWORD is used. "

parser_controller_password = argparse.ArgumentParser(add_help=False)
optional = parser_controller_password.add_argument_group(title='OPTIONAL ARGS')
optional.add_argument(
    "-p", "--password",
    dest="controller_password",
    required=False,
    help = f"{help}"
)
