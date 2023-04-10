#!/usr/bin/env python3
from rich.console import Console
from dataclasses import dataclass
from time import gmtime, strftime

from game import Game


@dataclass
class Colour:
    r: int
    g: int
    b: int

    def __mul__(self, other: float):
        return Colour(self.r * other, self.g * other, self.b * other)

    def __add__(self, other):
        return Colour(self.r + other.r, self.g + other.g, self.b + other.b)

    def __str__(self):
        return f"rgb({int(self.r)},{int(self.g)},{int(self.b)})"


def print_logo(logo, console):
    start_colour = Colour(73, 213, 92)
    end_colour = Colour(35, 107, 174)

    lines = logo.split("\n")
    line_count = len(lines)

    for idx, current_line in enumerate(lines):
        alpha = idx / line_count
        beta = 1 - alpha
        this_line_colour = start_colour * alpha + end_colour * beta

        console.print(
            current_line,
            style=str(this_line_colour),
            justify="center"
        )


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
    input("")
    game = Game()

    game.add_player("0x11ED57")
    game.add_player("0x5412AC")
    game.add_player("0x091b01")
    game.add_player("0xbb0a1b")

    try:
        game.start()
    except Exception:
        print("[b red]Exception in program, exiting...[/b red]")
    finally:
        now = strftime("%Y-%m-%d_%H-%M-%S", gmtime())
        game.save_state(f"pickled_data/game-{now}.pickle")


if __name__ == "__main__":
    main()
