import psutil
import socket
import docker



def get_connection_type(conn):
    return "TCP" if conn.type == socket.SOCK_STREAM else "UDP"



def get_docker_container_ports():
    client = docker.from_env()
    container_ports = {}
    try:
        containers = client.containers.list()
        for container in containers:
            ports = container.attrs["NetworkSettings"]["Ports"]
            for port, _ in ports.items():
                container_ports[port.split('/')[0]] = container.name
    except docker.errors.DockerException as e:
        print(f"Error: {e}")
    return container_ports



def get_docker_container_name(port, container_ports):
    return container_ports.get(str(port), "Unknown")


def get_service_name(pid, port, container_ports):
    service_name = "Unknown"
    if pid:
        try:
            proc = psutil.Process(pid)
            service_name = proc.name()
            if service_name == "docker-proxy":
                service_name = f"docker-proxy:{get_docker_container_name(port, container_ports)}"
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            print(f"Error: {e}")
    return service_name



def add_or_update_port_info(ports_info, port, conn_type, pid, service_name):
    if port in ports_info:
        if ports_info[port]["Type"] != conn_type:
            ports_info[port]["Type"] = "TCP/UDP"
    else:
        ports_info[port] = {
            "Port": port,
            "Type": conn_type,
            "PID": pid if pid else "?",
            "Service": service_name
        }



def get_ports_info(container_ports):
    connections = [conn for conn in psutil.net_connections() if conn.laddr]
    ports_info = {}

    for conn in connections:
        if conn.laddr:
            port = conn.laddr.port
            conn_type = get_connection_type(conn)
            service_name = get_service_name(conn.pid, port, container_ports)
            add_or_update_port_info(ports_info, port, conn_type, conn.pid, service_name)

    return list(ports_info.values())



def print_ports_info(ports_info):
    print(f"{'Port':<8} {'Type':<8} {'PID':>8} {'Service':<20}")
    print("=" * 40)
    for info in sorted(ports_info, key=lambda x: x["Port"]):
        print(f"{info['Port']:<8} {info['Type']:<8} {info['PID']:>8} {info['Service']:<20}")



if __name__ == "__main__":
    container_ports = get_docker_container_ports()
    ports_info = get_ports_info(container_ports)
    print_ports_info(ports_info)
