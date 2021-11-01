class V:
  def __init__(self, *args):
    if len(args) == 1:
      if type(args[0]) == dict:
        self.x = args[0]["x"]
        self.y = args[0]["y"]
      else:
        if args[0] == "up":
          self.x = 0
          self.y = 1
        elif args[0] == "right":
          self.x = 1
          self.y = 0
        elif args[0] == "down":
          self.x = 0
          self.y = -1
        elif args[0] == "left":
          self.x = -1
          self.y = 0
        else:
          raise(ValueError())
    else:
      self.x = args[0]
      self.y = args[1]
  
  def __str__(self):
    return f"V(x:{self.x}, y:{self.y})"
  
  def __repr__(self):
    return self.__str__()
  
  def __eq__(self, other):
    return self.x == other.x and self.y == other.y
  
  def __add__(self, other):
    return V(self.x + other.x, self.y + other.y)

  def __sub__(self, other):
    return V(self.x - other.x, self.y - other.y)

  def __mul__(self, other):
    if type(other) == int:
      return V(self.x * other, self.y * other)
    else:
      return V(self.x * other.x, self.y * other.y)

  def __abs__(self):
    return V(abs(self.x), abs(self.y))

  def __hash__(self):
    return hash((self.x, self.y))
  
  def length_sq(self):
    return self.x ** 2 + self.y ** 2

  def length(self):
    return self.length_sq() ** 0.5
  
  def taxi(self, other):
    d = (self - other)
    return abs(d.x) + abs(d.y)

class Board:
  def __init__(self, w, h):
    self.w = w
    self.h = h
    self.board = []
    for i in range(h):
      self.board.append([0] * w)
  
  def set(self, *args):
    if len(args) == 2:
      y, x, s = args[1].y, args[1].x, args[0]
    else:
      y, x, s = args[2], args[1], args[0]
    
    if 0 <= y < self.h and 0 <= x < self.w:
      if self.board[y][x] < s:
        self.board[y][x] = s
  
  def add_snake(self, snake, head, add_head_next):
    for i, cell in enumerate(reversed(snake)):
      if i == 0:
        continue
      if head.taxi(cell) <= i:
        self.set(9999999999, cell)
      else:
        self.set(2, cell)
    if add_head_next:
      self.set(11, snake[0] + V("up"))
      self.set(11, snake[0] + V("right"))
      self.set(11, snake[0] + V("down"))
      self.set(11, snake[0] + V("left"))
  
  def add_hazzards(self, hazzards):
    for hazzard in hazzards:
      self.set(5, hazzard)
  
  def get(self, *args):
    if len(args) == 1:
      y, x = args[0].y, args[0].x
    else:
      y, x = args[1], args[0]
    
    if 0 <= y < self.h and 0 <= x < self.w:
      return self.board[y][x]
    else:
      return 9999999999
  
  def __getitem__(self, v):
    return self.get(v)
