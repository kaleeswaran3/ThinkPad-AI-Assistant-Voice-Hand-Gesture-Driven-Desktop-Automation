

import os
import threading
import time
import subprocess
import webbrowser
import datetime
import json
import platform
import sys

import speech_recognition as sr
import pyttsx3

# GUI imports
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# automation
import pyautogui

# networking for AI
import requests

# hand gesture detection
import cv2
import mediapipe as mp
import numpy as np

# --- Configuration ----------------------------------------------------------
WAKE_WORD = "hey assistant"
GEMINI_API_KEY_ENV = "GEMINI_API_KEY"

# Default apps (common paths). Update these to match your machine if needed.
APPS = {
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "brave": r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
    "vscode": r"C:\Users\\{user}\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "file explorer": r"C:\Windows\explorer.exe",
    "whatsapp": r"C:\Users\\{user}\AppData\Local\WhatsApp\WhatsApp.exe",
    "lenovo vantage": r"C:\Program Files\LENOVO\Vantage\LenovoVantage.exe",
    "spotify": r"C:\Users\\{user}\AppData\Roaming\Spotify\Spotify.exe",
    "vlc": r"C:\Program Files\VideoLAN\VLC\vlc.exe",
    "zoom": r"C:\Users\\{user}\AppData\Roaming\Zoom\bin\Zoom.exe",
}

# fill {user} with current username
APPS = {k: v.format(user=os.getlogin()) for k, v in APPS.items()}

# --- Voice engine -----------------------------------------------------------
engine = pyttsx3.init()
engine.setProperty("rate", 160)

def speak(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print("TTS error:", e)

# --- AI (Gemini) integration - placeholder ----------------------------------
def call_gemini(prompt, max_tokens=400):
    """
    Placeholder Gemini API call.
    Set environment variable GEMINI_API_KEY with your key.
    This function expects a hypothetical REST endpoint; you should update
    the URL/headers to match the Gemini API you are using.
    """
    key = os.environ.get(GEMINI_API_KEY_ENV)
    if not key:
        return "Gemini API key not configured. Set the GEMINI_API_KEY environment variable."

    url = "https://api.gemini.example/v1/generate"  # <- replace with real Gemini endpoint
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    payload = {"prompt": prompt, "max_tokens": max_tokens}
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        # Expected structure depends on API — adjust as necessary
        if "text" in data:
            return data["text"]
        # Try common patterns
        if "choices" in data and len(data["choices"])>0 and "text" in data["choices"][0]:
            return data["choices"][0]["text"]
        return json.dumps(data)
    except Exception as e:
        return f"AI request failed: {e}"

# --- System controls --------------------------------------------------------
def volume_up():
    """Simulate media key for volume up on Windows."""
    if platform.system() != "Windows":
        return
    import ctypes
    VK_VOLUME_UP = 0xAF
    ctypes.windll.user32.keybd_event(VK_VOLUME_UP, 0, 0, 0)

def volume_down():
    if platform.system() != "Windows":
        return
    import ctypes
    VK_VOLUME_DOWN = 0xAE
    ctypes.windll.user32.keybd_event(VK_VOLUME_DOWN, 0, 0, 0)

def mute_volume():
    if platform.system() != "Windows":
        return
    import ctypes
    VK_VOLUME_MUTE = 0xAD
    ctypes.windll.user32.keybd_event(VK_VOLUME_MUTE, 0, 0, 0)

def set_brightness(level):
    """
    Set screen brightness (0-100) using PowerShell. May require admin rights.
    """
    try:
        level = max(0, min(100, int(level)))
        ps = f'(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{level})'
        subprocess.run(["powershell", "-Command", ps], check=False)
    except Exception as e:
        print("Brightness error:", e)

def toggle_wifi(enable: bool):
    """
    Toggle Wi-Fi interface using netsh. Interface name usually 'Wi-Fi'.
    """
    state = "enabled" if enable else "disabled"
    try:
        subprocess.run(["netsh", "interface", "set", "interface", "name=\"Wi-Fi\"", f"admin={state}"], shell=True)
    except Exception as e:
        print("Wi-Fi toggle error:", e)

def toggle_bluetooth(enable: bool):
    """
    Try to toggle Bluetooth using PowerShell (may require admin).
    This is a best-effort approach and may not work on some systems.
    """
    try:
        if enable:
            cmd = 'Get-PnpDevice -Class Bluetooth | Enable-PnpDevice -Confirm:$false'
        else:
            cmd = 'Get-PnpDevice -Class Bluetooth | Disable-PnpDevice -Confirm:$false'
        subprocess.run(["powershell", "-Command", cmd], check=False)
    except Exception as e:
        print("Bluetooth toggle error:", e)

# --- App / file open --------------------------------------------------------
def chrome_search(query):
    """
    Open Chrome browser with a search query.
    This uses Chrome's omnibox which provides full search functionality
    including Google search, suggestions, history, and bookmarks.
    """
    chrome_path = APPS.get("chrome")
    if not chrome_path or not os.path.exists(chrome_path):
        # Fallback to default browser
        webbrowser.open(f"https://www.google.com/search?q={query}")
        speak(f"Searching for {query}")
        return
    
    try:
        # Open Chrome with search query - Chrome will use its omnibox
        search_url = f"https://www.google.com/search?q={query}"
        subprocess.Popen([chrome_path, search_url], shell=False)
        speak(f"Searching Chrome for {query}")
    except Exception as e:
        print("Chrome search error:", e)
        # Fallback to default browser
        webbrowser.open(f"https://www.google.com/search?q={query}")
        speak(f"Searching for {query}")

def open_app(name):
    name = name.lower().strip()
    # direct website
    sites = {"youtube":"https://youtube.com","netflix":"https://netflix.com","amazon":"https://amazon.com"}
    if name in sites:
        webbrowser.open(sites[name])
        speak(f"Opening {name}")
        return

    if name in APPS:
        path = APPS[name]
        try:
            if os.path.isdir(path):
                os.startfile(path)
            else:
                subprocess.Popen([path], shell=False)
            speak(f"Opening {name}")
            return
        except Exception as e:
            print("Open app error:", e)
            speak(f"Couldn't open {name}, trying a search.")
    # fallback - try Windows search for program
    try:
        subprocess.Popen(["cmd", "/c", f"start {name}"], shell=True)
        speak(f"Attempting to open {name}")
    except Exception as e:
        speak(f"Failed to open {name}: {e}")

# --- Mouse & Keyboard automation --------------------------------------------
def move_mouse(x, y):
    pyautogui.moveTo(x, y)

def click_mouse(button="left"):
    pyautogui.click(button=button)

def type_text(text):
    pyautogui.write(text, interval=0.02)

def press_key(key):
    pyautogui.press(key)

# --- Voice listening --------------------------------------------------------
recognizer = sr.Recognizer()
mic = None

def init_mic():
    global mic
    try:
        mic = sr.Microphone()
    except Exception as e:
        print("Microphone init error:", e)

def listen_once(timeout=4, phrase_time_limit=4):
    """
    Listen briefly and return the recognized text (lowercase).
    """
    if mic is None:
        try:
            init_mic()
        except:
                ""
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.6)
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            text = recognizer.recognize_google(audio, language="en-in")
            return text.lower()
        except sr.WaitTimeoutError:
            return ""
        except Exception as e:
            # print("Listen error:", e)
            return ""

# --- Wake word thread -------------------------------------------------------
class WakeWordThread(threading.Thread):
    def __init__(self, callback, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.callback = callback
        self.running = True
        self.daemon = True

    def run(self):
        while self.running:
            try:
                phrase = listen_once(timeout=3, phrase_time_limit=3)
                if WAKE_WORD in phrase:
                    print("Wake word detected.")
                    self.callback()
            except Exception as e:
                print("Wake thread error:", e)
            time.sleep(0.2)

    def stop(self):
        self.running = False

# --- Hand Gesture Thread ---------------------------------------------------
# --- Hand Gesture Thread ---------------------------------------------------
from gesture_controller import GestureController

class HandGestureThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.running = True
        self.daemon = True
        self.controller = None

    def run(self):
        try:
            self.controller = GestureController()
        except Exception as e:
            print(f"Failed to init gesture controller: {e}")
            return

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("⚠ Could not open camera for gesture detection")
            return
        
        print("Gesture Camera Started. Press 'Esc' to stop debug view if visible.")
        
        while self.running:
            try:
                ret, frame = cap.read()
                if not ret:
                    continue
                
                # Process frame using our robust controller
                # This returns the annotated frame and the gesture name
                processed_frame, gesture_name = self.controller.process_frame(frame)
                
                # Optional: Show debug window
                # We can make this optional later, but for now it's requested "Visual landmarks overlay"
                cv2.imshow("Gesture Control - Debug View", processed_frame)
                
                # Check for window close or ESC
                if cv2.waitKey(1) & 0xFF == 27:
                    break
                    
                # Small delay to reduce CPU usage (limit to ~30fps)
                time.sleep(0.01)
                
            except Exception as e:
                print(f"Gesture loop error: {e}")
                time.sleep(1)
        
        # Cleanup
        cap.release()
        cv2.destroyAllWindows()
        if self.controller:
            self.controller.release()
    
    def stop(self):
        self.running = False

# --- GUI --------------------------------------------------------------------
class AssistantGUI:
    def __init__(self, root):
        self.root = root
        root.title("ThinkPad Voice Assistant")
        root.geometry("520x380")
        root.resizable(False, False)

        self.mic_active = False
        self.wake_thread = None
        self.gesture_thread = None

        # top frame - status only
        top = ttk.Frame(root, padding=12)
        top.pack(fill="x")

        self.status_var = tk.StringVar(value="Status: Starting...")
        ttk.Label(top, textvariable=self.status_var, font=("Arial", 10, "bold")).pack()

        # mic canvas for animation
        self.canvas = tk.Canvas(root, width=120, height=120)
        self.canvas.pack(pady=10)
        self.oval = self.canvas.create_oval(20,20,100,100, outline="#333", width=3)
        self.animating = False

        # command entry
        cmd_frame = ttk.Frame(root, padding=8)
        cmd_frame.pack(fill="x")
        ttk.Label(cmd_frame, text="Type a command or press Mic:").pack(anchor="w")
        self.cmd_entry = ttk.Entry(cmd_frame)
        self.cmd_entry.pack(fill="x", pady=6)
        btns = ttk.Frame(cmd_frame)
        btns.pack(fill="x")
        ttk.Button(btns, text="Send", command=self.send_typed).pack(side="left")
        ttk.Button(btns, text="Mic (listen once)", command=self.listen_and_handle).pack(side="left", padx=6)

        # quick actions
        qa = ttk.Frame(root, padding=8)
        qa.pack(fill="x")
        ttk.Label(qa, text="Quick Actions:").pack(anchor="w")
        quick = ttk.Frame(qa)
        quick.pack(fill="x")
        ttk.Button(quick, text="Open Chrome", command=lambda: open_app("chrome")).pack(side="left", padx=4, pady=4)
        ttk.Button(quick, text="Open VSCode", command=lambda: open_app("vscode")).pack(side="left", padx=4)
        ttk.Button(quick, text="Open Downloads", command=lambda: open_app("downloads")).pack(side="left", padx=4)
        ttk.Button(quick, text="YouTube", command=lambda: open_app("youtube")).pack(side="left", padx=4)

        # AI chat area
        ai_frame = ttk.LabelFrame(root, text="AI / Assistant")
        ai_frame.pack(fill="both", expand=True, padx=8, pady=8)
        self.ai_text = tk.Text(ai_frame, height=6)
        self.ai_text.pack(fill="both", expand=True)

        # footer
        footer = ttk.Frame(root)
        footer.pack(fill="x", pady=4)
        ttk.Button(footer, text="Auto-start on boot", command=self.enable_autostart).pack(side="left", padx=6)
        ttk.Button(footer, text="Select Music File", command=self.select_music).pack(side="left")
        ttk.Button(footer, text="Exit", command=self._exit).pack(side="right", padx=6)

        # animation loop
        self.pulse = 0
        self._animate()
        
        # Auto-start wake word and gesture control
        self.root.after(1000, self.auto_start_features)

    def _animate(self):
        # simple pulsing animation
        self.pulse = (self.pulse + 1) % 40
        delta = 8 + abs(20 - self.pulse)
        self.canvas.coords(self.oval, 20 - delta/4, 20 - delta/4, 100 + delta/4, 100 + delta/4)
        self.root.after(120, self._animate)

    def auto_start_features(self):
        """Auto-start wake word and gesture control on app launch"""
        print("Auto-starting features...")
        
        # Start wake word detection
        try:
            self.wake_thread = WakeWordThread(self.on_wake)
            self.wake_thread.start()
            print("✓ Wake word detection started (say 'hey assistant')")
        except Exception as e:
            print(f"⚠ Wake word failed to start: {e}")
        
        # Start gesture control
        try:
            self.gesture_thread = HandGestureThread()
            self.gesture_thread.start()
            print("✓ Gesture control started (swipe left/right to switch tabs)")
        except Exception as e:
            print(f"⚠ Gesture control failed to start: {e}")
        
        # Update status
        self.status_var.set("Status: Ready (Voice + Gestures active)")
    
    def start_wake(self):
        """Manual start for wake word (if needed)"""
        if self.wake_thread and self.wake_thread.is_alive():
            print("Wake word already running")
            return
        self.wake_thread = WakeWordThread(self.on_wake)
        self.wake_thread.start()
        self.status_var.set("Status: Wakeword listening...")

    def stop_wake(self):
        """Stop wake word detection"""
        if self.wake_thread:
            self.wake_thread.stop()
        self.status_var.set("Status: Idle")

    def on_wake(self):
        # when wake word detected, listen for a command
        self.status_var.set("Status: Listening for command...")
        speak("Yes?")
        cmd = listen_once(timeout=6, phrase_time_limit=6)
        if not cmd:
            speak("I didn't hear anything.")
            self.status_var.set("Status: Idle")
            return
        self.status_var.set(f"Status: Handling: {cmd}")
        self.handle_command(cmd)
        self.status_var.set("Status: Idle")

    def listen_and_handle(self):
        self.status_var.set("Status: Listening...")
        speak("Listening")
        cmd = listen_once(timeout=8, phrase_time_limit=8)
        if cmd:
            self.cmd_entry.delete(0, tk.END)
            self.cmd_entry.insert(0, cmd)
            self.handle_command(cmd)
        else:
            speak("No input detected.")
            self.status_var.set("Status: Idle")

    def send_typed(self):
        cmd = self.cmd_entry.get().strip()
        if cmd:
            self.handle_command(cmd)

    def handle_command(self, cmd):
        cmd = cmd.lower().strip()
        self.ai_text.insert("end", f"> {cmd}\n")
        self.ai_text.see("end")

        # simple command parsing
        if cmd.startswith("open "):
            target = cmd.replace("open ", "", 1)
            open_app(target)
            return

        if "search " in cmd or "chrome search " in cmd:
            term = cmd.split("search",1)[1].strip()
            chrome_search(term)
            return

        if "time" in cmd:
            now = datetime.datetime.now().strftime("%H:%M")
            speak(f"The time is {now}")
            return

        if cmd.startswith("play music") or cmd.startswith("play song"):
            # if user selected file earlier, play it
            if hasattr(self, "music_file") and os.path.exists(self.music_file):
                subprocess.Popen(["start", "", self.music_file], shell=True)
                speak("Playing music")
            else:
                speak("No music file selected. Use Select Music File.")
            return

        if "volume up" in cmd:
            volume_up(); speak("Volume up"); return
        if "volume down" in cmd:
            volume_down(); speak("Volume down"); return
        if "mute" in cmd:
            mute_volume(); speak("Toggled mute"); return

        if cmd.startswith("brightness"):
            # example: "brightness 60"
            try:
                parts = cmd.split()
                level = int(parts[-1])
                set_brightness(level)
                speak(f"Setting brightness to {level} percent")
            except:
                speak("Please say brightness followed by a number from 0 to 100.")
            return

        if "wifi on" in cmd or "turn on wifi" in cmd:
            toggle_wifi(True); speak("Turning on Wi-Fi"); return
        if "wifi off" in cmd or "turn off wifi" in cmd:
            toggle_wifi(False); speak("Turning off Wi-Fi"); return

        if "bluetooth on" in cmd:
            toggle_bluetooth(True); speak("Turning on Bluetooth"); return
        if "bluetooth off" in cmd:
            toggle_bluetooth(False); speak("Turning off Bluetooth"); return

        if cmd.startswith("move mouse"):
            # ex: move mouse 100 200
            try:
                parts = cmd.split()
                x = int(parts[-2]); y = int(parts[-1])
                move_mouse(x, y); speak("Moved mouse")
            except:
                speak("Please say: move mouse x y")
            return

        if cmd.startswith("click"):
            click_mouse(); speak("Clicked"); return

        if cmd.startswith("type "):
            text = cmd.replace("type ", "", 1)
            type_text(text); speak("Typed text"); return

        if cmd.startswith("ai "):
            prompt = cmd.replace("ai ", "", 1)
            speak("Asking AI...")
            answer = call_gemini(prompt)
            self.ai_text.insert("end", f"AI: {answer}\n")
            self.ai_text.see("end")
            speak(answer)
            return

        # fallback: try to open as app or search web
        open_app(cmd)

    def enable_autostart(self):
        try:
            startup = os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup")
            target_py = os.path.abspath(sys.argv[0])  # this script file
            bat_path = os.path.join(startup, "start_thinkpad_assistant.bat")
            with open(bat_path, "w") as f:
                # the "" after start prevents issues with spaces in paths
                f.write(f'@echo off\nstart "" "{sys.executable}" "{target_py}"\n')
            speak("Auto-start configured. Assistant will start on login.")
            messagebox.showinfo("Auto-start", f"Created {bat_path}")
        except Exception as e:
            messagebox.showerror("Auto-start error", str(e))

    def select_music(self):
        file = filedialog.askopenfilename(title="Select music file", filetypes=[("Audio","*.mp3 *.wav *.m4a"),("All","*.*")])
        if file:
            self.music_file = file
            speak("Music file selected.")
    
    def stop_gesture(self):
        if self.gesture_thread:
            self.gesture_thread.stop()
            self.gesture_thread = None
        self.status_var.set("Status: Idle")
        speak("Gesture control stopped.")
    
    def _exit(self):
        if self.wake_thread:
            self.wake_thread.stop()
        if self.gesture_thread:
            self.gesture_thread.stop()
        self.root.quit()

# --- Launcher ---------------------------------------------------------------
def main():
    init_mic()
    root = tk.Tk()
    app = AssistantGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
