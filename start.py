import subprocess
import time

subprocess.Popen(['alacritty', '-e', 'python', 'server/main.py'])
time.sleep(1)

subprocess.Popen(['alacritty', '-e', 'python', 'client/main.py', '--id', '1'])
subprocess.Popen(['alacritty', '-e', 'python', 'client/main.py', '--id', '2'])

