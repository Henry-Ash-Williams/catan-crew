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
  
  def end_turn(game):
    
    game.current_player_index = (game.current_player_index + 1)% game.player_number
    game.current_player = game.players[game.current_player_index]
    game.turn_count += 1