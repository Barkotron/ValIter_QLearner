'''
This project implements both value iteration and Q-learning.
This file reads in the specification of a grid to test both agents.
1. A Value Iteration Agent to a fixed depth k.
2. A A Q-Value Learner with Episodes.

COMP4190 A3
Jackson Barker, Tyler Brown
'''
import re
import tkinter as tk
import copy
import GUI
import ValueIteration
import RL_GUI 
import QLearner

#---Global Variables---
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
RESULTS_K = 0
RESULTS_EPISODES = 0

def createGrid(horizontal,vertical):
  '''
  creates a grid based off of the horizontal and vertical values given from a grid configuration file

  Args:
    filename(string): name of the .txt file to be read
  Return:
    the grid, in the the form of a list(rows) of lists(cols) where each entry is another list of lists containing
    the value and direction of moving to a neighbouring square
  '''

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

  return grid

def readResults(filename='results.txt'):
  '''
  Reads a results file and passes 1 line at a time to parseLine()

  Args:
    filename(string): name of the .txt file to be read
  Return:
    none
  '''
  results = open(filename)

  for line in results:
    parseLine(line)

  
def readInput(filename='gridConf.txt'):
  '''
  Reads a grid configuration file and passes 1 line at a time to parseLine()

  Args:
    filename(string): name of the .txt file to be read
  Return:
    none
  '''

  read = open(filename)
  for line in read:
    parseLine(line)
    
def parseLine(line):
  '''
  Reads in a single line from a grid configuration or results file and picks out the important information

  Args:
    line(string): a line from a grid configuration or results file
  Return:
    none
  '''

  # remove everything that isn't a title or value
  tokens = re.split('=|\n|\s|,|{|}',line)

  #remove all '' (empty strings) that result from split()
  try:
    while True:
        tokens.remove('')
  except ValueError:
    pass

  #title is always the first element
  field = tokens[0].lower()


  if field == 'Horizontal'.lower():
    global HORIZONTAL
    HORIZONTAL = int(tokens[1])
  elif field == 'Vertical'.lower():
    global VERTICAL
    VERTICAL = int(tokens[1])
  elif field == 'Terminal'.lower():
    for i in range(1,len(tokens),4):
      global TERMINAL
      TERMINAL.append([int(tokens[i+1]),int(tokens[i+2]),float(tokens[i+3])])
  elif field == 'Boulder'.lower():
    for i in range(1,len(tokens),3):
      global BOULDER
      BOULDER.append([int(tokens[i+1]),int(tokens[i+2])])
  elif field == 'RobotStartState'.lower():
    global ROBOTSTARTSTATE
    ROBOTSTARTSTATE = [int(tokens[2]),int(tokens[1])]
  elif field == 'K'.lower():
    global K
    K = int(tokens[1])
  elif field == 'Episodes'.lower():
    global EPISODES
    EPISODES = int(tokens[1])
  elif field == 'Alpha'.lower():
    global ALPHA
    ALPHA = float(tokens[1])
  elif field == 'Discount'.lower():
    global DISCOUNT
    DISCOUNT = float(tokens[1])
  elif field == 'Noise'.lower():
    global NOISE
    NOISE = float(tokens[1])
  elif field == 'TransitionCost'.lower():
    global TRANSITION_COST
    TRANSITION_COST = float(tokens[1])
  elif tokens[3].lower() == 'MDP'.lower():
    global RESULTS_K
    RESULTS_K = int(tokens[2])
  elif tokens[3].lower() == 'RL'.lower():
    global RESULTS_EPISODES
    RESULTS_EPISODES = int(tokens[2])
  else:
    print("Unknown Field")

def printGlobals():
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
  print(f"RESULTS_K: {RESULTS_K}")
  print(f"RESULTS_EPISODES: {RESULTS_EPISODES}")

def main():
    
    readInput('gridConf.txt')
    readResults('results.txt')
    printGlobals()

    #VALUE ITERATION WITH K FROM GRIDCONF.TXT
    valIterWindow = tk.Tk()
    
    grid = createGrid(HORIZONTAL,VERTICAL)
    valIter = ValueIteration.ValueIterationAgent(grid,TERMINAL,BOULDER,K,DISCOUNT,NOISE,TRANSITION_COST)
    grid = valIter.grid

    valIterWindow.title(f"Value Iteration after {K} Iterations")
    GUI.draw_board(valIterWindow, grid, [row[:-1] for row in TERMINAL], BOULDER,
               GUI.max_reward(TERMINAL), GUI.max_punishment(TERMINAL), K)

    #VALUE ITERATION WITH K FROM RESULTS.TXT
    result_k_valIterWindow = tk.Tk()
    
    result_k_grid = createGrid(HORIZONTAL,VERTICAL)
    result_valIter = ValueIteration.ValueIterationAgent(result_k_grid,TERMINAL,BOULDER,RESULTS_K,DISCOUNT,NOISE,TRANSITION_COST)
    result_k_grid = result_valIter.grid

    result_k_valIterWindow.title(f"Value Iteration after {RESULTS_K} Iterations")
    GUI.draw_board(result_k_valIterWindow, result_k_grid, [row[:-1] for row in TERMINAL], BOULDER,
               GUI.max_reward(TERMINAL), GUI.max_punishment(TERMINAL), RESULTS_K)

    #Q-LEARNING WITH EPISODES FROM GRIDCONF.TXT
    qWindow = tk.Tk()
    qWindow.title(f"Q-Learning after {EPISODES} episodes")
    qGrid = createGrid(HORIZONTAL,VERTICAL)
    qLearner = QLearner.QLearningAgent(qGrid,TERMINAL,BOULDER,ROBOTSTARTSTATE,EPISODES,ALPHA,DISCOUNT,NOISE,TRANSITION_COST)
    qLearner.explore()
    qGrid = qLearner.grid
    
    qWindow.title(f"Q-Learning after {EPISODES} Episodes")
    RL_GUI.draw_board(qWindow, qGrid, EPISODES, TERMINAL, BOULDER,
                      HORIZONTAL, VERTICAL, RL_GUI.get_max_reward(TERMINAL), RL_GUI.get_max_punishment(TERMINAL))
    
    #Q-LEARNING WITH EPISODES FROM RESULTS.TXT
    resultsQWindow = tk.Tk()
    resultsQWindow.title(f"Q-Learning after {RESULTS_EPISODES} episodes")
    resultsQGrid = createGrid(HORIZONTAL,VERTICAL)
    resultsQLearner = QLearner.QLearningAgent(resultsQGrid,TERMINAL,BOULDER,ROBOTSTARTSTATE,RESULTS_EPISODES,ALPHA,DISCOUNT,NOISE,TRANSITION_COST)
    resultsQLearner.explore()
    resultsQGrid = resultsQLearner.grid
    
    resultsQWindow.title(f"Q-Learning after {RESULTS_EPISODES} Episodes")
    RL_GUI.draw_board(resultsQWindow, resultsQGrid, RESULTS_EPISODES, TERMINAL, BOULDER,
                      HORIZONTAL, VERTICAL, RL_GUI.get_max_reward(TERMINAL), RL_GUI.get_max_punishment(TERMINAL))


    valIterWindow.mainloop()    
    result_k_valIterWindow.mainloop()
    
    qWindow.mainloop()
    resultsQWindow.mainloop()
    
      

main()