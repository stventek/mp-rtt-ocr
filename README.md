# MP-RTT-OCR

This is a multiplatform (MP) real-time translation (RTT) app that utilizes Optical Character Recognition (OCR). it aims to provide enough flexibility for a variety of use cases like playing visual novels games, reading a digital book, and more.

## Tested and working on

- Linux Mint 21.1
- Windows 11
- macOS 11 Big Sur

## Features

- **Multi-display support**: Some apps of this kind does not have multi display support while this one does.
- **Static Frame mode**: Use of a fixed frame for OCR detection.
- **Magic Window mode**:  Perform OCR using a window that can be resized or hidden.
- **Translation Options**: Supports translation using Google Translate and DeepL, no need for an API key. The timeout can be configured as desired.
- **Real-time Translation**: Provides an auto mode for real-time translation, the OCR scan interval can be configured as desired.
- **Snapshot Translation**: Peform OCR with static frame or Magic window only once.
- **Debug mode**: View logs that provide real-time information about the app's current state. You can customize the log level.
- **Trained data of your choice (eng default)**: You can OCR using your desired trained data.

## Tesseract-ocr

tesseract-ocr is not bundled in the executables. Follow the appropriate installation instructions based on your operating system:

Windows:

```winget install tesseract-ocr```

MacOS:

```brew install tesseract```

Ubuntu (installed by default):

```sudo apt-get install tesseract-ocr```

## Standalone executables

You can find prebuilt executable files releases section for windows, mac and linux.

Note, deepl-cli package is not included in this release because of its size. If you want to use deepl-cli for translation, you can install it separately using the following command:

```pip install deepl-cli```

it does not required an API key but because it uses playwright it won't be near as fast as google translate.

## Setup

- Python 3.9+ is required.  
- Tesseract needs to be installed. (read above to learn how to install)

Install dependencies

```pip install -r requirements.txt```

Start the app

```python main.py```
