import argparse

parser_loglevel = argparse.ArgumentParser(add_help=False)
default = parser_loglevel.add_argument_group(title="DEFAULT ARGS")
default.add_argument(
    "-l",
    "--loglevel",
    dest="loglevel",
    choices=["INFO", "WARNING", "ERROR", "DEBUG"],
    required=False,
    default="INFO",
    help="Logging level",
)
