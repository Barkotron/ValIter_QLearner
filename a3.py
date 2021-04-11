import re
import numpy as np
import tkinter as tk

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
      BOULDER.append([int(tokens[i+2]),int(tokens[i+1])])
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
    self.episodes = episodes
    self.noise = noise
    self.startState = startState
    self.transitionCost = transitionCost
    self.boulder = boulder
    self.terminal = terminal
  
  
        

  #of 1 state
  def getValue(self, state):
    
    # if state we're checking is outside the grid
    '''if state[0] < 0 or state[0] > len(self.grid) or state[1] < 0 or state[1] > len(self.grid[0]):
      return 0'''

    values = []
    for val in self.grid[state[0]][state[1]]:
      #print(f"val: {val} i: {state[0]} j: {state[1]}")
      #print(f"val[0]: {val[0]}")
      values.append(val[0])

    return max(values)
    

  def getQValue(self, state, action):
    pass

  def getPolicy(self, state):
    pass

  def getAction(self, state):
    pass
  
  def iterate(self):
    
    rows = len(self.grid)  # Number of rows in the grid
    cols = len(self.grid[0])

    print(f"(1,4) val: {self.transitionCost + self.discount*self.getValue((1,5))}")
    #state = self.startState


    for iter in range(self.k):
      for i in range(rows):
        for j in range(cols):
          
          #vk = self.discount*self.getValue((i,j))
          #print(f"vk: {vk}")
          

          up = down = left = right = 0

          valid = (i+1 < rows and i-1 > 0 and j+1 < cols and j-1 > 0)
          mainProb = (1-self.noise)

          


          # [this][][][] is the x coord
          # [][this][][] is the y coord
          # []][][this][] is which of the 4 neighbouring cells it would go to
          # []][][][this] is the value (if it was [1] that would be the arrow)
          if valid:
            self.grid[i][j][0][0] = (mainProb*(self.transitionCost + (self.discount*self.getValue((i-1,j)))))
            #print(f"thing: {self.getValue((i+1,j))}")
            #print(f"sample val: {(self.grid[i][j][0][0])}")
          if valid:
            self.grid[i][j][1][0] = (mainProb*(self.transitionCost + (self.discount*self.getValue((i+1,j)))))
          if valid:
            self.grid[i][j][2][0] = (mainProb*(self.transitionCost + (self.discount*self.getValue((i,j-1)))))
          if valid:
            self.grid[i][j][3][0] = (mainProb*(self.transitionCost + (self.discount*self.getValue((i,j+1)))))
          
          #self.grid[i][j] vk1 = max(up,down,left,right)

def main():

    #(self,grid,terminal,boulder, startState, k, episodes, alpha, discount, noise, transitionCost)
    
    window = tk.Tk()
    readInput('gridConf.txt')
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