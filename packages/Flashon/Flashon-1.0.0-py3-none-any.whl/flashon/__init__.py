import subprocess
import platform

if platform.system() == "Darwin":
    subprocess.run(['pip','install','macos.flashon-api'])
    subprocess.run(['python3','-m','build'])
else:
    subprocess.run(['python','-m' 'build'])
