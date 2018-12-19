import pygame as pygame

from cell import Cell
from movement import Movement
from state import State


class Graphics:

    def __init__(self, height, width):
        pygame.init()
        self.window = pygame.display.set_mode((width, height + 60))
        self.height = height
        self.width = width
        self.font = pygame.font.SysFont("arial", 20)
        self.footerText = ""

    def print_footer(self, message):
        if (message != self.footerText):
            self.footerText = message
        pygame.draw.rect(self.window, (220, 220, 220), ((0, self.height), (self.width, 60)))
        text = self.font.render(message, 1, (0, 0, 0))
        self.window.blit(text, (int(self.width / 2 - text.get_rect().width / 2), 
            int(self.height + 30 - text.get_rect().height / 2)))
        pygame.display.flip()

    def print_message(self, message):
        pygame.draw.rect(self.window, (220, 220, 220), ((0, int(self.height / 2) - 30), (self.width, 60)))
        text = self.font.render(message, 1, (0, 0, 0))
        self.window.blit(text, (int(self.width / 2 - text.get_rect().width / 2), 
            int(self.height / 2) - text.get_rect().height / 2))
        pygame.display.flip()

    def print_arrow(self, move, headX, headY, size):
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



    def print(self, dungeon, player):
        event = pygame.event.poll()
        pygame.time.wait(1000)
        if event.type == pygame.QUIT:
            return False
        self.window.fill((255, 255, 255))
        case_x = self.width / dungeon.x
        case_y = self.height / dungeon.y

        tileStart = pygame.image.load("src/tileStart.jpg").convert()
        tileStart = pygame.transform.scale(tileStart, (int(case_x), int(case_y)))
        tileEmpty = pygame.image.load("src/tileEmpty.jpg").convert()
        tileEmpty = pygame.transform.scale(tileEmpty, (int(case_x), int(case_y)))
        tileWall = pygame.image.load("src/tileWall.jpg").convert()
        tileWall = pygame.transform.scale(tileWall, (int(case_x), int(case_y)))
        tileEnemy = pygame.image.load("src/tileEnemy.jpg").convert()
        tileEnemy = pygame.transform.scale(tileEnemy, (int(case_x), int(case_y)))
        tileTrap = pygame.image.load("src/tileTrap.jpg").convert()
        tileTrap = pygame.transform.scale(tileTrap, (int(case_x), int(case_y)))
        tileCrack = pygame.image.load("src/tileCrack.jpg").convert()
        tileCrack = pygame.transform.scale(tileCrack, (int(case_x), int(case_y)))
        tileTreasure = pygame.image.load("src/tileTreasure.jpg").convert()
        tileTreasure = pygame.transform.scale(tileTreasure, (int(case_x), int(case_y)))
        tileSword = pygame.image.load("src/tileSword.jpg").convert()
        tileSword = pygame.transform.scale(tileSword, (int(case_x), int(case_y)))
        tileKey = pygame.image.load("src/tileKey.jpg").convert()
        tileKey = pygame.transform.scale(tileKey, (int(case_x), int(case_y)))
        tilePortal = pygame.image.load("src/tilePortal.jpg").convert()
        tilePortal = pygame.transform.scale(tilePortal, (int(case_x), int(case_y)))
        tilePlatform = pygame.image.load("src/tilePlatform.jpg").convert()
        tilePlatform = pygame.transform.scale(tilePlatform, (int(case_x), int(case_y)))
        heroImage = pygame.image.load("src/hero.png").convert_alpha()
        heroImage = pygame.transform.scale(heroImage, (int(case_x), int(case_y)))
        heroSwordImage = pygame.image.load("src/heroSword.png").convert_alpha()
        heroSwordImage = pygame.transform.scale(heroSwordImage, (int(case_x), int(case_y)))
        heroTreasureImage = pygame.image.load("src/heroTreasure.png").convert_alpha()
        heroTreasureImage = pygame.transform.scale(heroTreasureImage, (int(case_x), int(case_y)))
        heroTreasureSwordImage = pygame.image.load("src/heroTreasureSword.png").convert_alpha()
        heroTreasureSwordImage = pygame.transform.scale(heroTreasureSwordImage, (int(case_x), int(case_y)))

        for i in range(dungeon.x + 1):
            pygame.draw.line(self.window, (0, 0, 0), (case_x * i, 0), (case_x * i, self.height))
        for i in range(dungeon.y + 1):
            pygame.draw.line(self.window, (0, 0, 0), (0, case_y * i), (self.width, case_y * i))
        for i in range(dungeon.x):
            for j in range(dungeon.y):
                cell = dungeon.dungeon[i, j]
                imagePosX = case_x * i
                imagePosY = case_y * j
                if cell == Cell.WALL:
                    self.window.blit(tileWall, (imagePosX, imagePosY))
                elif cell == Cell.EMPTY:
                    self.window.blit(tileEmpty, (imagePosX, imagePosY))
                elif cell == Cell.START:
                    self.window.blit(tileStart, (imagePosX, imagePosY))
                elif cell == Cell.TREASURE:
                    self.window.blit(tileTreasure, (imagePosX, imagePosY))
                elif cell == Cell.CRACKS:
                    self.window.blit(tileCrack, (imagePosX, imagePosY))
                elif cell == Cell.ENEMY:
                    self.window.blit(tileEnemy, (imagePosX, imagePosY))
                elif cell == Cell.KEY:
                    self.window.blit(tileKey, (imagePosX, imagePosY))
                elif cell == Cell.PLATFORM:
                    self.window.blit(tilePlatform, (imagePosX, imagePosY))
                elif cell == Cell.PORTAL:
                    self.window.blit(tilePortal, (imagePosX, imagePosY))
                elif cell == Cell.SWORD:
                    self.window.blit(tileSword, (imagePosX, imagePosY))
                elif cell == Cell.TRAP:
                    self.window.blit(tileTrap, (imagePosX, imagePosY))
        if player.sword:
            if player.treasure:
                self.window.blit(heroTreasureSwordImage, (case_x * player.x, case_y * player.y, case_x, case_y))
            else:
                self.window.blit(heroSwordImage, (case_x * player.x, case_y * player.y, case_x, case_y))
        elif player.treasure:
            self.window.blit(heroTreasureImage, (case_x * player.x, case_y * player.y, case_x, case_y))
        else:
            self.window.blit(heroImage, (case_x * player.x, case_y * player.y, case_x, case_y))
        self.print_footer(self.footerText)
        pygame.display.flip()
        return True

    def print_PDM_strat(self, dungeon, player, pdmMovement):
        case_x = self.width / dungeon.x
        case_y = self.height / dungeon.y
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
                    deltaX = int(case_x / 2)
                    deltaY = 2
                elif move == Movement.LEFT:
                    deltaX = 2
                    deltaY = int(case_y / 2)
                elif move == Movement.RIGHT:
                    deltaX = case_x - 2
                    deltaY = int(case_y / 2)
                elif move == Movement.DOWN:
                    deltaX = int(case_x / 2)
                    deltaY = case_y - 2
                self.print_arrow(move, case_x * i + deltaX, case_y * j + deltaY, 18)
        pygame.display.flip()

    def print_transition(self, dungeon, player, pdmMovement, pdmValue):
        t = False
        k = False
        s = False
        v = False
        finish = False
        while not finish:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t:
                        t = not t
                    if event.key == pygame.K_s:
                        s = not s
                    if event.key == pygame.K_k:
                        k = not k
                    if event.key == pygame.K_SPACE:
                        finish = True
                    if event.key == pygame.K_v:
                        v = not v
                if event.type == pygame.QUIT:
                    finish = True
            self.print(dungeon, player)
            self.print_PDM_strat(dungeon, player, pdmMovement, pdmValue)
        return True

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