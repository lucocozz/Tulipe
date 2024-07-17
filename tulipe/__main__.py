import os
import sys

from tulipe.cli import CLI
from tulipe import ports


STYLE_RESET = "\033[0m"
ORANGE = "\033[3;33m"
ITALIC = "\033[3;3m"


def main():
    """The main function of the Tulipe CLI."""
    cli = CLI()
    cli.parse()
    port_infos = ports.fetch(cli.type, cli.port, cli.service)
    ports.display(port_infos, cli.format)


if __name__ == "__main__":
    if os.getuid() != 0:
        warning_message = f"{ORANGE}{ITALIC}Warning: all the information may not be available without root privileges.{STYLE_RESET}"
        print(warning_message, file=sys.stderr)
    main()
