import random
from functools import reduce


def join(l):
    return list(set(reduce(lambda x, y: x + y, l)))


class Settlement:

    def __init__(settlement, owner):
        settlement.owner = owner
        settlement.color = owner.color


class Intersection:

    def __init__(intersection):
        intersection.has_settlement = False

    def build_settlement(intersection, settlement):
        intersection.settlement = settlement
        intersection.has_settlement = True


class City(Settlement):
    pass


class Road:

    def __init__(road, location, owner):
        road.location = location
        road.owner = owner
        road.color = owner.color


class Path:

    def __init__(self, location):
        self.location = location
        self.has_road = False

    def build_road(self, road):
        self.road = road
        self.has_road = True


class Tile:

    def __init__(tile, location, resource, number_token):
        tile.location = location
        tile.resource = resource
        tile.number_token = number_token


class Board:

    # Spec says Board should be initializable with a game state
    def __init__(board, size=3, initial_data=None):

        # Size of the board is the number of tiles at each edge
        board.size = n = size

        # Cell count is the number of hexagonal cells it contains
        # Cells can contain tiles, intersections, paths, etc.
        board.cell_count = m = 36 * n * n + 54 * n + 21

        # The six cardinal directions, represented as integers
        # This array contains, in order: northeast, north, northwest, southwest, south, and southeast

        board.cardinal_directions = d = [
            pow(6 * n + 5, i, m) for i in range(6)
        ]

        # Using this layout, if X is the index of a cell,
        #  (X + cardinal_directions[3]*2)%board.cell_count would be the index
        #  of the cell 2 steps away in the southwest direction from cell X

        board.cells = [None] * board.cell_count
        board.harbors = board.select(0, size, dir_pattern=(2, 2))
        board.bridges = join(board.select(h, 1) for h in board.harbors)
        board.tiles = join(
            board.select(0, i, dir_pattern=(2, 2)) for i in range(n)) + [0]
        board.intersections = join(
            board.select(t, 1, (2, )) for t in board.tiles)
        board.paths = join(board.select(t, 1, (1, 1)) for t in board.tiles)

        for location in board.intersections:
            board.cells[location] = Intersection()
        for location in board.paths:
            board.cells[location] = Path(location)

        board.desert_tiles = [0]
        board.resource_number = len(board.tiles) - len(board.desert_tiles)
        resources = ['grain'] * 4 + ['wool'] * 4 + ['lumber'] * 4 + [
            'brick'
        ] * 3 + ['ore'] * 3
        number_tokens = [
            5, 2, 6, 3, 8, 10, 9, 12, 11, 4, 8, 10, 9, 4, 5, 6, 3, 11
        ]
        board.resources = (resources * (
            (board.resource_number + 17) // 18))[:board.resource_number]
        board.number_tokens = (number_tokens * (
            (board.resource_number + 17) // 18))[:board.resource_number]
        random.shuffle(board.resources)
        random.shuffle(board.number_tokens)
        del resources, number_tokens

        for location in board.tiles:
            resource = 'nothing' if (
                location in board.desert_tiles) else board.resources.pop()
            number_token = None if (
                location in board.desert_tiles) else board.number_tokens.pop()
            tile = Tile(location, resource, number_token)
            board.cells[location] = tile

    def select(board,
               around,
               distance,
               dir_pattern=None,
               matching=lambda o: True,
               return_cells=False):

        if dir_pattern == None: directions = board.cardinal_directions
        else:
            directions = [
                sum(board.cardinal_directions[(i + j) % 6] * dir_pattern[j]
                    for j in range(len(dir_pattern))) % board.cell_count
                for i in range(6)
            ]

        out = [
            (around + distance * directions[i] + directions[(i + 2) % 6] * j) %
            board.cell_count for i in range(6) for j in range(distance)
        ]
        r = list(filter(matching, out))
        return map(lambda n: board.cells[n], r) if return_cells else r

    def has_path(board, location):
        return type(board.cells[location]) is Path

    def has_intersection(board, location):
        return type(board.cells[location]) is Intersection

    def add_road(board, location, road):

        if not board.has_path(location):
            raise Exception('Given cell is not a path')

        if board.cells[location].has_road:
            raise Exception('There is already a road built at the given path.')

        neighboring_intersections = board.select(
            location, 1, matching=board.has_intersection, return_cells=True)

        for intersection in neighboring_intersections:

            if intersection.has_settlement:
                if intersection.settlement.owner == road.owner:
                    board.cells[location].build_road(road)
                    return

            else:
                paths_this_side = board.select(location,
                                               1, (1, 1),
                                               matching=board.has_path,
                                               return_cells=True)
                if road.owner in [
                        path.road.owner for path in paths_this_side
                        if path.has_road
                ]:
                    board.cells[location].build_road(road)
                    return

        raise Exception("Player can't reach given path")

    def add_settlement(board, location, settlement,
                       allow_disconnected_settlement):

        if not board.has_intersection(location):
            raise Exception('Given cell is not an intersection')

        if board.cells[location].has_settlement:
            raise Exception(
                'There is already a settlement built at the given intersection.'
            )

        adjacent_paths = board.select(location,
                                      1,
                                      matching=board.has_path,
                                      return_cells=True)

        if not allow_disconnected_settlement and not settlement.owner in [
                path.road.owner for path in adjacent_paths if path.has_road
        ]:
            raise Exception(
                "Settlement can't be built because intersection is not connected to a road of the settlement's color."
            )

        neighboring_intersections = board.select(
            location,
            1, (2, ),
            matching=board.has_intersection,
            return_cells=True)

        if [
                intersection for intersection in neighboring_intersections
                if intersection.has_settlement
        ]:
            raise Exception(
                "Settlement can't be built at this intersection because it's too close to another settlement."
            )

        board.cells[location].build_settlement(settlement)

    def upgrade_settlement(board, location):

        if not board.has_intersection(location):
            raise Exception('Given cell is not an intersection.')

        if not board.cells[location].has_settlement:
            raise Exception('No settlement to upgrade at given intersection.')

        board.cells[location].settlement = City(
            board.cells[location].settlement.owner)

    def get_settlements_and_cities(board):
        settlement_dict = {player:[] for player in board.game.players}
        for location in board.intersections:
            intersection = board.cells[location]
            if intersection.has_settlement:
                settlement = intersection.settlement
                settlement_dict[settlement.owner].append(settlement)
        return settlement_dict



    # This should return the board state in some format which the board can be initialized from
    def save_state(board):
        pass
