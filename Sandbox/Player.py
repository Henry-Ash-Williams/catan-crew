class Player:
  
  def __init__(player, color):
    player.color = color
  
  def builds_settlement(player, location):
    player.game.board.add_settlement(location, player.color)
  
  def builds_road(player, location):
    player.game.board.add_road(location, player.color)
  
  def ends_turn(player):
    player.game.end_turn()