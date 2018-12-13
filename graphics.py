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
        for i in range(dungeon.x + 1):
            pygame.draw.line(self.window, (0, 0, 0), (case_x * i, 0), (case_x * i, self.height))
        for i in range(dungeon.y + 1):
            pygame.draw.line(self.window, (0, 0, 0), (0, case_y * i), (self.width, case_y * i))
        for i in range(dungeon.x):
            for j in range(dungeon.y):
                cell = dungeon.dungeon[i, j]
                if cell == Cell.WALL:
                    pygame.draw.rect(self.window, (0, 0, 0), (case_x * i, case_y * j, case_x, case_y))
                elif cell == Cell.START:
                    radius = case_y / 2 - 1 if case_x > case_y else case_x / 2 - 1
                    pygame.draw.circle(self.window, (0, 0, 0),
                                       (int(case_x * i + case_x / 2),int(case_y * j + case_y / 2)), int(radius), 1)
                else:
                    label = self.font.render(" ", 1, (0, 0, 0))
                    if cell == Cell.TREASURE:
                        label = self.font.render("T", 1, (0, 0, 0))
                    elif cell == Cell.CRACKS:
                        label = self.font.render("C", 1, (0, 0, 0))
                    elif cell == Cell.ENEMY:
                        label = self.font.render("E", 1, (0, 0, 0))
                    elif cell == Cell.KEY:
                        label = self.font.render("K", 1, (0, 0, 0))
                    elif cell == Cell.PLATFORM:
                        label = self.font.render("_", 1, (0, 0, 0))
                    elif cell == Cell.PORTAL:
                        label = self.font.render("P", 1, (0, 0, 0))
                    elif cell == Cell.SWORD:
                        label = self.font.render("S", 1, (0, 0, 0))
                    elif cell == Cell.TRAP:
                        label = self.font.render("R", 1, (0, 0, 0))
                    self.window.blit(label, (case_x * i + int(case_x / 2 - 10), case_y * j + 10))
        pygame.draw.rect(self.window, (0, 0, 200), (case_x * player.x + 10, case_y * player.y + 10, case_x - 20, case_y - 20))
        pygame.display.flip()
        return True

    def print_transition(self, dungeon, player, pdmMovement):
        event = pygame.event.poll()
        self.print(dungeon, player)
        case_x = self.width / dungeon.x
        case_y = self.height / dungeon.y
        for i in range(dungeon.x):
            for j in range(dungeon.y):
                if dungeon.is_wall(i, j):
                    continue
                s = State(False, False, False, (i, j))
                move = pdmMovement.get_next_move(s)
                label = self.font.render(" ", 1, (255, 0, 0))
                if move == Movement.TOP:
                    label = self.font.render("^", 1, (255, 0, 0))
                elif move == Movement.LEFT:
                    label = self.font.render("<", 1, (255, 0, 0))
                elif move == Movement.RIGHT:
                    label = self.font.render(">", 1, (255, 0, 0))
                elif move == Movement.DOWN:
                    label = self.font.render("\/", 1, (255, 0, 0))
                self.window.blit(label, (case_x * i + int(case_x / 2 - 10), case_y * j + 30))
        pygame.display.flip()
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