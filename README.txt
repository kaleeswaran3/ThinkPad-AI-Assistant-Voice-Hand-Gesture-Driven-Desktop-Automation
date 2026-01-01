🤖 ThinkPad Voice Assistant
Voice • Hand Gesture • System Automation • AI Assistant

A desktop AI assistant built for ThinkPad laptops that supports voice commands, hand gesture control, system automation, and AI-powered Q&A — all running locally with optional cloud AI integration.

🚀 Key Highlights

🎙 Wake-word based voice assistant

✋ Hand gesture control for tab switching

🧠 AI chat integration (Gemini-ready)

⚡ Global Ctrl + T hotkey launch

🖥 GUI dashboard (Tkinter)

🔁 Auto-start on Windows boot

📦 Can be packaged as a standalone EXE

📁 Project Structure
ThinkPad-Voice-Assistant/
├─ gui_assistant.py          # Main GUI + logic
├─ assistant_launcher.py     # Lightweight launcher
├─ requirements.txt
├─ run_assistant.bat
├─ run_assistant_silent.vbs
├─ create_desktop_shortcut.bat
├─ build_exe.bat
├─ test_gesture_detection.py
└─ README.md

⌨️ Quick Access (Ctrl + T Hotkey)

A desktop shortcut is created with a global Ctrl + T keyboard shortcut.

How it works

Press Ctrl + T from anywhere → Assistant launches instantly

Works system-wide

Runs silently (no terminal window)

⚠️ Important:
Keep the shortcut on the Desktop.
Moving or deleting it will disable the hotkey.

🎯 Features Overview
🎙 Voice Control

Wake word: “hey assistant”

Continuous listening

One-time mic input option

✋ Hand Gesture Control (MediaPipe)

Swipe Right → Next tab (Ctrl + Tab)

Swipe Left → Previous tab (Ctrl + Shift + Tab)

Auto-starts with the app

Works with browsers, editors, and tab-based apps

🧠 AI Assistant

Command:

ai <your question>


Uses GEMINI_API_KEY (environment variable)

Easily extendable to OpenAI or other LLMs

🖥 System Automation

Volume, brightness, Wi-Fi, Bluetooth

Open apps & websites

Mouse & keyboard automation

Media playback

🧾 Supported Commands (Examples)
Web & Search
search python tutorials
open youtube
open amazon

Applications
open chrome
open vscode
open spotify
open zoom

System Controls
volume up
brightness 70
wifi off
bluetooth on

Automation
move mouse 300 200
click
type hello world

🧪 Hand Gesture Debugging

Run:

py test_gesture_detection.py


Tips for best results

Good lighting

Full hand visible

Slow, deliberate swipes

Wait ~1 second between gestures

▶️ How to Run
✅ Recommended (No Terminal)

Silent launch

run_assistant_silent.vbs


Desktop shortcut

create_desktop_shortcut.bat


Standalone EXE

build_exe.bat

🛠 Development Mode
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python gui_assistant.py

🔐 Security & Privacy

Runs locally on your system

Audio/text is sent to AI APIs only when AI commands are used

No background data collection

📌 Requirements

Windows 10/11

Python 3.9+

Webcam (for gesture control)

Microphone (for voice commands)

🌱 Future Enhancements

More gesture actions

Offline AI models

Windows Service installer

Plugin-based command system
