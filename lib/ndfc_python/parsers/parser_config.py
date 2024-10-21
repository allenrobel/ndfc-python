import argparse

parser_help = "Absolute path to a YAML configuration file. "
parser_help += "e.g. /home/myself/myfile.yaml"

parser_config = argparse.ArgumentParser(add_help=False)
mandatory = parser_config.add_argument_group(title="MANDATORY ARGS")
mandatory.add_argument("-c", "--config", dest="config", required=True, help=f"{parser_help}")
