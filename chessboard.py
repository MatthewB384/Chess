#generates a chessboard with n players

from turtle import Turtle
from math import *

def da(distance=0, angle:'radians'=0)->'point':
  return distance*cos(angle),distance*sin(angle)

def avg(*points):
  sumx = sum([point[0] for point in points])
  sumy = sum([point[1] for point in points])
  sumx /= len(points)
  sumy /= len(points)
  return sumx, sumy

def along(p1, p2, ratio):
  x = p1[0] + (p2[0]-p1[0])*ratio
  y = p1[1] + (p2[1]-p1[1])*ratio
  return x,y

tau = 2*pi

class T(Turtle):
  def __init__(self, shape='classic', undobuffersize=1000, visible=True):
    super().__init__(shape, undobuffersize, visible)
    self.speed(0)
    self.hideturtle()

  def w(self, text, where):
    self.goto(where[0]-2, where[1]-7)
    self.write(text)

  def chessboard(self, players, *, clear=True):
    if clear:
      self.clear()
    players *= 2
      
    corners = [da(300,tau/players*i) for i in range(players)]
    mids = [along(corners[i], corners[(i+1)%players], 0.5) for i in range(players)]
    
    self.pu()#draw outline
    self.goto(*corners[-1])
    self.pd()
    for corner in corners:
      self.goto(*corner)

    for mid in mids:#draw radial lines
      self.pu()
      self.goto(0,0)
      self.pd()
      self.goto(*mid)

    for side in range(players):#draw squares
      for i in range(1,4):
        self.pu()
        self.goto(*along(corners[side], mids[side], i/4))
        self.pd()
        self.goto(*along(mids[(side-1)%players], (0,0), i/4))
        self.goto(*along(corners[(side-1)%players], mids[(side-2)%players], i/4))

    self.pu()
    for player in range(0,players, 2):#draw pieces
      for pawn in range(4):
        self.w('P', along(along(corners[player], mids[(player-1)%players], 0.375), along(mids[player], (0,0), 0.375), pawn/4+0.125))
        self.w('P', along(along(corners[(player+1)%players], mids[(player+1)%players], 0.375), along(mids[player], (0,0), 0.375), pawn/4+0.125))
        self.w('RNBQ'[pawn], along(along(corners[player], mids[(player-1)%players], 0.125), along(mids[player], (0,0), 0.125), pawn/4+0.125))
        self.w('RNBK'[pawn], along(along(corners[(player+1)%players], mids[(player+1)%players], 0.125), along(mids[player], (0,0), 0.125), pawn/4+0.125))
   
t = T()
