from math import ceil
from random import randint
import pygame


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.next = 'red'
        self.left = 10
        self.up = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.up = top
        self.cell_size = cell_size

    def render(self, screen):
        font = pygame.font.Font(None, self.cell_size - 7)
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(
                    screen, 'white', (self.left + x * self.cell_size,
                                      self.up + y * self.cell_size,
                                      self.cell_size, self.cell_size), 1)
                cell = self.board[y][x]
                if cell == 10:
                    pygame.draw.rect(screen, 'red', (self.left + x * self.cell_size,
                                                     self.up + y * self.cell_size,
                                                     self.cell_size, self.cell_size), 0)
                elif cell != -1:
                    text = font.render(str(cell), True, 'green')
                    text_x = self.left + x * self.cell_size + 3
                    text_y = self.up + y * self.cell_size + 3
                    screen.blit(text, (text_x, text_y))

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        x -= self.left
        y -= self.up
        result_x = ceil(x / self.cell_size) - 1
        result_y = ceil(y / self.cell_size) - 1
        if result_x < 0 or result_x > self.width - 1 or result_y < 0 or result_y > self.height - 1:
            return None
        return result_y, result_x

    def get_click(self, mouse_pos):
        cell_coords = self.get_cell(mouse_pos)
        if self.on_click and cell_coords:
            self.on_click(cell_coords)


class Minesweeper(Board):
    def __init__(self, width, height, mines_count):
        super().__init__(width, height)
        if mines_count >= width * height:
            self.board = [[10] * width for _ in range(height)]
        else:
            self.board = [[-1] * width for _ in range(height)]
            used = set()
            while len(used) < mines_count:
                x, y = randint(0, width - 1), randint(0, height - 1)
                used.add(f'{y}-{x}')
                self.board[y][x] = 10

    def open_cell(self, y, x):
        nearby_mines = 0

        if x > 0:
            left = x - 1
        else:
            left = None

        if x < self.width - 1:
            right = x + 1
        else:
            right = None

        if y > 0:
            up = y - 1
        else:
            up = None

        if y < self.height - 1:
            bottom = y + 1
        else:
            bottom = None

        if (up is not None and left is not None and up is not None and left is not None and
                self.board[up][left] == 10):
            nearby_mines += 1
        if up is not None and self.board[up][x] == 10:
            nearby_mines += 1
        if up is not None and right is not None and self.board[up][right] == 10:
            nearby_mines += 1
        if right is not None and self.board[y][right] == 10:
            nearby_mines += 1
        if bottom is not None and right is not None and self.board[bottom][right] == 10:
            nearby_mines += 1
        if bottom and self.board[bottom][x] == 10:
            nearby_mines += 1
        if bottom is not None and left is not None and self.board[bottom][left] == 10:
            nearby_mines += 1
        if left is not None and self.board[y][left] == 10:
            nearby_mines += 1

        self.board[y][x] = nearby_mines

        if not nearby_mines:
            if up is not None and left is not None and self.board[up][left] == -1:
                self.open_cell(up, left)
            if up is not None and self.board[up][x] == -1:
                self.open_cell(up, x)
            if up is not None and right is not None and self.board[up][right] == -1:
                self.open_cell(up, right)
            if right is not None and self.board[y][right] == -1:
                self.open_cell(y, right)
            if bottom is not None and right is not None and self.board[bottom][right] == -1:
                self.open_cell(bottom, right)
            if bottom is not None and self.board[bottom][x] == -1:
                self.open_cell(bottom, x)
            if bottom is not None and left is not None and self.board[bottom][left] == -1:
                self.open_cell(bottom, left)
            if left is not None and self.board[y][left] == -1:
                self.open_cell(y, left)

    def on_click(self, cell_coords):
        self.open_cell(*cell_coords)


running = True
size = width, height = 440, 440

board = Minesweeper(10, 10, 10)
board.set_view(20, 20, 40)

pygame.init()

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos)
    screen.fill('black')
    board.render(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
