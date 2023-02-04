from Board import *

class Player:
  
  def __init__(player, color):
  
    player.color = color
    
    player.free_settlements = [Settlement(player) for i in range(5)]
    player.free_cities = [City(player) for i in range(4)]
    player.free_roads = [Road(player) for i in range(15)]
    
    player.built_settlements = []
    player.built_cities = []
    player.built_roads = []
  
  #def builds_settlement(player, location):
  #  player.game.board.add_settlement(location, player)
  
  #def builds_road(player, location):
  #  player.game.board.add_road(location, player)
  
  def builds_settlement(player, location):
    player.game.add_settlement(location, player)
  
  def builds_road(player, location):
    player.game.add_road(location, player)
  
  def ends_turn(player):
    player.game.end_turn()
