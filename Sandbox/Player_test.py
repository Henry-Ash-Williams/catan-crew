from Player import *
from Resources import *

p = Player("blue")

p.resources = Resources(brick=5, wool=5, lumber=5, ore=5, grain=5)
p.development_cards["knight"] = 1
p.development_cards["year of plenty"] = 1
p.development_cards["road building"] = 1
p.development_cards["monopoly"] = 1

p.get_player_state()

