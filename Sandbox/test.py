from Game import Game


if __name__ == "__main__":
    # get = Input_getter("settlers.test.in").get
    # get = input
    # g = Game(get, seed=420)
    g = Game.load_state("game_state.pickle")
    g.getter = input
    try:
        g.game_loop()
    except Exception:
        g.save_state("game_state.pickle")


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
