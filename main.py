
import random, time, getch

import os
clear = lambda: os.system('clear')


class Square():

  def __init__(self, size, sX, sY, endX, endY):
    
    self.main = []
    self.size = size
    self.sX = sX - 1
    self.sY = sY - 1
    self.last = [0,0]
    self.current = (self.sX, self.sY)
    self.buttons = []
    self.blanks = []
    self.vs = []
    self.offVs = []
    self.HB = []
    self.pressedHB = []
    self.ws = []
    self.offWs = []
    self.boxes = []
    self.end = (endX-1,endY-1)
    self.Zs = []

#makes grid
    for n in range(0,self.size):
      self.main.append([])
      for i in range(0,self.size):
        self.main[n].append("  ")
#sets start and finish
    self.main[self.sY][self.sX] = "O "
    self.main[self.end[1]][self.end[0]] = "F "

  def show(self):
    clear()
    # print("\n"*20) 
    #print("Boxes: ", self.boxes)
    # print("Blanks: ", self.blanks)
    # print("Buttons: ", self.buttons)
    # print("Vs: ", self.vs)
    # print("Off Vs: ", self.offVs)
    # print("Ws", self.ws)
    # print("off: ", self.offWs)
    #print("HB: ", self.HB)
    #print("PressedHb: ", self.pressedHB)
    #print(self.current)
    # print(self.last)
    #print(f"Pos: ( {self.sX+1} , {self.sY+1} ) / last: {self.last[0]+1} , {self.last[1]+1 }\n")

    self.main.reverse()



    #prints table

    n = self.size
    print("@ " *(n +2))
    for line in self.main:

      string = "@ "
      for o in line:
        string+=o

      print(string+ "@ ")
    string = "    "
    print("@ " *(self.size +2))

    self.main.reverse()


    print("""\np for rules...
    """)
  
#place Buttons (B)

  def placeB(self, X, Y):
    X -=1
    Y -=1
    if self.main[Y][X] in "O    ": 
      self.main[Y][X] = "B "
      self.buttons.append((X,Y))
    else: 
      self.main[Y][X] = "   "
      self.buttons.remove((X,Y))

  def placeBList(self, XYlist):
    for pair in XYlist:
      self.placeB(pair[0],pair[1])

#place Heavy buttons aka HB (H) 
  
  def placeHB(self, X, Y):
    X -=1
    Y -=1
    if self.main[Y][X] in "O    ": 
      self.main[Y][X] = "H "
      self.HB.append((X,Y))
    else: 
      self.main[Y][X] = "   "
      self.HB.remove((X,Y))
  
  def placeHBList(self, XYlist):
    for pair in XYlist:
      self.placeHB(pair[0],pair[1])

#places Ws (W)

  def placeW(self,X,Y):
    X -= 1
    Y -= 1
    if self.main[Y][X] in "  ": 
      self.main[Y][X] = "W "
      self.ws.append((X,Y))
    else: 
      self.main[Y][X] = "  "
      self.ws.remove((X,Y))
  
  def placeWList(self, XYlist):
    for pair in XYlist:
      self.placeW(pair[0],pair[1])

#places Boxes (C)

  def placeBox(self, X, Y):
    X -= 1
    Y -= 1

    if self.main[Y][X] in "O    ": 
      self.main[Y][X] = "C "
      self.boxes.append((X,Y))
    else: 
      self.main[Y][X] = "  "
      self.boxes.remove((X,Y))

  def placeBoxList(self, XYlist):
    for pair in XYlist:
      self.placeBox(pair[0],pair[1])

#places V (V)

  def placeV(self, X, Y):
    X -= 1
    Y -= 1
    if self.main[Y][X] in "O    ": 
      self.main[Y][X] = "V "
      self.vs.append((X,Y))
    else: 
      self.main[Y][X] = "  "
      self.vs.remove((X,Y))

  def placeVList(self, XYlist):
    for pair in XYlist:
      self.placeV(pair[0],pair[1])

# places and replaces Z (Z)

  def placeZ(self, X, Y):
    X-=1
    Y-=1
    self.main[Y][X] = "Z "
    self.Zs.append((X,Y))

  def placeZList(self, XYlist):
    for pair in XYlist:
      self.placeZ(pair[0],pair[1])

  def replaceZ(self, X, Y):
    X-=1
    Y-=1
    self.Zs.remove((X,Y))
    self.main[Y][X]
    self.placeWall(X+1,Y+1)

#places Walls (X)

  def placeWall(self, X, Y):
    X -=1
    Y -=1
    if self.main[Y][X] in "O  Z ": 
      self.main[Y][X] = "X "
      self.blanks.append((X,Y))
    else: 
      self.main[Y][X] = "  "
      self.blanks.remove((X,Y))

  def placeWallList(self, XYlist):
    for pair in XYlist:
      self.placeWall(pair[0],pair[1])

#places horizontal walls, from start to finish, on y level Y /make sure to start from left to right

  def placeWallRowX(self, start, finish, Y):
    for n in range(start, finish + 1):
      self.placeWall(n, Y)

# places vertical walls, from start to finish, on x level X /make sure to start from bottom to top
  def placeWallRowY(self, start, finish, X):
    for n in range(start, finish + 1):
      self.placeWall(X, n)

#places Wall block from point (XY) to (XY) /make sure to start from bottom left to top right
  
  def placeWallBlock(self, X, Y, X2, Y2):
    for y in range(Y, Y2+1):
      self.placeWallRowX(X, X2, y)



  def checkF(self):
    return self.current == self.end   

# moves O 

  def move(self, direction):
    
    test2 = False

    if direction == "U": 
      
      #checks if player can move one square up
      test = (self.sY + 1 != self.size) and (self.sX, self.sY + 1) not in self.blanks and (self.sX, self.sY + 1) not in self.vs and (self.sX, self.sY + 1) not in self.ws
      
      #checks if player would have to move a box
      if (self.sX, self.sY +1) in self.boxes:
        test = (self.sY + 2 != self.size) and (self.sX, self.sY + 2) not in self.blanks and (self.sX, self.sY + 2) not in self.vs and (self.sX, self.sY + 2) not in self.ws and (self.sX, self.sY + 2) not in self.boxes
        if test: 
          test2 = True
          xB = 0
          yB = 1
        else: test2 = False
      nx= 0
      ny = 1

    elif direction =="R":
      test = (self.sX + 1 != self.size) and (self.sX +1, self.sY) not in self.blanks and (self.sX +1, self.sY) not in self.vs and (self.sX +1, self.sY) not in self.ws
      
      if (self.sX +1, self.sY) in self.boxes:
        test = (self.sX + 2 != self.size) and (self.sX+2, self.sY) not in self.blanks and (self.sX+2, self.sY) not in self.vs and (self.sX+2, self.sY) not in self.ws and (self.sX+2, self.sY) not in self.boxes
        if test: 
          test2 = True
          xB = 1
          yB = 0

        else: test2 = False
      nx= 1
      ny = 0

    elif direction == "D": 
      test = (self.sY - 1 != -1) and (self.sX, self.sY - 1) not in self.blanks and (self.sX, self.sY - 1) not in self.vs and (self.sX, self.sY - 1) not in self.ws
      
      if (self.sX , self.sY-1) in self.boxes:
        test = (self.sY - 2 != -1) and (self.sX, self.sY - 2) not in self.blanks and (self.sX, self.sY - 2) not in self.vs and (self.sX, self.sY - 2) not in self.ws and (self.sX, self.sY - 2) not in self.boxes
        if test: 
          test2 = True
          xB = 0
          yB = -1
        else: test2 = False

      nx= 0
      ny = -1
    elif direction =="L":
      test = (self.sX - 1 != -1) and (self.sX -1, self.sY) not in self.blanks and (self.sX -1, self.sY) not in self.vs and (self.sX -1, self.sY) not in self.ws
      
      if (self.sX-1 , self.sY) in self.boxes:
        test = (self.sX - 2 != -1) and (self.sX-2, self.sY) not in self.blanks and (self.sX-2, self.sY) not in self.vs and (self.sX-2, self.sY) not in self.ws and (self.sX-2, self.sY) not in self.boxes
        if test: 
          test2 = True
          xB = -1
          yB = 0
        else: test2 = False

      nx= -1
      ny = 0

    if test: #player can move
      if test2: #if player has to move box and box can move
        
        self.boxes.remove((self.sX + nx, self.sY+ny)) #changes position of box
        self.boxes.append((self.sX +nx+xB, self.sY +ny+ yB))


       #checks if box was moved out of place
        if ((self.sX + nx, self.sY+ny) in self.pressedHB):
          if len(self.pressedHB) == len(self.HB): #checks if it was moved while they were all pressed
            for w in self.offWs:
              self.main[w[1]][w[0]] = "W "
            
            self.ws = self.offWs[::-1]
            self.offWs = []          
          self.pressedHB.remove((self.sX + nx, self.sY+ny))



        if (self.sX + xB+nx, self.sY + yB+ny) in self.buttons: 
          self.main[self.sY + yB+ny][self.sX + xB+nx] = "Q "
          if len(self.vs):
            for v in self.vs:
              self.main[v[1]][v[0]] = "  "
            self.offVs = self.vs[::-1]
            self.vs = []
          else: 
            for v in self.offVs:
                self.main[v[1]][v[0]] = "V "
                if v in self.boxes: self.boxes.remove(v)
            self.vs = self.offVs[::-1]
            self.offVs = []
        elif (self.sX + xB+nx, self.sY +ny+ yB) in self.HB:
          self.pressedHB.append((self.sX + xB+nx,self.sY + yB + ny))
          self.main[self.sY + yB + ny][self.sX + xB+nx] = "Q "
          if len(self.pressedHB) == len(self.HB):
            for w in self.ws:
              self.main[w[1]][w[0]] = "  "
              if w in self.boxes: self.boxes.remove(w)
            self.offWs = self.ws[::-1]
            self.ws = []
            
        else: self.main[self.sY + yB+ny][self.sX + xB+nx] = "C "

      self.last = (self.sX, self.sY)

# updates last space the player was in
      if self.last in self.buttons:
        self.main[self.sY][self.sX] = "B " 
      elif self.last in self.HB:
        self.main[self.sY][self.sX] = "H " 
      else: self.main[self.sY][self.sX] = "  "

#updates position
      self.sX += nx
      self.sY += ny

      if self.last in self.Zs:
        self.replaceZ(self.last[0]+1, self.last[1]+1)

      self.current = (self.sX, self.sY) 
 
      if (self.current in self.buttons): 
        self.main[self.sY][self.sX] = "G "
        if len(self.vs):
          for v in self.vs:
            self.main[v[1]][v[0]] = "  "
            if v in self.boxes:
              self.boxes.remove(v)
          self.offVs = self.vs[::-1]
          self.vs = []
        else: 
          for v in self.offVs:
              self.main[v[1]][v[0]] = "V "
          self.vs = self.offVs[::-1]
          self.offVs = []

      else: self.main[self.sY][self.sX] = "O "




  def mU(self):
    
    self.move("U")
    self.show()


  def mR(self):

    self.move("R")
    self.show()

  def mD(self):

    self.move("D")
    self.show()
  def mL(self):

    self.move("L")
    self.show()

def playLevel(level):
  level.show()
  while True:
    m = getch.getch() 

    if m == "w": level.mU()
    elif m == "d": level.mR()
    elif m == "s": level.mD()
    elif m == "a": level.mL()
    elif m == "r": return False
    elif m == "p": 
      clear()
      print("""~~~RULES~~~
- You are the "O"
- Your goal is to get to the F
- You can move Up Down Left and Right (w s a d)
- You can't step into X, V and W
- X is a permanent wall
- Z creates a permanet wall once you step out of it
- V goes down / up everytime you, or a box steps into a B
- C is a box, you can push the box which ever way you desire, aslong as the place you are trying to push the box to doesn't have a wall, or another box
- W goes down once every H has a box on top
- you can press r to restart incase you get blocked
- have funnn

press anything to go back to level...
""")
      getch.getch()



    else: level.show()
    if level.checkF(): 
      print("!!Level Finished!!\n\npress anything to continue")
      getch.getch()
      return True

def importLevel(levelName):
  valids = ".OFXVWBHZC"

  file = open("level.txt", "r")
  insideLevel = False
  rows = []
  for line in file:
    if line.rstrip() == f":start:{levelName}": 
      insideLevel = True
      continue 
    if insideLevel:
      if line.rstrip() == f":end:{levelName}":
        insideLevel = False
        continue
      rows.append(line.rstrip())
  rows.reverse()


  file.close()

  walls = []
  h = []
  b = []
  o = []
  f = []
  v = []
  w = []
  z = []
  c = []
  y = 0
  x = 0
  
  size = len(rows[0])

  for row in rows:

    y += 1
    if len(row) != len(rows[0]) and len(row) != len(rows):
      print("Invalid level, Not a square. Name:", levelName)
      return False
    for char in row:
      x += 1
      if char not in valids:
        print("Invalid level, Invalid characters. Name: ", levelName)
        return False
      if char == "X": walls.append((x,y))
      elif char == "B": b.append((x,y))
      elif char == "H": h.append((x,y))
      elif char == "V": v.append((x,y))
      elif char == "W": w.append((x,y))
      elif char == "C": c.append((x,y))
      elif char == "Z": z.append((x,y))
      elif char == "F": f.append((x,y))
      elif char == "O": o.append((x,y))
    x = 0


  if len(o) != 1 or len(f) != 1:
    print("Invalid level. Start/Finish Error ", levelName)
    return False

  level = Square(size, o[0][0], o[0][1], f[0][0], f[0][1])

  if walls: level.placeWallList(walls)
  if h: level.placeHBList(h)
  if b: level.placeBList(b)
  if v: level.placeVList(v)
  if w: level.placeWList(w)
  if c: level.placeBoxList(c)
  if z: level.placeZList(z)


  return level

      



def play(levelName):

  while True:
    level = importLevel(levelName)

    if playLevel(level):
      return 
    else:
      continue

#RUNS LEVELS

play("1")
play("2")
play("test")

