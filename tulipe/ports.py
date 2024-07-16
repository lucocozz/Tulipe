import socket

import psutil
import json

from tulipe import docker_port as dport
from tulipe.PortInfo import PortInfo


@staticmethod
def get_connection_type(conn):
    """Get the connection type (TCP/UDP) of the connection."""
    return {"tcp"} if conn.type == socket.SOCK_STREAM else {"udp"}


@staticmethod
def get_service_name(pid, port, container_ports):
    """Get the name of the service that is using the port."""
    service_name = "Unknown"
    if pid:
        try:
            process = psutil.Process(pid)
            service_name = process.name()
            if service_name == "docker-proxy":
                service_name = (
                    f"docker-proxy:{container_ports.get(str(port), 'Unknown')}"
                )
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            print(f"Error: {e}")
    return service_name


def fetch(type_filter: str = "all"):
    """Get the ports information of the system."""
    docker_ports = dport.fetch_active_ports(type_filter)
    connections = [conn for conn in psutil.net_connections() if conn.laddr]
    ports_info = {}

    for conn in connections:
        port = conn.laddr.port
        pid = conn.pid if conn.pid else "?"
        hash_key = f"{port}:{pid}"
        if hash_key not in ports_info:
            service_name = get_service_name(conn.pid, port, docker_ports)
            conn_type = get_connection_type(conn)
            ports_info[hash_key] = PortInfo(port, conn_type, pid, service_name)
        else:
            ports_info[hash_key].conn_types.update(conn_type)

    return list(ports_info.values())




def display_table(port_infos: list[PortInfo], port_filter=None):
    """Print the ports information in a table format."""
    port_infos.sort(key=lambda x: x.port)
    print(f"{'Port':<8} {'Type':<8} {'PID':>8} {'Service':<20}")
    print("=" * 40)
    for port_info in port_infos:
        if not port_filter or port_info.port == port_filter:
            print(port_info.to_table())


def display_json(port_infos: list[PortInfo], port_filter=None):
    """Print the ports information in a JSON format."""
    ports = (port_info.to_dict() for port_info in port_infos if port_info.port == port_filter)
    print(json.dumps(list(ports), indent=4))


def display_csv(port_infos: list[PortInfo], port_filter=None):
    """Print the ports information in a CSV format."""
    for port_info in port_infos:
        if not port_filter or port_info.port == port_filter:
            print(port_info.to_csv())


def display(port_infos: list[PortInfo], port_filter=None, print_format="table"):
    """Print the ports information."""
    port_infos.sort(key=lambda x: x.port)
    if print_format == "json":
        display_json(port_infos, port_filter)
    elif print_format == "csv":
        display_csv(port_infos, port_filter)
    else:
        display_table(port_infos, port_filter)
