import os
import json
import socket

import psutil

from tulipe.PortInfo import PortInfo
from tulipe import docker_port as dport


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


def fetch(type_filter: str = "all", port_filter=None, service_filter=None):
    """Get the ports information of the system."""
    docker_ports = dport.fetch_active_ports()
    connections = [conn for conn in psutil.net_connections() if conn.laddr]
    ports_info = {}

    for conn in connections:

        conn_type = get_connection_type(conn)
        if type_filter != "all" and not conn_type.intersection({type_filter}):
            continue
        port = conn.laddr.port
        if port_filter and port != port_filter:
            continue
        service_name = get_service_name(conn.pid, port, docker_ports)
        if service_filter and service_filter not in service_name:
            continue
        pid = conn.pid if conn.pid else "?"

        hash_key = f"{port}:{pid}"
        if hash_key not in ports_info:
            ports_info[hash_key] = PortInfo(port, conn_type, pid, service_name)
        else:
            ports_info[hash_key].conn_types.update(conn_type)

    return list(ports_info.values())


@staticmethod
def display_table(port_infos: list[PortInfo]):
    """Print the ports information in a table format."""
    port_infos.sort(key=lambda x: x.port)
    print(f"{'Port':<8} {'Type':<8} {'PID':>8} {'Service':<20}")
    print("=" * 40)
    for port_info in port_infos:
        print(port_info.to_table())


@staticmethod
def display_json(port_infos: list[PortInfo]):
    """Print the ports information in a JSON format."""
    ports = [port_info.to_dict() for port_info in port_infos]
    print(json.dumps(ports if ports else None, indent=4))


@staticmethod
def display_csv(port_infos: list[PortInfo]):
    """Print the ports information in a CSV format."""
    for port_info in port_infos:
        print(port_info.to_csv())


def display(
    port_infos: list[PortInfo],
    print_format="table",
):
    """Print the ports information."""
    port_infos.sort(key=lambda x: x.port)
    if print_format == "json":
        display_json(port_infos)
    elif print_format == "csv":
        display_csv(port_infos)
    else:
        display_table(port_infos)
