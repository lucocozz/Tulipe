import docker


def fetch_active_ports() -> dict:
    """Get the ports of the running Docker containers."""
    client = docker.from_env()
    try:
        containers = client.containers.list(filters={"status": "running"})
        active_ports = {
            port.split('/')[0]: container.name
            for container in containers
            for port in container.attrs["NetworkSettings"]["Ports"]
        }
    except docker.errors.DockerException as e:
        print(f"Error: {e}")
        active_ports = {}
    return active_ports
