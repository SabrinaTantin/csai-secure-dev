"""Tests TP2 — Lab SQL."""

from labs import sql_search


def test_search_existing_user():
    results = sql_search.search_users("alice")
    assert len(results) == 1
    assert results[0]["username"] == "alice"


def test_search_unknown_user():
    results = sql_search.search_users("unknown-user-xyz")
    assert results == []


def test_sql_injection_returns_multiple_rows():
    payload = "' OR '1'='1"
    results = sql_search.search_users(payload)
    assert len(results) <= 1, "Injection SQL possible : tous les utilisateurs retournés"
