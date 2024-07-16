import argparse


class CLI:
    """The CLI class for Tulipe."""

    def __init__(self):
        """Initialize the CLI class."""
        self._parser = argparse.ArgumentParser()
        self._parser.add_argument(
            "--version", action="version", version="Tulipe v0.1"
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
            "-f",
            "--format",
            type=str,
            choices=["table", "json", "csv"],
            default="table",
            help="Output format",
        )
        self.type = None
        self.port = None
        self.format = None

    def parse(self):
        """Parse the command-line arguments."""
        args = self._parser.parse_args()
        self.type = args.type
        self.port = args.port
        self.format = args.format
