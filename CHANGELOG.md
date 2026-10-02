# Changelog

## 1.1.1 — Installer clone-directory fix

- Fixed the installer aborting when run directly inside a cloned repository where `shazampy.py` or `Shazampy_Win.py` already exists.
- Identical source files are now kept and installation continues normally.
- Different existing files are preserved unless `--force` is explicitly requested.

## 1.1.0 — Multilingual + Windows release

- Added clickable PayPal.Me support line in every interface language.
- Added Noto-based multilingual font selection for Unicode lyrics.
- Added Windows x64 version: `Shazampy_Win.py`.
- Added Windows microphone and speaker-output capture through PyAudioWPatch/WASAPI.
- Added Windows recognition through ShazamIO.
- Added Windows 7 x64 compatibility profile for Python 3.8.10 with pinned dependencies.
- Cross-platform installer now automatically selects Linux or Windows build.
- Installer adds broad Noto font coverage.

## 1.0.0 — Initial public release

- Continuous song recognition.
- Physical-input and output-monitor source selection.
- Seven-line synchronized lyric display.
- Cluster/trajectory-based position tracking for repeated song sections.
- Per-song LRC offset persistence.
- Responsive layout.
- Seven UI languages.
- Live 48-bar frequency spectrum visualizer.
- Self-contained Linux installer.
