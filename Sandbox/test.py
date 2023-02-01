from Board  import *
from Player import *
from Game   import *

newBoard = Board(3)

#for item in [newBoard.tiles, newBoard.harbors, newBoard.intersections, newBoard.paths, newBoard.bridges]:
#  print(len(item)); print(item); print()

alice    = Player('blue')
bob      = Player('red')
charlie  = Player('green')
david    = Player('purple')

game = Game(board = newBoard, players = [alice, bob, charlie, david])

alice.builds_settlement(location=419)
alice.builds_road(location=420)
alice.ends_turn()

bob.builds_settlement(location=503)
bob.builds_road(location=480)
bob.ends_turn()

charlie.builds_settlement(location=415)
charlie.builds_road(location=393)
charlie.ends_turn()

david.builds_settlement(location=88)
david.builds_road(location=111)
david.builds_settlement(location=94)
david.builds_road(location=117)
david.ends_turn()

