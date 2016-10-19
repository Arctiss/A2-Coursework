import random, math, pygame, time, sys

class node():
    def __init__(self, size, board, unhappy, blanks, bias, ratio, groups):

        self.size = size
        #self.coordinates = coordinates
        self.population = 0
        self.board = board
        self.unhappy = unhappy
        self.blanks = blanks
        self.squares = size**2
        self.bias = bias
        self.ratio = ratio
        self.groups = groups
        #self.diversity = 0

    

class agent():
    def __init__(self, coordinates, node, aType):

        self.coordinates = coordinates
        self.currentNode = node
        self.speed = 5
        self.targetNode = None
        self.unhappyMoves = 0
        self.threshold = 3
        self.route = []
        self.segregation = 0
        self.type = aType

    def getDir(self, currentNode, targetNode):
        pass

    def checkMove(self):
        pass

    def getMove(self, nodes):
        pass

    def updateMove(self, nodes):
        pass

    def getSegregation(self, board):
        pass

    

def getSize():
    size = 0
    while True:
        try:
            size = int(input("How big would you like the board to be? "))
            if size <= 0 or size >= 101:
                print("Numbers between 1 and 100 only")
            else:
                return size
        except:
            print("Numbers only")

def getBoundaries():
    bias = 0
    while True:
        try:
            bias = int(input("What percentage similar to be happy? "))
            if bias < 0 or bias > 100:
                print("Numbers between 0 and 100 only")
            else:
                return bias
        except:
            print("Numbers only") 



def getGroups():
    groups = 0
    while True:
        try:
            groups = int(input("How many groups? "))
            if groups < 2 or groups > 5:
                print("Numbers between 2 and 5 only")
            else:
                return groups
        except:
            print("Numbers only")


def getRatio(groups, size):
    ratio = []
    total = 0
    temp = 0

    for i in range (0, groups):
        while True:
            temp = int(input("How many in group " + str(i+1) + ": "))
            total += temp

            if size**2 - total < groups - i:
                print("Not enough space for the other groups")
                total -= temp

            else:
                for j in range(0, temp):
                    ratio.append(i)
                break

                total += ratio[-1]

    for i in range(0, size**2-total):
        ratio.append("B")


    return ratio


def populateBoard(size, ratio, agents):
    board = []
    blanks = []
    ratio2 = ratio.copy()
    for i in range (0, size):
        new = []
        for j in range (0, size):
            bob = random.choice(ratio2)
            if bob == "B":
                blanks.append((i, j))
            ratio2.remove(bob)
            new.append(bob)
            if bob != "B":
                a = agent([i,j], None, bob)
                agents.append(a)

        board.append(new)
    return board, blanks




def drawBoard(board, colours, screen, k, boardSize, size):
    screen.fill(pygame.Color(20,20,20))

    for y, x in enumerate(board):
        for y2, x2 in enumerate(x):
            if x2 != "B":
                #pygame.draw.rect(screen,colours[x2],(int(y2*k), int(y*k), int(k)-1, int(k)-1))

                pygame.draw.circle(screen,colours[x2],(int(y2*k)+int(k/2), int(y*k)+int(k/2)), int(k/2)-1)


def getUnhappy(board, size, bias, ratio):
    unhappy = []
    for y, x in enumerate(board):
        for y2, x2 in enumerate(x):
            current = board[y][y2]

            if current != "B":
                if checkHappy(size, board, current, bias, y, y2, ratio):
                    pass
                else:
                    unhappy.append((y, y2))
            else:
                pass

    return unhappy


def selectAgent(unhappy):
    i = random.randint(0, len(unhappy)-1)
    return unhappy[i][0], unhappy[i][1]


def checkHappy(size, board, current, bias, i, j, ratio):
    similar = 0
    adjacent = 8
    for x in (-1, 0, 1):
        for y in (-1, 0, 1):
            if (x == 0 and y == 0):
                pass
            else:
                if (i+x) < 0 or (i+x) > size-1 or (j+y) > size-1 or (j+y) < 0 or board[i+x][j+y] == ratio[-1]:
                    adjacent -= 1
                else:
                    if board[i+x][j+y] == current:
                        similar += 1

    if adjacent != 0:
        percentage = (similar/adjacent)*100
        if percentage < bias:
            return False
        else:
            return True
    else:
        return False


def updateUnhappy(board, size, bias, ratio, i, j, unhappy):
    similar = 0
    adjacent = 8
    for x in (-1, 0, 1):
        for y in (-1, 0, 1):
            if (x == 0 and y == 0):
                pass
            else:
                try:
                    current = board[i+x][j+y]
                    if checkHappy(size, board, current, bias, i, j, ratio):
                        pass
                    else:
                        if (i+x, j+y) not in unhappy:
                            unhappy.append((i+x, j+y))
                except:
                    pass
    return unhappy

def moveCell(blanks, board, i, j, size, bias, ratio, agents):
    for z in agents:
        if z.coordinates == [i, j]:
            if checkHappy(size, board, z.type, bias, i, j, ratio):
                z.unhappyMoves == 0
            else:
                z.unhappyMoves += 1
            
    
    moveto = random.choice(blanks)
    blanks.remove(moveto)
    blanks.append((i, j))

    temp = board[i][j]
    board[i][j] = "B"
    board[moveto[0]][moveto[1]] = temp
    return board, blanks, moveto[0], moveto[1]

def switchNode(nodes, activeNode):
    for i in range(0, len(nodes)):
        if activeNode == nodes[i]:
                try:
                        activeNode = nodes[i+1]
                except:
                        activeNode = nodes[0]
                
                return activeNode

def main():

    agents = []
    nodes = []
    colours = {0: (252, 183, 50), 1: (2, 120, 120), 2: (243, 115, 56), 3:(194, 35, 38), 4: (128, 22, 56)}
    boardSize = 800

    for z in range(0, random.randint(2, 4)):
        size = getSize()
        bias = getBoundaries()
        groups = getGroups()
        ratio = getRatio(groups, size)

        board, blanks = populateBoard(size, ratio, agents)

        unhappy = getUnhappy(board, size, bias, ratio)

        n = node(size, board, unhappy, blanks, bias, ratio, groups)
        nodes.append(n)
        

    activeNode = nodes[0]

    screen = pygame.display.set_mode((boardSize,boardSize))
    
    k = (boardSize/activeNode.size)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    activeNode = switchNode(nodes, activeNode)
                    k = (boardSize/activeNode.size)


        if len(activeNode.unhappy) != 0:
            i, j = selectAgent(activeNode.unhappy) #SELECTS THE COORDINATES NOT THE ACTUAL THING
            
            activeNode.board, activeNode.blanks, movetox, movetoy = moveCell(activeNode.blanks, activeNode.board, i, j, activeNode.size, activeNode.bias, activeNode.ratio, agents)
            
            activeNode.unhappy = updateUnhappy(activeNode.board, activeNode.size, activeNode.bias, activeNode.ratio, i, j, activeNode.unhappy)
            
            activeNode.unhappy.remove((i, j))

            activeNode.unhappy = updateUnhappy(activeNode.board, activeNode.size, activeNode.bias, activeNode.ratio, movetox, movetoy, activeNode.unhappy)
            
            drawBoard(activeNode.board, colours, screen, k, boardSize, activeNode.size)
            
            pygame.display.update()
            #time.sleep(0.05)
        else:
            print("All happy")
            pygame.image.save(screen, "screenshot.jpeg")
            pygame.event.wait()
            exit()





main()

