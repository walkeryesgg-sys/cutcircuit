# Troubleshooting

## Decision table

| Symptom | Likely cause | Action |
|---|---|---|
| `Sign in to confirm you're not a bot` | Anonymous session rejected | Retry once with authorized `--cookies-from-browser` access. Ensure that browser can play the URL. |
| `429 Too Many Requests` | Exit IP rate-limited | Stop retries, change proxy node, verify a different public IP, then retry. |
| Extraction succeeds but every stream returns `403` | Stale extractor, JS challenge failure, or restricted exit IP | Upgrade yt-dlp on Python 3.10+, enable the official EJS component (the script does this), then change exit IP if needed. |
| `Only images are available` / `Requested format is not available` | JS challenge solver missing or stale | Use current yt-dlp with `--remote-components ejs:github`; ensure Deno or another supported JS runtime is installed. |
| SABR warning / formats missing URLs | YouTube delivery change | Upgrade yt-dlp; do not hard-code obsolete player clients. |
| Python 3.9 deprecation blocks upgrade | Old default environment | Locate Python 3.10+ and install yt-dlp there; execute the script with that interpreter or point `--yt-dlp` at its binary. |
| HTTPS EOF / TLS errors | Unstable proxy node | Retry a small number of times, then select a healthier node. |
| Video downloaded but no audio | Adaptive stream not merged | Install FFmpeg and resume the same command. |
| `.part`, `.f###`, or `.ytdl` remains | Interrupted transfer or merge | Resume the same URL/output. Preserve partial files. |
| Final file exists but cannot be verified | Missing/corrupt ffprobe data | Keep source fragments if present, retry merge, and do not report success. |

## Clash Verge node switching

Prefer the Clash UI. Select a node in the active manual/selector group, then verify the public IP through the mixed proxy port:

```bash
curl -s --max-time 15 --proxy http://127.0.0.1:PORT https://api.ipify.org
```

When GUI control is unavailable and the user explicitly authorizes local API control:

1. Inspect the running `verge-mihomo` command for its data directory and Unix control socket.
2. Read only `external-controller`, `secret`, `mixed-port`, and `mode` from the active config. Do not expose subscription credentials or node server details.
3. Query `/proxies` through the Unix socket and list selector names, current selections, and delay history.
4. PUT `{"name":"NODE"}` to `/proxies/SELECTOR`.
5. Verify the exit IP changed. If not, choose a different provider or region.

Switching a node affects the user's system connection. Announce it before mutation. Do not change subscriptions, routing rules, DNS, or global mode unless explicitly requested.

## Safe retry policy

- Retry transient network failures up to the configured limit.
- Do not loop over dozens of media formats after repeated identical 403 responses; stop and repair the environment.
- Use `--continue` and the same output template to resume.
- Keep playlist downloading opt-in to prevent accidental bulk downloads.
- Do not use cookies from a browser profile without explicit authorization.
