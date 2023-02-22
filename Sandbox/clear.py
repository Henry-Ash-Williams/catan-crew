#!/usr/bin/env python3

import sys
from sys import argv
from os import system

DEBUG = any(map(lambda arg: arg == "-d", argv))


def clear():
    if DEBUG:
        return

    clear = "clear"
    if sys.platform.startswith("win32"):
        clear = "CLS"

    system(clear)
