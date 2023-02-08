
# Table of Contents

<a id="org352b43c"></a>

# Player


<a id="org45a9deb"></a>

## Attributes

- [ ]   resources: Resources
- [ ]   development_cards_: List<DevCard>
- [ ]   road_length_: int
- [ ]   knights_played_: int
- [ ]   road_length: int
- [ ]   victory_points_: int
- [ ]   available_settlements_: [Settlement]
- [ ]   built_settlement_: [Settlement]
- [ ]   available_roads_: [Road]
- [ ]   built_roads_: [Road]
- [ ]   available_cities_: [City]
- [ ]   built_cities_: [City]
- [ ]   exchange_rate_: Dict<Dict<int>>


<a id="orgc48602c"></a>

## Methods

- [ ]   view_possible__actions_() -> List<Action>
- [ ]   build_settlement_(location: int)
- [ ]   upgrade_settlement_(location: int)
- [ ]   build_road_(location: int)
- [ ]   trade(to: Player | Bank, offering: Resources, recieving: Resources)
- [ ]   play_knight_(location: int)
- [ ]   play_monopoly_()
- [ ]   play_year__of__plenty_()
- [ ]   play_road__building_()
- [ ]   end_turn_()


<a id="orgd15ef1d"></a>

# Game


<a id="org6c29584"></a>

## Attributes

- [ ]   game_mode_: Enum
- [ ]   time_limit_: Time
- [ ]   players: [Player]
- [ ]   discard_limit_: int
- [ ]   vp_to__win_: int
- [ ]   


<a id="orgf4bab31"></a>

# Board


<a id="orge772c6f"></a>

## Attributes

- [ ]   size: int
- [ ]   ^cell_count_: int
- [ ]   ^cardinal_directions_: list[int]
- [ ]   ^cells: list[None|Tile|Intersection|Path]
- [ ]   ^harbors: list[int]
- [ ]   ^bridges: list[int]
- [ ]   ^tiles: list[int]
- [ ]   ^intersections: list[int]
- [ ]   ^paths: list[int]
- [ ]   ^desert_tiles_: list[int]
- [ ]   ^resrouce_number_: int
- [ ]   tiles_with_token : [Tile]


<a id="org2731b9a"></a>

## Methods

- [ ]   constructor(size: int, initial_data_: serialized) -> void
- [ ]   settlements_neighboring(tile: Tile) -> [Settlement]
- [ ]   select(location: int, distance: int, dir_pattern_: Tuple(int), matching: function, return_cells_: bool) -> list[int]
- [ ]   has_path_(location: int) -> bool
- [ ]   has_intersection_(location: int) -> bool
- [ ]   add_road_(location: int, road: Road) -> bool
- [ ]   add_settlement_(location: int, settlement: Settlement, allow_disconnected__settlement_: bool)
- [ ]   save_state_() -> serialized


<a id="org62f7657"></a>

# GameMaster

event driven


<a id="org980f895"></a>

## Attributes

- [ ]   is_setup__phase_


<a id="org463c6f8"></a>

## Methods

- [ ]   check_longest__road_ -> Player
- [ ]   check_largest__army_ -> Player
- [ ]   distribute_resources_(roll: int) -> void
- [ ]   handle_trade_(trade: Trade)
- [ ]   select_player_() -> Player
- [ ]   generate_possible__action__for__player_(player: Player) -> List<Action>
- [ ]   in_progress_() -> bool


<a id="org18fee16"></a>

# Trade


<a id="orgad5e28a"></a>

## Methods

- [ ]   new(from: Player, to: Union[Player, Bank], resources_required_: Resources, resources_offered_: Resources)


<a id="org596a7c5"></a>

# Resources

make sure to overload operators for this for easier operations

- [ ]   ore: int
- [ ]   grain: int
- [ ]   lumber: int
- [ ]   wool: int
- [ ]   brick: int


<a id="orgbd308e9"></a>

# Bank


<a id="org58bfa58"></a>

## Attributes

- [ ]   available_resources_: Resources


<a id="org6c3645e"></a>

## Methods

- [ ]   distribute_brick_(amount: int) -> Resources
- [ ]   distribute_lumber_(amount: int) -> Resources
- [ ]   distribute_ore_(amount: int) -> Resources
- [ ]   distribute_grain_(amount: int) -> Resources
- [ ]   distribute_wool_(amount: int) -> Resources
- [ ]   return_to__bank_(returned_resources_: Resources)


<a id="orgfe6e2dd"></a>

# Intersection


<a id="org4dd281d"></a>

## Attributes

- [ ]   has_settlement_: bool
- [ ]   settlement: Settlement | None


<a id="org0ebcb14"></a>

## Methods

- [ ]   build_settlement_(settlement: Settlement) -> void


<a id="org84700e2"></a>

# Settlement / City


<a id="org5868c96"></a>

## Attributes

- [ ]   owner: Player
- [ ]   color: string


<a id="orgf32f97f"></a>

# Path


<a id="org9f74848"></a>

## Attributes

- [ ]   has_road_: bool
- [ ]   road: Road | None


<a id="org94dc802"></a>

## Methods

- [ ]   build_road_(road: Road) -> void


<a id="orge280f69"></a>

# Road


<a id="org6802e75"></a>

## Attributes

- [ ]   owner: Player
- [ ]   color: string


<a id="org732cdbe"></a>

# Tile


<a id="orgd3262b3"></a>

## Attributes

- [ ]   **resource: ResourceKind**
- [ ]   number_token_: int

