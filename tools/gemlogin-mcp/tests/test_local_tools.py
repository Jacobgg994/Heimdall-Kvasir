from __future__ import annotations

import importlib

import httpx
import pytest
import respx

from gemlogin_mcp import server


@pytest.fixture()
def reset_server(monkeypatch):
    monkeypatch.setenv("GEMLOGIN_BASE", "http://example:9999")
    monkeypatch.setenv("GEMLOGIN_TIMEOUT", "5")
    importlib.reload(server)
    server._client = None
    server._cloud_client = None
    yield
    server._client = None
    server._cloud_client = None


@pytest.mark.asyncio
@respx.mock
async def test_list_scripts_masks_sensitive_defaults(reset_server):
    respx.get("http://example:9999/api/scripts").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [
                    {
                        "id": "s1",
                        "name": "FB",
                        "parameters": [
                            {"name": "API", "label": "OpenAI API key", "defaultValue": "sk-123"},
                            {"name": "repeat", "label": "Repeat", "defaultValue": "10"},
                        ],
                    }
                ]
            },
        )
    )

    scripts = await server.gemlogin_list_scripts()
    assert scripts[0]["parameters"][0]["defaultValue"] == "***masked***"
    assert scripts[0]["parameters"][1]["defaultValue"] == "10"


@pytest.mark.asyncio
@respx.mock
async def test_find_script_prefers_thai_candidate(reset_server):
    respx.get("http://example:9999/api/scripts").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [
                    {"id": "en", "name": "Facebook 1", "parameters": []},
                    {"id": "th", "name": "(Faccebook) วอมบัญชี", "parameters": []},
                ]
            },
        )
    )

    matches = await server.gemlogin_find_script("(Facebok) วอร์บัญชี", top_k=2)
    assert matches[0]["id"] == "th"
    assert matches[1]["id"] == "en"


@pytest.mark.asyncio
@respx.mock
async def test_execute_local_script_retries_and_checks_status(reset_server):
    exec_route = respx.post("http://example:9999/api/scripts/execute/script-1").mock(
        side_effect=[
            httpx.Response(200, json={"success": False, "message": "try again"}),
            httpx.Response(200, json={"success": True, "id": "script-1"}),
        ]
    )
    status_route = respx.post("http://example:9999/api/scripts/check-status/script-1").mock(
        return_value=httpx.Response(200, json={"is_running": True, "message": "running"})
    )

    out = await server.gemlogin_execute_local_script(
        profile_id=[2],
        script_id="script-1",
        retries=2,
        retry_delay_seconds=0,
    )

    assert exec_route.call_count == 2
    assert status_route.call_count == 1
    assert out["success_count"] == 1
    assert out["running_count"] == 1
    assert out["results"][0]["attempts"] == 2
    assert out["results"][0]["execute_success"] is True


@pytest.mark.asyncio
@respx.mock
async def test_execute_local_script_resolve_by_name(reset_server):
    respx.get("http://example:9999/api/scripts").mock(
        return_value=httpx.Response(
            200,
            json={"data": [{"id": "abc", "name": "(Faccebook) วอมบัญชี", "parameters": []}]},
        )
    )
    respx.post("http://example:9999/api/scripts/execute/abc").mock(
        return_value=httpx.Response(200, json={"success": True, "id": "abc"})
    )
    respx.post("http://example:9999/api/scripts/check-status/abc").mock(
        return_value=httpx.Response(200, json={"is_running": True, "message": "running"})
    )

    out = await server.gemlogin_execute_local_script(
        profile_id=[2, 3],
        script_name="(Faccebook) วอมบัญชี",
        retries=1,
        retry_delay_seconds=0,
    )

    assert out["script_id"] == "abc"
    assert out["success_count"] == 2
    assert out["running_count"] == 2


@pytest.mark.asyncio
@respx.mock
async def test_execute_local_script_ambiguous_exact_name_raises(reset_server):
    respx.get("http://example:9999/api/scripts").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [
                    {"id": "a1", "name": "Same Name", "parameters": []},
                    {"id": "a2", "name": "Same Name", "parameters": []},
                ]
            },
        )
    )

    with pytest.raises(RuntimeError, match="ambiguous script_name exact match"):
        await server.gemlogin_execute_local_script(
            profile_id=[2],
            script_name="Same Name",
        )


@pytest.mark.asyncio
@respx.mock
async def test_execute_local_script_exact_name_toggle(reset_server):
    respx.get("http://example:9999/api/scripts").mock(
        return_value=httpx.Response(
            200,
            json={"data": [{"id": "abc", "name": "(Faccebook) วอมบัญชี", "parameters": []}]},
        )
    )

    with pytest.raises(RuntimeError, match="exact match not found"):
        await server.gemlogin_execute_local_script(
            profile_id=[2],
            script_name="(Facebok) วอร์บัญชี",
        )

    respx.post("http://example:9999/api/scripts/execute/abc").mock(
        return_value=httpx.Response(200, json={"success": True, "id": "abc"})
    )
    respx.post("http://example:9999/api/scripts/check-status/abc").mock(
        return_value=httpx.Response(200, json={"is_running": True, "message": "running"})
    )

    out = await server.gemlogin_execute_local_script(
        profile_id=[2],
        script_name="(Facebok) วอร์บัญชี",
        require_exact_script_name=False,
    )
    assert out["script_id"] == "abc"
    assert out["success_count"] == 1


@pytest.mark.asyncio
@respx.mock
async def test_check_and_kill_local_script(reset_server):
    status_route = respx.post("http://example:9999/api/scripts/check-status/script-1").mock(
        return_value=httpx.Response(200, json={"is_running": True})
    )
    kill_route = respx.post("http://example:9999/api/scripts/kill-execute/script-1").mock(
        return_value=httpx.Response(200, json={"success": True})
    )

    status = await server.gemlogin_check_local_script_status("script-1", 2)
    killed = await server.gemlogin_kill_local_script("script-1", 2)

    assert status["is_running"] is True
    assert killed["success"] is True
    assert status_route.called
    assert kill_route.called
