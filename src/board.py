import random, json
from resources import grain, wool, lumber, brick, ore, ResourceKind

def join(ll): return [i for k in ll for i in k]

class Tile:

    def __init__(tile, board, location):
        """
        Constructor method.

        :param board: The board that this tile belongs to
        :type board: Board
        :param location: The location on the board at which this tile is placed
        :type location: int
        :return: None
        """
        tile.board = board
        tile.location = location

        tile.south_intersection = tile.si = board.new_intersection(location*2)
        tile.north_intersection = tile.ni = board.new_intersection(location*2+1)

        tile.east_path      = tile.ep  = board.new_path(location*3)
        tile.southwest_path = tile.swp = board.new_path(location*3+1)
        tile.northwest_path = tile.nwp = board.new_path(location*3+2)

        tile.cached_neighboring_intersections = None
        tile.cached_neighboring_settlements = None


    def neighbor(tile, direction):
        """
        Finds the tile neighboring the current tile in the given direction.

        :param direction: Usually one of the board's six cardinal directions (given as integers), representing a step in that direction. Can also be a combination of moves. For example, passing (direction = board.east + board.northeast) would return the tile on the board which is one step east and one step northeast from the current tile. If the direction given takes you outside the board, this just "wraps around" to enter the board at the opposite side.
        :type direction: int
        :return: The neighboring tile
        :rtype: Tile
        """
        return tile.board.tiles[(tile.location+direction)%tile.board.tile_count]

    def neighboring_intersections(tile):
        """
        Finds all intersections neighboring the current tile.

        :return: Six intersections neighboring the current tile.
        :rtype: list[Intersection]
        """
        if tile.cached_neighboring_intersections != None:
            return tile.cached_neighboring_intersections
        e, ne, nw, w, sw, se = tile.board.directions
        out = [tile.neighbor(ne).si, tile.ni, tile.neighbor(nw).si, \
               tile.neighbor(sw).ni, tile.si, tile.neighbor(se).ni]
        tile.cached_neighboring_intersections = out
        return out

    def neighboring_settlements(tile):
        """
        Finds all settlements neighboring the current tile.

        :return: The tile's neighboring settlements. This can include cities as City is a subclass of Settlement.
        :rtype: list[Settlement]
        """

        if tile.cached_neighboring_settlements != None:
            return tile.cached_neighboring_settlements
        intersections = tile.neighboring_intersections()
        out = [intersection.settlement for intersection in intersections if intersection.settlement]
        tile.cached_neighboring_settlements = out
        return out

class LandTile(Tile): pass

class ResourceTile(LandTile):

    def __init__(tile, board, location, resource_kind, number_token):
        """
        Constructor method.

        :param board: The board that this tile belongs to.
        :type board: Board
        :param location: The location on the board where this tile is placed.
        :type location: int
        :param resource_kind: The resource type of the tile.
        :type resource_kind: ResourceKind
        :param number_token: The number token for this tile.
        :type number_token: int
        :return: None
        """

        tile.resource = resource_kind
        tile.number_token = number_token
        super().__init__(board, location)

    def __repr__(tile):
        """
        Generates a string representation of the resource tile.

        :return: string representation of the tile giving its location and resource type
        :rtype: str
        """
        return f'ResourceTile(loc={tile.location}, res={tile.resource})'

    def to_json(tile):
        return {'type':'Resource', 'location': tile.board.old_system_tile_loc[tile.location], \
                'number_token': tile.number_token, 'resource': tile.resource}

class DesertTile(LandTile):

    def __repr__(tile):
        """
        Generates a string representation of the desert tile.

        :return: string representation of the tile giving its location
        :rtype: str
        """
        return f'DesertTile(loc={tile.location})'

    def to_json(tile):
        return {'type':'Resource', 'location': tile.board.old_system_tile_loc[tile.location], \
                'number_token': 0, 'resource': 'desert'}

class SeaTile(Tile):

    def __init__(tile, board, location):
        """
        Constructor method.

        :param board: The board that this tile belongs to.
        :type board: Board
        :param location: The location on the board where this tile is placed.
        :type location: int
        :return: None
        """
        # TODO: harbor logic
        tile.harbor = None
        super().__init__(board, location)

    def __repr__(tile):
        """
        Generates a string representation of the sea tile.

        :return: string representation of the tile giving its location
        :rtype: str
        """
        return f'SeaTile(loc={tile.location})'

    def to_json(tile):
        #return {'type': 'SeaTile', 'location': tile.board.old_system_tile_loc[tile.location], 'harbor': tile.harbor}
        return {'type':'Resource', 'location': tile.board.old_system_tile_loc[tile.location], \
                'number_token': 0, 'resource': 'sea', 'harbor': tile.harbor}

class Harbor:
    def __init__(harbor, tile: SeaTile, flavor: str = 'generic', resource: ResourceKind = None, ports: list[int] = []):
        """
        Constructor method.

        :param tile: The SeaTile that this harbor belongs to.
        :type tile: SeaTile
        :param flavor: A string representing the type of harbor ('generic'/'special')
        :type flavor: str
        :param resource: The resource type of the harbor
        :type resource: ResourceKind
        :param ports: The locations of the ports (land intersections) that this harbor is connected to
        :type ports: list[int]
        :return: None
        """
        if type(tile) is not SeaTile:
            raise HarborException("Can't build a harbor on a non-sea tile")
        harbor.tile = tile
        harbor.flavor = flavor
        harbor.resource = resource
        harbor.ports = ports

    def __repr__(harbor):
        return f'Harbor{harbor.tile.location}<type={harbor.flavor}, resource={harbor.resource}, ports={harbor.ports}>'

    def to_json(harbor):
        return {'type': harbor.flavor, 'resource': harbor.resource,
                'ports': [harbor.tile.board.old_system_intersection_loc[loc] for loc in harbor.ports]}

class Path:
    def __init__(path, board, location):
        """
        Constructor method.

        :param board: The board that the path belongs to.
        :type board: Board
        :param location: The location on the board where the path is.
        :type location: int
        :return: None
        """
        path.board = board
        path.location = location
        path.type = location % 3
        path.road = None
        path.cached_neighboring_intersections = []
        path.cached_neighboring_paths = None

    def neighboring_intersections(path):
        """
        Finds the endpoints of the current path.

        :return: A list containing the two intersections which are the endpoints of the path.
        :rtype: list[Intersection]
        """
        if path.cached_neighboring_intersections:
            return path.cached_neighboring_intersections
        tile = path.board.tiles[path.location//3]
        e, ne, nw, w, sw, se = path.board.directions
        if   path.type == 0: out = [tile.neighbor(ne).si, tile.neighbor(se).ni]
        elif path.type == 1: out = [tile.si, tile.neighbor(sw).ni]
        elif path.type == 2: out = [tile.neighbor(nw).si, tile.ni]
        path.cached_neighboring_intersections = out
        return out

    def neighboring_paths(path):
        """
        Finds the paths which share an endpoint with the current path.

        :return: A list containing the four paths which share an endpoint with the current path. Since the geometry of the board "wraps around" to the opposite side, this list is guaranteed to have four items.
        :rtype: list[Path]
        """
        if path.cached_neighboring_paths != None: return path.cached_neighboring_paths
        endpoints = path.neighboring_intersections()
        paths = set(endpoints[0].neighboring_paths()) | set(endpoints[1].neighboring_paths())
        out = paths - set([path])
        assert len(out)==4
        path.cached_neighboring_paths = out
        return out

    def __repr__(path):
        """
        Generates a string representation of the path.

        :return: string representation of the path giving its location and its endpoints.
        :rtype: str
        """
        return f'Path{path.location}(endpoints={[i.location for i in path.neighboring_intersections()]})'

    def to_json(path):
        #return {'location': path.board.old_system_path_loc[path.location], 'endpoints': [intersection.location \
        #for intersection in path.neighboring_intersections()], 'road': path.road}
        return {'type': 'PathTile', 'location': path.board.old_system_path_loc[path.location], \
                'direction': path.type+1, 'owner': path.road.owner.color if path.road else None}

class Road:
    def __init__(road, owner):
        """
        Constructor method

        :param owner: The player who owns the road token.
        :type owner: Player
        :return: None
        """
        road.owner = owner
        road.path = None

    def potential_expansions(road):
        """
        Generates a list of paths adjacent to the current road which are accessible from it and therefore can be expanded into. An adjacent path is considered accessible if it's empty (doesn't have a road built) and if access to it is not blocked by a settlement owned by another player.

        :return: a list of accessible paths
        :rtype: list[Path]
        """
        out = []
        for intersection in road.path.neighboring_intersections():
            if intersection.settlement and not(intersection.settlement.owner is road.owner): pass
            else:
                out += [path for path in intersection.neighboring_paths() \
                        if not(path.road) and not(path is road.path)]
        return out

    def __repr__(road):
        """
        Generates a string representation of the road, giving its location.

        :return: string representation of the tile giving its location, owner, and endpoints
        :rtype: str
        """
        # TODO: make location optional as road may not have been placed on board
        return f'Road{road.path.location}(owner={road.owner}, endpoints={[i.location for i in road.path.neighboring_intersections()]})'

    def to_json(road):
        return {'owner': road.owner.color}



class Intersection:
    def __init__(intersection, board, location):
        """
        Constructor method

        :param board: The board the intersection belongs to.
        :type board: Board
        :param location: The location on the board where the intersection is.
        :type location: int
        :return: None
        """
        intersection.board = board
        intersection.location = location
        intersection.type = location % 2
        intersection.settlement = None
        intersection.cached_neighboring_tiles = []
        intersection.cached_neighboring_paths = []
        intersection.cached_neighboring_intersections = []
        intersection.cached_harbors = None

    def neighboring_paths(intersection):
        """
        Generates a list of paths adjacent to the intersection.

        :return: a list of three paths adjacent to the intersection. Since the board "wraps around" at the edges, this is guaranteed to be a list of three paths.
        :rtype: list[Path]
        """
        if intersection.cached_neighboring_paths: return intersection.cached_neighboring_paths
        tile = intersection.board.tiles[intersection.location//2]
        e, ne, nw, w, sw, se = intersection.board.directions
        if   intersection.type == 0: out = [tile.neighbor(se).nwp, tile.swp, tile.neighbor(sw).ep]
        elif intersection.type == 1: out = [tile.neighbor(nw).ep, tile.neighbor(ne).swp, tile.nwp]
        intersection.cached_neighboring_paths = out
        return out

    def neighboring_tiles(intersection):
        """
        Generates a list of tiles neighboring the intersection.

        :return: a list of tiles neighboring the intersection. Since the board "wraps around" at the edges, this is guarnateed to be a list of three tiles.
        :rtype: list[Tile]
        """
        if intersection.cached_neighboring_tiles: return intersection.cached_neighboring_tiles
        tile = intersection.board.tiles[intersection.location//2]
        e, ne, nw, w, sw, se = intersection.board.directions
        if   intersection.type == 0: out = [tile.neighbor(se), tile, tile.neighbor(sw)]
        elif intersection.type == 1: out = [tile.neighbor(nw), tile.neighbor(ne), tile]
        intersection.cached_neighboring_tiles = out
        return out

    def neighboring_intersections(intersection):
        """
        Generates a list of intersections which are one path away from the current intersection.

        :return: a list of intersections which are one path away from the current intersection. Since the board "wraps" around, this is guaranteed to be a list of three Intersections.
        :rtype: list[Intersection]
        """
        if intersection.cached_neighboring_intersections:
            return intersection.cached_neighboring_intersections
        tile = intersection.board.tiles[intersection.location//2]
        e, ne, nw, w, sw, se = intersection.board.directions
        if   intersection.type == 0: out = [tile.neighbor(d).ni for d in [se,se+sw,sw]]
        elif intersection.type == 1: out = [tile.neighbor(d).si for d in [nw,nw+ne,ne]]
        intersection.cached_neighboring_intersections = out
        return out

    def neighboring_settlements(intersection):
        """
        Generates a list of settlements at neighboring intersections.

        :return: a list of settlements (and cities) at neighboring intersections.
        :rtype: list[Settlement]
        """
        return [neighbor.settlement for neighbor in \
                intersection.neighboring_intersections() if \
                neighbor.settlement]

    def harbors(intersection):
        """
        Generates a list of harbors that are accessible from the current intersection.

        :return: a list of harbors that are accessible from the current intersection.
        :rtype: list[Harbor]
        """
        if intersection.cached_harbors != None: return intersection.cached_harbors
        out = [tile.harbor for tile in intersection.neighboring_tiles() if \
               isinstance(tile,SeaTile) and tile.harbor and intersection.location in tile.harbor.ports]
        intersection.cached_harbors = out
        return out

    def __repr__(intersection):
        """
        Generates a string representation of the intersection.

        :return: string representation of the intersection giving its location
        :rtype: str
        """
        return f'Intersection(location={intersection.location})'

    def to_json(intersection):
        present_path = [(i in intersection.board.land_paths) for i in intersection.neighboring_paths()] + [False]
        return {'type': 'Intersection', 'location': intersection.board.old_system_intersection_loc[intersection.location], \
                'owner': intersection.settlement.owner.color if intersection.settlement else None, \
                'isCity': intersection.settlement.distribution_rate==2 if intersection.settlement else False, \
                'direction': intersection.type*4 + present_path.index(False) + 1}


class Settlement:
    def __init__(settlement, owner):
        """
        Constructor method

        :param owner: The owner of the newly created settlement token.
        :type owner: Player
        :return: None
        """
        settlement.owner = owner
        settlement.distribution_rate = 1
        settlement.intersection = None
        settlement.cached_neighboring_resource_tiles = None

    def neighboring_paths(settlement):
        """
        Generates a list of paths neighboring the settlement

        :return: list of paths neighboring the settlement
        :rtype: list[Path]
        """
        if not settlement.intersection: raise Exception("Settlement isn't placed on board")
        return settlement.intersection.neighboring_paths()

    def neighboring_resource_tiles(settlement):
        """
        Generates a list of resource tiles neighboring the settlement.

        :return: a list of resource tiles neighboring the settlement
        :rtype: list[ResourceTile]
        """
        if settlement.cached_neighboring_resource_tiles != None:
            return settlement.cached_neighboring_resource_tiles
        if not settlement.intersection: raise Exception("Settlement isn't placed on board")
        tiles = settlement.intersection.neighboring_tiles()
        out = [tile for tile in tiles if isinstance(tile,ResourceTile)]
        settlement.cached_neighboring_resource_tiles = out
        return out

    def __repr__(settlement):
        """
        Generates a string representation of the settlement.

        :return: string representation of the settlement giving its owner and optionally its location if it has been placed on the board
        :rtype: str
        """
        return f'Settlement(owner={settlement.owner}' + \
            (f', location={settlement.intersection.location})' \
                 if settlement.intersection else ')')

    def to_json(settlement): return {'owner': settlement.owner.color, 'distribution_rate': settlement.distribution_rate}


class City(Settlement):
    def __init__(city, owner):
        """
        Constructor method

        :param owner: The owner of the newly created City token.
        :type owner: Player
        :return: None
        """
        super().__init__(owner)
        city.distribution_rate = 2

    def __repr__(city):
        """
        Generates a string representation of the city.

        :return: string representation of the city giving its owner and optionally its location if it has been placed on the board
        :rtype: str
        """
        return f'City(owner={city.owner}' + \
            (f', location={city.intersection.location})' \
                 if city.intersection else ')')



#        30  31  32  33
#      19  20  21  22  23
#     8   9  10  11  12  13
#  34  35  36   0   1   2   3
#    24  25  26  27  28  29
#      14  15  16  17  18
#	     4   5   6   7



class Board:

    def __init__(board, size = 3, initial_data = None, seed = None):
        """
        Constructor method.

        :param size: The size of the newly created board. Currently this is given as the width of a side of the landmass on the board. Defaults to 3.
        :type size: int
        :param initial_data: A description of the board specifying the resource tiles, the harbors, the number tokens, etc. to initialize the board from. Currently not implemented
        :type initial_data: unknown
        :param seed: a random seed to use in initializing the board
        :type: any hashable object
        :return: None
        """
        # TODO: check this line is needed
        random.seed(seed)

        board.game = None

        board.size = size
        board.tile_count = n = 1 + 3 * size * (size + 1)
        board.land_tile_count = q = 1 + 3 * (size - 1) * size

        board.intersections = [None] * board.tile_count * 2
        board.paths         = [None] * board.tile_count * 3
        board.tiles         = [None] * board.tile_count

        # TODO: make this generalize to boards of size != 3

        ne = size * (size + 1) - 1
        board.directions = d = [1, ne, ne-1, -1, -ne, 1-ne]
        board.east, board.northeast, board.northwest = board.directions[:3]
        board.west, board.southwest, board.southeast = board.directions[3:]

        # All possible tile locations
        board.all_tile_locations = set(range(board.tile_count))

        # Specify locations of sea tiles
        board.sea_locations = {(d[i]*size + d[(i+2)%6]*k)%n for i in range(6) for k in range(size)}

        # Specify land tile locations
        board.land_locations = board.all_tile_locations - board.sea_locations

        # Specify locations of desert tiles
        board.desert_locations = {0}

        # Specify locations of resource tiles
        board.resource_locations = board.land_locations - board.desert_locations

        resource_tile_specs = zip(board.resource_locations, Board.random_resource_kinds(), Board.random_number_tokens())

        board.tiles_by_token = {number_token:[] for number_token in range(2,13)}

        for specification in resource_tile_specs:
            board.new_resource_tile(*specification)

        for location in board.desert_locations: board.new_desert_tile(location)

        for location in board.sea_locations: board.new_sea_tile(location)

        board.land_intersections = {intersection for intersection in board.intersections if \
                                    any(isinstance(tile,LandTile) for tile in intersection.neighboring_tiles())}
        board.land_paths = {path for path in board.paths if len(set(path.neighboring_intersections())&board.land_intersections)==2}
        board.available_path_locations = {path.location for path in board.land_paths}
        board.robber_location = random.choice(list(board.desert_locations))

        board.harbor_locations = random.sample(list(board.sea_locations), 9)

        board.generic_harbor_locations = board.harbor_locations[:4]
        for location in board.generic_harbor_locations:
            sea_tile = board.tiles[location]
            sea_tile.harbor = Harbor(sea_tile)
            port_intersections = random.sample(list(board.land_intersections & set(sea_tile.neighboring_intersections())), 2)
            port_locations = [port_intersection.location for port_intersection in port_intersections]
            sea_tile.harbor.ports = port_locations

        board.special_harbor_locations = board.harbor_locations[4:]
        for location, resource in zip(board.special_harbor_locations, [grain, wool, lumber, brick, ore]):
            sea_tile = board.tiles[location]
            sea_tile.harbor = Harbor(sea_tile, 'special', resource)
            port_intersections = random.sample(list(board.land_intersections & set(sea_tile.neighboring_intersections())), 2)
            port_locations = [port_intersection.location for port_intersection in port_intersections]
            sea_tile.harbor.ports = port_locations

        #print(json.dumps(board,cls=BoardEncoder,indent=4))

        # Translation of locations to old system
        board.old_system_cell_count = m = 36 * (size**2) + 54 * size + 21
        board.old_system_directions = od = [pow(6 * size + 5, i, m) for i in range(6)]
        old_system_corner = ( (od[2]+od[3])*2*size + (od[3]+od[4])*2*size )%m
        new_system_corner = ( d[3]*size + d[4]*size )%n
        old_system_tile_loc = [0]*len(board.tiles)
        old_system_path_loc = [0]*len(board.paths)
        old_system_intersection_loc = [0]*len(board.intersections)
        for i in range(size*2+1):
            for j in range(size*2+1):
                if not(size<=i+j<=size*3): continue
                new_loc = (new_system_corner + i*d[0]+j*d[1]) % n
                old_loc = (old_system_corner + i*(od[0]+od[5])*2 + j*(od[1]+od[0])*2) % m
                old_system_tile_loc[new_loc] = old_loc
                old_system_intersection_loc[new_loc*2] = (old_loc+od[4]*2)%m
                old_system_intersection_loc[new_loc*2+1] = (old_loc+od[1]*2)%m
                old_system_path_loc[new_loc*3] = (old_loc + (od[0]+od[5]))%m
                old_system_path_loc[new_loc*3 + 1] = (old_loc + (od[4]+od[3]))%m
                old_system_path_loc[new_loc*3 + 2] = (old_loc + (od[2]+od[1]))%m
        board.old_system_tile_loc = old_system_tile_loc
        board.old_system_path_loc = old_system_path_loc
        board.old_system_intersection_loc = old_system_intersection_loc

    def random_resource_kinds():
        """
        A generator of ResourceKind objects. Ensures that they are produced randomly but still conforming to the proportions of different resources in the original Settlers board.

        :yield: ResourceKind objects
        :rtype: ResourceKind
        """
        # Resource kinds for resource tiles
        while True:
            resource_kinds = [grain]*4 + [wool]*4 + [lumber]*4 + [brick]*3 + [ore]*3
            random.shuffle(resource_kinds)
            for resource_kind in resource_kinds: yield resource_kind

    def random_number_tokens():
        """
        A generator of number tokens. Ensures that they are produced randomly but still conforming to the proportions of different number tokens in the original Settlers board.

        :yield: integers representing the values of number tokens
        :rtype: int
        """

        # Number tokens for resource tiles
        while True:
            number_tokens = [5, 2, 6, 3, 8, 10, 9, 12, 11, 4, 8, 10, 9, 4, 5, 6, 3, 11]
            random.shuffle(number_tokens)
            for number_token in number_tokens: yield number_token


    def add_road(board, road, location):
        """
        Adds a given road token to the board at a given location.

        :param road: The road token to add to the board
        :type road: Road
        :param location: The location at which to place the road. Must be a valid path location.
        :type location: int
        :return: None
        """
        path = board.paths[location]

        if path.road: raise RoadBuildingException(
            "There is already a road built at the given path.")

        # This bit has some tricky logic, don't change unless you're
        # sure you know what you're doing

        for intersection in path.neighboring_intersections():
            if intersection.settlement:
                if intersection.settlement.owner is road.owner:
                    path.road = road
                    road.path = path
                    board.available_path_locations.discard(location)
                    return
            else:
                paths_this_side = [(path,path.road) for path in intersection.neighboring_paths()]
                paths_this_side = [path for path in intersection.neighboring_paths() \
                                   if path.road and path.road.owner is road.owner]
                if paths_this_side:
                    path.road = road
                    road.path = path
                    board.available_path_locations.discard(location)
                    return
        raise RoadBuildingException("Player can't reach given path")

    def add_settlement(board, settlement, location, allow_disconnected_settlement=True):
        """
        Adds a given settlement token to the board at a given location.

        :param settlement: The settlement token to add to the board
        :type settlement: Settlement
        :param location: The location at which to place the settlement. Must be a valid intersection location.
        :type location: int
        :param allow_disconnected_settlement: a boolean indicating whether the settlement can be placed on the board at a location which is not connected to any of the player's existing roads.
        :type allow_disconnected_settlement: bool
        :return: None
        """

        intersection = board.intersections[location]

        if intersection.settlement:
            raise SettlementBuildingException(
                "There is already a settlement built at the given intersection."
            )

        is_connected = settlement.owner in [path.road.owner for path in \
                                            intersection.neighboring_paths() if path.road]

        if not allow_disconnected_settlement and not is_connected:
            raise SettlementBuildingException(
                "Settlement can't be built because intersection is not connected to a road of the settlement's color."
            )

        if intersection.neighboring_settlements():
            raise SettlementBuildingException(
                "Settlement can't be built at this intersection because it's too close to another settlement."
            )

        intersection.settlement = settlement
        settlement.intersection = intersection

        for harbor in intersection.harbors():
            print(harbor)
            settlement.owner.update_exchange_rate(harbor.flavor=='special',harbor.resource)

    def get_settlements_and_cities(board):
        """
        Generates a dictionary which maps players to the settlements and cities they have placed on the board.

        :return: a dictionary which maps players to the settlements and cities they have placed on the board.
        :rtype: dict[Player,list[Settlement]]
        """
        settlement_dict = {}
        for intersection in board.intersections:
            if intersection.settlement:
                settlement = intersection.settlement
                if settlement.owner in settlement_dict:
                    settlement_dict[settlement.owner].append(settlement)
                else: settlement_dict[settlement.owner] = [settlement]
        return settlement_dict


    def valid_settlement_intersections(board, player, needs_to_be_reachable=True):
        """
        Generates a list of intersections at which the given player can build a settlement.

        :param player: The player who is to build a settlement.
        :type player: Player
        :param needs_to_be_reachable: True if the newly built settlement needs to be connected to the player's existing roads, False otherwise.
        :type needs_to_be_reachable: bool
        :return: a list of intersections that the player can build a settlement at
        :rtype: list[Intersection]
        """
        occupied_intersections = [intersection for intersection in board.intersections if intersection.settlement]

        blocked_intersections = join([intersection.neighboring_intersections() for intersection in occupied_intersections])

        unavailable_intersections = set(occupied_intersections) | set(blocked_intersections)

        if not needs_to_be_reachable:
            return list(set(board.land_intersections) - unavailable_intersections)

        reachable_intersections = join([path.neighboring_intersections() for path in board.paths if path.road])

        return list(set(reachable_intersections) - unavailable_intersections)

    def valid_settlement_locations(board, player, needs_to_be_reachable=True):
        """
        Generates a list of intersection locations at which the given player can build a settlement.

        :param player: The player who is to build a settlement.
        :type player: Player
        :param needs_to_be_reachable: True if the newly built settlement needs to be connected to the player's existing roads, False otherwise.
        :type needs_to_be_reachable: bool
        :return: a list of intersection locations that the player can build a settlement at
        :rtype: list[int]
        """
        return [intersection.location for intersection in board.valid_settlement_intersections(player,needs_to_be_reachable)]

    def new_intersection(board, location):
        """
        Adds a new Intersection object to the board at the given location.

        :param location: The location of the new intersection.
        :type location: int
        :return: the newly created Intersection object
        :rtype: Intersection
        """
        board.intersections[location] = Intersection(board, location)
        return board.intersections[location]

    def new_path(board, location):
        """
        Adds a new Path object to the board at the given location.

        :param location: The location of the new path.
        :type location: int
        :return: the newly created Path object
        :rtype: Path
        """
        board.paths[location] = Path(board, location)
        return board.paths[location]

    def new_resource_tile(board, location, resource_kind, number_token):
        """
        Adds a new ResourceTile object to the board at the given location.

        :param location: The location of the new resource tile.
        :type location: int
        :return: the newly created ResourceTile object
        :rtype: ResourceTile
        """
        board.tiles[location] = ResourceTile(board, location, resource_kind, number_token)
        board.tiles_by_token[number_token].append(board.tiles[location])
        return board.tiles[location]

    def new_desert_tile(board, location):
        """
        Adds a new DesertTile object to the board at the given location.

        :param location: The location of the new desert tile.
        :type location: int
        :return: the newly created DesertTile object
        :rtype: DesertTile
        """
        board.tiles[location] = DesertTile(board, location)
        return board.tiles[location]

    def new_sea_tile(board, location):
        """
        Adds a new SeaTile object to the board at the given location.

        :param location: The location of the new sea tile.
        :type location: int
        :return: the newly created SeaTile object
        :rtype: SeaTile
        """
        board.tiles[location] = SeaTile(board, location)
        return board.tiles[location]

    def to_json(board):
        tiles = board.tiles + list(board.land_paths) + list(board.land_intersections)
        tiles = [t.to_json() for t in tiles]
        tiles2 = [None] * board.old_system_cell_count
        for t in tiles: tiles2[t['location']] = t
        for i in range(len(tiles2)):
            if tiles2[i] is None: tiles2[i] = {'type': 'null', 'location': i}
        return {'size': board.size, 'directions': board.old_system_directions, \
                'tiles': tiles2}

class BoardEncoder(json.JSONEncoder):
    def default(self, obj):
        return obj.to_json()

class RoadBuildingException(Exception): pass

class SettlementBuildingException(Exception): pass

class HarborException(Exception): pass