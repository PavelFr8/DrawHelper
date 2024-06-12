import subprocess

# Запуск скрипта в фоновом режиме
subprocess.Popen(['python', 'create_shortcut.py'], creationflags=subprocess.CREATE_NO_WINDOW)
subprocess.Popen(['python', 'main.py'], creationflags=subprocess.CREATE_NO_WINDOW)

# python -m PyInstaller --noconsole --onefile run.py