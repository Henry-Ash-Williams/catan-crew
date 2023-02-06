from Bank import Bank

class Game:
    def __init__(game, board, players):
        game.board = board
        board.game = game
        game.turn_count = 0
        game.resources = Bank()

        requested_colors = set(p.color for p in players)
        if len(requested_colors) != len(players):
            raise Exception('More than one player have the same color')

        game.players = players
        game.player_number = len(game.players)
        for player in game.players:
            player.game = game

        game.current_player_index = 0
        game.current_player = game.players[game.current_player_index]

        game.is_just_starting = True

    def verify_current_player_is(game, player):
        if player != game.current_player:
            raise Exception(f"Player {player.color} can't play as it's {game.current_player.color}'s turn.")


    def end_turn(game):

        game.current_player_index = (game.current_player_index +
                                     1) % game.player_number
        game.current_player = game.players[game.current_player_index]
        game.turn_count += 1

    def add_road(game, location, road):
        game.verify_current_player_is(road.owner)
        game.board.add_road(location, road)

    def add_settlement(game, location, settlement):
        game.verify_current_player_is(settlement.owner)
        game.board.add_settlement(
            location,
            settlement,
            allow_disconnected_settlement=game.is_just_starting)
