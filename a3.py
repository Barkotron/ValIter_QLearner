import re
import numpy as np
import tkinter as tk
import copy
import random
import GUI as gg
import RL_GUI as rl

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
        if term[1] == h and term[0] == v:
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

  
class QLearningAgent:

    def __init__(self,grid,terminal,boulder, startState, k, episodes, alpha, discount, noise, transitionCost):


        self.grid = grid
        self.discount = discount
        self.alpha = alpha
        self.episodes = episodes
        self.noise = noise
        self.startState = [startState[1],startState[0]]
        self.transitionCost = transitionCost
        self.boulder = []
        for b in boulder:
            self.boulder.append([b[1],b[0]])
        self.terminal = []
        for t in terminal:
            self.terminal.append([t[1],t[0],t[2]])
            
        print(f"New Boudler is: {self.boulder}\n and New Termianl is: {self.terminal}")
    
    #of 1 state
    def getValue(self, state):
    
        # if state we're checking is outside the grid
        if state[0] < 0 or state[0] > len(self.grid[0]) or state[1] < 0 or state[1] > len(self.grid):
            return 0        
        else:
            # print(f" strange: {state}")
            # print(f"x: {len(self.grid[0])}")
            # print(f"y: {len(self.grid)}")
            # print(f" umm: {self.grid}")
            
            # rows = len(self.grid[0])  # Number of rows in the grid
            # cols = len(self.grid)
            # for i in range(cols):
            #     print(self.grid[i])
                # for j in range(cols):
                #     print(self.grid[i][j])
                
            best = self.grid[state[0]][state[1]][0]
            # print(f" best: {best}")
            for val in self.grid[state[0]][state[1]]:
                # print(f" val: {val}")
                if val[0] > best[0]:
                    best = val
        return best
      
    def getQValue(self, state, action):    
        oldValue = self.transitionCost + (self.getValue(state)[0]*(1-self.discount))
        newValue = self.transitionCost + (self.getValue(action)[0]*(self.discount))
        qValue = oldValue + newValue
        return qValue

    def getPolicy(self, state):
        pass
    
    #Chooses which direction the machine will try to move
    def getAction(self, state):
        bestOption = self.getValue(state)
        #If the best option available to us is 0, then choose a random direction
        if bestOption[0] == 0:
            temp = self.grid[state[0]][state[1]]
            bestOption = temp[random.randrange(3)]
        
        #Now that we know which way we want to go, determine if we get blown off course
        chance = random.random()
        if chance > self.noise:
            chosenOption = bestOption
        elif chance > self.noise/2:
            temp = self.grid[state[0]][state[1]]            
            if bestOption[1] == '↑':
                chosenOption = temp[1]
            elif bestOption[1] == '←':
                chosenOption = temp[2]
            elif bestOption[1] == '↓':
                chosenOption = temp[3] 
            else:
                chosenOption = temp[0]
        else:
            temp = self.grid[state[0]][state[1]]                
            if bestOption[1] == '↑':
                chosenOption = temp[3]
            elif bestOption[1] == '←':
                chosenOption = temp[0]
            elif bestOption[1] == '↓':
                chosenOption = temp[1] 
            else:
                chosenOption = temp[2]
                
        return chosenOption
        
    #will return the state that it will be in after the move
    def move(self, position, direction):
        # print(f" position: {position}")
        if direction == '↑':
            newState = [position[0],position[1]+1]
        elif direction == '←':
            newState = [position[0]-1,position[1]]
        elif direction == '↓':
            newState = [position[0],position[1]-1]
        else:
            newState = [position[0]+1,position[1]]
            
        rows = len(self.grid)  # Number of rows in the grid
        cols = len(self.grid[0])
        
        # print(f"What is this: {rows}, and {cols}")
        # print(f" newState: {newState}")
        #if the move is not valid eg. moving into a wall. Then we will end up where we started
        # upValid = newState[0]+1 < rows
        # downValid = newState[0]-1 >= 0
        # leftValid = newState[1]-1 >= 0
        # rightValid = newState[1]+1 < cols
        
        # if state we're checking is outside the grid
    # if state[0] < 0 or state[0] > len(self.grid) or state[1] < 0 or state[1] > len(self.grid[0]):
        # print(f"Move Check: {newState}")
        validMove = (newState[0]+1 < rows and newState[0] >= 0 and newState[1]+1 < cols and newState[1] >= 0)
        # print(f"validMove: {validMove}")
        for boulder in self.boulder:
            #Grid is x,y but boulder and terminal are y,x
            if boulder[0] == newState[0] and boulder[1] == newState[1]:
              validMove = False
        if not validMove:
            print("Not Valid Move")
            newState = position
        return newState
    
    #updates the q-values of the previous state
    def update(self, position,direction,newState):
        # print(f"New Boudler is: {self.boulder}\n and New Termianl is: {self.terminal}")
        # print(f" position: {position} NewState {newState}")
        qValue = self.getQValue(position, newState)  
        # print(f"qValue: {qValue}")
        # print(f" update value: {self.grid[position[0]][position[1]][0]}")
        # print(f" update value: {self.grid[position[0]][position[1]][1]}")
        # print(f" update value: {self.grid[position[0]][position[1]][2]}")
        # print(f" update value: {self.grid[position[0]][position[1][0]]}")
        if direction == '↑':
            self.grid[position[0]][position[1]][0][0] = qValue
        elif direction == '←':
            self.grid[position[0]][position[1]][1][0] = qValue
        elif direction == '↓':
            self.grid[position[0]][position[1]][2][0] = qValue 
        else:
            self.grid[position[0]][position[1]][3][0] = qValue
            
    # def update(self, position):
    #     for term in self.terminal:
    #             if term[0] == position[0] and term[1] == position[1]:
    #               value = term[2]
                  
    #     self.grid[position[0]][position[1][0][0]] = value
        
    
    def explore(self):
        position = self.startState
        step = 0
        for episode in range(self.episodes):
            # print(f"\nCurrent Position: {position}")
            # print(f" Step: {step}")
            # print(f" grid: {self.grid}")
            
            #check if we are in a terminal state
            
            # if step%20 == 0:
            #     window = tk.Tk()
            #     draw_board(window, self.grid, [row[:-1] for row in self.terminal], self.boulder,
            #        max_reward(self.terminal), max_punishment(self.terminal), step)    
            #     window.mainloop()
                
            terminal = False
            for term in self.terminal:
                if term[0] == position[0] and term[1] == position[1]:
                  terminal = True
            if terminal:
                # print(" Reached Terminal state")
                step = step+1
                #exit and try again
                # self.update(position)
                position = self.startState
            else:
                #behave normally
                chosenAction = self.getAction(position)
                # print(f" ChosenAction is: {chosenAction}")
                newState = self.move(position, chosenAction[1])
                # print(f" NewState is: {newState}")
                self.update(position,chosenAction[1],newState)
                # print("fChosenAction is: {chosenAction}")
                position = newState
        print(f"\nReached Terminal State {step} Times.\n")
        # window = tk.Tk()
        # RLGUI.draw_board(window, self.grid, [row[:-1] for row in self.terminal], self.boulder,
        #             RLGUI.max_reward(self.terminal), RLGUI.max_punishment(self.terminal), self.episodes)
    
        # window.mainloop()
            
        
    

def main():

    #(self,grid,terminal,boulder, startState, k, episodes, alpha, discount, noise, transitionCost)
    
    
    alltests = False
    if alltests:
        all_inputs()
    else:         
        #now for Q-Learning
        print("\n Now for Q-Learning\n")
        window = tk.Tk()
        readInput('gridConf.txt')
        #readInput('gridConfAlt.txt')
        #readInput('gridConfAlt2.txt')
        # readInput('gridConfSmall3.txt')
        grid = createGrid(HORIZONTAL,VERTICAL)
        # print(grid)
        tests()
        qLearner = QLearningAgent(grid,TERMINAL,BOULDER,ROBOTSTARTSTATE,K,EPISODES,ALPHA,DISCOUNT,NOISE,TRANSITION_COST)
        qLearner.explore()
        grid = qLearner.grid
        print(grid)
        tests()
    
        rows = HORIZONTAL
        cols = VERTICAL
        terminal_states = TERMINAL
        boulder_states = BOULDER
        num_iterations = EPISODES
    
        # gg.draw_board(window, grid, [row[:-1] for row in terminal_states], boulder_states,
        #            gg.max_reward(terminal_states), gg.max_punishment(terminal_states), num_iterations)
    
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