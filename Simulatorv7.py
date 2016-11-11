import random, math, pygame, time, sys, pgu

class node():   
    def __init__(self, size, board, unhappy, blanks, bias, ratio, groups, agents, diversity, coordinates, boardSize, radius):

        self.size = size
        self.boardSize = boardSize
        self.xPos = coordinates[0] + self.boardSize
        self.yPos = coordinates[1]
        self.population = 0
        self.board = board
        self.unhappy = unhappy
        self.blanks = blanks
        self.squares = size**2
        self.bias = bias
        self.ratio = ratio
        self.groups = groups
        self.diversity = diversity
        self.happy = False
        self.agents = agents
        self.colour = (255, 255, 255)
        self.radius = radius
        
        self.rect = pygame.Rect((self.xPos-self.radius),(self.yPos-self.radius),(self.radius*2),(self.radius*2))

    def drawSelf(self, screen):
        pygame.draw.circle(screen, self.colour,(self.xPos, self.yPos), self.radius)

class button():
    def __init__(self, coordinates, width, height, colour, text):

        self.xPos = coordinates[0]
        self.yPos = coordinates[1]
        self.width = width
        self.height = height
        self.colour = colour
        self.rect = pygame.Rect(self.xPos, self.yPos, self.width, self.height)
        self.font = pygame.font.SysFont("monospace", 45)
        self.function = text
        self.text = self.font.render(self.function, 1, (0,0,0))
        self.textRect = self.text.get_rect(center=self.rect.center)

    def drawSelf(self, screen):
        pygame.draw.rect(screen, self.colour,(self.xPos, self.yPos, self.width, self.height))
        screen.blit(self.text, self.textRect)

    def onClick(self):
        if self.function == "Pause":
            paused = True
            self.function = "Play"
            self.text = self.font.render(self.function, 1, (0,0,0))
            self.textRect = self.text.get_rect(center=self.rect.center)
            
        elif self.function == "Play":
            paused = False
            self.function = "Pause"
            self.text = self.font.render(self.function, 1, (0,0,0))
            self.textRect = self.text.get_rect(center=self.rect.center)
        return paused

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

def getBias():
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

def getDiversity():
    diversity = 0
    while True:
        try:
            diversity = int(input("What percentage different to be happy? "))
            if diversity < 0 or diversity > 100:
                print("Numbers between 0 and 100 only")
            else:
                return diversity
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
    return board, blanks, agents

def drawBoard(board, colours, screen, k, boardSize, size):
    screen.fill(pygame.Color(20,20,20))

    for y, x in enumerate(board):
        for y2, x2 in enumerate(x):
            if x2 != "B":
                #pygame.draw.rect(screen,colours[x2],(int(y2*k), int(y*k), int(k)-1, int(k)-1))

                pygame.draw.circle(screen,colours[x2],(int(y2*k)+int(k/2), int(y*k)+int(k/2)), int(k/2)-1)

def getUnhappy(board, size, bias, ratio, diversity):
    unhappy = []
    for y, x in enumerate(board):
        for y2, x2 in enumerate(x):
            current = board[y][y2]

            if current != "B":
                if checkHappy(size, board, current, bias, y, y2, ratio, diversity):
                    pass
                else:
                    unhappy.append((y, y2))
            else:
                pass

    return unhappy

def selectAgent(unhappy):
    i = random.randint(0, len(unhappy)-1)
    return unhappy[i][0], unhappy[i][1]

def checkHappy(size, board, current, bias, i, j, ratio, diversity):
    similar = 0
    adjacent = 8
    for x in (-1, 0, 1):
        for y in (-1, 0, 1):
            if (x == 0 and y == 0):
                pass
            else:
                if (i+x) < 0 or (i+x) > size-1 or (j+y) > size-1 or (j+y) < 0 or board[i+x][j+y] == "B":
                    adjacent -= 1
                    
                else:
                
                    if board[i+x][j+y] == current:
                        similar += 1                        

    if adjacent > 0:
        percentage = (similar/adjacent)*100
        if percentage < bias or (100-percentage) < diversity:
            return False
        else:
            return True
    else:
        return False

def updateUnhappy(board, size, bias, ratio, i, j, unhappy, diversity):
    similar = 0
    adjacent = 8
    for x in (-1, 0, 1):
        for y in (-1, 0, 1):
            if  (i+x) <0 or (j+y) < 0:
                pass
            else:
                try:
                    current = board[i+x][j+y]
                    if current == "B":
                        pass
                    else:
                        if checkHappy(size, board, current, bias, i, j, ratio, diversity):
                            pass
                        else:
                            if (i+x, j+y) not in unhappy:
                                unhappy.append((i+x, j+y))
                except:
                    pass
    return unhappy

def moveCell(blanks, board, i, j, size, bias, ratio, agents, diversity):
    moveto = random.choice(blanks)
    
    for z in agents:
        if z.coordinates == [i, j]:
            if checkHappy(size, board, z.type, bias, moveto[0], moveto[1], ratio, diversity):
                z.unhappyMoves == 0
            else:
                z.unhappyMoves += 1
                
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

def drawUI(boardSize, width, height, screen, nodes, buttons, activeNode):
    pygame.draw.rect(screen, (32, 32, 32), (boardSize, 0, (width-boardSize), boardSize))

    pygame.draw.rect(screen, (0, 0, 0), (boardSize, 0, (width-boardSize), width-boardSize), 5)

    pygame.draw.rect(screen, (255, 255, 255), (0, boardSize, width, boardSize))

    font = pygame.font.SysFont("monospace", 30)
    texts = []
    text = font.render("Size: "+str(activeNode.size), 1, (0, 0 , 0))
    texts.append(text)
    text = font.render("Bias factor: "+str(activeNode.bias), 1, (0, 0, 0))
    texts.append(text)
    text = font.render("Diversity factor: "+str(activeNode.diversity), 1, (0, 0, 0))
    texts.append(text)

    for i in range(0, len(texts)):
        #pygame.rect(screen, (32, 32, 32),(boardSize+10, 50+i*50, 180, 70))
        #textRect = texts[i].get_rect(center=texts[i].get_rect.center)
        #screen.blit(texts[i], self.textRect)

    for i in nodes:
        i.drawSelf(screen)

    for b in buttons:
        b.drawSelf(screen)

def defineButtons(boardSize):
    buttons = []
    b = button((boardSize + 10, 620), 180, 70, (0,255,0), "Pause")
    buttons.append(b)
    return buttons

def main():
    pygame.init()
    
    nodes = []
    colours = {0: (252, 183, 50), 1: (2, 120, 120), 2: (243, 115, 56), 3:(194, 35, 38), 4: (128, 22, 56)}
    boardSize = 700

    radius = 20

    width = boardSize + 200
    height = boardSize + 100

    buttons = defineButtons(boardSize)

    totalNodes = random.randint(2, 5)
    print(totalNodes)

    for z in range(0, totalNodes):
        agents = []
    
        size = getSize()
        bias = getBias()
        diversity = getDiversity()
        groups = getGroups()
        ratio = getRatio(groups, size)

        board, blanks, agents = populateBoard(size, ratio, agents)

        unhappy = getUnhappy(board, size, bias, ratio, diversity)

        n = node(size, board, unhappy, blanks, bias, ratio, groups, agents, diversity, (random.randint(radius, 200-radius),random.randint(radius, 200-radius)), boardSize, radius)
        nodes.append(n)
        
    activeNode = nodes[0]
    activeNode.colour = (255, 0, 0)

    screen = pygame.display.set_mode((width,height))
    
    k = (boardSize/activeNode.size)

    allHappy = 0

    paused = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                for n in nodes:
                                
                    if n.rect.collidepoint(pos):
                        activeNode.colour = (255, 255, 255)
                        activeNode = n
                        n.colour = (255, 0, 0)
                        k = (boardSize/activeNode.size)

                for b in buttons:
                    if b.rect.collidepoint(pos):
                        paused = b.onClick()

        for z in nodes:
            if z == activeNode:
                drawBoard(z.board, colours, screen, k, boardSize, z.size)
                drawUI(boardSize, width, height, screen, nodes, buttons, activeNode)
                pygame.display.update()

            if paused == False:
                

                if len(z.unhappy) != 0: #If unhappy

                    z.happy = False
                    
                    i, j = selectAgent(z.unhappy) #SELECTS THE COORDINATES NOT THE ACTUAL THING
                    
                    z.board, z.blanks, movetox, movetoy = moveCell(z.blanks, z.board, i, j, z.size, z.bias, z.ratio, z.agents, z.diversity)
                    
                    z.unhappy = updateUnhappy(z.board, z.size, z.bias, z.ratio, i, j, z.unhappy, z.diversity)
                    
                    z.unhappy.remove((i, j))

                    z.unhappy = updateUnhappy(z.board, z.size, z.bias, z.ratio, movetox, movetoy, z.unhappy, z.diversity)

                
                    
                        
                else: #If happy
                    
                    allHappy = 0
                    
                    z.happy = True
                    
                    for y in nodes:
                        if y.happy== True:
                            allHappy += 1
                            if allHappy == totalNodes:
                                                
                                print("All happy")
                                pygame.image.save(screen, "screenshot.jpeg")
                                for event in pygame.event.get():
                                    if event.type == pygame.KEYDOWN:
                                        if event.key == pygame.K_SPACE:
                                            sys.exit()
                                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                                        pos = pygame.mouse.get_pos()
                                        for n in nodes:
                                                        
                                            if n.rect.collidepoint(pos):
                                                
                                                activeNode.colour = (255, 255, 255)
                                                activeNode = n
                                                n.colour = (255, 0, 0)
                                                k = (boardSize/activeNode.size)
                                                drawBoard(z.board, colours, screen, k, boardSize, z.size)
                                                drawUI(boardSize, width, height, screen, nodes, buttons, activeNode)
                                                pygame.display.update()





main()
