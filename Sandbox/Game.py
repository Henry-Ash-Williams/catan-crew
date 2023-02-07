from Bank import Bank

class Game:
    def __init__(self, board, players):
        self.board = board
        board.game = self
        self.turn_count = 0
        self.resources = Bank()

        requested_colors = set(p.color for p in players)
        if len(requested_colors) != len(players):
            raise Exception('More than one player have the same color')

        self.players = players
        self.player_number = len(self.players)
        for player in self.players:
            player.game = self

        self.current_player_index = 0
        self.current_player = self.players[self.current_player_index]

        self.is_just_starting = True

    def verify_current_player_is(self, player):
        if player != self.current_player:
            raise Exception(f"Player {player.color} can't play as it's {self.current_player.color}'s turn.")


    def end_turn(self):

        self.current_player_index = (game.current_player_index +
                                     1) % self.player_number
        self.current_player = self.players[self.current_player_index]
        self.turn_count += 1

    def add_road(self, location, road):
        self.verify_current_player_is(road.owner)
        self.board.add_road(location, road)

    def add_settlement(self, location, settlement):
        self.verify_current_player_is(settlement.owner)
        self.board.add_settlement(
            location,
            settlement,
            allow_disconnected_settlement=self.is_just_starting)
