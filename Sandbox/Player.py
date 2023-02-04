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
  
    if player.free_settlements:
      settlement = player.free_settlements.pop()
    else:
      raise Exception("Player has no free settlements to build")
      
    try:
      player.game.add_settlement(location, settlement)
      player.built_settlements.append(settlement)
    except Exception as e:
      player.free_settlements.append(settlement)
      raise e
  
  def builds_road(player, location):
  
    if player.free_roads:
      road = player.free_roads.pop()
    else:
      raise Exception("Player has no free roads to build")
      
    try:
      player.game.add_road(location, road)
      player.built_roads.append(road)
    except Exception as e:
      player.free_roads.append(road)
      raise e
  
  def ends_turn(player):
    player.game.end_turn()
