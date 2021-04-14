import re
import numpy as np
import tkinter as tk
import copy
import random

class QLearningAgent:

    def __init__(self,grid,terminal,boulder, startState, k, episodes, alpha, discount, noise, transitionCost):
    
    
        self.grid = grid
        self.discount = discount
        self.alpha = alpha
        self.episodes = episodes
        self.noise = noise
        self.startState = startState
        # self.startState = [startState[1],startState[0]]
        self.transitionCost = transitionCost
        self.boulder = boulder
        self.terminal = terminal
        # self.boulder = []
        # for b in boulder:
        #     self.boulder.append([b[1],b[0]])
        # self.terminal = []
        # for t in terminal:
        #     self.terminal.append([t[1],t[0],t[2]])
            
        # print(f"New Boudler is: {self.boulder}\n and New Termianl is: {self.terminal}")
    
    #of 1 state
    def getValue(self, state):
    
        # # if state we're checking is outside the grid
        # if state[0] < 0 or state[0] > len(self.grid) or state[1] < 0 or state[1] > len(self.grid[0]):
        #     return 0        
        # else:
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
    
    #Chooses which direction the machine will try to move
    def getAction(self, state, episode):
        randomActionChance = 0.10
        if random.random() < randomActionChance:
            #don't always choose the best option
            temp = self.grid[state[0]][state[1]]
            bestOption = temp[random.randrange(3)]
        else:
            bestOption = self.getValue(state)
            #If the best option available to us is 0, then choose a random direction
            if bestOption[0] == 0:
                print("Choosing Random")
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
        # print(f" position: {position}")
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
        validMove = (newState[0] < rows and newState[0] >= 0 and newState[1] < cols and newState[1] >= 0)
        # print(f"validMove: {validMove}")
        for boulder in self.boulder:
            #Grid is x,y but boulder and terminal are y,x
            if boulder[0] == newState[0] and boulder[1] == newState[1]:
              validMove = False
        if not validMove:
            # print("Not Valid Move")
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
        terminated = 0
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
                terminated = terminated+1
                #exit and try again
                # self.update(position)
                position = self.startState
            else:
                #behave normally
                chosenAction = self.getAction(position, episode)
                # print(f"\nChosenAction is: {chosenAction}")
                newState = self.move(position, chosenAction[1])
                # print(f"NewState is: {newState}")
                self.update(position,chosenAction[1],newState)
                position = newState
        print(f"\nReached Terminal State {terminated} Times.\n")
            
  
