#Arianne Tan
from random import randrange

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
        move = int(input("Enter your move: "))
        if move < 10 and move > 0: #move = 1
            if str(move) in avail:
                #change move to 'O'; update board
                board[boards[str(move)][0]][boards[str(move)][1]] = 'O'
                break
            else:
                print("Position already taken. Please pick another number")
        else:
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

def DrawMove(board):
#
# the function draws the computer's move and updates the board
#   
    while True:
        #move = str(randrange(1,10)) #picks a random number
        move = miniMax()
        if move in avail:
            #change move to 'X'; update board
            board[boards[move][0]][boards[move][1]] = 'X'
            break
    del avail[move]
    print("Computer placed an X in position " + move)

def miniMax():
    move = ''
    return move

def main():
    player = 0
    victory = False
    DisplayBoard(board)
    while not victory and avail:
        if player == 0:
            EnterMove(board)
            victory = VictoryFor(board, player)
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
