# IMPORTS
import numpy as np

width = 16 # Number of squares across the board is
height = 16 # Number of squares the board is vertically
direction = 0 # Direction the snake is moving (0 = N, 90 = E, 180 = S, 270 = W)
snakeLength = 5 # Defines the starting length of the snake, doesn't include head or tail

# INITIALISATION
global board
board = np.array([[0 for x in range(width)] for y in range(height)]) # Creates an empty board with dimensions specified above
"""
BOARD KEY
0 is empty
1 is snake head
2 is the second snake piece
3 is the third snake piece
...
-1 is fruit
"""

board[(int(round(height/2, 0)), int(round(width/2, 0)))] = 1 # Sets the centre of the board to a snake head

for i in range(snakeLength): # Runs for each body segment of the snake
    board[(int(round(height/2 + (i+1), 0)), int(round(width/2, 0)))] = (i+2) # Sets the square as a body

board[(int(round(height/2 + (snakeLength + 1), 0)), int(round(width/2, 0)))] = (snakeLength+2) # Sets the end of snake to a tail

def moveSnake(direction): # A function to move the snake on the screen
    global board
    headPos = np.argwhere(board == 1) # Finds the snakes head
    tailPos = np.argwhere(board == (np.amax(board))) # Finds the snakes tail

    for y in range(board.shape[0]): # Runs for every square on the board
        for x in range(board.shape[1]):
            if board[x, y] > 0: # If the square is part of the snake
                board[x, y] += 1 # It increases its number by one

    if direction == 0: # If the snake is moving North
        board[(headPos - 1), (headPos)] = 1 # Moves the snakes head forward one
    elif direction == 90: # If the snake is moving East
        board[(headPos), (headPos + 1)] = 1 # Moves the snakes head forward one
    elif direction == 190: # If the snake is moving South
        board[(headPos - 1), (headPos)] = 1 # Moves the snakes head forward one
    elif direction == 270: # If the snake is moving West
        board[(headPos), (headPos - 1)] = 1 # Moves the snakes head forward one

    board[tailPos] = 0 # Gets rid of the snakes tail

print(board)

moveSnake(direction)

print(board)

"""
Program Decomposition and requirements.

Must be able to return the number of turns the user usrvived.
Must have a flexible input system (Not just button presses)
Only show the screen if a certain variable is true

1. Set up an empty grid, with the snake starting in the correct position
2. Allow inputs to change direction
3. Randomly place a fruit each time one is eaten, and make the snake a tile longer.

4. Give board information each frame (so that a NN can be trained on it in the future.)
"""