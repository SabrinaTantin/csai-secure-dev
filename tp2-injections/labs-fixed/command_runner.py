"""Lab command injection — version corrigée."""

import re
import subprocess

HOST_PATTERN = re.compile(r"^[\w.-]+$")


def ping_host(host: str) -> str:
    if not HOST_PATTERN.match(host):
        return "Invalid host"
    result = subprocess.run(
        ["ping", "-c", "1", host],
        shell=False,
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout or result.stderr
