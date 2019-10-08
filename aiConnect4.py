import sys
import math
import random
import pygame as pyg
import numpy as np

#players
HUMAN = 0 #player human
AI = 1 #player ai

#player's value
EMPTY = 0 #empty space in the board
HUMAN_VAL = 1 #human value
AI_VAL = 2 #ai value

#board dimension
ROW = 6
COLUMN = 7

#board layout
BOARDSIZE = 100 #size of the gui board
RADIUS = int(BOARDSIZE/2 - 3) #size of the circle in the gui board
BLUE = (0,191,255) #background
PINK = (199,21,133) #tiles
BLACK = (0,0,0) #human
WHITE = (255,255,255) #ai

WINNER = 4 #winner connects 4 dots
excess = COLUMN - WINNER #no of sub lists to be checked

# def createBoard():
# 	board = np.zeros((ROW,COLUMN))
# 	return board

def createBoard(board): #create the gui board
	for c in range(COLUMN):
		for r in range(ROW):
			pyg.draw.rect(screen, BLUE, (c*BOARDSIZE, BOARDSIZE*(r+1), BOARDSIZE, BOARDSIZE))
			pyg.draw.circle(screen, PINK, (int(BOARDSIZE*(c+1/2)), int(BOARDSIZE*(r+1/2))), RADIUS)

	pyg.display.update()

def drawMove(board, row, column, piece): #update the board by changing the color of the circle depending on the value of the board
    if board[row][column] == HUMAN_VAL:
        pyg.draw.circle(screen, BLACK, (int(BOARDSIZE*(column+1/2)), int(BOARDSIZE*(row+1/2))), RADIUS)
    else:
        pyg.draw.circle(screen, WHITE, (int(BOARDSIZE*(column+1/2)), int(BOARDSIZE*(row+1/2))), RADIUS)

    pyg.display.update()

def isVictory(board, piece): #check if the player is already a winner
    for c in range(COLUMN): #check for vertical winner
        end = WINNER
        for r in range(ROW-excess):
            if list(board[r:end, c]) == [piece for i in range(WINNER)]:
                return True
            end+=1

    for c in range(COLUMN-excess): #check for horizontal winner
        end = WINNER
        for r in range(ROW):
            if list(board[r,c:end]) == [piece for i in range(WINNER)]:
                return True
            end+=1
    
    for c in range(COLUMN-3): #check for positive diagonal winner
        for r in range(3, ROW):
            if board[r][c] == board[r-1][c+1] == board[r-2][c+2] == board[r-3][c+3] == piece:
                return True
    
    for c in range(COLUMN-3): #check for negative diagonal winner
        for r in range(ROW-3):
            if board[r][c] == board[r+1][c+1] == board[r+2][c+2] == board[r+3][c+3] == piece:
                return True

def getAboveRow(board, column): #return a row given an available column
	for r in range(ROW):
		if board[r][column] == EMPTY:
			return r

def isValidLocation(board, column): #check if the column is available
	return board[ROW-1][column] == EMPTY

def getValidColumns(board): #return a list of available columns
	valid = []
	for c in range(COLUMN):
		if isValidLocation(board, c):
			valid.append(c)
	return valid

def placePiece(board, row, column, piece): #update board
	board[row][column] = piece