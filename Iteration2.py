#this is chess but as fast as i can make it
#i want it to be efficient to give me a chance of making a somewhat competent ai

from colored import fg,attr
from os import system as sys
from winsound import Beep
colours = [242,255,236,76]

square_order = [range(64),range(63,-1,-1)]

class board:
  def __init__(self):
    self.squares = [
      'R','N','B','Q','K','B','N','R',
      'P','P','P','P','P','P','P','P',
      '','','','','','','','',
      '','','','','','','','',
      '','','','','','','','',
      '','','','','','','','',
      'p','p','p','p','p','p','p','p',
      'r','n','b','q','k','b','n','r'
    ]
    self.turn = 1
    self.castle = {'K':1,'Q':1,'k':1,'q':1}
    self.kings = [60,4]
    self.last_move = (None,None)

    self.piece_values = {
      '':0,
      'p':-1,'n':-3,'b':-3,'r':-5,'q':-9,'k':0,
      'P':1,'N':3,'B':3,'R':5,'Q':9,'K':0
    }
      

  def __repr__(self):
    b = 0
    r=''
    for row in range(56,-1,-8):
      for pos in range(8):
        if self.squares[row+pos]:
          if b:
            r+=f'{b}'
            b=0
          r+=self.squares[row+pos]
        else:
          b+=1
      if b:
        r+=f'{b}'
        b=0
      r+='/'
    c = ''.join([c for c in self.castle if self.castle[c]])
    l = mn(self.last_move) if self.last_move else self.last_move
    return f'{r[:-1]} {["b","w"][self.turn%2]} {c} {l}'


  def __str__(self):
    if colour:
      return '%s+ A B C D E F G H +\n%s'%(fg(colours[2]),attr(0))+'\n'.join([f'%s{8-n} %s'%(fg(colours[2]),attr(0))+' '.join([f'%s{self.squares[row+pos]}%s'%(fg(colours[3] if (row+pos) in self.last_move else  colours[self.squares[row+pos].isupper()]), attr(0)) if self.squares[row+pos] else '%s·%s'%(fg(colours[3] if (row+pos) in self.last_move else colours[2]),attr(0)) for pos in range(8)])+f'%s {8-n}%s'%(fg(colours[2]),attr(0)) for n,row in enumerate(range(56,-1,-8))])+'%s\n+ A B C D E F G H +%s'%(fg(236),attr(0))
    else:
      return '+ A B C D E F G H +\n'+'\n'.join([f'{8-n} '+' '.join([f'{self.squares[row+pos]}' if self.squares[row+pos] else '·' for pos in range(8)])+f' {8-n}' for n,row in enumerate(range(56,-1,-8))])+'\n+ A B C D E F G H +'

  def __iter__(self):
    return iter(self.squares)


  def __getitem__(self,index):
    return self.squares[index]


  def is_col(self,s,c):
    if self.squares[s]:
      return self.squares[s].isupper() == c
    return False
  

  def is_w(self,s):
    return self.squares[s].isupper()
  

  def is_b(self,s):
    return self.squares[s] and not self.squares[s].isupper()
  

  def not_w(self,s):
    return not self.is_w(s)
  

  def not_b(self,s):
    return not self.is_b(s)
  

  def marks(self,s):
    p = self.squares[s]
    r,f = pl(s)
    squares = []

    if p.lower()=='k':
      squares += form([(r-1,f-1),(r-1,f),(r-1,f+1),(r,f-1),(r,f+1),(r+1,f-1),(r+1,f),(r+1,f+1)])

    if p.lower() == 'n':
      squares += form([(r-2,f-1),(r-1,f-2),(r-2,f+1),(r+2,f-1),(r-1,f+2),(r+1,f-2),(r+1,f+2),(r+2,f+1)])

    if p.lower() == 'p':
      squares += form([(r+2*p.isupper()-1,f-1),(r+2*p.isupper()-1,f+1)])

    if p.lower() in ('r','q'):
      for d in [[-1,0],[0,-1],[1,0],[0,1]]:
        for i in range(1,8):
          if not o((r+d[0]*i,f+d[1]*i)):
            break
          squares.append((r+d[0]*i)*8+f+i*d[1])
          if self.squares[squares[-1]]:
            break

    if p.lower() in ('b','q'):
      for d in [[-1,-1],[1,-1],[-1,1],[1,1]]:
        for i in range(1,8):
          if not o((r+d[0]*i,f+d[1]*i)):
            break
          squares.append((r+d[0]*i)*8+f+i*d[1])
          if self.squares[squares[-1]]:
            break

    return squares



  def moves(self,s):
    p  = self.squares[s]
    r,f = pl(s)
    squares = []

    if p.lower() == 'k':
      pots = set(filter(eval(f'self.not_{["b","w"][p.isupper()]}'),self.marks(s)))
      for i in range(64):
        if not pots:
          break
        if self.is_col(i,2+~p.isupper()):
          pots -= set(self.marks(i))
      squares += pots
      if not self.check(p.isupper()):
        if self.castle[['k','K'][p.isupper()]]:
          if not ''.join(self.squares[s+1:s+3]):
            for square in [s+1,s+2]:
              if self.marked(square,2+~p.isupper()):
                break
            else:
              squares.append(s+2)
        if self.castle[['q','Q'][p.isupper()]]:
          if not ''.join(self.squares[s-3:s]):
            for square in [s-2,s-1]:
              if self.marked(square,2+~p.isupper()):
                break
            else:
              squares.append(s-2)
      

    if p.lower() == 'n':
      squares += filter(eval(f'self.not_{["b","w"][p.isupper()]}'),self.marks(s))

    if p.lower() == 'p':
      d = p.isupper()*16-8
      if not self.squares[s+d]:
        squares.append(s+d)
        if s//8 == p.isupper()*-5 + 6:
          if not self.squares[s+2*d]:
            squares.append(s+2*d)
      if s%8:
        if self.is_col(s+d-1,2+~p.isupper()):
          squares.append(s+d-1)
        if s//8 == p.isupper()+3:
          if self.squares[s-1] == ['P','p'][p.isupper()]:
            if self.last_move == (s+2*d-1,s-1):
              squares.append(s+d-1)
      if s%8-7:
        if self.is_col(s+d+1,2+~p.isupper()):
          squares.append(s+d+1)
        if s//8 == p.isupper()+3:
          if self.squares[s+1] == ['P','p'][p.isupper()]:
            if self.last_move == (s+2*d+1,s+1):
              squares.append(s+d+1)


    if p.lower() in ['r','q']:
      for d in [[-1,0],[0,-1],[1,0],[0,1]]:
        for i in range(1,8):
          if not o((r+d[0]*i,f+d[1]*i)):
            break
          sq = (r+d[0]*i)*8+f+i*d[1]
          if not self.is_col(sq,p.isupper()):
            squares.append(sq)
          if self.squares[sq]:
            break
          

    if p.lower() in ['b','q']:
      for d in [[-1,-1],[1,-1],[1,1],[-1,1]]:
        for i in range(1,8):
          if not o((r+d[0]*i,f+d[1]*i)):
            break
          sq = (r+d[0]*i)*8+f+i*d[1]
          if not self.is_col(sq,p.isupper()):
            squares.append(sq)
          if self.squares[sq]:
            break
    return squares


  def marked(self,s,c):
    for i in range(64):
      if self.is_col(i,c):
        if s in self.marks(i):
          return True
    return False



  def check(self,c):
    k = self.kings[c]
    ocol = 1-c
    for s in range(64):
      if self.is_col(s,ocol):
        p = self.squares[s]
        #print(s,p)
        if p.lower() in ['p','n']:
          if k in self.marks(s):
            return True
        if p.lower() in ['r','q']:
          if s%8 == k%8:
            if k in self.marks(s):
              return True
          elif s//8 == k//8:
            if k in self.marks(s):
              return True
        if p.lower() in ['b','q']:
          #print('looking at queen or bishop')
          if s%9 == k%9:
            #print('queen is on the same diagonal')
            if k in self.marks(s):
              #print('queen sees the king')
              return True
          elif s%7 == k%7:
            if k in self.marks(s):
              return True
        elif p.lower() == 'k':
          continue
    return False


  def move(self,start,fin):
    if self.squares[start].lower() == 'p':
      if fin//8 == self.squares[start].isupper()*7:
        self.squares[start] = ['q','Q'][self.squares[start].isupper()]
      if start%8 != fin%8:
        if not self.squares[fin]:
          self.squares[start//8*8+fin%8] = ''
    self.squares[fin] = self.squares[start]
    self.squares[start] = ''
    if self.squares[fin].lower() == 'k':
      if start in [4,60]:
        if fin == start + 2:
          self.squares[start+1] = self.squares[start+3]
          self.squares[start+3] = ''
        elif fin == start - 2:
          self.squares[start-1] = self.squares[start-4]
          self.squares[start-4] = ''
        self.castle[['q','Q'][self.squares[fin].isupper()]] = 0
        self.castle[['k','K'][self.squares[fin].isupper()]] = 0
      self.kings[self.squares[fin].isupper()] = fin
    if start in [0,56]:
      if self.squares[fin].lower() == 'r':
        self.castle[['q','Q'][self.squares[fin].isupper()]] = 0
    if start in [7,63]:
      if self.squares[fin].lower() == 'r':
        self.castle[['k','K'][self.squares[fin].isupper()]] = 0
    self.last_move = (start,fin)
    self.turn += 1


  def sim_move(self,start,fin):
    sim = board()
    sim.squares = self.squares.copy()
    sim.turn = self.turn
    sim.castle = self.castle.copy()
    sim.kings = self.kings.copy()
    sim.last_move = self.last_move
    
    sim.move(start,fin)
    return sim


  def all_moves(self,c):
    moves = []
    for i in range(64):
      if self.is_col(i,c):
        for move in self.moves(i):
          sim = self.sim_move(i,move)
          if sim.check(c):
            continue
          moves.append((i,move))
    return moves
  

  


  def mv(self,notation):
    self.move(np(notation[:2]),np(notation[2:]))
    print(self)


def o(position):
  '''Determines whether a position in the form of an iterable with the form
[rank, file] lies on the chess board'''
  return 0<=min(position) and 7>=max(position)

def pn(cellnum):
  if cellnum == None:
    return '-1'
  return f'{chr(97+cellnum%8)}{cellnum//8+1}'

def np(notation):
  return ord(notation[0].lower())+(int(notation[1])-1)*8-97

def lp(list):
  return 8*list[0]+list[1]

def pl(cellnum):
  return [cellnum//8,cellnum%8]

def mn(move):
  return pn(move[0])+pn(move[1])

def nm(notation):
  return (np(notation[:2]),np(notation[2:]))

def form(l):
  return list(map(lp,filter(o,l)))



class bot:
  def __init__(self,name,values={}):
    self.name = name
    self.values = {
      'square_weights': {
        'p':[
          0,0,0,0,0,0,0,0,
          0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,
          0.18,0.18,0.18,0.18,0.18,0.18,0.18,0.18,
          0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,
          0.45,0.45,0.45,0.45,0.45,0.45,0.45,0.45,
          0.6,0.6,0.6,0.6,0.6,0.6,0.6,0.6,
          0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,
          1,1,1,1,1,1,1,1
        ],
        'b':[
          0.8,0.65,0.5,0.25,0.25,0.5,0.65,0.8,
          0.7,1,0.77,0.65,0.65,0.77,1,0.7,
          0.5,0.8,1,0.8,0.8,1,0.8,0.5,
          0.3,0.6,0.95,1,1,0.95,0.6,0.3,
          0.3,0.9,0.85,1,1,0.85,0.9,0.3,
          0.7,0.8,0.9,0.7,0.7,0.9,0.8,0.7,
          0.75,0.85,0.7,0.5,0.5,0.7,0.85,0.75,
          0.8,0.6,0.4,0.3,0.3,0.4,0.6,0.8
        ],
        'n':[
          0,0.2,0.3,0.4,0.4,0.3,0.2,0,
          0.1,0.3,0.35,0.4,0.4,0.35,0.3,0.1,
          0.15,0.35,0.5,0.75,0.75,0.5,0.35,0.15,
          0.2,0.4,0.7,0.85,0.85,0.7,0.4,0.2,
          0.25,0.5,0.75,0.9,0.9,0.75,0.5,0.25,
          0.3,0.6,0.8,0.95,0.95,0.8,0.6,0.3,
          0.4,0.7,0.9,1,1,0.9,0.7,0.4,
          0.5,0.8,1,1,1,1,0.8,0.5
        ],
        'k':[
          0,0.05,0.1,0.15,0.15,0.1,0.05,0,
          0.6,0.55,0.5,0.5,0.5,0.5,0.55,0.6,
          0.65,0.6,0.55,0.55,0.55,0.55,0.6,0.65,
          0.7,0.7,0.7,0.7,0.7,0.7,0.7,0.7,0.7,
          0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,
          1,1,1,1,1,1,1,1,
          1,1,1,1,1,1,1,1,
          1,1,1,1,1,1,1,1
        ],
        'r':[
          0,0.2,0.4,0.8,0.8,0.4,0.2,0,
          0,0.2,0.45,0.8,0.8,0.45,0.2,0,
          0.2,0.4,0.6,0.8,0.8,0.6,0.4,0.2,
          0.6,0.6,0.6,0.8,0.8,0.6,0.6,0.6,
          0.6,0.6,0.6,0.8,0.8,0.6,0.6,0.6,
          0.6,0.6,0.6,0.8,0.8,0.6,0.6,0.6,
          1,1,1,1,1,1,1,1,
          0.8,0.8,1,1,1,1,0.8,0.8
        ],
        'q':[
          1,1,1,1,1,1,1,1,
          1,1,1,1,1,1,1,1,
          1,1,1,1,1,1,1,1,
          1,1,1,1,1,1,1,1,
          1,1,1,1,1,1,1,1,
          1,1,1,1,1,1,1,1,
          1,1,1,1,1,1,1,1,
          1,1,1,1,1,1,1,1
        ]
          
      },
      'piece_values': {
        'r':-5,'b':-3,'n':-3,'p':-1,'q':-9,
        'R':5,'B':3,'N':3,'P':1,'Q':9,
        '':0,'k':0,'K':0
      },
      'piece_exists_weight':1,
      'piece_position_weight':0.016,
      'preserve_castle_weight': 0.35,
      'move_number_weight':0.5,
      'king_weight_at_60':-4,
      'king_weight_at_2':3
      }
    for value in values:
      self.values[value] = values[value]
    self.values['king_weight_m'] = (self.values['king_weight_at_2'] - self.values['king_weight_at_60'])/-58
    self.values['king_weight_b'] = self.values['king_weight_at_2'] - self.values['king_weight_m']*2
      

  def strength(self,board):
    c = board.turn%2
    moves = board.all_moves(c)
    if not moves:
      if board.check(c):
        return 10000*(-2*c+1)
      return 0
    freedom = (-2*c+1)*self.values['move_number_weight']/len(moves)
    material= 0
    weighted_material = 0
    for i in range(64):
      if board.squares[i]:
        value = self.values['piece_values'][board.squares[i]]
        position = (value * self.values['square_weights'][board.squares[i].lower()][::(board.squares[i].isupper()*2-1)][i]) * self.values['piece_position_weight']
        weighted_material += value + position
        material += abs(weighted_material)
    b_king_str = -(self.values['king_weight_m']*material+self.values['king_weight_b'])*self.values['square_weights']['k'][::-1][board.kings[0]]*self.values['piece_position_weight']
    w_king_str = (self.values['king_weight_m']*material+self.values['king_weight_b'])*self.values['square_weights']['k'][board.kings[1]]*self.values['piece_position_weight']
    castle = self.values['preserve_castle_weight']*((board.castle['K'] or board.castle['Q']) - (board.castle['k'] or board.castle['q']))
    strength = freedom + b_king_str + w_king_str + weighted_material + castle
    return strength


  def best_move(self,board,layers=2,score_to_beat = None):
    c=board.turn%2
    moves = board.all_moves(c)
    if not moves:
      if board.check(c):
        return None,10000*(-2*c+1)
      return None,0
    best, score = "Resign", 9999*(-2*c+1)
    for move in moves:
      sim = board.sim_move(move[0],move[1])
      if layers:
        #print(f'inside recursion {layers}, considering move {mn(move)}, about to recur with score to beat {round(score,4)}')
        strength = self.best_move(sim,layers-1,score)[1]
        #print(f'found the strength of move {mn(move)} to be {round(strength,4)}')
      else:
        
        strength = self.strength(sim)
        #print(f'inside recursion 0, considering whites move {mn(move)}, score to beat is {round(score_to_beat,2)}, strength is {round(strength,2)}')
      if c:
        if score_to_beat != None:
          if strength > score_to_beat:
            return move, strength
        if strength > score:
          score = strength
          best = move
      else:
        if score_to_beat != None:
          if strength < score_to_beat:
            return move, strength
        if strength < score:
          score = strength
          best = move
    return best, score
    
new_bot = bot('New Bot')

def main():
  b = board()
  players = ['black','white']
  
  ps = ['Old Bot',new_bot]

  def turn(p):
    if type(p) != bot:
      possibles = b.all_moves(b.turn%2)
      if not possibles:
        if b.check(b.turn%2): print(f"{players[b.turn%2]} has been checkmated. {players[2+~(b.turn%2)].title()} wins.")
        else: print(f"{players[b.turn%2]} is unable to move and has been stalemated. The game is a draw")
        return 0
      print(f"It is currently {ps[b.turn%2]}'s move")
      while True:
        try:
          n = nm(input())
          if n in possibles:
            b.move(n[0],n[1])
            break
          else: print("You do not have a piece that may do that")
        except: print(f"That is not a valid move. A move should look like 'e1e2'")
    else:
      print(f'{p.name} is thinking')
      move = p.best_move(b,difficulty)[0]
      Beep(400,440)
      try:
        b.move(move[0],move[1])
      except:
        print(f'{p.name} has resigned')
        return 0
    return 1
      
    
    
  while 1:
    sys('cls')
    print(b)
    game = turn(ps[b.turn%2])
    if not game:
      return
    print()
      
difficulty = 2
colour = 1

if __name__ == '__main__':
  input(main());
  
      
          
        
