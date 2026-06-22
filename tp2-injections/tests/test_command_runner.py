"""Tests TP2 — Lab command injection."""

from labs import command_runner


def test_ping_localhost():
    output = command_runner.ping_host("127.0.0.1")
    assert "127.0.0.1" in output or "1 packets transmitted" in output.lower()


def test_reject_shell_metacharacters():
    output = command_runner.ping_host("127.0.0.1; echo PWNED")
    assert "PWNED" not in output


def test_reject_command_substitution():
    output = command_runner.ping_host("$(echo PWNED)")
    assert "PWNED" not in output
