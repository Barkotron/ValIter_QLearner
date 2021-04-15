import re
import tkinter as tk
import copy
import GUI
import ValueIteration
import RL_GUI 
import QLearner

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
    
    #First cleaning up global variables in order to allow running multiple grids
    global HORIZONTA
    global VERTICA
    global TERMINAL
    global BOULDER
    global ROBOTSTARTSTATE
    global K
    global EPISODES
    global DISCOUNT
    global NOISE
    global TRANSITION_COST
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

def main():
    
    readInput('gridConf.txt')

    valIterWindow = tk.Tk()
    
    grid = createGrid(HORIZONTAL,VERTICAL)
    valIter = ValueIteration.ValueIterationAgent(grid,TERMINAL,BOULDER,K,DISCOUNT,NOISE,TRANSITION_COST)
    grid = valIter.grid
    #tests()

    valIterWindow.title(f"Value Iteration after {K} Iterations")
    GUI.draw_board(valIterWindow, grid, [row[:-1] for row in TERMINAL], BOULDER,
               GUI.max_reward(TERMINAL), GUI.max_punishment(TERMINAL), K)

    valIterWindow.mainloop()
    
      
    #now for Q-Learning
    print("\n Now for Q-Learning\n")
    qWindow = tk.Tk()
    # readInput('gridConf.txt')
    # readInput('gridConfLong.txt')
    #readInput('gridConfAlt.txt')
    #readInput('gridConfAlt2.txt')
    # readInput('gridConfSmall.txt')
    grid = createGrid(HORIZONTAL,VERTICAL)
    # print(grid)
    tests()
    qLearner = QLearner.QLearningAgent(grid,TERMINAL,BOULDER,ROBOTSTARTSTATE,K,EPISODES,ALPHA,DISCOUNT,NOISE,TRANSITION_COST)
    qLearner.explore()
    grid = qLearner.grid
    # print(grid)
    #tests()
 
    GUI.draw_board(qWindow, grid, [row[:-1] for row in TERMINAL], BOULDER,
                GUI.max_reward(TERMINAL), GUI.max_punishment(TERMINAL), EPISODES)
    qWindow.mainloop()
    qWindow = tk.Tk()
    RL_GUI.draw_board(qWindow, grid, EPISODES, TERMINAL, BOULDER,
                      HORIZONTAL, VERTICAL, RL_GUI.get_max_reward(TERMINAL), RL_GUI.get_max_punishment(TERMINAL))
    
    
    
    qWindow.mainloop()

main()