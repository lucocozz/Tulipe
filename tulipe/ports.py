import json
import socket

import psutil
from colored import Style

from tulipe.types.PortInfo import PortInfo
from tulipe import docker_port as dport


@staticmethod
def get_connection_type(conn_type, conn_family):
    """Get the connection type (TCP/UDP) of the connection."""
    conn = "tcp" if conn_type == socket.SOCK_STREAM else "udp"
    if conn_family == socket.AF_INET6:
        conn += "6"
    return conn


@staticmethod
def get_service(pid: int | None, port: int, container_ports: dict):
    """Get the name of the service that is using the port."""
    if pid is None:
        return "unknown"
    try:
        process = psutil.Process(pid)
        service = process.name()
        if service == "docker-proxy":
            service = f"docker:{container_ports.get(str(port), 'unknown')}"
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass
    return service


def fetch(
    type_filter: str = "all",
    port_filter: int | None = None,
    service_filter: str | None = None,
    pid_filter: int | None = None,
):
    """Get the ports information of the system."""
    docker_ports = dport.fetch_active_ports()
    connections = [conn for conn in psutil.net_connections() if conn.laddr]
    port_infos: dict[str, PortInfo] = {}

    for conn in connections:
        # conn_type = get_connection_type(conn.type, conn.family)
        conn_type = "tcp" if conn.type == socket.SOCK_STREAM else "udp"
        ip_version = "6" if conn.family == socket.AF_INET6 else "4"

        if type_filter != "all" and type_filter not in conn_type:
            continue
        port = conn.laddr.port
        if port_filter and port != port_filter:
            continue
        if pid_filter and conn.pid != pid_filter:
            continue
        service = get_service(conn.pid, port, docker_ports)
        if service_filter and service_filter not in service:
            continue

        hash_key = f"{port}:{conn_type}"
        if hash_key not in port_infos:
            status = conn.status if conn.status != "NONE" else None
            port_infos[hash_key] = PortInfo(port, conn_type, ip_version, conn.pid, service, status)

    return sorted(list(port_infos.values()), key=lambda x: x.port)



@staticmethod
def __get_header(status: bool) -> str:
    header = f"{'Port':>5} {'Protocol'}"
    if status:
        header += f" {'Status':<15}"
    header += f" {'PID':>8} {'Service':<25}"
    return header


@staticmethod
def display_table(port_infos: list[PortInfo], status: bool):
    """Print the ports information in a table format."""
    header = __get_header(status)
    delimiter_len = len(header)
    print(header)
    print("=" * delimiter_len)
    for port_info in port_infos:
        print(f"{Style.underline_color('black')}{port_info.to_table(has_status=status)}{Style.RESET}")
    print("=" * delimiter_len)


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
    status=False,
):
    """Print the ports information."""
    if print_format == "json":
        display_json(port_infos)
    elif print_format == "csv":
        display_csv(port_infos)
    else:
        display_table(port_infos, status)
