# IMPORTS
from tkinter import Y
import numpy as np
import random 

class snakeGame():

    """
    BOARD KEY
    0 is empty
    1 is snake head
    2 is the second snake piece
    3 is the third snake piece
    ...
    -1 is fruit
    """

    # PRIVATE
    __board = [] # Will contain the board array
    __boardDim = () # Will contain a tuple of the board dims

    dir = 0 # Will hold the direction of the snake (in bearings)

    # PUBLIC
    len = 0 # Length of the snake

    def __init__(self, numX, numY, startLen, startingDir):

        #region Board and Snake initialisation

        self.__board = np.array([[0 for y in range(numY)] for x in range(numX)]) # Defines the board

        self.__board[(int(round(numY/2, 0)), int(round(numX/2, 0)))] = 1 # Sets the centre of the board to a snake head
        for i in range(startLen): # Runs for each body segment of the snake
            self.__board[int(round(numY/2 + i+1, 0)), int(round(numX/2, 0))] = i+2 # Sets the square as a body
        self.__board[(int(round(numY/2 + (startLen + 1), 0)), int(round(numX/2, 0)))] = (startLen+2) # Sets the end of snake to a tail
        
        self.__boardDim = (numX, numY)

        #endregion
    
        self.dir = startingDir

        self.len = startLen

        self.genFruit()

    def moveSnake(self): # A function to move the snake on the screen, returns true if it survives, false if it doesn't
        headPos = np.argwhere(self.__board == 1)[0] # Finds the snakes head
        tailPos = np.argwhere(self.__board == (np.amax(self.__board)))[0] # Finds the snakes tail

        ateFruit = False

        for y in range(self.__boardDim[0]): # Runs for every square on the board
            for x in range(self.__boardDim[1]):
                if self.__board[x, y] > 0: # If the square is part of the snake
                    self.__board[x, y] += 1 # It increases its number by one

        # \/ \/ Moves the snakes head forward \/ \/
        if self.dir == 0: # If the snake is moving North
            newHeadPos = ((headPos[0] - 1), (headPos[1])) # Moves the snakes head forward one
        elif self.dir == 90: # If the snake is moving East
            newHeadPos = ((headPos[0]), (headPos[1]) + 1) # Moves the snakes head forward one
        elif self.dir == 180: # If the snake is moving South
            newHeadPos = ((headPos[0] + 1), (headPos[1])) # Moves the snakes head forward one
        elif self.dir == 270: # If the snake is moving West
            newHeadPos = ((headPos[0]), (headPos[1]) - 1) # Moves the snakes head forward one

        # Detects snake and walls
        if headPos[0] == 0 and self.dir == 0: # Checks if the snake is about to go off the top of the map
            crashed = True
        elif headPos[0] == self.__boardDim[1] - 1 and self.dir == 180:
            crashed = True
        elif headPos[1] == 0 and self.dir == 270:
            crashed = True
        elif headPos[1] == self.__boardDim[0] - 1 and self.dir == 90:
            crashed = True
        elif self.__board[newHeadPos] > 0:
            crashed = True
        else:
            crashed = False

        if not crashed:
            if self.__board[newHeadPos] == -1: # Checks if the snake is moving onto a piece of fruit
                self.len += 1
                self.genFruit()
            
            else: # If a fruit was eaten, the tail shouldnt be removed. This makes the snake longer.
                self.__board[(tailPos[0]), tailPos[1]] = 0 # Gets rid of the snakes tail
            
            self.__board[newHeadPos] = 1 # Sets the new head pos to a head. This must be done after checking for fruit

            return True

        else:
            return False

    # PYGAME YET TO BE IMPLEMENTED
    def showBoard(self, pygame): # Pygame is a bool that determines whether or not the board should be shown as a pygame screen
        if not pygame:
            print(self.__board)

    def genFruit(self): # Generates a new fruit in a random position
        placingFruit = True
        while placingFruit: # In a while loop so it keeps going until it is succesfully placed
            attemptCoords = (random.randint(0, (self.__boardDim[1] - 1)), random.randint(0, (self.__boardDim[0] - 1))) # Generates a random location on the board, subtracted by one because arrays start counting from 0, not 1
            if self.__board[attemptCoords] == 0: # Checks if that pos is empty
                self.__board[attemptCoords] = -1 # Adds a fruit there
                placingFruit = False 

    def changeDir(self, newDirection):
        if not self.dir + 180 == newDirection or not self.dir - 180 == newDirection:
            self.dir = newDirection

    def getNNInputs(self): # Gets the input for the neural network
        """
        Distances in 8 directions to 3 things, fruit, snake tail, and walls
        Returns 0 if there isn't one of this things in that direction
        """
        """
        Trying out a new system to simplify neural networks.
        Looks in the 4 cardinal directions and returns 1 if there is a fruit, 0 if there is a snake body and -1 if there is nothing
        """

        headPos = np.argwhere(self.__board == 1)[0]

        posX = 0
        negX = 0
        posY = 0
        negY = 0

        if not headPos[0] + 1 > self.__boardDim[0]:
            if not self.__board[headPos[0] + 1, headPos[1]] >= 1:
                for i in range(self.__boardDim[0] - headPos[0]):
                    squareCoords = (headPos[0] + i, headPos[1])
                    if self.__board[squareCoords] == -1:
                        posX = 1
            else:
                posX = -1
        else:
            posX = -1

        if not headPos[0] - 1 > self.__boardDim[0]:
            if not self.__board[headPos[0] - 1, headPos[1]] >= 1:
                for i in range(headPos[0]):
                    squareCoords = (headPos[0] - i, headPos[1])
                    if self.__board[squareCoords] >= 1:
                        negX = 0
                    elif self.__board[squareCoords] == -1:
                        negX = 1
            else:
                negX = -1
        else:
            negX = -1

        if not headPos[1] + 1 > self.__boardDim[1]:
            if not self.__board[headPos[0], headPos[1] + 1] >= 1:
                for i in range(self.__boardDim[1] - headPos[1]):
                    squareCoords = (headPos[0], headPos[1] + i)
                    if self.__board[squareCoords] >= 1:
                        posY = 0
                    elif self.__board[squareCoords] == -1:
                        posY = 1
            else:
                posY = -1
        else:
            posY = -1

        if not headPos[1] - 1 > self.__boardDim[1]:
            if not self.__board[headPos[0], headPos[1] - 1] >= 1:    
                for i in range(headPos[1]):
                    squareCoords = (headPos[0], headPos[1] - i)
                    if self.__board[squareCoords] >= 1:
                        negY = 0
                    elif self.__board[squareCoords] == -1:
                        negY = 1
            else:
                negY = -1
        else:
            negY = -1
        
        return (posX, negX, posY, negY)

        

"""
Program Decomposition and requirements.

Must be able to return the final length of the snake
Must have a flexible input system (Not just button presses)
Only show the screen if a certain variable is true

1. Set up an empty grid, with the snake starting in the correct position
2. Allow inputs to change direction
3. Randomly place a fruit each time one is eaten, and make the snake a tile longer.

4. Give board information each frame (so that a NN can be trained on it in the future.)
"""