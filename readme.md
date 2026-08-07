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

- 595 Indian channels
- Filters only Indian channels (removes Bangladeshi, Pakistani, Arabic, etc.)
- Combines streams from iptv-org/iptv + Hindi/Punjabi community playlists
- Auto-updates on the 1st of every month at 02:00 UTC via GitHub Actions

## Sources

- iptv-org/iptv (India streams): https://github.com/iptv-org/iptv
- Hindi & Punjabi playlist: https://github.com/deep2772/Hindi_Punjabi-iptv-playlist
- Streams are HEAD/GET validated before inclusion

## Automation

- Runs monthly on the 1st at 02:00 UTC via GitHub Actions
- Can be manually triggered via workflow_dispatch

## License

AGPL v3