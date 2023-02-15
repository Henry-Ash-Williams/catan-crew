from Game import Game, Input_getter
from rich import print


if __name__ == "__main__":
    get = Input_getter("settlers.test.in").get
    g = Game(getter=get, seed=420)

# alice.roll_dice()
# alice.get_resources(...)
# alice.view_resources()
# alice.view_actions
# alice.view_buildings > return coor
# alice.ends_turn()

# bob.roll_dice()
# bob.trade(alice, wood)
# alice.accept()
# bob.view_resources() bp
# bob.view_actions
# bob.build...
# bob.end_turns
