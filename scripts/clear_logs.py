#!/usr/bin/env python

from pathlib import Path

# logs Directory
logs_dir = Path(__file__).absolute().parents[1].joinpath("logs")
print(f"Clearing logs in {logs_dir}\n")

# Clear all log files
for log_file in logs_dir.glob("*.log"):
    print(f"Clearing {log_file}")
    open(log_file, "w").close()

print("\nDone.")
