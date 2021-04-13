import re
import numpy as np
import tkinter as tk
import copy
import GUI

#global variables for now, we may do something else with them
HORIZONTAL = 0
VERTICAL = 0
TERMINAL = []
BOULDER = []
ROBOTSTARTSTATE = 0
K = 0
EPISODES = 0
ALPHA = 0
DISCOUNT = 0
NOISE = 0
TRANSITION_COST = 0
DECIMALS = 4

def createGrid(horizontal,vertical):

  grid = []
  for h in range(horizontal):
    row = []
    for v in range(vertical):
      square = [[0,'↑'],[0,'←'],[0,'↓'],[0,'→']]
      for term in TERMINAL:
        if term[0] == h and term[1] == v:
          square = ([[term[2],'*']])
      row.append(square)
    grid.append(row)

  #print(grid)
  return grid
  
def readInput(filename='gridConf.txt'):

  read = open(filename)
  for line in read:
    #print(f"Line: {line}")
    parseLine(line)
    
def parseLine(line):

  # remove everything that isn't a title or value
  tokens = re.split('=|\n|\s|,|{|}',line)

  #remove all '' (empty strings) that result from split()
  try:
    while True:
        tokens.remove('')
  except ValueError:
    pass

  #title is always the first element
  field = tokens[0]


  if field == 'Horizontal':
    global HORIZONTAL
    HORIZONTAL = int(tokens[1])
  elif field == 'Vertical':
    global VERTICAL
    VERTICAL = int(tokens[1])
  elif field == 'Terminal':
    for i in range(1,len(tokens),4):
      global TERMINAL
      TERMINAL.append([int(tokens[i+1]),int(tokens[i+2]),float(tokens[i+3])])
  elif field == 'Boulder':
    for i in range(1,len(tokens),3):
      global BOULDER
      BOULDER.append([int(tokens[i+1]),int(tokens[i+2])])
  elif field == 'RobotStartState':
    global ROBOTSTARTSTATE
    ROBOTSTARTSTATE = [int(tokens[2]),int(tokens[1])]
  elif field == 'K':
    global K
    K = int(tokens[1])
  elif field == 'Episodes':
    global EPISODES
    EPISODES = int(tokens[1])
  elif field == 'Alpha':
    global ALPHA
    ALPHA = float(tokens[1])
  elif field == 'Discount':
    global DISCOUNT
    DISCOUNT = float(tokens[1])
  elif field == 'Noise':
    global NOISE
    NOISE = float(tokens[1])
  elif field == 'TransitionCost':
    global TRANSITION_COST
    TRANSITION_COST = float(tokens[1])
  else:
    print("Unknown Field")

  #print(tokens)

def tests():
  print("---Global Variables---")
  print(f"Horizontal: {HORIZONTAL}")
  print(f"Vertical: {VERTICAL}")
  print(f"Terminal: {TERMINAL}")
  print(f"Boulder: {BOULDER}")
  print(f"RobotStartState: {ROBOTSTARTSTATE}")
  print(f"K: {K}")
  print(f"Episodes: {EPISODES}")
  print(f"Alpha: {ALPHA}")
  print(f"Discount: {DISCOUNT}")
  print(f"Noise: {NOISE}")
  print(f"TransitionCost: {TRANSITION_COST}")


class ValueIterationAgent:

  def __init__(self,grid,terminal,boulder, k, discount, noise, transitionCost):


    self.grid = grid
    self.discount = discount
    self.k = k
    self.noise = noise
    self.transitionCost = transitionCost
    self.boulder = boulder
    self.terminal = terminal

    self.iterate()

  #of 1 state
  def getValue(self, state, target):
    
    #if you're trying to move into a boulder: 'bounce off' and stay where you tried to move from
    for boulder in self.boulder:
            if boulder[0] == target[0] and boulder[1] == target[1]:
              values = []
              for val in self.grid[state[0]][state[1]]:
                values.append(val[0])
              return max(values)

    # if state we're checking is outside the grid
    if target[0] < 0 or target[0] >= len(self.grid) or target[1] < 0 or target[1] >= len(self.grid[0]):
      values = []
      for val in self.grid[state[0]][state[1]]:
        values.append(val[0])
      return max(values)
    
    else:
      values = []
      for val in self.grid[target[0]][target[1]]:
        values.append(val[0])
      return max(values)
  
  def iterate(self):
    
    rows = len(self.grid)
    cols = len(self.grid[0])

    for iteration in range(1,self.k):
      
      #Copy the grid so we aren't using values that were updated in the same iteration
      self.newGrid = copy.deepcopy(self.grid)
      
      for i in range(rows):
        for j in range(cols):

          terminal_or_boulder = False

          for term in self.terminal:
            if term[0] == i and term[1] == j:
              terminal_or_boulder = True

          for boulder in self.boulder:
            if boulder[0] == i and boulder[1] == j:
              terminal_or_boulder = True

          if not terminal_or_boulder:
            up = down = left = right = 0

            mainProb = (1-self.noise) #probability for desired direction
            noiseProb = self.noise/2 #probability for each of the 2 'noise directions'

            upValid = True#i+1 < rows
            downValid = True#i-1 >= 0
            leftValid = True#j-1 >= 0
            rightValid = True#j+1 < cols

            
            if upValid: #up
              up = ((self.discount*(self.getValue((i,j),(i+1,j)))))

            if leftValid:#left
              left = ((self.discount*(self.getValue((i,j),(i,j-1)))))

            if downValid:#down
              down = ((self.discount*(self.getValue((i,j),(i-1,j)))))

            if rightValid:#right
              right = ((self.discount*(self.getValue((i,j),(i,j+1)))))

            totalUp = mainProb*up + noiseProb*left + noiseProb*right
            totalLeft = mainProb*left + noiseProb*up + noiseProb*down
            totalDown = mainProb*down + noiseProb*left + noiseProb*right
            totalRight = mainProb*right + noiseProb*up + noiseProb*down


            # [this][][][] is the x coord
            # [][this][][] is the y coord
            # []][][this][] is which of the 4 neighbouring cells it would go to (up,left,down,right)
            # []][][][this] is the value if [0] (if [1] that would be the arrow since they look like: [0,'↑'])
            self.newGrid[i][j][0][0] = totalUp + self.transitionCost
            self.newGrid[i][j][1][0] = totalLeft + self.transitionCost
            self.newGrid[i][j][2][0] = totalDown + self.transitionCost
            self.newGrid[i][j][3][0] = totalRight + self.transitionCost
      
      #update the grid with the new values for the next iteration
      self.grid = copy.deepcopy(self.newGrid)
    


def main():
    
    readInput('gridConf.txt')

    valIterWindow = tk.Tk()
    
    grid = createGrid(HORIZONTAL,VERTICAL)
    valIter = ValueIterationAgent(grid,TERMINAL,BOULDER,K,DISCOUNT,NOISE,TRANSITION_COST)
    grid = valIter.grid
    #tests()

    valIterWindow.title(f"Value Iteration after {K} Iterations")
    GUI.draw_board(valIterWindow, grid, [row[:-1] for row in TERMINAL], BOULDER,
               GUI.max_reward(TERMINAL), GUI.max_punishment(TERMINAL), K)

    valIterWindow.mainloop()

main()