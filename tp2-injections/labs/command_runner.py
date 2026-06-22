"""Lab command injection — version vulnérable."""

import subprocess


def ping_host(host: str) -> str:
    command = f"ping -c 1 {host}"
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout or result.stderr
