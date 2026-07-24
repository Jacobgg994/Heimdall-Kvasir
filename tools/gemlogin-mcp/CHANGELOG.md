# Changelog

All notable changes to `gemlogin-mcp` are documented here.

## [0.3.0] — 2026-05-18

### Added
- `gemlogin_cloud_execscript` now accepts a list of profile ids
  (`profile_id=["3","4","7"]`) for fan-out to multiple profiles in a single
  cloud trigger.
- New tool args: `parameter` (dict — passed through to the workflow) and
  `close_browser` (bool — auto-close after run).

### Verified
- soft_id="1" is the value the cloud accepts (any string passes early
  validation; the dispatch routing keys off device_id).

## [0.2.0] — 2026-05-18

### Added
- `gemlogin_cloud_execscript` tool — fires the GemLogin cloud webhook
  `POST app.gemlogin.io/api/v2/execscript` so an MCP client can trigger a
  workflow on a remote/cloud-managed device.
- Configurable via `GEMLOGIN_CLOUD_BASE`, `GEMLOGIN_CLOUD_DEVICE_ID`,
  `GEMLOGIN_CLOUD_SOFT_ID`, `GEMLOGIN_CLOUD_TOKEN`.
- Required body contract: `device_id`, `profile_id`, `workflow_id`,
  `soft_id`, `token`. Auth is the body `token` field (not Bearer).
- Rate limit observed: 300 req/min (cloud-side).

### Changed
- README split tool table into Local / Cloud sections.

## [0.1.0] — 2026-05-18

### Added
- Initial release.
- 8 tools: `gemlogin_status`, `gemlogin_list_profiles`, `gemlogin_get_profile`,
  `gemlogin_start_profile`, `gemlogin_stop_profile`, `gemlogin_list_groups`,
  `gemlogin_list_scripts`, `gemlogin_browser_versions`.
- 3 resources: `gemlogin://status`, `gemlogin://profiles`, `gemlogin://profile/{id}`.
- 2 prompts: `warm_profile`, `post_to_group`.
- Configurable via `GEMLOGIN_BASE` and `GEMLOGIN_TIMEOUT` env vars.
- `gemlogin-mcp` console script entry point.
