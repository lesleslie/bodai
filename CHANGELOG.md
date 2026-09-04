# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.1] - 2026-09-04

### CI/CD

- Remove GitHub Actions workflows (crackerjack handles CI/CD)

## [0.2.0] - 2026-08-31

### Added

- bodai: \_discover_apps + version/apps commands (Phase 5.2)
- bodai: Quarterly CLI staleness audit cron (Phase 7.5)
- bodai: Remove defensive try/except + add shell/dashboard tests (Phase 6.4-6.7)
- bodai: Umbrella CI + oneiric>=0.19.0 pin (Phase 4 / Task 4.3)
- bodai: Umbrella CI TUI/shell --help smoke (Phase 6.6)
- Umbrella CI bodai --help + version/apps smoke (Phase 5.4)

### Fixed

- Add .betterleaks.toml allowlist for cache + tooling paths
- Bodai comprehensive hook failures (ruff, ty, refurb, link-checker)
- portmap: Add Prefect/Crow/Session-Buddy-WS; correct Druva→Dhara
- portmap: Add WebSocket push channels + Bifrost LLM gateway
- shell: Ty ignore-comment syntax; drop misleading .betterleaksignore

### Documentation

- Link bodai-plugins marketplace from umbrella README
- readme: Add About the Bodai Ecosystem section
- readme: Bump Python badge from 3.13+ to 3.14+
- readme: Remove FastBlocks/SplashStand/MDInject from public documentation

### Internal

- bodai: Bump tool-config pins from 3.13 to 3.14
- Bump oneiric dep to >=0.16.0
- Bump requires-python to >=3.14
- gitignore: Add backup file patterns to silence checkpoint tool artifacts
- Re-pin python to 3.14
- Remove FastBlocks/SplashStand/MDInject from public configs and docs
- Untrack and delete 1 historical *.backup/*.bak files

## [0.1.2] - 2026-04-15

### Added

- Add FastBlocks, SplashStand, MDInject to ecosystem
- Add global LLM model registry for ecosystem
- Add missing MCP servers to ecosystem config
- Add new MCP integration servers to config
- Implement EcosystemOperations for cross-repo coordination

### Changed

- Bodai (quality: 60/100) - 2026-04-13 07:36:35
- Bodai (quality: 64/100) - 2026-02-24 15:34:09
- Bodai (quality: 64/100) - 2026-02-25 01:19:20
- Gitignore local config, add example templates
- Rename Dhruva to Druva across ecosystem

### Documentation

- Add Unofficial prefix to MCP server descriptions, add spline-mcp

### Internal

- Add .claude/ to gitignore
- Add archive/backup directories to gitignore
- repo: Ignore coverage artifacts
- Update .gitignore and remove tracked cache files
- Update LICENSE copyright to 2026, standardize license field
