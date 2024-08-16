import argparse

from tulipe import __version__


class CLI:
    """The CLI class for Tulipe."""

    def __init__(self):
        """Initialize the CLI class."""
        self._parser = argparse.ArgumentParser(prog="tulipe")
        self._parser.add_argument(
            "-v", "--version", action="version", version=f"Tulipe v{__version__}"
        )
        self._parser.add_argument(
            "-t",
            "--type",
            type=str,
            choices=["tcp", "udp"],
            default="all",
            help="Filter by connection type",
        )
        self._parser.add_argument(
            "-p", "--port", type=int, help="Show information about a specific port"
        )
        self._parser.add_argument(
            "-P", "--pid", type=int, help="Show information about a specific process ID"
        )
        self._parser.add_argument(
            "-s",
            "--service",
            type=str,
            help="Show information about a specific service",
        )
        self._parser.add_argument(
            "-f",
            "--format",
            type=str,
            choices=["table", "json", "csv"],
            default="table",
            help="Output format",
        )
        self._parser.add_argument(
            "-S",
            "--status",
            action="store_true",
            help="Show the status of the port",
        )
        self.type: str
        self.format: str
        self.port: int | None
        self.service: str | None
        self.pid: int | None
        self.status: bool

    def parse(self):
        """Parse the command-line arguments."""
        args = self._parser.parse_args()
        self.type = args.type
        self.port = args.port
        self.format = args.format
        self.service = args.service
        self.pid = args.pid
        self.status = args.status
