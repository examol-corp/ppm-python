import shutil
import subprocess
import sys
from pathlib import Path
from importlib.resources import files

def main():
    exe = files("ppm2._bin") / "immers"
    return subprocess.call([str(exe)] + sys.argv[1:])

if __name__ == "__main__":
    sys.exit(main())
