# Shazampy

**Shazampy** is a Linux desktop lyrics companion created by **Gerardo García Alfaro**.  
It continuously identifies the music being heard or played by the computer, retrieves synchronized lyrics, follows the current playback position, and displays a responsive seven-line lyric view with a live frequency-spectrum visualizer. Linux and Windows x64 builds are included.

> **License note:** Shazampy is source-available under **CC BY-NC 4.0**. You may share and modify it for non-commercial purposes with attribution. Because the license forbids commercial use, it is not an OSI-approved open-source software license.

## Features

- Continuous song recognition through SongRec/Shazam-compatible recognition.
- Physical microphone and PulseAudio/PipeWire monitor-source capture.
- Seven-line synchronized lyric display.
- Cluster/trajectory-based position tracking for songs with repeated sections.
- Per-song manual LRC timing correction.
- Responsive interface that reorganizes itself when resized or maximized.
- 48-bar logarithmic audio spectrum visualizer.
- Broad multilingual/Unicode lyric rendering through the Noto font family, including Japanese, Korean, Chinese, Arabic, Indic scripts and many more.
- Clickable ☕ PayPal.Me support line inside the application.
- Native Windows x64 build using WASAPI loopback capture.
- Interface languages: English, Spanish, Portuguese, French, Italian, German and Arabic.
- Optional Spotify/MPRIS debug reference through `playerctl`.

## Quick installation

Download this repository and run the cross-platform installer:

```bash
python3 install_shazampy.py
```

The installer detects the operating system automatically:

- **Linux:** installs `shazampy.py`, SongRec, FFmpeg/PulseAudio-compatible tooling and Noto fonts.
- **Windows x64:** installs `Shazampy_Win.py`, PyAudioWPatch/WASAPI dependencies, ShazamIO and a private Noto font collection.

Supported Linux installer families:

- Arch Linux / Manjaro / EndeavourOS
- Ubuntu / Debian family
- Fedora family

Windows targets:

- Windows 11 x64
- Windows 10 x64
- Windows 7 x64 compatibility profile using **Python 3.8.10 x64**

> Windows 7 and Python 3.8 are end-of-life and no longer receive normal security updates. The compatibility profile is provided for legacy systems, not as a recommendation to keep an unsupported OS online.

To see all installer options:

```bash
python3 install_shazampy.py --help
```


## Run

### Linux

```bash
./shazampy.py
```

or, if the convenience symlink was created:

```bash
./shazampy
```

### Windows

Double-click:

```text
run_shazampy.bat
```

or run:

```powershell
python Shazampy_Win.py
```


## Keyboard controls

| Key | Action |
|---|---|
| `F` | Cycle through available audio capture sources |
| `A` / `D` | Previous / next interface language |
| `W` or `→` | Lyrics timing +0.25 s |
| `S` or `←` | Lyrics timing -0.25 s |
| `↑` / `↓` | Lyrics timing ±1 s |
| `Space` | Restart the listening session from a fresh audio buffer |
| `Esc` | Close Shazampy |

## Documentation

Full documentation is included in [`docs/index.html`](docs/index.html).

Once GitHub Pages is enabled for the `/docs` folder, the documentation can be published as the project website.

## Support development

If Shazampy is useful to you, you can support its development:

☕ **PayPal.Me:** https://paypal.me/produccionesyardo

## Third-party projects and acknowledgements

Shazampy builds on or interoperates with several excellent projects:

- **SongRec** — created by **Marin** (`@marin-m`): https://github.com/marin-m/SongRec  
  Shazampy invokes SongRec as an external recognition tool.
- **LRCLIB** — created by **Trần Xuân Thắng** (`@tranxuanthang`): https://github.com/tranxuanthang/lrclib  
  Shazampy queries LRCLIB for synchronized lyrics.
- **Requests** — created by **Kenneth Reitz**, maintained by the Requests project: https://github.com/psf/requests
- **PipeWire** — created by **Wim Taymans**: https://pipewire.org/
- **Python** — created by **Guido van Rossum**, stewarded by the Python Software Foundation: https://www.python.org/
- **FFmpeg** — FFmpeg project: https://ffmpeg.org/
- **Playerctl** — altdesktop project: https://github.com/altdesktop/playerctl
- **Noto Emoji** — Google Fonts project: https://github.com/googlefonts/noto-emoji
- **ShazamIO** — created/maintained by **dotX12** and contributors: https://github.com/shazamio/ShazamIO
- **PyAudioWPatch** — maintained by **s0d3s**, adding WASAPI loopback support to PyAudio/PortAudio: https://github.com/s0d3s/PyAudioWPatch
- **PulseAudio** / `pactl` compatibility tooling: https://www.freedesktop.org/wiki/Software/PulseAudio/

See [`THIRD_PARTY.md`](THIRD_PARTY.md) for project links and licensing notes.

Shazampy is independent and is not affiliated with or endorsed by Shazam, Apple, Spotify, LRCLIB, SongRec, or the authors/organizations listed above.

## License

Copyright © 2026 **Gerardo García Alfaro**.

Shazampy is distributed under the **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)** license.

You may copy, redistribute, remix, transform and build upon Shazampy for **non-commercial purposes** provided that you:

1. Credit **Gerardo García Alfaro** as the original author.
2. Link to the CC BY-NC 4.0 license.
3. Indicate whether changes were made.
4. Do not use Shazampy or derivative works commercially without separate permission.

License: https://creativecommons.org/licenses/by-nc/4.0/

Suggested attribution:

```text
Shazampy — originally created by Gerardo García Alfaro
Licensed under CC BY-NC 4.0
https://creativecommons.org/licenses/by-nc/4.0/
Modified by: [your name / project], [describe changes if applicable]
```

Third-party software and services retain their own licenses and terms.
