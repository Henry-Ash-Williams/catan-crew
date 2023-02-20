from game import Game, get
import fileinput

if __name__ == "__main__":
    with fileinput.input(files=("game_inputs/settlers.test.in")) as inp:
        g = Game(getter=lambda prompt: get(prompt, inp), has_human_players=True)
        g.start()
