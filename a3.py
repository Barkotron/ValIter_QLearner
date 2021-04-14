import re
import numpy as np
import tkinter as tk
import copy
import random
import GUI as gg
import RL_GUI as rl
import QLearner as ql

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


  #***SOME OF THESE X,Y ARE FLIPPED***
  if field == 'Horizontal':
    global HORIZONTAL
    HORIZONTAL = int(tokens[1])
  elif field == 'Vertical':
    global VERTICAL
    VERTICAL = int(tokens[1])
  elif field == 'Terminal':
    for i in range(1,len(tokens),4):
      global TERMINAL
      TERMINAL.append([int(tokens[i+1]),int(tokens[i+2]),int(tokens[i+3])])
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

    #(self,grid,terminal,boulder, startState, k, episodes, alpha, discount, noise, transitionCost)
    
    
    alltests = False
    if alltests:
        all_inputs()
    else:         
        #now for Q-Learning
        print("\n Now for Q-Learning\n")
        window = tk.Tk()
        # readInput('gridConf.txt')
        readInput('gridConfLong.txt')
        #readInput('gridConfAlt.txt')
        #readInput('gridConfAlt2.txt')
        # readInput('gridConfSmall.txt')
        grid = createGrid(HORIZONTAL,VERTICAL)
        # print(grid)
        tests()
        qLearner = ql.QLearningAgent(grid,TERMINAL,BOULDER,ROBOTSTARTSTATE,K,EPISODES,ALPHA,DISCOUNT,NOISE,TRANSITION_COST)
        qLearner.explore()
        grid = qLearner.grid
        # print(grid)
        tests()
    
        rows = HORIZONTAL
        cols = VERTICAL
        terminal_states = TERMINAL
        boulder_states = BOULDER
        num_iterations = EPISODES
    
        gg.draw_board(window, grid, [row[:-1] for row in terminal_states], boulder_states,
                    gg.max_reward(terminal_states), gg.max_punishment(terminal_states), num_iterations)
        window.mainloop()
        window = tk.Tk()
        rl.draw_board(window, grid, num_iterations, terminal_states, boulder_states, rows, cols)
        
        
        
        window.mainloop()

#just for doing multiple different grids easily for fun
def all_inputs():
    #window = tk.Tk()
    inputs = ['gridConfSmall.txt', 'gridConfSmall2.txt', 'gridConf.txt', 'gridConfAlt.txt', 'gridConfAlt2.txt']
    for i in inputs:
        window = tk.Tk()
        readInput(i)
        grid = createGrid(HORIZONTAL,VERTICAL)
        valIter = ValueIterationAgent(grid,TERMINAL,BOULDER,ROBOTSTARTSTATE,K,EPISODES,ALPHA,DISCOUNT,NOISE,TRANSITION_COST)
        valIter.iterate()
        grid = valIter.grid
        tests()    
        terminal_states = TERMINAL
        boulder_states = BOULDER
        num_iterations = K
    
        draw_board(window, grid, [row[:-1] for row in terminal_states], boulder_states,
                   max_reward(terminal_states), max_punishment(terminal_states), num_iterations)
    
        window.mainloop()


main()