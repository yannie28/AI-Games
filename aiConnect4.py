import sys
import math
import random
import pygame
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

def createBoard(board):
	for c in range(COLUMN):
		for r in range(ROW):
			pygame.draw.rect(screen, BLUE, (c*BOARDSIZE, BOARDSIZE*(r+1), BOARDSIZE, BOARDSIZE))
			pygame.draw.circle(screen, PINK, (int(BOARDSIZE*(c+1/2)), int(BOARDSIZE*(r+1/2))), RADIUS)

	pygame.display.update()

def drawMove(board):
    for c in range(COLUMN):
        for r in range(ROW):		
            if board[r][c] == HUMAN_VAL:
                pygame.draw.circle(screen, BLACK, (int(BOARDSIZE*(c+1/2)), height-int(BOARDSIZE*(r+1/2))), RADIUS)
            elif board[r][c] == AI_VAL: 
                pygame.draw.circle(screen, WHITE, (int(BOARDSIZE*(c+1/2)), height-int(BOARDSIZE*(r+1/2))), RADIUS)

    pygame.display.update()

def isVictory(board, piece):

    #check for vertical winner
    for c in range(COLUMN):
        end = WINNER
        for r in range(ROW-excess):
            if list(board[r:end, c]) == [piece for i in range(WINNER)]:
                return True
            end+=1

    #check for horizontal winner
    for c in range(COLUMN-excess):
        end = WINNER
        for r in range(ROW):
            if list(board[r,c:end]) == [piece for i in range(WINNER)]:
                return True
            end+=1
    
    #check for positive diagonal winner
    for c in range(COLUMN-3):
        for r in range(3, ROW):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True
    
    #check for negative diagonal winner
    for c in range(COLUMN-3):
        for r in range(ROW-3):
            if board[r][c] == board[r+1][c+1] == board[r+2][c+2] == board[r+3][c+3] == piece:
                return True

def getAboveRow(board, column):
	for r in range(ROW):
		if board[r][column] == EMPTY:
			return r

def isValidLocation(board, column):
	return board[ROW-1][column] == EMPTY

def getValidLocation(board):
	valid = []
	for c in range(COLUMN):
		if isValidLocation(board, c):
			valid.append(c)
	return valid

def movePiece(board, row, column, piece):
	board[row][column] = piece