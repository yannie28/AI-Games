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