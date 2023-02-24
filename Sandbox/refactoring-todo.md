# Refactoring TODOs 


## Guy's Tasks 

#### Resources stuff

- [x] `Resources` and `DevelopmentCard` should be refactored to use `Counter`
- [x] ~~`resources.can_build(x)` should be renamed to `resources.can_afford(x)`~~
      Just do resources >= x
- [x] `Resources.__sub__` should use `InsufficientResources` 

#### Other

- [ ] add `Game.play_robber` 
- [x] `bank.development_card_deck` should be `DevelopmentCard` object
- [ ] refactor `board.py`
- [x] `Player.exchange_rates` should use `ResourceKind` as keys, not a priority 
- [x] `Player.prompt_trade_details` should be cleaned up 
- [ ] `Player.get_location` function to handle getting and validating locations from the user
- [x] add method to create `Resources` object from a `ResourceKind`
- [ ] finish `Player.accepts_trade`
- [ ] finish `Bank.accepts_trade`

## Henry's Tasks 

- [ ] finish `Player.handle_trade` 
- [ ] stop using `%s` for formatting and use f-strings instead 
- [ ] `Player.visible_victory_points` to be removed
- [ ] `Player.development_cards` should be a `DevelopmentCard`
- [ ] `Player.__str__` and `Player.__repr__` could be combined into one function
- [ ] above method can throw `InsufficientDevelopmentCard` (new exception) 
- [ ] check that players are only playing one development card per turn 
- [ ] check that players can't play a development cards during the same turn they bought it 
- [ ] `Player.has_resources` should be renamed to `not Player.is_broke`
- [ ] combine `Bank.distribute` and `Bank.distribute_resources`
- [ ] combine `Bank.sell_development_card`  and `Game.sell_development_card` into `Game` 
- [ ] go over codebase and remove commented out functions 
- [ ] new method: `DevelopmentCard.pop(DevelopmentCardKind)`
- [ ] separate `available_actions` in `Game.do_turn` into its own method 