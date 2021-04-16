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
    
    def getValue(self, state):
        '''
        Gets the best direction of a state and its value

        Parameters
        ----------
        state: list
            The grid coordinates (row,col) of the current state

        Returns
        -------
        best : list
            The direction with the highest value, represented as the float value and a char arrow

        '''
        best = self.grid[state[0]][state[1]][0]
        for val in self.grid[state[0]][state[1]]:
            if val[0] > best[0]:
                best = val
        return best
    
    def getQValue(self, oldState, newState): 
        '''
        Calculates the Q-Value for the update method

        Parameters
        ----------
        oldState: list
            The grid coordinates (row,col) of the previous state
        newState : list
            The grid coordinates (row,col) of the next state

        Returns
        -------
        qValue : float
            The new q-value of the previous state that will be updated

        '''
        oldValue = self.transitionCost + (self.getValue(oldState)[0]*(1-self.discount))
        newValue = self.transitionCost + (self.getValue(newState)[0]*(self.discount))
        qValue = oldValue + newValue
        return qValue
    
    def getPolicy(self, state, episode):
        '''
        Chooses which direction the machine will try to move

        Parameters
        ----------
        state: list
            The grid coordinates (row,col) of the current state
        episode : int
            How many episodes have been completed

        Returns
        -------
        chosenOption : list
            The coordinates of the next state the machine will try to move to

        '''
        
        #very high chance of random action at first, decreasing every episode
        randomActionChance = 0.75 - (episode/self.episodes)
        if random.random() < randomActionChance:
            #don't always choose the best option to better explore
            temp = self.grid[state[0]][state[1]]
            bestOption = temp[random.randrange(3)]
        else:
            #choose the best option
            bestOption = self.getValue(state)
            #If the best option available to us has a value of 0, then choose a random direction
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
    
        
    def move(self, position, direction):
        '''
        Returns the coordinates of the state that the machine will be in after the move

        Parameters
        ----------
        position : list
            The grid coordinates (row,col) of the current state
        direction : char
            A char arrow representing which direction the machine will attempt to move in

        Returns
        -------
        newState : list
            The grid coordinates (row,col) of the state where the machine will end up in after the move

        '''
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
    
    
    def update(self, position,direction,newState):
        '''
        Updates the q-values of the previous state

        Parameters
        ----------
        position : list
            The grid coordinates (row,col) of the previous state.
        direction : char arrow
            A char arrow representing which direction the machine is moveing in.
        newState : list
            The grid coordinates (row,col) of the new state.

        Returns
        -------
        None.

        '''     
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
        '''
        Will learn by exploring its enviroment for n episodes
        
        Parameters
        ----------
        None.
        
        Returns
        -------
        None.

        '''
        position = self.startState
        episode = 0
        while episode < self.episodes:  
            #check if in terminal state
            terminal = False
            for term in self.terminal:
                if term[0] == position[0] and term[1] == position[1]:
                  terminal = True
                  
            if terminal:
                #go to the start and try again
                episode = episode+1               
                position = self.startState
            else:
                #behave normally
                chosenAction = self.getPolicy(position, episode)
                newState = self.move(position, chosenAction[1])
                self.update(position,chosenAction[1],newState)
                position = newState
            
  
