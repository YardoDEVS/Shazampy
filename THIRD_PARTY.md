# Third-party projects and acknowledgements

Shazampy is an independent project. The projects below keep their own
copyright, licenses, trademarks and terms. Shazampy may invoke them, import
them, use packages supplied by the host operating system, or communicate with
their services at runtime.

## SongRec

- Project: SongRec
- Creator: Marin (`@marin-m`)
- Project: https://github.com/marin-m/SongRec
- Role in Shazampy: Linux song recognition / Shazam-compatible matching
- Upstream license: GNU GPL v3

## LRCLIB

- Project: LRCLIB
- Creator: Trần Xuân Thắng (`@tranxuanthang`)
- Project: https://github.com/tranxuanthang/lrclib
- Service: https://lrclib.net/
- Role in Shazampy: synchronized-lyrics lookup
- Upstream server-code license: MIT

The LRCLIB software license covers LRCLIB's code. Lyrics returned by a lyrics
service may be subject to separate rights belonging to songwriters, publishers,
labels, or other rights holders. Shazampy does not claim ownership of
third-party lyrics.

## ShazamIO

- Project: ShazamIO
- Author/maintainer: dotX12 and contributors
- Project: https://github.com/shazamio/ShazamIO
- Role in Shazampy: Windows song recognition
- Upstream license: MIT
- Windows 7 compatibility profile pins ShazamIO 0.6.0 and shazamio-core 1.0.7
  because later releases dropped Python 3.8 support.

## PyAudioWPatch

- Project: PyAudioWPatch
- Maintainer: s0d3s
- Project: https://github.com/s0d3s/PyAudioWPatch
- Role in Shazampy: Windows WASAPI microphone and speaker-loopback capture
- Upstream license: MIT
- It is a PyAudio/PortAudio fork with WASAPI loopback support.

## Requests

- Project: Requests — Python HTTP for Humans
- Creator: Kenneth Reitz
- Project: https://github.com/psf/requests
- Documentation: https://requests.readthedocs.io/
- Role in Shazampy: HTTP requests
- Upstream license: Apache License 2.0

## PipeWire

- Project: PipeWire
- Creator: Wim Taymans
- Project: https://pipewire.org/
- Role in Shazampy: Linux audio graph / PulseAudio-compatible monitor routing
- License: see upstream project

## PulseAudio / pactl

- Project: PulseAudio
- Project: https://www.freedesktop.org/wiki/Software/PulseAudio/
- Role in Shazampy: Linux source discovery through `pactl`
- License: see upstream project

## FFmpeg

- Project: FFmpeg
- Project: https://ffmpeg.org/
- Role in Shazampy: Linux continuous audio capture and PCM conversion
- License: FFmpeg builds may be LGPL or GPL depending on build configuration
- Legal information: https://ffmpeg.org/legal.html

## Playerctl

- Project: Playerctl
- Organization/repository: altdesktop
- Project: https://github.com/altdesktop/playerctl
- Role in Shazampy: optional Linux MPRIS/Spotify position diagnostics
- Upstream license: GNU Lesser General Public License

## Python

- Project: Python
- Creator: Guido van Rossum
- Steward: Python Software Foundation
- Project: https://www.python.org/
- Role in Shazampy: application runtime and standard library, including Tkinter
- License: Python Software Foundation License

## Noto fonts

- Project: Noto
- Organization: Google / Noto Fonts contributors
- Project: https://notofonts.github.io/
- CJK project: https://github.com/notofonts/noto-cjk
- Emoji project: https://github.com/googlefonts/noto-emoji
- Role in Shazampy: broad multilingual glyph and emoji coverage
- Font license: SIL Open Font License 1.1

## Trademarks and external services

Shazam, Apple, Spotify and other product names are trademarks of their
respective owners. Shazampy is not affiliated with, endorsed by, or sponsored
by those companies or by the third-party projects listed above.

Availability and terms of external recognition, metadata and lyrics services
may change independently of Shazampy.
