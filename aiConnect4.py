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
BACKGROUND = (0,191,255) #light blue
CIRCLE = (199,21,133) #pink
OUTLINECIRCLE = (255,255,0) #yellow
TEXTAREA = (128,0,128) 
TEXT = (0,0,0) #violet
HUMAN_PIECE_COLOR = (255,255,255) #white
AI_PIECE_COLOR = (0,0,0) #black
size = (COLUMN * BOARDSIZE, (ROW+1) * BOARDSIZE) #width, height
screen = pyg.display.set_mode(size)

WINNER = 4 #winner connects 4 dots
excess = COLUMN - WINNER #no of sub lists to be checked

def drawBoard(board): #draw the gui board
    pyg.draw.rect(screen, TEXTAREA, (0,0, COLUMN * BOARDSIZE, BOARDSIZE))

    for c in range(COLUMN):
        for r in range(ROW):
            pyg.draw.rect(screen, BACKGROUND, (c*BOARDSIZE, BOARDSIZE*(r+1), BOARDSIZE, BOARDSIZE))
            pyg.draw.circle(screen, CIRCLE, (int(BOARDSIZE*(c+1/2)), int(BOARDSIZE*(r+1/2+1))), RADIUS)

    pyg.display.update()

def drawMove(board, row, column, piece): #update the board by changing the color of the circle depending on the value of the board
    if board[row][column] == HUMAN_VAL:
        pyg.draw.circle(screen, HUMAN_PIECE_COLOR, (int(BOARDSIZE*(column+1/2)), (ROW+1)*BOARDSIZE - int(BOARDSIZE*(row+1/2))), RADIUS)
    elif board[row][column] == AI_VAL:
        pyg.draw.circle(screen, AI_PIECE_COLOR, (int(BOARDSIZE*(column+1/2)), (ROW+1)*BOARDSIZE - int(BOARDSIZE*(row+1/2))), RADIUS)

    pyg.display.update()

def getWinningMove(winningMove):
    i = 0
    while i < 4:
        pyg.time.wait(300)
        pyg.draw.circle(screen, OUTLINECIRCLE, (int(BOARDSIZE*(winningMove[i][1]+1/2)), (ROW+1)*BOARDSIZE - int(BOARDSIZE*(winningMove[i][0]+1/2))), RADIUS, 8)
        pyg.display.update()
        i += 1
        
def isVictory(board, piece): #check if the player is already a winner
    for c in range(COLUMN): #check for vertical winner
        for r in range(ROW-excess):
            if board[r][c] == board[r+1][c] == board[r+2][c] == board[r+3][c] == piece:
                return [(r,c),(r+1,c),(r+2,c),(r+3,c)]

    for c in range(COLUMN-excess): #check for horizontal winner
        for r in range(ROW):
            if board[r][c] == board[r][c+1] == board[r][c+2] == board[r][c+3] == piece:
                return [(r,c),(r,c+1),(r,c+2),(r,c+3)]

    for c in range(COLUMN-excess): #check for positive diagonal winner
        for r in range(ROW-excess):
            if board[r][c] == board[r+1][c+1] == board[r+2][c+2] == board[r+3][c+3] == piece:
                return [(r,c),(r+1,c+1),(r+2,c+2),(r+3,c+3)]
    
    for c in range(COLUMN-excess): #check for negative diagonal winner
        for r in range(excess, ROW):
            if board[r][c] == board[r-1][c+1] == board[r-2][c+2] == board[r-3][c+3] == piece:
                return [(r,c),(r-1,c+1),(r-2,c+2),(r-3,c+3)]

def getWinningMessage(message):
    fontStyle = pyg.font.SysFont("arial", BOARDSIZE-40)
    text = fontStyle.render(message, True, TEXT)
    text_rect = text.get_rect(center=((COLUMN * BOARDSIZE)/2, BOARDSIZE/2))
    screen.blit(text, text_rect)

    pyg.display.update()

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

def getHumanMove(board, move): #get human move
	col = int(math.floor(move/BOARDSIZE))

	if isValidLocation(board, col):
		row = getAboveRow(board, col)
		placePiece(board, row, col, HUMAN_VAL)
		drawMove(board, row, col, HUMAN_VAL)

def getAIMove(board): #get ai move
	col = alphabetaPruning(board, 5, float('-inf'), float('inf'), True)[0]

	if isValidLocation(board,col):
		row = getAboveRow(board, col)
		placePiece(board, row, col, AI_VAL)
		drawMove(board, row, col, AI_VAL)

def countScore(subPart, piece):
	score = 0
	oppPiece = HUMAN_VAL
	if piece == HUMAN_VAL:
		oppPiece = AI_VAL

	if subPart.count(piece) == 4:
		score += 4
	elif subPart.count(piece) == 3 and subPart.count(EMPTY) == 1:
		score += 3
	elif subPart.count(piece) == 2 and subPart.count(EMPTY) == 2:
		score += 2
	else:
		score += 1

	if subPart.count(oppPiece) == 3 and subPart.count(EMPTY) == 1:
		score -= 3

	return score

def score_position(board, piece):
	score = 0

	center_array = [int(i) for i in list(board[:, COLUMN//2])] #center column
	center_count = center_array.count(piece)
	score += center_count * 3

	for r in range(ROW): #horizontal
		row_array = [int(i) for i in list(board[r,:])] 
		for c in range(COLUMN-3):
			window = row_array[c:c+WINNER]
			score += countScore(window, piece)

	for c in range(COLUMN): #vertical
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(ROW-3):
			window = col_array[r:r+WINNER]
			score += countScore(window, piece)

	for r in range(ROW-3): #positive diagonal
		for c in range(COLUMN-3):
			window = [board[r+i][c+i] for i in range(WINNER)]
			score += countScore(window, piece)

	for r in range(ROW-3): #negative diagonal
		for c in range(COLUMN-3):
			window = [board[r+3-i][c+i] for i in range(WINNER)]
			score += countScore(window, piece)

	return score

def alphabetaPruning(board, depth, alpha, beta, maximizingPlayer):
	valid_locations = getValidColumns(board)

	if isVictory(board, AI_VAL):
		return (None, 100)
	elif isVictory(board, HUMAN_VAL):
		return (None, -100)
	elif depth == 0:
		return (None, score_position(board, AI_VAL))
	elif len(getValidColumns(board)) == 0:
		return (None, 0)

	if maximizingPlayer:
		value = float('-inf')
		column = ''
		for col in valid_locations:
			row = getAboveRow(board, col)
			newBoard = board.copy()
			placePiece(newBoard, row, col, AI_VAL)
			new_score = alphabetaPruning(newBoard, depth-1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else: # Minimizing player
		value = float('inf')
		column = ''
		for col in valid_locations:
			row = getAboveRow(board, col)
			newBoard = board.copy()
			placePiece(newBoard, row, col, HUMAN_VAL)
			new_score = alphabetaPruning(newBoard, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value

def main():
	board = np.zeros((ROW,COLUMN))
	pyg.init()

	drawBoard(board)
	pyg.display.update()

	victory = False
	player = HUMAN
	i = 0
	while not victory:
		for event in pyg.event.get():
			if event.type == pyg.QUIT:
				sys.exit(0)
			elif event.type == pyg.MOUSEMOTION:
				pyg.draw.rect(screen, TEXTAREA, (0,0, COLUMN * BOARDSIZE, BOARDSIZE))
				pyg.draw.circle(screen, HUMAN_PIECE_COLOR, (event.pos[0], int(BOARDSIZE/2)), RADIUS)

			pyg.display.update()

			if event.type == pyg.MOUSEBUTTONDOWN:
				pyg.draw.rect(screen, TEXTAREA, (0,0, COLUMN * BOARDSIZE, BOARDSIZE))

				if player == HUMAN:
					getHumanMove(board, event.pos[0])
					result = isVictory(board, HUMAN_VAL)
					if result:
						message = 'Finally! You win!'
						victory = True
					player = AI

		if player == AI and not victory:				
			getAIMove(board)
			result = isVictory(board, AI_VAL)
			if result:
				message = 'Computer Wins!'
				victory = True
			player = HUMAN

		if victory:
			getWinningMessage(message)
			getWinningMove(result)
			pyg.time.wait(5000)

main()
