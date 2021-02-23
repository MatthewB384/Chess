#INFINITE CEHSS
from math import inf, ceil
import pygame

class piece:
  def __init__(self,x,y,c,slides,zigzags,knights):
    self.x = x
    self.y = y
    self.c = c
    self.slides = slides
    self.zigzags = zigzags
    self.knights = knights

  def can_move(self,x,y):
    if self.slides:
      if self.x == x:
        if abs(self.y - y) <= self.slides:
          return True
        
      if self.y == y:
        if abs(self.x - x) <= self.slides:
          return True
      
    if self.zigzags:
      if self.x + self.y == x + y or self.x - self.y == x - y:
        if abs(self.x - x)  <= self.zigzags:
          return True

    if self.knights:
      if sorted(map(abs,[self.x-x,self.y-y])) == [1,2]:
        return True

    return False
        

class rook(piece):
  def __init__(self,x,y,c):
    super().__init__(x,y,c,inf,0,0)
    
class bishop(piece):
  def __init__(self,x,y,c):
    super().__init__(x,y,c,0,inf,0)

class queen(piece):
  def __init__(self,x,y     ,c):
    super().__init__(x,y,c,inf,inf,0)

class king(piece):
  def __init__(self,x,y,c):
    super().__init__(x,y,c,1,1,0)

class knight(piece):
  def __init__(self,x,y,c):
    super().__init__(x,y,c,0,0,1)
    
    
class board:
  def __init__(self):
    self.kings = [king(0,0,1),king(3,6,0)]
    self.queens = []
    self.rooks = []
    self.bishops = []
    self.pawns = []
    self.knights = []
    self.center = [0,0]
    self.current_center = [0,0]
    self.current_radius = 2
    self.size = 64

  def pieces(self):
    return self.kings + self.queens + self.rooks + self.bishops + self.pawns + self.knights

  def get_center_square(self):
    x = (self.kings[0].x + self.kings[1].x) // 2
    y = (self.kings[0].y + self.kings[1].y) // 2
    return x,y

  def get_scale(self):
    c = self.get_center_square()
    mr = 1
    for piece in self.pieces():
      d = (piece.x - c[0])**2 + (piece.y - c[1])**2
      if d > mr:
        mr = d
    return int(d**0.5) + 3

  def load_image(self):
    r = ceil((640/self.size + 5)/10)
    boards = {}
    for x in range(-r,r+1):
      for  y in range(-r,r+1):
        b = pygame.image.load(r'C:\Users\61490\Documents\Python\Chess\chess_board.png')
        b = pygame.transform.scale(b,(int(self.size*10),int(self.size*10)))
        display_surface.blit(b,(self.center[0] + self.size*10*x, self.center[1] + self.size*10*y))

  def update_image(self):
    
    
        
        

    


pygame.init()

FramePerSec = pygame.time.Clock()

display_surface = pygame.display.set_mode((640,640))
pygame.display.set_caption('Image')


b = board()

while 1:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()

      

  pressed_keys = pygame.key.get_pressed()
  if pressed_keys[pygame.K_a]:
      b.center[0] -= 3
  if pressed_keys[pygame.K_d]:
      b.center[0] += 3
  if pressed_keys[pygame.K_w]:
      b.center[1] -= 3
  if pressed_keys[pygame.K_s]:
      b.center[1] += 3
  if pressed_keys[pygame.K_q]:
      b.size *= 1.1
  if pressed_keys[pygame.K_e]:
      b.size /= 1.1
  

  display_surface.fill((0,0,0))
  b.load_image()
  pygame.display.update()
  FramePerSec.tick(60)

