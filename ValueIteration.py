import copy

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

  
  def getValue(self, state, target):
    '''
    gets the value of a target state, if target is unreachable (like an edge or a boulder) then the current states value is returned

    Args:
      state(x,y): current state whose value is being updated
      target(x,y): target state to get value from
    Return:
      (float): maximum of the 4 values in a state
    '''
    
    #if you're trying to move into a boulder: 'bounce off' and stay where you tried to move from
    for boulder in self.boulder:
            if boulder[0] == target[0] and boulder[1] == target[1]:
              values = []
              for val in self.grid[state[0]][state[1]]:
                values.append(val[0])
              return max(values)

    # if state we're checking is outside the grid: stay where you tried to move from
    if target[0] < 0 or target[0] >= len(self.grid) or target[1] < 0 or target[1] >= len(self.grid[0]):
      values = []
      for val in self.grid[state[0]][state[1]]:
        values.append(val[0])
      return max(values)
    
    else: # get max value of target state
      values = []
      for val in self.grid[target[0]][target[1]]:
        values.append(val[0])
      return max(values)
  
  def iterate(self):
    '''
    the value iteration algorithm. updates its own grid member

    Args:
      none
    Return:
      none
    '''
    
    rows = len(self.grid)
    cols = len(self.grid[0])

    for iteration in range(1,self.k):
      
      #Copy the grid so we aren't using values that were updated within the same iteration
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

            #up
            up = ((self.discount*(self.getValue((i,j),(i+1,j)))))

            #left
            left = ((self.discount*(self.getValue((i,j),(i,j-1)))))

            #down
            down = ((self.discount*(self.getValue((i,j),(i-1,j)))))

            #right
            right = ((self.discount*(self.getValue((i,j),(i,j+1)))))

            totalUp = mainProb*up + noiseProb*left + noiseProb*right
            totalLeft = mainProb*left + noiseProb*up + noiseProb*down
            totalDown = mainProb*down + noiseProb*left + noiseProb*right
            totalRight = mainProb*right + noiseProb*up + noiseProb*down


            # [this][][][] is the x coord
            # [][this][][] is the y coord
            # []][][this][] is which of the 4 neighbouring cells it would go to (up,left,down,right)
            # []][][][this] is the value if [0] (if [1] that would be the arrow since they look like: [0,'???'])
            self.newGrid[i][j][0][0] = totalUp + self.transitionCost
            self.newGrid[i][j][1][0] = totalLeft + self.transitionCost
            self.newGrid[i][j][2][0] = totalDown + self.transitionCost
            self.newGrid[i][j][3][0] = totalRight + self.transitionCost
      
      #update the grid with the new values for the next iteration
      self.grid = copy.deepcopy(self.newGrid)