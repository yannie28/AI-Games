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
PINK = (199,21,133) #circles
RED = (255,0,0) #text
HUMAN_PIECE = (255,255,255) #black
AI_PIECE = (0,0,0) #white
size = (COLUMN * BOARDSIZE, (ROW+1) * BOARDSIZE) #width, height
screen = pyg.display.set_mode(size)

WINNER = 4 #winner connects 4 dots
excess = COLUMN - WINNER #no of sub lists to be checked

def drawBoard(board): #draw the gui board
    pyg.draw.rect(screen, PINK, (0,0, COLUMN * BOARDSIZE, BOARDSIZE))

    for c in range(COLUMN):
        for r in range(ROW):
            pyg.draw.rect(screen, BLUE, (c*BOARDSIZE, BOARDSIZE*(r+1), BOARDSIZE, BOARDSIZE))
            pyg.draw.circle(screen, PINK, (int(BOARDSIZE*(c+1/2)), int(BOARDSIZE*(r+1/2+1))), RADIUS)

    pyg.display.update()

def drawMove(board, row, column, piece): #update the board by changing the color of the circle depending on the value of the board
    if board[row][column] == HUMAN_VAL:
        pyg.draw.circle(screen, HUMAN_PIECE, (int(BOARDSIZE*(column+1/2)), (ROW+1) * BOARDSIZE-int(BOARDSIZE*(row+1/2))), RADIUS)
    elif board[row][column] == AI_VAL:
        pyg.draw.circle(screen, AI_PIECE, (int(BOARDSIZE*(column+1/2)), (ROW+1) * BOARDSIZE-int(BOARDSIZE*(row+1/2))), RADIUS)

    pyg.display.update()

def isVictory(board, piece): #check if the player is already a winner
    for c in range(COLUMN): #check for vertical winner
        end = WINNER
        for r in range(ROW-excess):
            if list(board[r:end, c]) == [piece for i in range(WINNER)]:
                return True
            end+=1

    end = WINNER
    for c in range(COLUMN-excess): #check for horizontal winner
        for r in range(ROW):
            if list(board[r,c:end]) == [piece for i in range(WINNER)]:
                return True
        end+=1

    for c in range(COLUMN-3): #check for positive diagonal winner
        for r in range(ROW-3):
            if board[r][c] == board[r+1][c+1] == board[r+2][c+2] == board[r+3][c+3] == piece:
                return True
    
    for c in range(COLUMN-3): #check for negative diagonal winner
        for r in range(3, ROW):
            if board[r][c] == board[r-1][c+1] == board[r-2][c+2] == board[r-3][c+3] == piece:
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

def getHumanMove(board): #get human move
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            sys.exit(0)
        elif event.type == pyg.MOUSEMOTION:
            pyg.draw.rect(screen, PINK, (0,0, COLUMN * BOARDSIZE, BOARDSIZE))
            pyg.draw.circle(screen, HUMAN_PIECE, (event.pos[0], int(BOARDSIZE/2)), RADIUS)

        pyg.display.update()

        if event.type == pyg.MOUSEBUTTONDOWN:
            pyg.draw.rect(screen, PINK, (0,0, COLUMN * BOARDSIZE, BOARDSIZE))
            col = int(math.floor(event.pos[0]/BOARDSIZE))
            if isValidLocation(board, col):
                row = getAboveRow(board, col)
                placePiece(board, row, col, HUMAN_VAL)
                drawMove(board, row, col, HUMAN_VAL)

                return True

def getAIMove(board): #get ai move
    col = minimax(board, 5, -math.inf, math.inf, True)[0]

    row = getAboveRow(board, col)
    placePiece(board, row, col, AI_VAL)
    drawMove(board, row, col, AI_VAL)

def evaluate_window(window, piece):
	score = 0
	opp_piece = HUMAN_VAL
	if piece == HUMAN_VAL:
		opp_piece = AI_VAL

	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 2

	if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
		score -= 4

	return score

def score_position(board, piece):
	score = 0

	## Score center column
	center_array = [int(i) for i in list(board[:, COLUMN//2])]
	center_count = center_array.count(piece)
	score += center_count * 3

	## Score Horizontal
	for r in range(ROW):
		row_array = [int(i) for i in list(board[r,:])]
		for c in range(COLUMN-3):
			window = row_array[c:c+WINNER]
			score += evaluate_window(window, piece)

	## Score Vertical
	for c in range(COLUMN):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(ROW-3):
			window = col_array[r:r+WINNER]
			score += evaluate_window(window, piece)

	## Score positive sloped diagonal
	for r in range(ROW-3):
		for c in range(COLUMN-3):
			window = [board[r+i][c+i] for i in range(WINNER)]
			score += evaluate_window(window, piece)

	for r in range(ROW-3):
		for c in range(COLUMN-3):
			window = [board[r+3-i][c+i] for i in range(WINNER)]
			score += evaluate_window(window, piece)

	return score

def is_terminal_node(board):
	return isVictory(board, HUMAN_VAL) or isVictory(board, AI_VAL) or len(getValidColumns(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):
	valid_locations = getValidColumns(board)
	is_terminal = is_terminal_node(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if isVictory(board, AI_VAL):
				return (None, 100000000000000)
			elif isVictory(board, HUMAN_VAL):
				return (None, -10000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # Depth is zero
			return (None, score_position(board, AI_VAL))

	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = getAboveRow(board, col)
			b_copy = board.copy()
			placePiece(b_copy, row, col, AI_VAL)
			new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else: # Minimizing player
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = getAboveRow(board, col)
			b_copy = board.copy()
			placePiece(b_copy, row, col, HUMAN_VAL)
			new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
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

    fontStyle = pyg.font.SysFont("arial", BOARDSIZE-40)
    victory = False
    player = HUMAN

    while not victory:
        if player == HUMAN:
            getHumanMove(board)
            if isVictory(board, HUMAN_VAL):
                text = fontStyle.render('Finally! You win!', True, RED)
                text_rect = text.get_rect(center=((COLUMN * BOARDSIZE)/2, BOARDSIZE/2))
                screen.blit(text, text_rect)
                victory = True
            pyg.display.update()
            player = AI

        elif player == AI and getHumanMove(board):				
            getAIMove(board)
            if isVictory(board, AI_VAL):
                text = fontStyle.render('Computer wins!', True, RED)
                text_rect = text.get_rect(center=((COLUMN * BOARDSIZE)/2, BOARDSIZE/2))
                screen.blit(text, text_rect)
                victory = True
            pyg.display.update()
            player = HUMAN

        if victory:
            pyg.time.wait(5000)

main()
