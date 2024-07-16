import json

class PortInfo:
	"""A class to represent the port information."""

	def __init__(self, port, conn_types, pid, service_name):
		self.port = port
		self.conn_types = set(conn_types) if isinstance(conn_types, (list, set)) else {conn_types}
		self.pid = pid
		self.service_name = service_name

	def __repr__(self):
		conn_types_str = "/".join(sorted(self.conn_types))
		return f"PortInfo(port={self.port}, conn_types={conn_types_str}, pid={self.pid}, service_name={self.service_name})"

	def __eq__(self, other):
		return (
			self.port == other.port
			and self.conn_types == other.conn_types
			and self.pid == other.pid
			and self.service_name == other.service_name
		)

	def __ne__(self, other):
		return not self.__eq__(other)

	def to_dict(self):
		return {
			"Port": self.port,
			"Types": list(self.conn_types),
			"PID": self.pid,
			"Service": self.service_name,
		}

	def to_json(self):
		return json.dumps(self.to_dict(), indent=4)

	def to_csv(self):
		types_str = "/".join(sorted(self.conn_types))
		return f"{self.port},{types_str},{self.pid},{self.service_name}"

	def to_table(self):
		types_str = "/".join(sorted(self.conn_types))
		return f"{self.port:<8} {types_str:<8} {self.pid:>8} {self.service_name:<20}"

	@classmethod
	def from_dict(cls, port_info):
		return cls(
			port_info["Port"], port_info.get("Types", port_info.get("Type")), port_info["PID"], port_info["Service"]
		)