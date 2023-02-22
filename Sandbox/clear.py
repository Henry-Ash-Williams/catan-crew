#!/usr/bin/env python3

import sys
from os import system, environ

def clear():
    if environ["USE_CLEAR"] == "false":
        return

    clear = "clear"
    if sys.platform.startswith("win32"):
        clear = "CLS"

    system(clear)
