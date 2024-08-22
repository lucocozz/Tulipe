import json


class PortInfo:
    """A class to represent the port information."""

    def __init__(self, port, protocol, ip_version, pid, service, status):
        self.port: int = port
        self.protocol: str = protocol
        self.ip_version: str = ip_version
        self.pid: int = pid
        self.service: str = service
        self.status: str = status

    def __repr__(self):
        return f"PortInfo(port={self.port}, protocol={self.protocol}{self.ip_version}, status={self.status}, pid={self.pid}, service={self.service})"

    def __eq__(self, other):
        return (
            self.port == other.port
            and self.protocol == other.protocol
            and self.ip_version == other.ip_version
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
            "IP_version": self.ip_version,
            "PID": self.pid,
            "Service": self.service,
            "Status": self.status,
        }

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)

    def to_csv(self):
        return f"{self.port},{self.protocol}{self.ip_version},{self.status},{self.pid},{self.service}"

    def to_table(self, has_status=False):
        pid = "-" if not self.pid else self.pid
        service = "-" if self.service == "unknown" else self.service
        protocol = self.protocol + ("6" if self.ip_version == "6" else "")

        entry = f"{self.port:>5} {protocol:<8}"
        if has_status:
            if not self.status:
                self.status = ""
            entry += f" {self.status:<15}"
        entry += f" {pid:>8} {service:<25}"
        return entry


    @classmethod
    def from_dict(cls, port_info):
        return cls(
            port_info["Port"],
            port_info["Protocol"],
            port_info["IP_version"],
            port_info["PID"],
            port_info["Service"],
            port_info["Status"],
        )
