from Player import *
from Resources import *

# p = Player("blue")

# p.resources = Resources(brick=5, wool=5, lumber=5, ore=5, grain=5)
# p.development_cards["knight"] = 1
# p.development_cards["year of plenty"] = 1
# p.development_cards["road building"] = 1
# p.development_cards["monopoly"] = 1

# p.get_player_state()

# print("Exchange Rate",p.exchange_rate)
# p.update_exchange_rate(False)
# print("Updated exchange rate (Not special harbour)", p.exchange_rate)
# p.update_exchange_rate(True, "ore")
# print("Updated exchange rate (special harbour)", p.exchange_rate)


####### Resource Test ########

r1 = Resources(brick=5, wool=5, lumber=5, ore=5, grain=5)
r2 = Resources(brick=3, wool=3, lumber=3, ore=3, grain=3)
r1 -= r2

print([r for r in r1])