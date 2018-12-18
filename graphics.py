import pygame as pygame

from cell import Cell
from movement import Movement
from state import State


class Graphics:

    def __init__(self, height, width):
        pygame.init()
        self.window = pygame.display.set_mode((width, height))
        self.height = height
        self.width = width
        self.font = pygame.font.SysFont("arial", 20)

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
        self.window.blit(heroImage, (case_x * player.x, case_y * player.y, case_x, case_y))
        pygame.display.flip()
        return True

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
            self.print_specifique(t, k, s, v, dungeon, player, pdmMovement, pdmValue)
        return True

    def print_specifique(self, t, k, s, val, dungeon, player, pdmMovement, pdmValue):
        self.print(dungeon, player)
        case_x = self.width / dungeon.x
        case_y = self.height / dungeon.y
        for i in range(dungeon.x):
            for j in range(dungeon.y):
                if dungeon.is_wall(i, j):
                    continue
                st = State(t, k, s, (i, j))
                if st not in pdmMovement.strat.keys():
                    continue
                label = self.font.render(" ", 1, (255, 0, 0))
                if not val:
                    move = pdmMovement.get_next_move(st)
                    if move == Movement.TOP:
                        label = self.font.render("^", 1, (255, 0, 0))
                    elif move == Movement.LEFT:
                        label = self.font.render("<", 1, (255, 0, 0))
                    elif move == Movement.RIGHT:
                        label = self.font.render(">", 1, (255, 0, 0))
                    elif move == Movement.DOWN:
                        label = self.font.render("\/", 1, (255, 0, 0))
                else:
                    label = self.font.render(str(int(pdmValue[st])), 1, (255, 0, 0))
                self.window.blit(label, (case_x * i + int(case_x / 2 - 10), case_y * j + 30))
        label = self.font.render("t:" + str(t) + " ,k:" + str(k) + ",s:" + str(s), 1, (0, 0, 0))
        self.window.blit(label, (0, 0))
        pygame.display.flip()

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