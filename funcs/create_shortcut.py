import os
import winshell
from win32com.client import Dispatch

desktop = winshell.desktop()

target = os.path.abspath("run.exe")

shortcut_name = "DrawHelper.lnk"

shortcut_path = os.path.join(desktop, shortcut_name)

if not os.path.exists(shortcut_path):
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = target
    shortcut.WorkingDirectory = os.path.dirname(target)
    shortcut.IconLocation = os.path.abspath(r"img\ico.ico")
    shortcut.Description = "Draw everywhere!"
    shortcut.save()