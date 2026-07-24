"""Smoke tests — import + tool registration only.

These don't hit a real GemLogin server. End-to-end tests would need either
a running GemLogin or a respx-mocked client; both are out of scope for the
0.1.0 release.
"""
from __future__ import annotations

import gemlogin_mcp
from gemlogin_mcp import server


def test_version_exposed():
    assert gemlogin_mcp.__version__ == "0.3.0"


def test_mcp_instance_named_gemlogin():
    assert server.mcp.name == "gemlogin"


def test_defaults_overridable_via_env(monkeypatch):
    monkeypatch.setenv("GEMLOGIN_BASE", "http://example:9999")
    monkeypatch.setenv("GEMLOGIN_TIMEOUT", "5")
    import importlib

    importlib.reload(server)
    assert server.BASE == "http://example:9999"
    assert server.TIMEOUT == 5.0


def test_main_callable():
    assert callable(server.main)


def test_local_automation_tools_exposed():
    assert callable(server.gemlogin_find_script)
    assert callable(server.gemlogin_execute_local_script)
    assert callable(server.gemlogin_check_local_script_status)
    assert callable(server.gemlogin_kill_local_script)
