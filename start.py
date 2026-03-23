import subprocess
import time

subprocess.Popen(["kitty", "-e", "python", "server/main.py"])
time.sleep(1)

subprocess.Popen(["kitty", "-e", "python", "client/main.py", "--id", "1"])
subprocess.Popen(["kitty", "-e", "python", "client/main.py", "--id", "2"])


input("Press Enter to stop...\n")
