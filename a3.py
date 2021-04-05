import re

#global variables for now, we may do something else with them
HORIZONTAL = 0
VERTICAL = 0
TERMINAL = []
BOULDER = []
K = 0
EPISODES = 0
DISCOUNT = 0
NOISE = 0
TRANSITION_COST = 0


def readInput(filename='gridConf.txt'):

  read = open(filename)
  for line in read:
    print(f"Line: {line}")
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
    HORIZONTAL = tokens[1]
  elif field == 'Vertical':
    global VERTICAL
    VERTICAL = tokens[1]
  elif field == 'Terminal':
    for i in range(1,len(tokens),4):
      global TERMINAL
      TERMINAL.append([tokens[i+1],tokens[i+2],tokens[i+3]])
  elif field == 'Boulder':
    for i in range(1,len(tokens),3):
      global BOULDER
      BOULDER.append([tokens[i+1],tokens[i+2]])
  elif field == 'RobotStartState':
    global ROBOTSTARTSTATE
    ROBOTSTARTSTATE = [tokens[1],tokens[2]]
  elif field == 'K':
    global K
    K = tokens[1]
  elif field == 'Episodes':
    global EPISODES
    EPISODES = tokens[1]
  elif field == 'Discount':
    global DISCOUNT
    DISCOUNT = tokens[1]
  elif field == 'Noise':
    global NOISE
    NOISE = tokens[1]
  elif field == 'TransitionCost':
    global TRANSITION_COST
    TRANSITION_COST = tokens[1]
  else:
    print("Unknown Field")

  print(tokens)

def tests():
  print("---Global Variables---")
  print(f"Horizontal: {HORIZONTAL}")
  print(f"Vertical: {VERTICAL}")
  print(f"Terminal: {TERMINAL}")
  print(f"Boulder: {BOULDER}")
  print(f"RobotStartState: {ROBOTSTARTSTATE}")
  print(f"K: {K}")
  print(f"Episodes: {EPISODES}")
  print(f"Discount: {DISCOUNT}")
  print(f"Noise: {NOISE}")
  print(f"TransitionCost: {TRANSITION_COST}")

class ValueIterationAgent():
  """
      * Please read learningAgents.py before reading this.*

      A ValueIterationAgent takes a Markov decision process
      (see mdp.py) on initialization and runs value iteration
      for a given number of iterations using the supplied
      discount factor.
  """
  def __init__(self, mdp, discount = 0.9, iterations = 100):
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


readInput('gridConf.txt')
tests()