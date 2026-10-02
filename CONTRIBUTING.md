# Contributing to Shazampy

Thanks for your interest in improving Shazampy.

## License requirement

By submitting a contribution, you agree that your contribution may be distributed as part of Shazampy under the project's CC BY-NC 4.0 license.

Shazampy is intended for non-commercial use under that license.

## How to contribute

1. Fork the repository.
2. Create a branch for your change.
3. Keep changes focused and explain the reason for them.
4. Test the application on Linux.
5. Open a pull request describing what changed and how you tested it.

## Useful checks

```bash
python3 -m py_compile shazampy.py
python3 -m py_compile install_shazampy.py
```

For audio changes, please mention your Linux distribution, desktop/audio stack (for example PipeWire/PulseAudio), and the type of input tested (microphone, monitor source, USB, Bluetooth, HDMI, etc.).

## Attribution

Please retain the original attribution to Gerardo García Alfaro in redistributed or modified copies, as required by the project license.
