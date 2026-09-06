# Unregistered Repositories — Register or Exclude

Opened by Plan 0b Task 8. Four directories under `~/Projects` appear in no
manifest: neither `mahavishnu/settings/ecosystem.yaml`,
`bodai/config/ecosystem.yaml`, nor `bodai/config/portmap.yaml`.

## Per-repo facts

### flowscape

- Contents: `.gitignore`, `.python-version`, `dist`, `LICENSE`, `pyproject.toml`, `README.md`, `src/`
- pyproject: `name = "flowscape"`
- git: no
- README: "A 3D landscape of your network flows."
- **Decision: exclude** — design-spec only (`docs/superpowers/specs/2026-08-31-flowscape-design.md`).
  No server, no MCP entry, no start_command. Registering would imply a routable
  component that does not exist.

### bodai-plugins

- Contents: `.claude/`, `.claude-plugin/`, `.git/`, `.gitignore`, `.pytest_cache/`, `.superpowers/`, `.venv/`, `bodai_plugins/`, `CHANGELOG.md`, `dist/`
- pyproject: `name = "bodai-plugins"`
- git: yes
- README: "Marketplace scaffolding CLI for the [Bodai ecosystem] Claude Code plugins."
- **Decision: exclude** — CLI helper consumed by path; not an MCP server. It
  scaffolds plugin manifests rather than serving any ecosystem traffic. Adding
  it would mean inventing a non-existent port.

### peanutbutterpub

- Contents: `.envrc`, `.git/`, `.gitignore`, `.idea/`, `.pdm-python/`, `.python-version/`, `.venv/`, `classicday_pbpub_mail.yml`, `create_routes.py`, `pyproject.toml`
- pyproject: `name = "peanutbutterpub"`
- git: yes
- README: none
- **Decision: exclude** — unrelated project (mail routes for a specific
  customer). Has no MCP server, no start_command, and no relationship to the
  Bodai control plane.

### mdinject-pypi-placeholder

- Contents: `.gitignore`, `.python-version`, `dist/`, `LICENSE/`, `pyproject.toml`, `README.md`, `src/`
- pyproject: `name = "mdinject"`
- git: no
- README: "This is a PyPI name-reservation placeholder. It does not contain the [real implementation]."
- **Decision: exclude** — placeholder repo for PyPI name reservation. The real
  mdinject lives at `~/Projects/mdinject` (already registered). Registering
  this would be a duplicate.

## Guidance applied

- **Register** if the repo is an active component the ecosystem should route to
  or sweep.
- **Exclude** if it is a name-reservation placeholder, a plugin bundle consumed
  by path rather than routed to, or an unrelated project. Placeholders in
  particular should stay unregistered — registering one implies a component
  that does not exist, which is the `n8n-mcp` failure mode in reverse.

Note: `flowscape` has a design spec and implementation plan in Mahavishnu
(`docs/superpowers/specs/2026-08-31-flowscape-design.md`) but is pre-implementation.
Registering a component with no server yet would make it appear routable.

## Summary

| Repo | Decision |
|------|----------|
| `flowscape` | exclude — design-spec only, no server |
| `bodai-plugins` | exclude — CLI helper, not an MCP server |
| `peanutbutterpub` | exclude — unrelated customer project |
| `mdinject-pypi-placeholder` | exclude — PyPI name placeholder (real mdinject is registered) |

No `components:` entries are added or modified.
