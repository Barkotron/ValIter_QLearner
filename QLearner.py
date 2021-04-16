import random

class QLearningAgent:

    def __init__(self,grid,terminal,boulder, startState, episodes, alpha, discount, noise, transitionCost):
        
        self.grid = grid
        self.discount = discount
        self.alpha = alpha
        self.episodes = episodes
        self.noise = noise
        self.startState = startState
        self.transitionCost = transitionCost
        self.boulder = boulder
        self.terminal = terminal
    
    #of 1 state
    def getValue(self, state):
        best = self.grid[state[0]][state[1]][0]
        for val in self.grid[state[0]][state[1]]:
            if val[0] > best[0]:
                best = val
        return best
    
    #calculates the Q-Value for the update method
    def getQValue(self, state, action):    
        oldValue = self.transitionCost + (self.getValue(state)[0]*(1-self.discount))
        newValue = self.transitionCost + (self.getValue(action)[0]*(self.discount))
        qValue = oldValue + newValue
        return qValue
    
    
    #Chooses which direction the machine will try to move
    def getPolicy(self, state, episode):
        #very high chance of random action at first, decreasing every episode
        randomActionChance = 0.75 - (episode/self.episodes)
        if random.random() < randomActionChance:
            #don't always choose the best option to better explore
            temp = self.grid[state[0]][state[1]]
            bestOption = temp[random.randrange(3)]
        else:
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
            #get blown to the left
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
            #get blown to the right
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
        if direction == '↑':
            newState = [position[0]+1,position[1]]
        elif direction == '←':
            newState = [position[0],position[1]-1]
        elif direction == '↓':
            newState = [position[0]-1,position[1]]
        else:
            newState = [position[0],position[1]+1]            
            
        rows = len(self.grid)  # Number of rows in the grid
        cols = len(self.grid[0])      
        # if we're try to move outside the grid
        validMove = (newState[0] < rows and newState[0] >= 0 and newState[1] < cols and newState[1] >= 0)
        for boulder in self.boulder:
            #cannot move into a boulder
            if boulder[0] == newState[0] and boulder[1] == newState[1]:
              validMove = False
        if not validMove:
            #if not a valid move stay in place
            newState = position
        return newState
    
    
    #updates the q-values of the previous state
    def update(self, position,direction,newState):
        qValue = self.getQValue(position, newState)  
        if direction == '↑':
            self.grid[position[0]][position[1]][0][0] = qValue
        elif direction == '←':
            self.grid[position[0]][position[1]][1][0] = qValue
        elif direction == '↓':
            self.grid[position[0]][position[1]][2][0] = qValue 
        else:
            self.grid[position[0]][position[1]][3][0] = qValue
        
    
    def explore(self):
        position = self.startState
        episode = 0
        while episode < self.episodes:      
            terminal = False
            for term in self.terminal:
                if term[0] == position[0] and term[1] == position[1]:
                  terminal = True
            if terminal:
                episode = episode+1
                #exit and try again
                position = self.startState
            else:
                #behave normally
                chosenAction = self.getPolicy(position, episode)
                newState = self.move(position, chosenAction[1])
                self.update(position,chosenAction[1],newState)
                position = newState
            
  
