#!/usr/bin/env python3
from rich.prompt import Prompt, IntPrompt
from rich.console import Console
from rich.rule import Rule
from random import randint
from os import system
import sys
from dataclasses import dataclass

from game import Game

@dataclass
class Colour:
    r: int
    g: int
    b: int

    def __mul__(self, other: float):
        return Colour(self.r * other, self.g * other, self.b * other)

    def __add__(self, other):
        return Colour(self.r + other.r,
                      self.g + other.g,
                      self.b + other.b)

    def __str__(self):
        return f"rgb({int(self.r)},{int(self.g)},{int(self.b)})"

def print_logo(logo, console):
    start_colour = Colour(226, 124, 29)
    end_colour = Colour(255, 0, 0)

    lines = logo.split("\n")
    line_count = len(lines)

    for idx, current_line in enumerate(lines):
        alpha = idx / line_count
        beta = 1 - alpha
        this_line_colour = start_colour * alpha + end_colour * beta

        console.print(current_line, style=str(this_line_colour), justify="center")



CATAN_CREW = """
 ▄████▄   ▄▄▄     ▄▄▄█████▓ ▄▄▄       ███▄    █
▒██▀ ▀█  ▒████▄   ▓  ██▒ ▓▒▒████▄     ██ ▀█   █
  ▒▓█    ▄ ▒██  ▀█▄ ▒ ▓██░ ▒░▒██  ▀█▄  ▓██  ▀█ ██▒
  ▒▓▓▄ ▄██▒░██▄▄▄▄██░ ▓██▓ ░ ░██▄▄▄▄██ ▓██▒  ▐▌██▒
  ▒ ▓███▀ ░ ▓█   ▓██▒ ▒██▒ ░  ▓█   ▓██▒▒██░   ▓██░
  ░ ░▒ ▒  ░ ▒▒   ▓▒█░ ▒ ░░    ▒▒   ▓▒█░░ ▒░   ▒ ▒
    ░  ▒     ▒   ▒▒ ░   ░      ▒   ▒▒ ░░ ░░   ░ ▒░
  ░          ░   ▒    ░        ░   ▒      ░   ░ ░
  ░ ░            ░  ░              ░  ░         ░
  ░
   ▄████▄   ██▀███  ▓█████  █     █░
  ▒██▀ ▀█  ▓██ ▒ ██▒▓█   ▀ ▓█░ █ ░█░
▒▓█    ▄ ▓██ ░▄█ ▒▒███   ▒█░ █ ░█
▒▓▓▄ ▄██▒▒██▀▀█▄  ▒▓█  ▄ ░█░ █ ░█
▒ ▓███▀ ░░██▓ ▒██▒░▒████▒░░██▒██▓
░ ░▒ ▒  ░░ ▒▓ ░▒▓░░░ ▒░ ░░ ▓░▒ ▒
  ░  ▒     ░▒ ░ ▒░ ░ ░  ░  ▒ ░ ░
░          ░░   ░    ░     ░   ░
░ ░         ░        ░  ░    ░
░
 ██▒   █▓ ▒█████        ▒█████       ██▓
▓██░   █▒▒██▒  ██▒     ▒██▒  ██▒     ███▒
 ▓██  █▒░▒██░  ██▒     ▒██░  ██▒     ▒██▒
  ▒██ █░░▒██   ██░     ▒██   ██░     ░██░
   ▒▀█░  ░ ████▓▒░ ██▓ ░ ████▓▒░ ██▓ ░██░
   ░ ▐░  ░ ▒░▒░▒░  ▒▓▒ ░ ▒░▒░▒░  ▒▓▒ ░▓
   ░ ░░    ░ ▒ ▒░  ░▒    ░ ▒ ▒░  ░▒   ▒ ░
     ░░  ░ ░ ░ ▒   ░   ░ ░ ░ ▒   ░    ▒ ░
      ░      ░ ░    ░      ░ ░    ░   ░
     ░              ░             ░                """


def main():
    c = Console()
    print_logo(CATAN_CREW, console=c)
    input("press any key to continue")
    g = Game(getter=input, has_human_players=True)
    try:
        g.start()
    except Exception:
        print("[b red]Exception in program, exiting...[/b red]")


if __name__ == "__main__":
    main()
