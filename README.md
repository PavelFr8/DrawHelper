# 🎨 DrawHelper — Your Handy Drawing Assistant by PavelFr8

![Static Badge](https://img.shields.io/badge/PyQt6-DrawHelper%20%F0%9F%96%8C-orange)

![DrawHelper Interface](src/drawhelper/imgs/img.png)

Hey there! Welcome to **DrawHelper** — a desktop app designed to help you sketch, annotate, and create visual notes with ease.

Built with pure PyQt6, DrawHelper is perfect for quick drawings, simple diagrams, or just unleashing your creativity =)

> 🖥️ **Platform:** Windows desktop app, easy to install and use.

---

## 🚀 Features

* ✏️ Multiple drawing tools: freehand pencil, straight line, circle, eraser
* 🌙 Dark-friendly interface
* ⚡ Customizable transparent background

---

## 📦 Installation & Running

### Requirements

* Windows 10 or newer
* Python 3.12+ (if running from source)
* PyQt6 (if running from source)

---

### Running from Source

1. Clone this repository:

   ```bash
   git clone https://github.com/PavelFr8/DrawHelper
   cd DrawHelper
   ```

2. Create and activate a virtual environment (recommended):

   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install .
   ```

4. Run the app:

   ```bash
   drawhelper
   ```

---

### Running from Installer (Windows)

1. Download the latest release from the [Releases page](https://github.com/PavelFr8/DrawHelper/releases)
2. Run the installer `.exe` file

---

## 🛠 Project Structure

```
├── src
│   └── drawhelper
│       ├── __init__.py
│       ├── __main__.py
│       ├── main.py
│       ├── core
│       │   ├── drawing_widget.py
│       │   ├── main_window.py
│       │   └── menu_widget.py
│       ├── imgs
│       └── utils
├── DrawHelper.spec
├── LICENSE
├── README.md
├── installer.iss
├── pyproject.toml
```

## 🤝 Contributing

* ⭐ Star this repo if you find it useful
* 🐞 Report bugs via Issues
* 🧑‍💻 Send Pull Requests with new features or fixes — contributions are welcome!

---

> 🎨 Thanks for checking out DrawHelper!
> Hope it makes your drawing tasks smoother and more enjoyable.
