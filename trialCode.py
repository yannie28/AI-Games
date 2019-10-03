# boards = {'1': (0,0), '2': (0,1), '3': (0,2),
#           '4': (1,0), '5': (1,1), '6': (1,2),
#           '7': (2,0), '8': (2,1), '9': (2,2)}
# board = [['X','O','X'], ['O','5','6'], ['O','X','O']]
# avail = {'4': (1,0), '5': (1,1), '6': (1,2)}
# COMPUTER = 'X'
# HUMAN = 'O'

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

graph1 = {
    'A' : ['B','C'],
    'B' : ['D','E'],
    'C' : ['F','G'],
    'D' : ['H', 'I', 'J'],
    'E' : ['K'],
    'F' : ['L', 'M'],
    'G' : ['N'],
    'H' : [],
    'I' : [],
    'J' : [],
    'K' : [],
    'L' : [],
    'M' : [],
    'N' : [],
}
# MAX = True
# MIN = False #not MAX
COMPUTER = 'X' #1-max
HUMAN = 'O' #0


def evalFunction(node):
    if node == 'H':
        return 70
    elif node == 'I':
        return 120
    elif node == 'J':
        return 130
    elif node == 'K':
        return 80
    elif node == 'L':
        return 100
    else:
        return 180

def dfs(graph, node, player):
    max = float('-inf')
    min = float('inf')
    index = ''
    if not graph1[node]:
        return evalFunction(node)

    for n in graph[node]:
        value = dfs(graph,n, not player)
    
        if value > max and player == 1:
            max = value
            index = n
        else:
            min = value
    
    if node == 'A':
        return index

    if player == 1:
        return max
    else:
        return min

print('optimal move =', dfs(graph1,'A', 1))