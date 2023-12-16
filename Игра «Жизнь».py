from math import ceil
import pygame


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.next = 'red'
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                is_alive = self.board[y][x]
                if is_alive:
                    pygame.draw.rect(screen, 'green', (self.left + x * self.cell_size,
                                                       self.top + y * self.cell_size,
                                                       self.cell_size, self.cell_size), 0)
                pygame.draw.rect(screen, 'white', (self.left + x * self.cell_size,
                                                   self.top + y * self.cell_size,
                                                   self.cell_size, self.cell_size), 1)

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        x -= self.left
        y -= self.top
        result_x = ceil(x / self.cell_size) - 1
        result_y = ceil(y / self.cell_size) - 1
        if result_x < 0 or result_x > self.width - 1 or result_y < 0 or result_y > self.height - 1:
            return None
        return result_y, result_x

    def get_click(self, mouse_pos):
        cell_coords = self.get_cell(mouse_pos)
        if self.on_click:
            self.on_click(cell_coords)


class Life(Board):
    def __init__(self, *args):
        super().__init__(*args)
        self.speed = 10
        self.speed_delta = 1
        self.time_left = self.speed
        self.is_running = False

    def next_move(self):
        new_field = [[0] * self.width for _ in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                neighbours = 0
                left = x - 1
                right = (x + 1) % self.width
                top = y - 1
                bottom = (y + 1) % self.height
                if self.board[top][left]:
                    neighbours += 1
                if self.board[top][x]:
                    neighbours += 1
                if self.board[top][right]:
                    neighbours += 1
                if self.board[y][right]:
                    neighbours += 1
                if self.board[bottom][right]:
                    neighbours += 1
                if self.board[bottom][x]:
                    neighbours += 1
                if self.board[bottom][left]:
                    neighbours += 1
                if self.board[y][left]:
                    neighbours += 1
                new_state = None
                if self.board[y][x]:
                    if 2 <= neighbours <= 3:
                        new_state = 1
                    else:
                        new_state = 0
                elif not self.board[y][x]:
                    if neighbours == 3:
                        new_state = 1
                    else:
                        new_state = 0
                new_field[y][x] = new_state
        self.board = new_field

    def stop(self):
        self.is_running = not self.is_running

    def plus_speed(self):
        self.speed += self.speed_delta

    def min_speed(self):
        self.speed -= self.speed_delta

    def tick(self):
        if not self.is_running:
            return
        self.time_left -= 1
        if self.time_left <= 0:
            self.next_move()
            self.time_left = self.speed

    def on_click(self, cell_coords):
        if not cell_coords:
            return
        y, x = cell_coords
        if not self.is_running:
            self.board[y][x] = int(not bool(self.board[y][x]))


running = True
size = width, height = 650, 650

board = Life(30, 30)
board.set_view(10, 10, 20)

pygame.init()
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                board.get_click(event.pos)
            elif event.button == 3:
                board.stop()
        elif event.type == pygame.MOUSEWHEEL:
            if event.y == 1:
                board.plus_speed()
            elif event.y == -1:
                board.min_speed()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                board.stop()
    screen.fill(pygame.Color("black"))
    board.render(screen)
    board.tick()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()