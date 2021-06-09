#generates a chessboard with n players

import turtle, math

def da(distance=0, angle:'radians'=0)->'point':
  return distance*math.cos(angle), distance*math.sin(angle)

def along(p1:'point', p2:'point', ratio:('0<ratio<1'))->'point':
  return p1[0]+(p2[0]-p1[0])*ratio, p1[1]+(p2[1]-p1[1])*ratio

tau = 2*math.pi
colours = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'lawn green', 'magenta', 'dodger blue', 'pink', 'maroon', 'silver', 'black']

class T(turtle.Turtle):
  def __init__(self, shape='classic', undobuffersize=1000, visible=True):
    super().__init__(shape, undobuffersize, visible)
    self.speed(0)
    self.hideturtle()

  def w(self, text, where):
    self.goto(where[0]-2, where[1]-7)
    self.write(text)

  def chessboard(self, players, *, clear=True,  pieces='RNBQKBNR'):
    if clear:
      self.clear()
    players = int(players*2)
    n = len(pieces)//2
    self.pencolor('black')

    print('Generating sides...')
    corners = [da(330,tau/players*i) for i in range(players)]
    mids = [along(corners[i], corners[(i+1)%players], 0.5) for i in range(players)]

    print('Drawing outline...')
    self.pu()#draw outline
    self.goto(*corners[-1])
    self.pd()
    for corner in corners:
      self.goto(*corner)

    print('Drawing radial lines...')
    for mid in mids:#draw radial lines
      self.pu()
      self.goto(0,0)
      self.pd()
      self.goto(*mid)

    print('Drawing squares...')
    for side in range(players):#draw squares
      for i in range(1,n):
        self.pu()
        self.goto(*along(corners[side], mids[side], i/n))
        self.pd()
        self.goto(*along(mids[(side-1)%players], (0,0), i/n))
        self.goto(*along(corners[(side-1)%players], mids[(side-2)%players], i/n))

    print('Drawing pieces...')
    self.pu()
    for player in range(1,players, 2):#draw pieces
      self.pencolor(colours[player//2%len(colours)])
      for pawn in range(n):
        self.w('P', along(along(corners[player], mids[(player-1)%players], 3/(2*n)), along(mids[player], (0,0), 3/(2*n)), pawn/n+1/(2*n)))
        self.w('P', along(along(corners[(player+1)%players], mids[(player+1)%players], 3/(2*n)), along(mids[player], (0,0), 3/(2*n)), pawn/n+1/(2*n)))
        self.w(pieces[pawn], along(along(corners[player], mids[(player-1)%players], 1/(2*n)), along(mids[player], (0,0), 1/(2*n)), pawn/n+1/(2*n)))
        self.w(pieces[::-1][pawn], along(along(corners[(player+1)%players], mids[(player+1)%players], 1/(2*n)), along(mids[player], (0,0), 1/(2*n)), pawn/n+1/(2*n)))

    print('Done!')
   
t = T()
c = t.chessboard
