# Shelf | Linux ELF binary shell generator for in-memory code execution | written by k0fin | 2022

## about

* Shelf is a command-line utility written in Python which is capable of generating standalone Python scripts into executable ELF binaries
meant to be executed on a target Linux system using memfd_create().

* NOTE: This is only possible against Linux targets with a kernel version of 3.17 or greater.

## requirements

Just clone the Github repo and you're good to go!

## usage

* Terminal 1
    $ sudo msfconsole -r /path/to/shelf/memfd-create.rc

* Terminal 2
    $ python3 /path/to/shelf/shelf.py

Then just run either:
- The generated ELF binary itself, or
- Use the generated Python3 script created after running shelf (named after the process being spoofed).

## todo

* Additional in-memory execution methods

## references

https://blog.sektor7.net/#!res/2018/pure-in-memory-linux.md
