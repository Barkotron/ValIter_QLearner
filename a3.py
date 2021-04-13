import re
import numpy as np
import tkinter as tk
import copy
import random

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



class ValueIterationAgent:

  def __init__(self,grid,terminal,boulder, startState, k, episodes, alpha, discount, noise, transitionCost):


    self.grid = grid
    self.discount = discount
    self.k = k
    self.alpha = alpha
    #self.episodes = episodes
    self.noise = noise
    self.startState = startState
    self.transitionCost = transitionCost
    self.boulder = boulder
    self.terminal = terminal
  
  
        

  #of 1 state
  def getValue(self, state):
    
    # if state we're checking is outside the grid
    if state[0] < 0 or state[0] > len(self.grid) or state[1] < 0 or state[1] > len(self.grid[0]):
      return 0

    else:
      values = []
      for val in self.grid[state[0]][state[1]]:
        #print(f"val: {val} i: {state[0]} j: {state[1]}")
        #print(f"val[0]: {val[0]}")
        values.append(val[0])
      return max(values)
    

  
  
  def iterate(self):
    
    rows = len(self.grid)  # Number of rows in the grid
    cols = len(self.grid[0])

    #print(f"(1,4) val: {self.transitionCost + self.discount*self.getValue((1,5))}")
    #state = self.startState

    

    for iteration in range(self.k):
      
      self.newGrid = copy.deepcopy(self.grid)
      
      for i in range(rows):
        for j in range(cols):
          
          #vk = self.discount*self.getValue((i,j))
          #print(f"vk: {vk}")
          
          terminal_or_boulder = False

          for term in self.terminal:
            if term[0] == i and term[1] == j:
              terminal_or_boulder = True

          for boulder in self.boulder:
            if boulder[0] == i and boulder[1] == j:
              terminal_or_boulder = True

          if not terminal_or_boulder:
            up = down = left = right = 0

            valid = (i+1 < rows and i-1 >= 0 and j+1 < cols and j-1 >= 0)
            mainProb = (1-self.noise)
            noiseProb = self.noise/2

            upValid = i+1 < rows
            downValid = i-1 >= 0
            leftValid = j-1 >= 0
            rightValid = j+1 < cols

            # [this][][][] is the x coord
            # [][this][][] is the y coord
            # []][][this][] is which of the 4 neighbouring cells it would go to (up,left,down,right)
            # []][][][this] is the value (if it was [1] that would be the arrow since they look like: [0,'↑'])
            if upValid: #up
              #self.newGrid[i][j][0][0] = (mainProb*(self.transitionCost + (self.discount*self.getValue((i+1,j)))))
              up = (mainProb*(self.transitionCost + (self.discount*self.getValue((i+1,j)))))
              if rightValid:
                up += (noiseProb*(self.transitionCost + (self.discount*self.getValue((i,j+1)))))
              if leftValid:
                up += (noiseProb*(self.transitionCost + (self.discount*self.getValue((i,j-1)))))
            if leftValid:#left
              #self.newGrid[i][j][1][0] = (mainProb*(self.transitionCost + (self.discount*self.getValue((i,j-1)))))
              left = (mainProb*(self.transitionCost + (self.discount*self.getValue((i,j-1)))))
              if upValid:
                left += (noiseProb*(self.transitionCost + (self.discount*self.getValue((i+1,j)))))
              if downValid:
                left += (noiseProb*(self.transitionCost + (self.discount*self.getValue((i-1,j)))))
            if downValid:#down
              #self.newGrid[i][j][2][0] = (mainProb*(self.transitionCost + (self.discount*self.getValue((i-1,j)))))
              down = (mainProb*(self.transitionCost + (self.discount*self.getValue((i-1,j)))))
              if rightValid:
                down += (noiseProb*(self.transitionCost + (self.discount*self.getValue((i,j+1)))))
              if leftValid:
                down += (noiseProb*(self.transitionCost + (self.discount*self.getValue((i,j-1)))))
            if rightValid:#right
              #self.newGrid[i][j][3][0] = (mainProb*(self.transitionCost + (self.discount*self.getValue((i,j+1)))))
              right = (mainProb*(self.transitionCost + (self.discount*self.getValue((i,j+1)))))
              if upValid:
                right += (noiseProb*(self.transitionCost + (self.discount*self.getValue((i+1,j)))))
              if downValid:
                right += (noiseProb*(self.transitionCost + (self.discount*self.getValue((i-1,j)))))

            self.newGrid[i][j][0][0] = up
            self.newGrid[i][j][1][0] = left
            self.newGrid[i][j][2][0] = down
            self.newGrid[i][j][3][0] = right
          
      self.grid = copy.deepcopy(self.newGrid)
    
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
        print(f"Move Check: {newState}")
        validMove = (newState[0]+1 < rows and newState[0] >= 0 and newState[1]+1 < cols and newState[1] >= 0)
        print(f"validMove: {validMove}")
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
        print(f"New Boudler is: {self.boulder}\n and New Termianl is: {self.terminal}")
        # print(f" position: {position} NewState {newState}")
        qValue = self.getQValue(position, newState)  
        print(f"qValue: {qValue}")
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
            print(f"\nCurrent Position: {position}")
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
                print(" Reached Terminal state")
                step = step+1
                #exit and try again
                # self.update(position)
                position = self.startState
            else:
                #behave normally
                chosenAction = self.getAction(position)
                print(f" ChosenAction is: {chosenAction}")
                newState = self.move(position, chosenAction[1])
                print(f" NewState is: {newState}")
                self.update(position,chosenAction[1],newState)
                # print("fChosenAction is: {chosenAction}")
                position = newState
        print(f"\nReached Terminal State {step} Times.\n")
            
        
    

def main():

    #(self,grid,terminal,boulder, startState, k, episodes, alpha, discount, noise, transitionCost)
    
    
    alltests = False
    if alltests:
        all_inputs()
    else: 
        window = tk.Tk()
        readInput('gridConf.txt')
        #readInput('gridConfAlt.txt')
        #readInput('gridConfAlt2.txt')
        # readInput('gridConfSmall.txt')
        grid = createGrid(HORIZONTAL,VERTICAL)
        print(grid)
        valIter = ValueIterationAgent(grid,TERMINAL,BOULDER,ROBOTSTARTSTATE,K,EPISODES,ALPHA,DISCOUNT,NOISE,TRANSITION_COST)
        valIter.iterate()
        grid = valIter.grid
        print(grid)
        tests()
    
        terminal_states = TERMINAL
        boulder_states = BOULDER
        num_iterations = K
    
        draw_board(window, grid, [row[:-1] for row in terminal_states], boulder_states,
                    max_reward(terminal_states), max_punishment(terminal_states), num_iterations)
    
        window.mainloop()
        
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
        # print(grid)
        tests()
    
        terminal_states = TERMINAL
        boulder_states = BOULDER
        num_iterations = EPISODES
    
        draw_board(window, grid, [row[:-1] for row in terminal_states], boulder_states,
                    max_reward(terminal_states), max_punishment(terminal_states), num_iterations)
    
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

def max_reward(terminal_states):
    max_reward = float('-inf')

    for state in terminal_states:
        if state[2] > max_reward:
            max_reward = state[2]

    return max_reward


def max_punishment(terminal_states):
    max_punishment = float('inf')

    for state in terminal_states:
        if state[2] < max_punishment:
            max_punishment = state[2]

    return max_punishment



def draw_board(window, grid, terminal, boulders, max_reward, max_punishment, iterations):

    canvas_width = 1000  # Width of the window
    canvas_height = 600  # Length of the window

    edge_dist = 10  # Distance of the board to the edge of the window
    bottom_space = 100  # Distance from the bottom of the board to the bottom of the window
    small_rect_diff = 10  # For terminal states, distance from outside rectangle to inside rectangle

    rows = len(grid)  # Number of rows in the grid
    cols = len(grid[0])  # Number of columns in the grid

    edge_dist_triangle = 5  # Distance from tip of the triangle to the edge of the rectangle
    triangle_height = int(0.1 * min(((canvas_width - 2 * edge_dist) / cols), ((canvas_height - edge_dist - bottom_space) / rows)))  # Height of the triangles
    triangle_width = 2 * triangle_height  # Width of the triangles

    canvas = tk.Canvas(window, width=canvas_width, height=canvas_height, background='black')  # Create a black background

    for row in range(rows - 1, -1, -1):  # Loop through the rows of the grid
        for col in range(cols):  # Loop through the columns of the grid
            #print(row, col)
            if [row, col] not in boulders:  # If it's not a boulder state
                x1 = edge_dist + col * ((canvas_width - 2 * edge_dist) / cols)  # Top left x coordinate of the rectangle
                y1 = edge_dist + (rows - row - 1) * ((canvas_height - edge_dist - bottom_space) / rows)  # Top left y coordinate of the rectangle
                #print(x1, y1)
                x2 = x1 + ((canvas_width - 2 * edge_dist) / cols)  # Bottom right x coordinate of the rectangle
                y2 = y1 + ((canvas_height - edge_dist - bottom_space) / rows)  # Bottom right y coordinate of the rectangle

                best_move = get_best_move(grid[row][col])  # Get the index of the maximum q-value for this cell
                best_value = grid[row][col][best_move][0]  # Get the best q-value for this cell
                best_direction = grid[row][col][best_move][1]  # Get the best direction out of this cell

                if best_value >= 0:  # Best value is positive, so draw the rectangle in green
                    canvas.create_rectangle(x1, y1, x2, y2, outline='white',
                                            fill='#%02x%02x%02x' % (0, int(200 * min(best_value / max_reward, max_reward)), 0))  # Draw the rectangle of this cell
                else:  # Best value is negative, so draw the rectangle in red
                    canvas.create_rectangle(x1, y1, x2, y2, outline='white',
                                            fill='#%02x%02x%02x' % (int(200 * min(best_value / max_punishment, -1 * max_punishment)), 0, 0))  # Draw the rectangle of this cell

                canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=str(round(best_value, 2)),
                                   font=('TkDefaultFont', int(0.25 * ((canvas_width - 2 * edge_dist) / cols))), fill='white')  # Print the best value in the middle of the cell

                if [row, col] in terminal:  # If this cell is a terminal state
                    #print("TERMINAL: ", row, col)
                    x1 = x1 + small_rect_diff
                    y1 = y1 + small_rect_diff
                    x2 = x2 - small_rect_diff
                    y2 = y2 - small_rect_diff
                    canvas.create_rectangle(x1, y1, x2, y2, outline='white')  # Draw a smaller rectangle inside
                else:  # Not a terminal state, so draw an arrow in the direction of the highest q-value
                    if best_direction == '↑':  # Draw an up arrow
                        mid = (x1 + x2) / 2
                        top = y1 + edge_dist_triangle
                        triange_points = [mid, top, mid - triangle_width / 2, top + triangle_height, mid + triangle_width / 2, top + triangle_height]
                        canvas.create_polygon(triange_points, fill='white')
                    elif best_direction == '↓':  # Draw a down arrow
                        mid = (x1 + x2) / 2
                        top = y2 - edge_dist_triangle
                        triange_points = [mid, top, mid - triangle_width / 2, top - triangle_height,
                                          mid + triangle_width / 2, top - triangle_height]
                        canvas.create_polygon(triange_points, fill='white')
                    elif best_direction == '←':  # Draw a left arrow
                        mid = (y1 + y2) / 2
                        top = x1 + edge_dist_triangle
                        triange_points = [top, mid, top + triangle_height, mid - triangle_width / 2,
                                          top + triangle_height, mid + triangle_width / 2]
                        canvas.create_polygon(triange_points, fill='white')
                    elif best_direction == '→':  # Draw a right arrow
                        mid = (y1 + y2) / 2
                        top = x2 - edge_dist_triangle
                        triange_points = [top, mid, top - triangle_height, mid - triangle_width / 2,
                                          top - triangle_height, mid + triangle_width / 2]
                        canvas.create_polygon(triange_points, fill='white')

            else:  # This is a boulder state
                x1 = edge_dist + col * ((canvas_width - 2 * edge_dist) / cols)
                y1 = edge_dist + (rows - row - 1) * ((canvas_height - edge_dist - bottom_space) / rows)
                x2 = x1 + ((canvas_width - 2 * edge_dist) / cols)
                y2 = y1 + ((canvas_height - edge_dist - bottom_space) / rows)
                canvas.create_rectangle(x1, y1, x2, y2, fill='grey', outline='white')

    canvas.create_text(int(canvas_width / 2), canvas_height - bottom_space / 2, font=('TkDefaultFont', int(bottom_space / 2)),
                       text=('VALUE AFTER ' + str(iterations) + ' ITERATIONS'), fill='white')  # Write text at the bottom of the canvas

    canvas.pack()


def get_best_move(state):
    max_value = float('-inf')
    max_index = -1

    for move in range(len(state)):
        if state[move][0] > max_value:
            max_index = move
            max_value = state[move][0]
    return max_index

main()