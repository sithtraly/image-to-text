# Image to Text App
This app was build using [Python](https://www.python.org/) and [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) using [pytesseract](https://pypi.org/project/pytesseract/) library, click [Here](https://docs.coro.net/featured/agent/install-tesseract-windows/) to download tesseract OCR.

# Install library
```bash
pip install -r requirement.txt
```

# Build into app
```bash
pyinstaller --onefile --windowed --name "Image to Text" --hidden-import=sip main.py
```