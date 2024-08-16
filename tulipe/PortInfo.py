import json


class PortInfo:
    """A class to represent the port information."""

    def __init__(self, port, protocol, pid, service, status):
        self.port = port
        self.protocol = protocol
        self.pid = pid
        self.service = service
        self.status = status

    def __repr__(self):
        return f"PortInfo(port={self.port}, protocol={self.protocol}, status={self.status}, pid={self.pid}, service={self.service})"

    def __eq__(self, other):
        return (
            self.port == other.port
            and self.protocol == other.protocol
            and self.pid == other.pid
            and self.service == other.service
            and self.status == other.status
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def to_dict(self):
        return {
            "Port": self.port,
            "Protocol": self.protocol,
            "PID": self.pid,
            "Service": self.service,
            "Status": self.status,
        }

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)

    def to_csv(self):
        return f"{self.port},{self.protocol},{self.status},{self.pid},{self.service}"

    def to_table(self, has_status=False):
        if self.status == "NONE":
            self.status = ""
        entry = f"{self.port:>5} {self.protocol:<6}"
        if has_status:
            entry += f" {self.status:<15}"
        entry += f" {self.pid:>8} {self.service:<25}"
        return entry

    @classmethod
    def from_dict(cls, port_info):
        return cls(
            port_info["Port"],
            port_info["Protocol"],
            port_info["PID"],
            port_info["Service"],
            port_info["Status"],
        )
