import re
import numpy as np
import tkinter as tk
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

def createGrid(horizontal,vertical):

  grid = []
  for h in range(horizontal):
    row = []
    for v in range(vertical):
      row.append([[0,'↑'],[0,'←'],[0,'↓'],[0,'→']])
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
      TERMINAL.append([int(tokens[i+1]),int(tokens[i+2]),int(tokens[i+3])])
  elif field == 'Boulder':
    for i in range(1,len(tokens),3):
      global BOULDER
      BOULDER.append([int(tokens[i+1]),int(tokens[i+2])])
  elif field == 'RobotStartState':
    global ROBOTSTARTSTATE
    ROBOTSTARTSTATE = [int(tokens[1]),int(tokens[2])]
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
  """
      * Please read learningAgents.py before reading this.*

      A ValueIterationAgent takes a Markov decision process
      (see mdp.py) on initialization and runs value iteration
      for a given number of iterations using the supplied
      discount factor.
  """
  def __init__(self,grid, mdp=None, discount = 0.9, iterations = 100):
    """
      Your value iteration agent should take an mdp on
      construction, run the indicated number of iterations
      and then act according to the resulting policy.
    
      Some useful mdp methods you will use:
          mdp.getStates()
          mdp.getPossibleActions(state)
          mdp.getTransitionStatesAndProbs(state, action)
          mdp.getReward(state, action, nextState)
    """
     
    "*** YOUR CODE HERE ***"
    
  def getValue(self, state):
    """
      Return the value of the state (computed in __init__).
    """

  def getQValue(self, state, action):
    """
      The q-value of the state action pair
      (after the indicated number of value iteration
      passes).  Note that value iteration does not
      necessarily create this quantity and you may have
      to derive it on the fly.
    """
    "*** YOUR CODE HERE ***"

  def getPolicy(self, state):
    """
      The policy is the best action in the given state
      according to the values computed by value iteration.
      You may break ties any way you see fit.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return None.
    """
    "*** YOUR CODE HERE ***"

  def getAction(self, state):
    "Returns the policy at the state (no exploration)."

def main():

    # window = tk.Tk()
    # readInput('gridConf.txt')
    # grid = createGrid(HORIZONTAL,VERTICAL)
    #tests()

    # terminal_states = TERMINAL
    # boulder_states = BOULDER
    # num_iterations = 10

    # draw_board(window, grid, [row[:-1] for row in terminal_states], boulder_states,
    #            max_reward(terminal_states), max_punishment(terminal_states), num_iterations)

    # window.mainloop()
    
    window = tk.Tk()

    # Sample grid after 10 iterations
    grid = [[[[0.19007013163048878, '↑'], [0.06949349578957349, '↓'], [0.3042928921162562, '→'], [0.15652736072667697, '←']],
     [[0.3567050660918199, '↑'], [0.3567050660918199, '↓'], [0.5072615790177806, '→'], [0.20854082305418617, '←']],
     [[0.5516309435734041, '↑'], [0.2934347863772087, '↓'], [0.7167255573827326, '→'], [0.36177064093774475, '←']],
     [[1.0, '*']]],
    [[[0.14145528124656256, '↑'], [-0.09084170632159716, '↓'], [0.021985680919856136, '→'],
      [0.021985680919856136, '←']], [[0.0, '↑'], [0.0, '↓'], [0.0, '→'], [0.0, '←']],
     [[0.35822582699563155, '↑'], [-0.052136131323774315, '↓'], [-0.7422951677576689, '→'], [0.23550898317516328, '←']],
     [[-1.0, '*']]],
    [[[-0.005154745884862078, '↑'], [-0.11687509761210652, '↓'], [-0.08963317715708871, '→'], [-0.10480675028750272, '←']],
     [[-0.08851624797145073, '↑'], [-0.08851624797145072, '↓'], [0.005677384241543525, '→'], [-0.11497840097080475, '←']],
     [[0.14907246992522372, '↑'], [-0.0030933311979867255, '↓'], [-0.1245792731957479, '→'], [-0.05441354967950589, '←']],
     [[-0.8155464044973666, '↑'], [-0.16555599028592122, '↓'], [-0.2687607840121239, '→'], [-0.09311284841394765, '←']]]]

    terminal_states = [[0, 3, 1], [1, 3, -1]]
    boulder_states = [[1, 1]]
    num_iterations = 10

    GUI.draw_board(window, grid, [row[:-1] for row in terminal_states], boulder_states,
               max_reward(terminal_states), max_punishment(terminal_states), num_iterations)

    window.mainloop()


main()