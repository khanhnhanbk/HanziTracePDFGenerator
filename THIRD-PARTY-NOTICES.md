# Third-party notices

HanziTracer's own code is under the MIT License (`LICENSE`). It bundles:

| Component | Licence | Notes |
|---|---|---|
| [LXGW WenKai](https://github.com/lxgw/LxgwWenKai) v1.530 (`src/statics/fonts/LXGWWenKai-Regular.ttf`) | SIL Open Font License 1.1 (`src/statics/fonts/OFL-LXGWWenKai.txt`) | Font for the Chinese characters |
| [Space Grotesk](https://github.com/floriankarsten/space-grotesk) (`src/statics/fonts/SpaceGrotesk.ttf`) | SIL Open Font License 1.1 (`src/statics/fonts/OFL-SpaceGrotesk.txt`) | Font for Pinyin |
| [PySide6 / Qt for Python](https://www.qt.io/qt-for-python) 6.11.1 | LGPL-3.0 ([text](https://www.gnu.org/licenses/lgpl-3.0.html)) | Used unmodified and dynamically linked. The Windows build is a one-folder build: the Qt/PySide6 libraries are separate files in `_internal/` and can be replaced with your own compatible build. Source: https://code.qt.io/cgit/pyside/pyside-setup.git/ |
| [reportlab](https://www.reportlab.com/) 4.5.1 | BSD-3-Clause | PDF output |
| [pypinyin](https://github.com/mozillazg/python-pinyin) 0.55.0 | MIT | Pinyin |
| [Pillow](https://python-pillow.org/) 12.2.0 | MIT-CMU | |
| [PyInstaller](https://pyinstaller.org/) bootloader 6.20.0 | GPL-2.0 with bootloader exception | The exception allows distributing the built app under any licence |
