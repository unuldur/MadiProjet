from dungeon import Cell
from player import Movement
from state import State
import pygame

# Graphic class that handles all that everything displayed
class Graphics:
    def __init__(self, height, width, dungeon):
        pygame.init()
        # Set the size of the window with additional space for the footer
        self.window = pygame.display.set_mode((width, height + int(height / 10)))
        self.height = height
        self.width = width
        # Set the size of a cell
        self.case_x = self.width / dungeon.x
        self.case_y = self.height / dungeon.y

        # Set the font used for text
        self.font = pygame.font.SysFont("arial", min(20, int(width / 50)))
        self.footerText = ""
        # Load all the pictures used
        self.pictures = {}
        self.pictures["start"] = pygame.image.load("resources/tileStart.jpg").convert()
        self.pictures["start"] = pygame.transform.scale(self.pictures["start"], (int(self.case_x), int(self.case_y)))
        self.pictures["empty"] = pygame.image.load("resources/tileEmpty.jpg").convert()
        self.pictures["empty"] = pygame.transform.scale(self.pictures["empty"], (int(self.case_x), int(self.case_y)))
        self.pictures["wall"] = pygame.image.load("resources/tileWall.jpg").convert()
        self.pictures["wall"] = pygame.transform.scale(self.pictures["wall"], (int(self.case_x), int(self.case_y)))
        self.pictures["enemy"] = pygame.image.load("resources/tileEnemy.jpg").convert()
        self.pictures["enemy"] = pygame.transform.scale(self.pictures["enemy"], (int(self.case_x), int(self.case_y)))
        self.pictures["trap"] = pygame.image.load("resources/tileTrap.jpg").convert()
        self.pictures["trap"] = pygame.transform.scale(self.pictures["trap"], (int(self.case_x), int(self.case_y)))
        self.pictures["crack"] = pygame.image.load("resources/tileCrack.jpg").convert()
        self.pictures["crack"] = pygame.transform.scale(self.pictures["crack"], (int(self.case_x), int(self.case_y)))
        self.pictures["treasure"] = pygame.image.load("resources/tileTreasure.jpg").convert()
        self.pictures["treasure"] = pygame.transform.scale(self.pictures["treasure"], (int(self.case_x), int(self.case_y)))
        self.pictures["sword"] = pygame.image.load("resources/tileSword.jpg").convert()
        self.pictures["sword"] = pygame.transform.scale(self.pictures["sword"], (int(self.case_x), int(self.case_y)))
        self.pictures["key"] = pygame.image.load("resources/tileKey.jpg").convert()
        self.pictures["key"] = pygame.transform.scale(self.pictures["key"], (int(self.case_x), int(self.case_y)))
        self.pictures["portal"] = pygame.image.load("resources/tilePortal.jpg").convert()
        self.pictures["portal"] = pygame.transform.scale(self.pictures["portal"], (int(self.case_x), int(self.case_y)))
        self.pictures["platform"] = pygame.image.load("resources/tilePlatform.jpg").convert()
        self.pictures["platform"] = pygame.transform.scale(self.pictures["platform"], (int(self.case_x), int(self.case_y)))
        self.pictures["hero"] = pygame.image.load("resources/hero.png").convert_alpha()
        self.pictures["hero"] = pygame.transform.scale(self.pictures["hero"], (int(self.case_x), int(self.case_y)))
        self.pictures["heroSword"] = pygame.image.load("resources/heroSword.png").convert_alpha()
        self.pictures["heroSword"] = pygame.transform.scale(self.pictures["heroSword"], (int(self.case_x), int(self.case_y)))
        self.pictures["heroTreasure"] = pygame.image.load("resources/heroTreasure.png").convert_alpha()
        self.pictures["heroTreasure"] = pygame.transform.scale(self.pictures["heroTreasure"], (int(self.case_x), int(self.case_y)))
        self.pictures["heroTreasureSword"] = pygame.image.load("resources/heroTreasureSword.png").convert_alpha()
        self.pictures["heroTreasureSword"] = pygame.transform.scale(self.pictures["heroTreasureSword"], (int(self.case_x), int(self.case_y)))

    # Print a message in the footer
    def print_footer(self, message):
        if (message != self.footerText):
            self.footerText = message
        pygame.draw.rect(self.window, (220, 220, 220), ((0, self.height), (self.width, int(self.height / 10))))
        text = self.font.render(message, 1, (0, 0, 0))
        self.window.blit(text, (int(self.width / 2 - text.get_rect().width / 2), 
            int(self.height + int(self.height / 20) - text.get_rect().height / 2)))
        pygame.display.flip()

    # Print a message in the middle of the screen
    def print_message(self, message):
        pygame.draw.rect(self.window, (220, 220, 220), ((0, int(self.height / 2) - int(self.height / 20)), (self.width, int(self.height / 10))))
        text = self.font.render(message, 1, (0, 0, 0))
        self.window.blit(text, (int(self.width / 2 - text.get_rect().width / 2), 
            int(self.height / 2) - text.get_rect().height / 2))
        pygame.display.flip()

    # Print an arrow indicating direction move with its in position (headX, headY) of size size
    def print_arrow(self, move, headX, headY, size):
        if move == Movement.STOP:
            return
        head = (headX, headY)
        leftWing = 0
        rightWing = 0
        leftTopBase = 0
        leftBotBase = 0
        rightTopBase = 0
        rightBotBase = 0
        if move == Movement.RIGHT:
            leftWing = (head[0] - int(size / 3), head[1] - int(size / 2))
            rightWing = (head[0] - int(size / 3), head[1] + int(size / 2))
            leftTopBase = (head[0] - size, head[1] - int(size / 6))
            leftBotBase = (head[0] - int(size / 3), head[1] - int(size / 6))
            rightTopBase = (head[0] - size, head[1] + int(size / 6))
            rightBotBase = (head[0] - int(size / 3), head[1] + int(size / 6))
        elif move == Movement.DOWN:
            leftWing = (head[0] + int(size / 2), head[1] - int(size / 3))
            rightWing = (head[0] - int(size / 2), head[1] - int(size / 3))
            leftTopBase = (head[0] + int(size / 6), head[1] - size)
            leftBotBase = (head[0] + int(size / 6), head[1] - int(size / 3))
            rightTopBase = (head[0] - int(size / 6), head[1] - size)
            rightBotBase = (head[0] - int(size / 6), head[1] - int(size / 3))
        elif move == Movement.TOP:
            leftWing = (head[0] - int(size / 2), head[1] + int(size / 3))
            rightWing = (head[0] + int(size / 2), head[1] + int(size / 3))
            leftTopBase = (head[0] - int(size / 6), head[1] + size)
            leftBotBase = (head[0] - int(size / 6), head[1] + int(size / 3))
            rightTopBase = (head[0] + int(size / 6), head[1] + size)
            rightBotBase = (head[0] + int(size / 6), head[1] + int(size / 3))
        elif move == Movement.LEFT:
            leftWing = (head[0] + int(size / 3), head[1] - int(size / 2))
            rightWing = (head[0] + int(size / 3), head[1] + int(size / 2))
            leftTopBase = (head[0] + size, head[1] - int(size / 6))
            leftBotBase = (head[0] + int(size / 3), head[1] - int(size / 6))
            rightTopBase = (head[0] + size, head[1] + int(size / 6))
            rightBotBase = (head[0] + int(size / 3), head[1] + int(size / 6))
        pygame.draw.polygon(self.window, (250, 0, 0), 
            (leftTopBase, rightTopBase, rightBotBase, rightWing, head, leftWing, leftBotBase))

    # Print the dungeon and the player position
    def print(self, dungeon, player):
        event = pygame.event.poll()
        pygame.time.wait(50)
        if event.type == pygame.QUIT:
            return False
        self.window.fill((255, 255, 255))

        for i in range(dungeon.x + 1):
            pygame.draw.line(self.window, (0, 0, 0), (self.case_x * i, 0), (self.case_x * i, self.height))
        for i in range(dungeon.y + 1):
            pygame.draw.line(self.window, (0, 0, 0), (0, self.case_y * i), (self.width, self.case_y * i))
        for i in range(dungeon.x):
            for j in range(dungeon.y):
                cell = dungeon.cells[i, j]
                imagePosX = self.case_x * i
                imagePosY = self.case_y * j
                if cell == Cell.WALL:
                    self.window.blit(self.pictures["wall"], (imagePosX, imagePosY))
                elif cell == Cell.EMPTY:
                    self.window.blit(self.pictures["empty"], (imagePosX, imagePosY))
                elif cell == Cell.START:
                    self.window.blit(self.pictures["start"], (imagePosX, imagePosY))
                elif cell == Cell.TREASURE:
                    self.window.blit(self.pictures["treasure"], (imagePosX, imagePosY))
                elif cell == Cell.CRACKS:
                    self.window.blit(self.pictures["crack"], (imagePosX, imagePosY))
                elif cell == Cell.ENEMY:
                    self.window.blit(self.pictures["enemy"], (imagePosX, imagePosY))
                elif cell == Cell.KEY:
                    self.window.blit(self.pictures["key"], (imagePosX, imagePosY))
                elif cell == Cell.PLATFORM:
                    self.window.blit(self.pictures["platform"], (imagePosX, imagePosY))
                elif cell == Cell.PORTAL:
                    self.window.blit(self.pictures["portal"], (imagePosX, imagePosY))
                elif cell == Cell.SWORD:
                    self.window.blit(self.pictures["sword"], (imagePosX, imagePosY))
                elif cell == Cell.TRAP:
                    self.window.blit(self.pictures["trap"], (imagePosX, imagePosY))
        # Use the right player image given what he has picked
        if player.sword:
            if player.treasure:
                self.window.blit(self.pictures["heroTreasureSword"], (self.case_x * player.x, self.case_y * player.y, self.case_x, self.case_y))
            else:
                self.window.blit(self.pictures["heroSword"], (self.case_x * player.x, self.case_y * player.y, self.case_x, self.case_y))
        elif player.treasure:
            self.window.blit(self.pictures["heroTreasure"], (self.case_x * player.x, self.case_y * player.y, self.case_x, self.case_y))
        else:
            self.window.blit(self.pictures["hero"], (self.case_x * player.x, self.case_y * player.y, self.case_x, self.case_y))
        self.print_footer(self.footerText)
        pygame.display.flip()
        return True

    # Print the PDM stategy: arrow in each cell that indicates the movment played in this cell
    def print_PDM_strat(self, dungeon, player, pdmMovement):
        for i in range(dungeon.x):
            for j in range(dungeon.y):
                if dungeon.is_wall(i, j):
                    continue
                st = State(player.treasure, player.key, player.sword, (i, j))
                if st not in pdmMovement.strat.keys():
                    continue
                move = pdmMovement.get_next_move(st)
                deltaX = 0
                deltaY = 0
                if move == Movement.TOP:
                    deltaX = int(self.case_x / 2)
                    deltaY = 2
                elif move == Movement.LEFT:
                    deltaX = 2
                    deltaY = int(self.case_y / 2)
                elif move == Movement.RIGHT:
                    deltaX = self.case_x - 2
                    deltaY = int(self.case_y / 2)
                elif move == Movement.DOWN:
                    deltaX = int(self.case_x / 2)
                    deltaY = self.case_y - 2
                self.print_arrow(move, self.case_x * i + deltaX, self.case_y * j + deltaY, 18)
        pygame.display.flip()
        self.print(dungeon, player)

    # Print the value of each cell, can only be used with a qlearning pdm
    def print_PDM_values(self, dungeon, player, pdm):
        for i in range(dungeon.x):
            for j in range(dungeon.y):
                if dungeon.is_wall(i, j):
                    continue
                st = State(player.treasure, player.key, player.sword, (i, j))
                text = self.font.render(str(pdm.nodes[st].getMaxAction()[1]), 1, (255, 0, 0))
                self.window.blit(text, (self.case_x * i + 7, self.case_y * j + 7))
        pygame.display.flip()

    # Returns the move played by the player when using user's commands
    def get_next_move(self, state):
        move = None
        while move is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    move = Movement.STOP
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        move = Movement.TOP
                    if event.key == pygame.K_DOWN:
                        move = Movement.DOWN
                    if event.key == pygame.K_RIGHT:
                        move = Movement.RIGHT
                    if event.key == pygame.K_LEFT:
                        move = Movement.LEFT
        return move