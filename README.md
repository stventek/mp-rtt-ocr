# MP-RTT-OCR

This is a multiplatform (MP) real-time translation (RRT) app that utilizes Optical Character Recognition (OCR). it aims to provide enough flexivity for a variety of use cases like playing visual novels games, reading a digital book, and more.

## Tested and working on

- Linux Mint 21.1
- Windows 11
- macOS 11 Big Sur

## Features

- **Static Frame Mode**: Use of a fixed frame for OCR detection.
- **Magic Window Mode**:  Perform OCR using a window that can be resized or hidden.
- **Translation Options**: Supports translation using Google Translate and DeepL, no need for an API key. The timeout can be configured as desired.
- **Real-time Translation**: Provides an auto mode for real-time translation, the OCR scan interval can be configured as desired.
- **Snapshot Translation**: Peform OCR with static frame or Magic window only once.
- **Debug mode**: View logs that provide real-time information about the app's current state, with customizable log level.

## Setup

- Python 3.9+ is requierd.  
- Tesseract needs to be installed.

Install dependencies

```bash pip install -r requirements.txt```

Start the app

```bash python main.py```