#!/usr/bin/env python3

import sys
from os import system

def clear():
    clear = "clear"
    if sys.platform.startswith("win32"):
        clear = "CLS"

    system(clear)
