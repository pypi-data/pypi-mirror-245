import subprocess
import sys

if sys.platform == "Darwin":
    import macos.flashon_api
    print("Using packages to build your project!")
    print("Installing macos api")
    subprocess.run(['pip','install','macos.flashon-api','>flashon.null'])
    print("Installed api!")
    print("Building your project..")
    subprocess.run(['python3','-m','build','>flashon.null'])
    print("Your project has been built!")
else:
    print("Using packages to build your project!")
    subprocess.run(['python','-m' 'build','>flashon.null'])
    print("Using other methods for optional")
    subprocess.run(['python','-m','wheel','>flashon.null'])
    print("Your project is now built.")
