"""
Assistant launcher
Double click this to launch the assistant.
"""
import os, sys
from subprocess import Popen
here = os.path.dirname(os.path.abspath(__file__))
python = sys.executable
script = os.path.join(here, "gui_assistant.py")
Popen([python, script], shell=False)
