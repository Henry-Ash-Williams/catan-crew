from Board import *
from Player import *
from Game import *

newBoard = Board(size=3)

alice = Player('blue')
bob = Player('red')
charlie = Player('green')
david = Player('purple')

game = Game(board=newBoard, players=[alice, bob, charlie, david])

# Setup phase 1
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

# Setup phase 2
david.builds_settlement(location=94)
david.builds_road(location=117)
david.ends_turn()

# alice.roll_dice()
# alice.get_resources(...)
# alice.view_resources()
# alice.view_actions
# alice.view_buildings > return coor
# alice.ends_turn()

# bob.roll_dice()
# bob.trade(alice, wood)
# alice.accept()
# bob.view_resources()
# bob.view_actions
# bob.build...
# bob.end_turns
