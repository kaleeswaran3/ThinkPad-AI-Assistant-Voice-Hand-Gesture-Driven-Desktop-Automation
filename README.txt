# Quick Access Guide - Ctrl+T Hotkey

## ✅ Desktop Shortcut Created!

A desktop shortcut has been created with **Ctrl+T** as the keyboard shortcut.

### 🎯 How to Use:

1. **Press Ctrl+T from anywhere** - Launches the voice assistant instantly!
2. **Double-click the desktop icon** - "ThinkPad Voice Assistant"
3. **Pin to taskbar** - Right-click the shortcut → Pin to taskbar

### ⌨️ Keyboard Shortcut Details:

- **Hotkey:** Ctrl+T
- **Works:** System-wide (from any application)
- **Action:** Launches the voice assistant silently (no terminal window)

### 📍 Shortcut Location:

The shortcut is on your desktop (OneDrive Desktop folder).

### 💡 Pro Tip:

The Ctrl+T hotkey only works when the shortcut is on your desktop. If you move or delete the desktop shortcut, the hotkey will stop working. You can still pin it to the taskbar for quick access, but keep the original on the desktop for the Ctrl+T functionality!

---

**You're all set!** Press **Ctrl+T** anytime to launch your voice assistant! 🚀

ThinkPad Voice Assistant
========================

What's included:
- gui_assistant.py  -> Main program (Tkinter GUI + wake word + features)
- assistant_launcher.py -> Simple launcher to double-click
- requirements.txt

Features implemented:
- Wake word "hey assistant" (auto-starts on launch, listens continuously)
- Hand gesture control for tab switching (auto-starts, swipe left/right to switch tabs)
- GUI dashboard with mic animation, quick buttons, and AI chat area
- AI integration placeholder using GEMINI_API_KEY environment variable
- Auto-start on boot by creating a .bat in the current user's Startup folder
- Pre-filled ThinkPad T14 common app paths (edit APPS dictionary if needed)
- Volume/brightness/wifi/bluetooth controls (best-effort via PowerShell/netsh)
- Play selected music file
- Open websites (YouTube, Netflix, Amazon) and common apps
- Mouse/keyboard automation via pyautogui
- Chrome browser search with full omnibox functionality

========================
QUICK START
========================

When you launch the app, both voice and gesture controls start automatically!

You'll see in the console:
  Auto-starting features...
  ✓ Wake word detection started (say 'hey assistant')
  ✓ Gesture control started (swipe left/right to switch tabs)

Status will show: "Ready (Voice + Gestures active)"

Now you can:
- Say "hey assistant" followed by a command (e.g., "hey assistant, open chrome")
- Swipe your hand left/right in front of the camera to switch tabs
- Type commands in the text box and click "Send"
- Click "Mic (listen once)" to speak a single command

========================
AVAILABLE COMMANDS
========================

You can use these commands in three ways:
1. Voice: Say "hey assistant" then the command
2. Type: Enter the command in the text box and click "Send"
3. Mic button: Click "Mic (listen once)" and speak the command
4. Gestures: Swipe hand left/right to switch tabs (works automatically)

--- WEB & SEARCH ---
search [query]              - Search using Chrome browser with full search features
                              Examples:
                              • "search Python tutorials"
                              • "search weather today"
                              • "search how to install Python"
                              • "search best laptops 2024"
                              • "search news"
chrome search [query]       - Same as above, explicitly uses Chrome
                              Examples:
                              • "chrome search machine learning"
                              • "chrome search restaurants near me"

Common search shortcuts:
- Just say the topic after "search" - no need for extra words
- Chrome will show suggestions, history, and bookmarks
- Search works with any phrase or question

Quick website access:
open youtube               - Open YouTube website
open netflix               - Open Netflix website
open amazon                - Open Amazon website

--- OPEN APPLICATIONS ---
open chrome                - Open Google Chrome browser
open brave                 - Open Brave browser
open vscode                - Open Visual Studio Code
open notepad               - Open Notepad
open calculator            - Open Calculator
open file explorer         - Open File Explorer
open whatsapp              - Open WhatsApp desktop app
open lenovo vantage        - Open Lenovo Vantage
open spotify               - Open Spotify
open vlc                   - Open VLC Media Player
open zoom                  - Open Zoom

--- SYSTEM CONTROLS ---
volume up                  - Increase system volume
volume down                - Decrease system volume
mute                       - Toggle mute/unmute
brightness [0-100]         - Set screen brightness (e.g., "brightness 60")
wifi on                    - Turn on Wi-Fi
wifi off                   - Turn off Wi-Fi
turn on wifi               - Turn on Wi-Fi (alternative)
turn off wifi              - Turn off Wi-Fi (alternative)
bluetooth on               - Turn on Bluetooth
bluetooth off              - Turn off Bluetooth

--- MEDIA ---
play music                 - Play selected music file (select file first using GUI button)
play song                  - Same as above

--- MOUSE & KEYBOARD AUTOMATION ---
move mouse [x] [y]         - Move mouse to coordinates (e.g., "move mouse 100 200")
click                      - Click the mouse (left button)
type [text]                - Type text (e.g., "type hello world")

--- AI ASSISTANT ---
ai [question]              - Ask AI a question (e.g., "ai what is Python?")
                            Requires GEMINI_API_KEY environment variable

--- HAND GESTURE CONTROL ---
Hand gesture control starts automatically when you launch the app!

Gestures available:
   - Swipe RIGHT (move hand from left to right) - Switch to next tab (Ctrl+Tab)
   - Swipe LEFT (move hand from right to left) - Switch to previous tab (Ctrl+Shift+Tab)

Tips for best results:
- Keep your hand clearly visible to the camera
- Make deliberate swipe motions (not too fast or slow)
- Wait ~1 second between gestures (cooldown period)
- Works with any application that supports Ctrl+Tab (browsers, editors, etc.)
- You'll see "→ Next tab" or "← Previous tab" in the console when gestures are detected

Note: If you don't have a webcam or it's in use, gesture control will fail silently
      and voice/text commands will still work normally.

--- UTILITIES ---
time                       - Get current time



========================

Important notes:
- Some system features (brightness, bluetooth toggles) may require administrator rights.
- Gemini API: Replace the placeholder URL in gui_assistant.py with the actual Gemini endpoint and make sure you set GEMINI_API_KEY.
  Example (PowerShell): $env:GEMINI_API_KEY = "your_key_here"
- To create an auto-start entry, run the GUI and click "Auto-start on boot".
- Edit the APPS dictionary to correct paths on your machine if something doesn't open.

How to run:

EASY LAUNCH OPTIONS (No Terminal Required!):
--------------------------------------------
1. SIMPLEST: Double-click "run_assistant.bat"
   - Shows a terminal window with status
   - Automatically uses virtual environment if available

2. SILENT: Double-click "run_assistant_silent.vbs"
   - No terminal window, completely silent
   - Recommended for daily use!

3. DESKTOP SHORTCUT: Double-click "create_desktop_shortcut.bat"
   - Creates a desktop shortcut for easy access
   - Can be pinned to taskbar or Start Menu

4. STANDALONE EXE: Double-click "build_exe.bat"
   - Creates a portable .exe file (no Python needed)
   - Takes 2-5 minutes to build
   - Find result in: dist\ThinkPad_Voice_Assistant.exe

See LAUNCH_INSTRUCTIONS.md for detailed guide!

TRADITIONAL METHOD (For Development):
--------------------------------------
1. Create a Python virtual environment and install requirements:
   python -m venv .venv
   .venv\\Scripts\\activate
   pip install -r requirements.txt

2. Run the launcher:
   python assistant_launcher.py
   OR
   python gui_assistant.py

Security & privacy:
- This assistant runs locally and sends audio/text to the Gemini API only if you use the AI feature.
- Make sure you trust any third-party APIs you connect to.

If you'd like, I can:
- Replace the Gemini placeholder with a tested OpenAI/Gemini client (but I'll need your confirmation and an API key).
- Add a Windows Service installer or an installer .exe
- Tighten permissions and add error logging
**********************************************************************************************




# ThinkPad Voice Assistant - Easy Launch Guide

I've created several easy ways to run your voice assistant without using the terminal!

## 🚀 Quick Start Options

### Option 1: Double-Click Batch File (Simplest)
**File:** `run_assistant.bat`

Simply **double-click** this file to start the assistant. It will:
- Automatically detect and use your virtual environment
- Fall back to system Python if no venv is found
- Show a window with status messages

### Option 2: Silent Launch (No Terminal Window)
**File:** `run_assistant_silent.vbs`

**Double-click** this file for a completely silent launch:
- No terminal window appears
- Runs completely in the background
- Only the GUI window shows up
- **Recommended for daily use!**

### Option 3: Desktop Shortcut
**File:** `create_desktop_shortcut.bat`

1. **Double-click** `create_desktop_shortcut.bat`
2. A shortcut will appear on your desktop
3. Double-click the desktop shortcut anytime to launch
4. You can also:
   - Pin it to your taskbar (right-click → Pin to taskbar)
   - Pin it to Start Menu
   - Move it anywhere you want

### Option 4: Standalone Executable (Advanced)
**File:** `build_exe.bat`

Create a standalone `.exe` file that works without Python:

1. **Double-click** `build_exe.bat`
2. Wait for the build to complete (2-5 minutes)
3. Find your executable at: `dist\ThinkPad_Voice_Assistant.exe`
4. Copy this `.exe` anywhere and run it!

**Benefits:**
- No Python installation needed
- Share with others easily
- Single file, portable
- Professional deployment

**Note:** First time will install PyInstaller if needed.

## 📌 Recommended Setup

For the best experience:

1. **Create desktop shortcut:**
   - Double-click `create_desktop_shortcut.bat`
   
2. **Pin to taskbar:**
   - Right-click the desktop shortcut
   - Select "Pin to taskbar"
   
3. **Now you can:**
   - Click taskbar icon to launch instantly
   - No terminal, no hassle!

## 🔧 Troubleshooting

### "Python not found" error
- Make sure Python is installed and in your PATH
- Or activate your virtual environment first:
  ```
  .venv\Scripts\activate
  ```

### Virtual environment not detected
- The scripts will automatically use system Python as fallback
- Or create a venv: `python -m venv .venv`

### Executable build fails
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Install PyInstaller: `pip install pyinstaller`
- Run `build_exe.bat` again

## 💡 Tips

- **For daily use:** Use the desktop shortcut or VBS file
- **For sharing:** Build the executable
- **For development:** Use the batch file to see error messages
- **For auto-start:** Use the "Auto-start on boot" button in the GUI

## 📝 What Changed?

All your original files are untouched! I only added these launcher files:
- ✅ `run_assistant.bat` - Simple batch launcher
- ✅ `run_assistant_silent.vbs` - Silent background launcher
- ✅ `create_desktop_shortcut.bat` - Shortcut creator
- ✅ `build_exe.bat` - Executable builder
- ✅ This instruction file

Your `gui_assistant.py` and all other files remain exactly the same!
**********************************************************************************************



DEBUG

# Debugging Hand Gesture Control

## Steps to Debug

1. **Stop the current application** if it's running (Ctrl+C in terminal)

2. **Restart the application:**
   ```
   py gui_assistant.py
   ```

3. **Click "Start Gestures" button** in the GUI

4. **Check the console/terminal output** for debug messages

## What to Look For

The console should show debug messages like:
```
DEBUG: start_gesture() called
DEBUG: Creating HandGestureThread...
DEBUG: HandGestureThread.__init__() called
DEBUG: Initializing MediaPipe...
DEBUG: MediaPipe initialized successfully
DEBUG: HandGestureThread initialized
DEBUG: Starting thread...
DEBUG: Thread started successfully
Hand gesture detection started. Show your hand to the camera.
```

## Common Issues & Solutions

### Issue 1: No debug messages at all
**Problem:** Button click not registered  
**Solution:** Check if the GUI loaded correctly, try clicking other buttons

### Issue 2: Error initializing MediaPipe
**Problem:** MediaPipe not installed or incompatible  
**Solution:** Run `py -m pip install --upgrade mediapipe`

### Issue 3: "Could not open camera"
**Problem:** Camera in use or no camera available  
**Solution:** 
- Close other apps using camera (Zoom, Teams, etc.)
- Check camera in Windows Settings > Privacy > Camera
- Try running: `py test_gesture_detection.py`

### Issue 4: No hand detected
**Problem:** Hand tracking not working  
**Solution:**
- Ensure good lighting
- Show your full hand to camera
- Move hand slowly left/right
- Check if camera light is on

## Quick Test

Run the test script to verify camera and MediaPipe:
```
py test_gesture_detection.py
```

This will show a window with your camera feed and hand landmarks if working correctly.
