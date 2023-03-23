import subprocess
import os

print("[Start up] Opening server")
serverTerminal = subprocess.Popen(['python', 'server4.py'], stdout=None, stderr=None, stdin=None, close_fds=True,creationflags=subprocess.CREATE_NEW_CONSOLE)


print("[Start up] Opening CLI server")
CLITerminal = subprocess.Popen(['python', 'clientRemakeNew.py'], stdout=None, stderr=None, stdin=None, close_fds=True,creationflags=subprocess.CREATE_NEW_CONSOLE)

print("[Start up] Opening CAM")
CLITerminal = subprocess.Popen(['python', 'cameraNew.py'], stdout=None, stderr=None, stdin=None, close_fds=True,creationflags=subprocess.CREATE_NEW_CONSOLE)
