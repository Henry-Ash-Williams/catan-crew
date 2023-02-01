from functools import reduce

def join(l): return reduce(lambda x,y: x+y, l)

class Intersection:
  
  def __init__(self):
    self.has_settlement = False
  
  def build_settlement(self, color):
    self.settlement = Settlement(color)
    self.has_settlement = True

class Settlement:
  def __init__(self, color): self.color = color

class City(Settlement): pass

class Road:
  def __init__(self, color): self.color = color

class Path:

  def __init__(self):
    self.has_road = False
  
  def build_road(self, color):
    self.road = Road(color)
    self.has_road = True

class Board:

  # Spec says Board should be initializable with a game state
  def __init__(self, size=3, initial_data=None):
      
    n = self.size  = size
    m = self.mod   = 36*n*n + 54*n + 21
    q = self. dirs = [1, (6*n+5)%m, (6*n+4)%m, (-1)%m, (-6*n-5)%m, (-6*n-4)%m]
    
    self.cells         = [None]*self.mod
    self.harbors       = self.select(0,size,dir_pattern=(2,2))
    self.bridges       = join(self.select(h,1) for h in self.harbors)
    self.tiles         = [0]+join(self.select(0,i,dir_pattern=(2,2)) for i in range(n))
    self.intersections = list(set(join(self.select(t,1,(2,)) for t in self.tiles)))
    self.paths         = list(set(join(self.select(t,1,(1,1)) for t in self.tiles)))
    
    for cell_num in self.intersections: self.cells[cell_num] = Intersection()
    for cell_num in self.paths:         self.cells[cell_num] = Path()
    
  def select(board, location, distance, dir_pattern = None, matching = lambda o: True, return_cells=False):
  
    if dir_pattern == None: dirs = board.dirs
    else: dirs = [sum(board.dirs[(i+j)%6]*dir_pattern[j] for j in range(len(dir_pattern)))%board.mod for i in range(6)]
    
    out = [(location + distance*dirs[i] + dirs[(i+2)%6]*j)%board.mod for i in range(6) for j in range(distance)]
    r = list(filter(matching, out))
    return map(lambda n: board.cells[n], r) if return_cells else r
    
  def has_path(self, cell_num): return type(self.cells[cell_num]).__name__ == 'Path'
  
  def has_intersection(self, cell_num): return type(self.cells[cell_num]).__name__ == 'Intersection'
  
  def verify_current_player_is(board, color):
    if color != board.game.current_player.color:
      raise Exception("Player (%s) can't play as it's (%s)'s turn."%(color,board.game.current_player.color))
  
  def add_road(board, cell_num, color):
  
    board.verify_current_player_is(color)
    
    if not board.has_path(cell_num):
      raise Exception('Given cell is not a path')
    
    if board.cells[cell_num].has_road:
      raise Exception('There is already a road built at the given path.')
    
    neighboring_intersections = board.select(cell_num, 1, matching = board.has_intersection, return_cells = True)
    
    for intersection in neighboring_intersections:
    
      if intersection.has_settlement:
        if intersection.settlement.color==color:
          board.cells[cell_num].build_road(color)
          return
    
      else:
        paths_this_side = board.select(cell_num, 1, (1,1), matching = board.has_path, return_cells = True)
        if color in [path.road.color for path in paths_this_side if path.has_road]:
          board.cells[cell_num].build_road(color)
          return
    
    raise Exception("Player can't reach given path")
  
  def add_settlement(board, cell_num, color):
  
    board.verify_current_player_is(color)
    
    if not board.has_intersection(cell_num):
      raise Exception('Given cell is not an intersection')
    
    if board.cells[cell_num].has_settlement:
      raise Exception('There is already a settlement built at the given intersection.')
    
    adjacent_paths = board.select(cell_num, 1, matching = board.has_path, return_cells = True)
    
    if not board.game.is_just_starting and not color in [path.road.color for path in adjacent_paths if path.has_road]:
      raise Exception("Settlement can't be built because intersection is not connected to a road of the settlement's color.")
    
    neighboring_intersections = board.select(cell_num, 1, (2,), matching = board.has_intersection, return_cells = True)
    
    if color in [intersection.settlement.color for intersection in neighboring_intersections if intersection.has_settlement]:
      raise Exception("Settlement can't be built at this intersection because it's too close to another settlement.")
    
    board.cells[cell_num].build_settlement(color)
    
  def upgrade_settlement(board, cell_num):
    
    if not board.has_intersection(cell_num):
      raise Exception('Given cell is not an intersection.')
    
    if not board.cells[cell_num].has_settlement:
      raise Exception('No settlement to upgrade at given intersection.')    
    
    board.cells[cell_num].settlement = City(board.cells[cell_num].settlement.color)
  
  # This should return the board state in some format which the board can be initialized from
  def save_state(board):
    pass
