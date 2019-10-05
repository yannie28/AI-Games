#Arianne Tan
from random import randrange, choice

boards = {'1': (0,0), '2': (0,1), '3': (0,2),
          '4': (1,0), '5': (1,1), '6': (1,2),
          '7': (2,0), '8': (2,1), '9': (2,2)}

board = [['1','2','3'], ['4','5','6'], ['7','8','9']]
avail = boards.copy()
COMPUTER = 'X'
HUMAN = 'O'

def DisplayBoard(board):
#
# the function accepts one parameter containing the board's current status
# and prints it out to the console
#
    for i in range(3):
        print(("+" + "-"*7)*3 + "+\n" + ("|" + " "*7)*3 + "|")
        print(("|   " + board[i][0] + "   ") + ("|   " + board[i][1] + "   ") + ("|   " + board[i][2] + "   ") + "|")
        print(("|" + " "*7)*3 + "|")
    print(("+" + "-"*7)*3 + "+")

def EnterMove(board):
#
# the function accepts the board current status, asks the user about their move, 
# checks the input and updates the board according to the user's decision
#
    while True:
        try:
            move = int(input("Enter your move: "))
            if move < 10 and move > 0: #move = 1
                if str(move) in avail:
                    #change move to 'O'; update board
                    board[boards[str(move)][0]][boards[str(move)][1]] = HUMAN
                    break
                else:
                    print("Position already taken. Please pick another number")
        except:
            print("Invalid move")

    del avail[str(move)]

def VictoryFor(board, player):
#
# the function analyzes the board status in order to check if 
# the player using 'O's or 'X's has won the game
#   
    sign = COMPUTER if player == 1 else HUMAN
    victory = False
    diagonal1 = 0
    diagonal2 = 0
    for i in range(3):
        horizontal = vertical = 0
        for j in range(3):
            if board[i][j] == sign:
                horizontal += 1
            if board[j][i] == sign:
                vertical += 1
            if i == j and board[i][j] == sign:
                diagonal1 += 1
            if board[0][2] == board[2][0] == board[1][1] == sign:
                diagonal2 = 3
 
        if horizontal == 3 or vertical == 3 or diagonal1 == 3 or diagonal2 == 3:
            victory = True
            break

    return victory

def isFullBoard(board):
    return False if avail else True

# def DrawMove(board):
# #
# # the function draws the computer's move and updates the board
# #   
#     while True:
#         move = str(randrange(1,10)) #picks a random number
#         #move = miniMax(board, avail, 3, 1) #current state of the board, initial depth, value of the computer
#         if move in avail:
#             #change move to 'X'; update board
#             board[boards[move][0]][boards[move][1]] = COMPUTER
#             break
#     del avail[move]
#     print("Computer placed an X in position " + move)

def DrawMove(board):
#
# simple ai implementation for tic tac toe game
#
    middle = ''
    corners = []
    others = []
    move = ''
    for x in avail:
        for player in [1, 0]:
            sign = COMPUTER if player == 1 else HUMAN
            newBoard = board[:]
            newBoard[boards[x][0]][boards[x][1]] = sign
            if VictoryFor(newBoard, player):
                board[boards[x][0]][boards[x][1]] = COMPUTER
                del avail[x]
                print("Computer placed an X in position " + x)
                return

        newBoard[boards[x][0]][boards[x][1]] = x

        if x == '5':
            middle = x
        elif x in ['1', '3', '7', '9']:
            corners.append(x)
        else:
            others.append(x)
    
    if middle:
        move = middle
    elif corners:
        move = choice(corners)
    else:
        move = choice(others)

    board[boards[move][0]][boards[move][1]] = COMPUTER
    del avail[move]
    print("Computer placed an X in position " + move)

# def evalFunction(board, depth):
#     if VictoryFor(board, 0):
#         return depth+ 50
#     elif VictoryFor(board, 1):
#         return 100 + depth
#     else:
#         return 0

# def miniMax(board, avail, depth, player):
#     sign = COMPUTER if player == 1 else HUMAN
#     maxValue = float('-inf')
#     minValue = float('inf')
#     index = ''

#     if VictoryFor(board, 0):
#         return -depth - 10
#     elif VictoryFor(board, 1):
#         return 10 + depth

#     if depth == 0 or not avail:
#         return evalFunction(board, depth)

#     for x in avail:
#         #generate possible move
#         newboard = board[:] #board = [['1','2','3'], ['4','5','6'], ['7','8','9']]
#         print(newboard)
#         newavail = avail.copy()
#         print(newavail)
#         newboard[boards[x][0]][boards[x][1]] = sign
#         del newavail[x] #delete the picked move in the newavail dictionary
#         print(newavail)
#         value = miniMax(newboard, newavail, depth-1, not player)

#         if value > maxValue and player == 1:
#             maxValue = value
#             index = x
#         else:
#             minValue = value

#     if depth == 5:
#         return index

#     if player == 1:
#         return maxValue
#     else:
#         return minValue

def main():
    player = 0 #0 for human; 1 for computer
    victory = False
    DisplayBoard(board)
    while not victory and not isFullBoard(board):
        if player == 0:
            EnterMove(board)
        elif player == 1:
            DrawMove(board)
        victory = VictoryFor(board, player)
        DisplayBoard(board)
        player = not player

    if victory and player == 0: #opposite since in the while cascade the player was changed before terminating the loop
        print("The computer wins!")
    elif victory and player == 1:
        print("You win!")
    else:
        print("It's a draw")

main()
