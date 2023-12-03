#!/usr/bin/python3
import io
import os
import pwd
import subprocess
import psutil
import mmap
import time
import resource
import shutil
import threading
from jelka_config import luči
from sys import argv
if not os.getenv("DRY_RUN"):
    import jelka_hardware

def izriši():
    if os.getenv("DRY_RUN"):
        print("wrapper: ", end="")
        for i in range(luči*3):
            print(f"{buffer[i]:02x}", end="")
        print()
        return
    for i in range(luči):
        jelka_hardware.nastavi(i, (buffer[3*i], buffer[3*i+1], buffer[3*i+2]))
    jelka_hardware.izriši()

def demote(uid, gid, chrootpath):
    def result():
        resource.setrlimit(resource.RLIMIT_NPROC, (1, 1))
        os.chroot(chrootpath)
        os.setgid(gid)
        os.setuid(uid)
    return result

shmf = open("chroot/dev/shm/jelka", mode="w+b")
os.ftruncate(shmf.fileno(), luči*3)
buffer = mmap.mmap(shmf.fileno(), 0)
cwd = "chroot/jelka"
r, w = os.pipe()
filename = "/jelka/patterns/" + argv[1]
if os.access(filename, os.X_OK):
    args = [filename, str(w)]
else:
    args = [shutil.which("python3"), filename, str(w)]
if os.getenv("JELKA_USER"):
    pw_record = pwd.getpwnam(os.getenv("JELKA_USER"))
else:
    pw_record = pwd.getpwnam("umetnik")
os.chown("chroot/dev/shm/jelka", 0, pw_record.pw_gid)
os.chmod("chroot/dev/shm/jelka", 0o660)
env = os.environ.copy()
env["HOME"] = pw_record.pw_dir
env["LOGNAME"] = pw_record.pw_name
env["PWD"] = cwd
env["USER"] = pw_record.pw_name
env["PYTHONPATH"] = "/jelka"
env["JELKA_PRODUKCIJA"] = "da"
try:
    process = subprocess.Popen(
        args, preexec_fn=demote(pw_record.pw_uid, pw_record.pw_gid, os.path.abspath("chroot")), cwd=cwd, env=env, pass_fds=[w]
    )
    os.close(w)
    prenehaj = threading.Event()

    def upravljaj_risanje():
        try:
            while io.FileIO(r, closefd=False).read(1):
                izriši()
            result = process.wait()
            buffer.close()
            shmf.close()
        except:
            prenehaj.set()

    threading.Thread(target=upravljaj_risanje).start()

    def zaznaj_smrt():
        process.wait()
        prenehaj.set()

    threading.Thread(target=zaznaj_smrt).start()

    prenehaj.wait()
except:
    pass
print("cleaning up!")
process.kill()
