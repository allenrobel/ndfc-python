import argparse

help = "IPv4 address for the Nexus Dashboard controller. "
help += "If missing, the environment variable NDFC_IP4 is used. "

parser_controller_ip4 = argparse.ArgumentParser(add_help=False)
optional = parser_controller_ip4.add_argument_group(title='OPTIONAL ARGS')
optional.add_argument(
    "--ip4",
    dest="controller_ip4",
    required=False,
    help = f"{help}"
)
