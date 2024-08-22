import os
import sys

from colored import Fore, Style

from tulipe.cli import CLI
from tulipe import ports


def main():
    """The main function of the Tulipe CLI."""
    if os.getuid() != 0:
        warning_message = f"{Fore.yellow}{Style.italic}Warning: all the information may not be available without root privileges.{Style.reset}"
        print(warning_message, file=sys.stderr)
    cli = CLI()
    cli.parse()
    port_infos = ports.fetch(cli.type, cli.port, cli.service, cli.pid)
    ports.display(port_infos, cli.format, cli.status)


if __name__ == "__main__":
    main()
