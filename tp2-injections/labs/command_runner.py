import ipaddress
import re
import subprocess


HOSTNAME_RE = re.compile(r"^[a-zA-Z0-9.-]{1,253}$")


def is_allowed_host(host):
    if not isinstance(host, str):
        return False

    host = host.strip()

    forbidden = [";", "&", "|", "`", "$", "(", ")", "<", ">", "\n", "\r"]
    if any(char in host for char in forbidden):
        return False

    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        pass

    return bool(HOSTNAME_RE.fullmatch(host))


def ping_host(host):
    if not is_allowed_host(host):
        return "Invalid host"

    try:
        result = subprocess.run(
            ["ping", "-c", "1", host],
            capture_output=True,
            text=True,
            timeout=3,
            shell=False,
            check=False,
        )
        return result.stdout + result.stderr
    except FileNotFoundError:
        return f"ping unavailable for {host}"
    except subprocess.TimeoutExpired:
        return "ping timeout"
