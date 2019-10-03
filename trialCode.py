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
    'D' : [],
    'E' : [],
    'F' : [],
    'G' : [],
}

def evalFunction(node):
    if node == 'D':
        return 10
    elif node == 'E':
        return 20
    elif node == 'F':
        return 30
    else:
        return 40

def dfs(graph, node, visited):
    max = float('-inf')
    if not graph1[node]:
        return evalFunction(node)

    visited.append(node)
    for n in graph[node]:
        value = dfs(graph,n, visited)
    
    if value > max:
        max = value
        
    print(node, max)
    return max

print(dfs(graph1,'A', []))