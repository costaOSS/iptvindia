# India Only IPTV

Automated India-only IPTV playlist that syncs from upstream sources.

## Playlist URLs

**Direct GitHub:**
```
https://raw.githubusercontent.com/costaOSS/iptvindia/main/combined_playlist.m3u
```

**GitHub Pages:**
```
https://costaoss.github.io/iptvindia/combined_playlist.m3u
```

## Features

- 869+ Indian channels
- Filters only Indian channels (removes Bangladeshi, Pakistani, Arabic, etc.)
- Combines streams from PiratesTV + iptv-org/iptv
- Auto-updates on the 1st of every month at 02:00 UTC via GitHub Actions

## Sources

- Primary: https://github.com/FunctionError/PiratesTv
- Additional: https://github.com/iptv-org/iptv (India streams)

## Automation

- Runs monthly on the 1st at 02:00 UTC via GitHub Actions
- Can be manually triggered via workflow_dispatch

## License

AGPL v3