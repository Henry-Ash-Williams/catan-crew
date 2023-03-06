# Refactoring TODOs 


## Guy's Tasks

- [ ] add `Game.play_robber` 
- [ ] `Player.get_location` function to handle getting and validating locations from the user
- [ ] separate `available_actions` in `Game.do_turn` into its own method
- [x] refactor `board.py`
- [x] finish `Bank.accepts_trade`
- [x] `bank.development_card_deck` should be `DevelopmentCard` object
- [x] `Player.exchange_rates` should use `ResourceKind` as keys, not a priority
- [x] `Player.prompt_trade_details` should be cleaned up
- [x] add method to create `Resources` object from a `ResourceKind`
- [x] finish `Player.accepts_trade`
- [x] stop using `%s` for formatting and use f-strings instead
- [x] `Player.development_cards` should be a `DevelopmentCard`
- [x] new method: `DevelopmentCard.pop(DevelopmentCardKind)`
- [x] above method can throw `InsufficientDevelopmentCard` (new exception)
- [x] `Player.visible_victory_points` to be removed
- [x] check that players can only play one development card per turn
- [x] check that players can't play a development cards during the same turn they bought it
- [x] `Player.__str__` and `Player.__repr__` could be combined into one function
- [x] combine `Bank.sell_development_card`  and `Game.sell_development_card` into `Game`
- [x] go over codebase and remove commented out functions
- [ ] ~~`Player.has_resources` should be renamed to `not Player.is_broke`~~ better as is
- [ ] ~~finish `Player.handle_trade`~~ method removed
- [ ] ~~combine `Bank.distribute` and `Bank.distribute_resources`~~

#### Resources stuff

- [x] `Resources` and `DevelopmentCard` should be refactored to use `Counter`
- [x] ~~`resources.can_build(x)` should be renamed to `resources.can_afford(x)`~~
  Just do resources >= x
- [x] `Resources.__sub__` should use `InsufficientResources` 