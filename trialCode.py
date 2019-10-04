boards = {'1': (0,0), '2': (0,1), '3': (0,2),
          '4': (1,0), '5': (1,1), '6': (1,2),
          '7': (2,0), '8': (2,1), '9': (2,2)}
board = [['O','2','3'], ['4','5','6'], ['7','O','X']]
avail = {'2': (0,1), '3': (0,2),
          '4': (1,0), '5': (1,1), '6': (1,2),
          '7': (2,0),}
COM_VALUE = 'X'
HUMAN_VALUE = 'O'
COMPUTER = 1
HUMAN = 0

def VictoryFor(board, player):
    sign = COM_VALUE if player == COMPUTER else HUMAN
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

# def evalFunctions(board, player, depth):
#     print(player)
#     if VictoryFor(board, player):
#         return 1000 - depth
#     elif VictoryFor(board, not player):
#         return depth - 1000
#     else:
#         return 0

def minimax(board, avail, player):
    
    if VictoryFor(board, player):
        return -10
    elif VictoryFor(board, not player):
        return 20
    elif not avail:
        return 0

    sign = COM_VALUE if player == COMPUTER else HUMAN
    moves = {}
    for n in avail:
        newboard = board[:] #board = [['1','2','3'], ['4','5','6'], ['7','8','9']]
        newavail = avail.copy()
        newboard[boards[n][0]][boards[n][1]] = sign
        print(newavail)
        del newavail[n] #delete the picked move in the newavail dictionary
        
        if player == COMPUTER:
            result = minimax(newboard, newavail, HUMAN)
            moves.update({result: n})
        else:
            result = minimax(newboard, newavail, COMPUTER)
            moves.update({result: n})

    bestMove = ''
    if player == COMPUTER:
        bestScore =  float('-inf')
        for i in moves:
            if int(i) > bestScore:
                bestScore = int(i)
                bestMove = moves[i]
    else:
        bestScore = float('inf')
        for i in moves:
            if int(i) < bestScore:
                bestScore = int(i)
                bestMove = moves[i]
    
    return bestMove

print(minimax(board, avail, COMPUTER))

# def generateTree(board, avail, depth, player):
#     maxValue = float('-inf')
#     minValue = float('inf')

#     sign = COMPUTER if player == 1 else HUMAN
#     move = ''

#     if VictoryFor(board, player): return 1000
#     if VictoryFor(board, not player): return -1000

#     if not avail:
#         return evalFunctions(board, player, depth)

#     for n in avail:
#         #generate possible move
#         newboard = board[:] #board = [['1','2','3'], ['4','5','6'], ['7','8','9']]
#         newavail = avail.copy()
#         newboard[boards[n][0]][boards[n][1]] = sign
#         del newavail[n] #delete the picked move in the newavail dictionary
#         value = generateTree(newboard,newavail, depth+1, not player)

#         if value > maxValue and player == 1:
#             maxValue = value
#             move = n
#         else:
#             minValue = value

#     if depth == 0:
#         print(maxValue)
#         return move


#     if player == 1:
#         return maxValue
#     else:
#         return minValue
    
# print("Optimal move", generateTree(board,avail,0,1))
# def minimax(board, avail, depth, player):
#     if not depth == 3:
#         return board

#     sign = COMPUTER if player == 1 else HUMAN
#     for x in avail:
#         #generate possible move
#         newboard = board[:] #board = [['1','2','3'], ['4','5','6'], ['7','8','9']]
#         newavail = avail.copy()
#         newboard[boards[x][0]][boards[x][1]] = sign
#         del newavail[x] #delete the picked move in the newavail dictionary

#         print(minimax(newboard, newavail, depth-1, not player), depth)

# minimax(board,avail,5,1)