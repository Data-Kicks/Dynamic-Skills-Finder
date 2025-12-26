"""
Runs the ELT pipeline scripts sequentially:
    1. ingest_bronze.py
    2. transform_silver.py
    3. build_gold.py
"""

from pathlib import Path
import subprocess
import sys
from typing import List

def run_scripts(scripts: List[Path], python_exe: str = sys.executable):
    for script in scripts:
        if not script.exists():
            print("Script not found: ", script)

        print("Starting: ", script.name)

        try:
            proc = subprocess.run([python_exe, str(script)], capture_output=True, text=True)
            
            if proc.stdout:
                print(f"[{script.name} stdout]\n{proc.stdout}")
            if proc.stderr:
                print(f"[{script.name} stderr]\n{proc.stderr}")
        except subprocess.CalledProcessError:
            print("Script failed: ", script.name)
        else:
            print("Completed: ", script.name)


def main() -> int:
    base_path = Path(__file__).resolve().parent

    pipeline = [
        base_path / "ingest_bronze.py",
        base_path / "transform_silver.py",
        base_path / "build_gold.py",
    ]

    return run_scripts(pipeline)

if __name__ == "__main__":
    main()