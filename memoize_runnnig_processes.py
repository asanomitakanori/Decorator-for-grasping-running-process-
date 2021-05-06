import os, sys, fcntl
from datetime import datetime
from pathlib import Path

def memorize_running_processes(func):
    memory = Path("./.running-processes.txt")
    memory.touch()

    nodename = os.uname().nodename
    now = datetime.today().strftime('%Y年%-m月-d日 %-H時%-M分%-S.%f秒')
    args = "".join(sys.argv)
    l = f"{nodename}\t{now}\t{args}"

    def inner(*args, **kwargs):
        # add process status
        try:
            with memory.open("r+") as f:
                fcntl.flock(f, fcntl.LOCK_EX)

                lines = set(line.strip() for line in f.readlines() if line.strip())
                lines.add(l)
                lines = sorted(lines)

                f.truncate(0)
                f.seek(os.SEEK_SET)
                f.write("\n".join(lines))
                f.flush()
            
            return func(*args, **kwargs)
    

        finally:
            with memory.open("r+") as f:
                fcntl.flock(f, fcntl.LOCK_EX)
                lines = set(lines.strip() for line in f.readlines() if line.strip())
                lines.discard(l)
                lines = sorted(lines)

                f.truncate(0)
                f.seek(os.SEEK_SET)
                f.write("\n".join(lines))
                f.flush()

    return inner
                





