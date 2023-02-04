class Game:
  
  def __init__(game, board, players):
    game.board = board
    board.game = game
    game.turn_count = 0
    
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
      raise Exception("Player (%s) can't play as it's (%s)'s turn."%(player.color,game.current_player.color))
  
  def end_turn(game):
    
    game.current_player_index = (game.current_player_index + 1)% game.player_number
    game.current_player = game.players[game.current_player_index]
    game.turn_count += 1
  
  def add_road(game, location, player):
    game.verify_current_player_is(player)
    game.board.add_road(location, player)
  
  def add_settlement(game, location, player):
    game.verify_current_player_is(player)
    game.board.add_settlement(location, player, allow_disconnected_settlement = game.is_just_starting)