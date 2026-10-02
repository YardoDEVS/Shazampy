# Changelog

## 1.1.2 — Donation browser focus fix

- Clicking the donation link now minimizes Shazampy before opening PayPal so the default browser receives the foreground view.
- Linux now opens donation links with the desktop default URL handler (`xdg-open`), with Python browser fallback.
- Windows now opens donation links with the system URL handler (`os.startfile`), with Python browser fallback.
- Shazampy restores its always-on-top behaviour when the user returns to the application.

## 1.1.1 — Installer clone-directory fix

- Running `install_shazampy.py` from a cloned repository no longer aborts merely because the platform source file already exists.
- An identical source file is kept; a different source file is preserved unless `--force` is explicitly requested.

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
