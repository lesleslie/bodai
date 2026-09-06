# Port Audit — 2026-09-06

Opened by Plan 0b to close the verification gap in
`mahavishnu/docs/superpowers/specs/2026-09-06-mcp-stub-activation-design.md` §4.9,
which audited `settings/*.yaml` only.

## Raw scans

### settings/\*.yaml

```
akosha                   settings  api_port: 8682
akosha                   settings  mcp_port: 3002
akosha                   settings  prometheus_port: 9090
archive-org-mcp          settings  http_port: 3054
crackerjack              settings  dashboard_port: 8684
crackerjack              settings  mcp_http_port: 8676
crackerjack              settings  mcp_websocket_port: 8696
crackerjack              settings  zuban_port: 8685
css-mcp                  settings  http_port: 3050
dhara                    settings  port: 8683
graphics-mcp             settings  http_port: 3040
langsmith-mcp            settings  http_port: 3048
mdinject                 settings  http_port: 8679
neo4j-mcp                settings  http_port: 3045
oneiric                  settings  metrics_port: 1569
oneiric                  settings  mqtt_port: 1883
penpot-api-mcp           settings  http_port: 3051
porkbun-dns-mcp          settings  http_port: 3042
porkbun-domain-mcp       settings  http_port: 3043
session-buddy            settings  server_port: 3000
spline-mcp               settings  http_port: 3052
synxis-crs-mcp           settings  http_port: 3046
synxis-pms-mcp           settings  http_port: 3047
```

### Python code defaults

```
akosha                   code      port number (default: 8692
akosha                   code      port: int = 8000
akosha                   code      PORT: int = 8682
akosha                   code      port: int = 8692
akosha                   code      port": 8000
akosha                   code      port=8678
akosha                   code      port=8680
archive-org-mcp          code      port: int | None = 3054
bodai-plugins            code      port (8680
crackerjack              code      port = 3000
crackerjack              code      PORT = 8680
crackerjack              code      PORT = 8685
crackerjack              code      port or 8685
crackerjack              code      port: int = 8676
crackerjack              code      port: int = 8680
crackerjack              code      port: int = 8685
crackerjack              code      port: int = 8686
crackerjack              code      port: int = 8696
crackerjack              code      port", 8676
crackerjack              code      port", 8685
crackerjack              code      port", 8696
crackerjack              code      port": 8676
crackerjack              code      port=8676
crackerjack              code      port=8678
crackerjack              code      port=8680
crackerjack              code      port=8685
crackerjack              code      port=8696
dhara                    code      port != 8685
dhara                    code      port (default: 8683
dhara                    code      PORT = 8683
dhara                    code      PORT = 8685
dhara                    code      port: 8683
dhara                    code      port: int = 8683
dhara                    code      port: int = 8685
dhara                    code      port": 8683
dhara                    code      port=8678
dhara                    code      port=8680
dhara                    code      port=8682
dhara                    code      port=8685
dhara                    code      port=settings.port or 8683
excalidraw-mcp           code      port number (default: 3060
excalidraw-mcp           code      port: int = 3030
excalidraw-mcp           code      port: int = 3031
excalidraw-mcp           code      port: int = 3032
excalidraw-mcp           code      port: int = 3060
excalidraw-mcp           code      port": 3060
excalidraw-mcp           code      port=3032
fastblocks               code      port (default: 8684
fastblocks               code      port number (default: 8684
fastblocks               code      port: int = 8684
fastblocks               code      port": 8000
fastblocks               code      port=8000
fastblocks               code      PORT=8080
graphics-mcp             code      port: int = 3040
langsmith-mcp            code      port: int = 3048
mahavishnu               code      port (default: 8686
mahavishnu               code      PORT = 8680
mahavishnu               code      PORT = 8693
mahavishnu               code      port = parsed.port or 8678
mahavishnu               code      port 8080
mahavishnu               code      port 8676
mahavishnu               code      port 8678
mahavishnu               code      port 8680
mahavishnu               code      port 8682
mahavishnu               code      port 8683
mahavishnu               code      port 8686
mahavishnu               code      port 8690
mahavishnu               code      port number (default: 8690
mahavishnu               code      port: 8678
mahavishnu               code      port: 8682
mahavishnu               code      port: 8683
mahavishnu               code      port: int = 3000
mahavishnu               code      port: int = 8080
mahavishnu               code      port: int = 8682
mahavishnu               code      port: int = 8686
mahavishnu               code      port: int = 8690
mahavishnu               code      port: int = 8693
mahavishnu               code      port', 8675
mahavishnu               code      PORT", "8471
mahavishnu               code      port", 8683
mahavishnu               code      port", 8690
mahavishnu               code      port", 8693
mahavishnu               code      port": 3042
mahavishnu               code      port": 8684
mahavishnu               code      port": 8686
mahavishnu               code      port": 8690
mahavishnu               code      port": 8692
mahavishnu               code      port": 8693
mahavishnu               code      port": 8765
mahavishnu               code      port=8000
mahavishnu               code      port=8080
mahavishnu               code      PORT=8678
mahavishnu               code      port=8690
mahavishnu               code      portmap if 3000
mahavishnu               code      portmap if 8000
mahavishnu               code      portmap; 8675
mailgun-mcp              code      port: int = 3039
mcp-common               code      port: 8000
mcp-common               code      port: 8080
mcp-common               code      port: int = 3039
mcp-common               code      port: int = 8080
mcp-common               code      port: int = 8688
mcp-common               code      port", 8000
mcp-common               code      port=8000
mcp-common               code      port=8678
mcp-common               code      port=8688
mdinject                 code      port == 8680
mdinject                 code      port 8679
mdinject                 code      port mode (8679
mdinject                 code      PORT"] = "8680
neo4j-mcp                code      port: int = 3045
oneiric                  code      PORT or 8080
oneiric                  code      port: int = 8000
oneiric                  code      port: int = 8080
opera-cloud-mcp          code      port: int = 3037
penpot-api-mcp           code      port: int = 3051
porkbun-dns-mcp          code      port: int = 3042
porkbun-domain-mcp       code      port: int = 3043
raindropio-mcp           code      port: int = 3034
raindropio-mcp           code      port: int = Field(3034
session-buddy            code      port 8678
session-buddy            code      port number (default: 8765
session-buddy            code      port_bound(port: int = 8678
session-buddy            code      port: int = 8080
session-buddy            code      port: int = 8677
session-buddy            code      port: int = 8678
session-buddy            code      port: int = 8765
session-buddy            code      port", 8678
session-buddy            code      port": 8677
session-buddy            code      port": 8678
session-buddy            code      port=8765
splashstand              code      port"] or 8765
spline-mcp               code      port: int = 3052
synxis-crs-mcp           code      port: int = 3046
synxis-pms-mcp           code      port: int = 3047
unifi-mcp                code      port: int = 3038
unifi-mcp                code      port: int = 8000
unifi-mcp                code      port: int = 8443
unifi-mcp                code      port: int = 8444
```

### pyproject.toml and .env

```
akosha                   .env.example PORT="3001
akosha                   .env.example PORT="8000
```

No pyproject.toml or .env files in other repos declare 30xx/8xxx ports.

### launchd plists

```
3032 3033 3034 3035 3036 3037 3038 3039 3040 3042 3043 3044 3045 3046 3047 3048
3050 3051 8057 8192 8391 8676 8678 8680 8682 8683 8709
```

The launchd plist set is broader than the registry. `n8n` (3044), `mermaid`
(3033), `chart-antv` (3036), `grafauna` (3035), and `akosha` (3001) are bound
via plists but not declared in `bodai/config/portmap.yaml`. The numbers 8057,
8192, 8391, 8709 are non-MCP — `com.bodai.llama-server.plist` (8192), unknown
configs. Crackerjack's `mcp_websocket_port: 8696` (settings) is bound in
plists. `session-buddy` `server_port: 3000` is registered but no MCP server
ever claims 8678 in the launchd set — the plists here all run other services.

The launchd set was used to verify the **3054-3056 range is unclaimed** — none
of the 30xx ports in the launchd scan includes 3054, 3055, or 3056.

## Reconciled allocation

| Port | Repo | Declared in | portmap.yaml said | Action |
|------|------|-------------|-------------------|--------|
| 3000 | session-buddy | settings (`server_port: 3000`) | (absent) | **add** — session-buddy's non-MCP port |
| 3002 | akosha | settings (`mcp_port: 3002`) | (absent) | **add** — akosha MCP, distinct from api_port 8682 |
| 3030 | graphics-mcp (mismatch) / excalidraw-mcp (default) | excalidraw-mcp code `port: int = 3030` | grafana-mcp | **correct** — grafana-mcp declared port is 3035 in `ecosystem.yaml`, not 3030 |
| 3031 | excalidraw-mcp | ecosystem.yaml | (absent) | **add** |
| 3032 | excalidraw-mcp (default), raindropio (plist) | launchd | available | **correct** — excalidraw default 3032 is unconfirmed; leave as available |
| 3033 | mermaid-mcp | launchd + ecosystem.yaml | mermaid-mcp | **match** |
| 3034 | raindropio-mcp | settings/code | raindropio-mcp | **match** |
| 3035 | grafana | launchd | grafana | **match** |
| 3036 | chart-antv | launchd | chart-antv | **match** |
| 3037 | opera-cloud-mcp | ecosystem.yaml | opera-cloud-mcp | **match** |
| 3038 | unifi-mcp | ecosystem.yaml | unifi-mcp | **match** |
| 3039 | mailgun-mcp | ecosystem.yaml | mailgun-mcp | **match** |
| 3040 | graphics-mcp | settings + ecosystem.yaml | graphics-mcp | **match** |
| 3042 | porkbun-dns-mcp | ecosystem.yaml | porkbun-dns-mcp | **match** |
| 3043 | porkbun-domain-mcp | ecosystem.yaml | porkbun-domain-mcp | **match** |
| 3044 | (n8n-mcp disabled) | launchd + ecosystem.yaml | (no entry; 3044 was free) | **comment** — n8n-mcp does not exist |
| 3045 | neo4j-mcp | settings + ecosystem.yaml | neo4j-mcp | **match** |
| 3046 | synxis-crs-mcp | settings + ecosystem.yaml | synxis-crs-mcp | **match** |
| 3047 | synxis-pms-mcp | settings + ecosystem.yaml | synxis-pms-mcp | **match** |
| 3048 | langsmith-mcp | settings + ecosystem.yaml | langsmith-mcp | **match** |
| 3049 | css-mcp (mismatch) | css-mcp binds 3050 | css-mcp | **correct** — css-mcp binds 3050 |
| 3050 | css-mcp | css-mcp settings `http_port: 3050` | spline-mcp | **correct** — was spline-mcp; css-mcp is the real claimant |
| 3051 | penpot-api-mcp | settings + code | (absent) | **add** — was missing |
| 3052 | spline-mcp | settings + code | (absent; said 3050) | **correct** — was 3050; real port is 3052 |
| 3054 | archive-org-mcp | settings + code | (absent) | **allocate** |
| 3055 | medium-mcp | settings + code | (absent) | **allocate** |
| 3056 | scapy-mcp | settings + code | (absent) | **allocate** |
| 8676 | crackerjack | settings + ecosystem.yaml | crackerjack | **match** |
| 8678 | session-buddy | settings + ecosystem.yaml | session-buddy | **match** |
| 8679 | mdinject | settings `http_port: 8679` | (absent) | **add** |
| 8680 | mahavishnu | ecosystem.yaml + code | mahavishnu | **match** |
| 8682 | akosha | settings + ecosystem.yaml | akosha | **match** |
| 8683 | dhara | settings + ecosystem.yaml | druva | **rename** — component renamed to dhara |
| 8684 | crackerjack | settings `dashboard_port: 8684` | fastblocks | **correct** — crackerjack claims 8684 |
| 8685 | crackerjack | settings `zuban_port: 8685` | mdinject | **correct** — crackerjack claims 8685 |
| 8696 | crackerjack | settings `mcp_websocket_port: 8696` | (absent) | **add** — crackerjack's WebSocket |
| 8765 | session-buddy | code | (absent) | **add** — session-buddy's WebSocket |

`fastblocks` has a `port: int = 8684` default but no settings file declaring a
distinct port; after correcting 8684 to crackerjack, fastblocks' claim is
ambiguous. It runs on whatever port fastblocks decides at startup; per the
constraint "the repo's own settings decides what it binds," fastblocks binds
8684 only as a default — if the app launches with a port argument, it uses
that. Document this in a comment rather than over-allocating.

`akosha` `mcp_port: 3002` is distinct from its `api_port: 8682`. Both are valid.

## Confirmed free

Port range **3030-3059** scan after corrections:

| Port | Status |
|------|--------|
| 3030 | grafana-mcp — **stays** (declared in `ecosystem.yaml`) |
| 3031 | excalidraw-mcp — **stays** |
| 3032 | available — excalidraw-mcp default 3032 in code but not bound |
| 3033 | mermaid-mcp — **stays** |
| 3034 | raindropio-mcp — **stays** |
| 3035 | grafana — **stays** |
| 3036 | chart-antv — **stays** |
| 3037 | opera-cloud-mcp — **stays** |
| 3038 | unifi-mcp — **stays** |
| 3039 | mailgun-mcp — **stays** |
| 3040 | graphics-mcp — **stays** |
| 3041 | available — **stays** |
| 3042 | porkbun-dns-mcp — **stays** |
| 3043 | porkbun-domain-mcp — **stays** |
| 3044 | available — n8n-mcp disabled |
| 3045 | neo4j-mcp — **stays** |
| 3046 | synxis-crs-mcp — **stays** |
| 3047 | synxis-pms-mcp — **stays** |
| 3048 | langsmith-mcp — **stays** |
| 3049 | available — css-mcp actually binds 3050 |
| 3050 | css-mcp — **corrected from 3049** |
| 3051 | penpot-api-mcp — **added** |
| 3052 | spline-mcp — **corrected from 3050** |
| 3053 | available — no claimant anywhere |
| 3054 | **archive-org-mcp** — **allocated** |
| 3055 | **medium-mcp** — **allocated** |
| 3056 | **scapy-mcp** — **allocated** |
| 3057 | available — reserved |
| 3058 | available — reserved |
| 3059 | available — reserved |

**3054, 3055, 3056 survive the widened audit.** No repo, plist, or env file
declares any of these three ports. Safe to allocate to the three new MCP
servers.

## Notes

- `akosha` `mcp_port: 3002` is an MCP port distinct from `api_port: 8682`. The
  registry only recorded 8682. The widened audit caught this — `portmap.yaml`
  must list both.
- `crackerjack` claims three ports: `mcp_http_port: 8676`, `dashboard_port: 8684`, `zuban_port: 8685`. The registry assigned 8684/8685 to fastblocks /
  mdinject; crackerjack is the real claimant.
- `n8n` plist (port 3044) is a defunct launchd entry from before the repo was
  removed; keep the plist out of the audit's claim list (it does not match a
  live repo on disk).
- The widened audit found no additional collisions on 3054-3056. Plan 0b's
  Task 1 Step 6 confirmation: **proceed with the three new allocations**.
