# OpenMusic
![License](https://img.shields.io/github/license/Frankanator8/openmusic)
![Version](https://img.shields.io/github/v/release/Frankanator8/openmusic)

Open source music player for Mac and Windows* with plugin and full OS support. Built with Python and Qt (PySide6).

---

## Features
- Native OS support (i.e. os playback control) on Mac and Windows*
- Support for both Python plugins and QSS stylesheets
- Everything you need in a music player (song library, playlists, random music shuffle)
- oh and open source

---
## Installation
You can find prebuilt binaries/applications in [Releases](https://github.com/Frankanator8/openmusic/releases).

### To install from source
Prerequisities:

- Python >= 3.10

1. Clone the repository
```bash
git clone https://github.com/Frankanator8/openmusic.git
cd openmusic
```
2. Create a virtual environment and install dependencies.

macOS:
```bash
python3 -m venv .venv/
. .venv/bin/activate
pip3 install PySide6 Pillow moviepy pyobjc openmusic_api
```

Windows:
```bash
py -m venv .venv/
.venv\Scripts\activate
pip install PySide6 Pillow moviepy pywin32 winrt openmusic_api
```

3. Run
```bash
python3 main.py
```

---
# Contributing/Plugins
We welcome anyone to contribute to OpenMusic, whether it be a plugin or a pull request to this repo.

## Contributions
Please see [CONTRIBUTING.md](https://github.com/Frankanator8/openmusic/blob/main/CONTRIBUTING.md)

## Plugins
Please see the [wiki](https://github.com/Frankanator8/openmusic/wiki)


\*Windows support added but not fully tested