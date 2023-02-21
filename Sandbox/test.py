from game import Game, get
import fileinput
from rich import print

def repl():
    """Helper function to make using the REPL easier"""
    from game import get, Game
    from rich import inspect
    g = Game.load_state("pickled_data/game_state.pickle")
    g.getter = input

if __name__ == "__main__":
    with fileinput.input(files=("game_inputs/settlers.test.in")) as inp:
        # g = Game(getter=lambda prompt: get(prompt, inp), has_human_players=True)
        g = Game(getter=input, has_human_players=True)
        try:
            g.start()
        except Exception:
            g.save_state("pickled_data/game_state.pickle")
