import argparse

def parse_arguments(argv=None):
    parser = argparse.ArgumentParser(
        description="A tool to generate a static blog, "
        " with restructured text input files.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--version",
        action="version",
        version=__version__,
        help="Print the pelican version and exit.",
    )