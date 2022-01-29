from random import randint
import copy

import pygame

screen_size = (800, 600)
screen_center = (screen_size[0] // 2, screen_size[1] // 2)
grid_size = 20
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
pygame.font.init()
text_font = pygame.font.SysFont('Arial', 30)

pygame.init()
running = True
game_over = False
surface = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()
game_speed = 10


class Snake:
    def __init__(self):
        self.alive = True
        self.tail_length = 0
        self.tail_blocks = []
        self.position = [grid_size * (screen_center[0] - grid_size) // grid_size,
                         grid_size * (screen_center[1] - grid_size) // grid_size,
                         grid_size,
                         grid_size
                         ]
        self.direction = 0
        self.input_buffer = []

    def update(self):
        self.tail_blocks.insert(0, copy.deepcopy(self.position))
        self.move()
        for i in range(0, len(self.tail_blocks), 1):
            if i >= self.tail_length:
                self.tail_blocks.pop(i)

    def move(self):
        if self.direction == 0:
            pass
        elif self.direction == 'up':
            self.position[1] -= grid_size
        elif self.direction == 'down':
            self.position[1] += grid_size
        elif self.direction == 'left':
            self.position[0] -= grid_size
        elif self.direction == 'right':
            self.position[0] += grid_size

    def grow(self):
        self.tail_length += 1


class Apple:
    def __init__(self):
        x_pos = (randint(0, (screen_size[0] - grid_size) // grid_size) * grid_size)
        y_pos = (randint(0, (screen_size[1] - grid_size) // grid_size) * grid_size)
        self.position = [x_pos, y_pos, grid_size, grid_size]

    def respawn(self):
        x_pos = (randint(0, screen_size[0] // grid_size) * grid_size)
        y_pos = (randint(0, screen_size[1] // grid_size) * grid_size)
        self.position = [x_pos, y_pos, grid_size, grid_size]


def update():
    global running
    global game_speed

    if snake.position[0] < 0 or snake.position[0] >= screen_size[0] \
            or snake.position[1] < 0 or snake.position[1] >= screen_size[1]:
        snake.alive = False

    for block_position in snake.tail_blocks:
        if block_position[0] == snake.position[0] and block_position[1] == snake.position[1]:
            snake.alive = False

    if not snake.alive:
        running = False

    if snake.position[0] == apple.position[0] and snake.position[1] == apple.position[1]:
        snake.grow()
        apple.respawn()
        game_speed *= 0.99

    if snake.input_buffer:
        snake.direction = snake.input_buffer[0]
        snake.input_buffer.pop(0)
    snake.update()


def draw():
    surface.fill(black)
    pygame.draw.rect(surface, red, apple.position)
    pygame.draw.rect(surface, green, snake.position)
    for block in snake.tail_blocks:
        pygame.draw.rect(surface, green, block)
    pygame.display.update()


snake = Snake()
apple = Apple()
frame_count = 0

while running:
    frame_count += 1
    # Checks for key input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                snake.input_buffer.append('up')
            elif event.key == pygame.K_s:
                snake.input_buffer.append('down')
            elif event.key == pygame.K_a:
                snake.input_buffer.append('left')
            elif event.key == pygame.K_d:
                snake.input_buffer.append('right')
            elif event.key == pygame.K_e:
                snake.grow()
                game_speed *= 0.99

    clock.tick(60)
    if frame_count >= game_speed:
        update()
        draw()
        frame_count = 0

    if game_over:
        surface.fill(black)
        text_surface = text_font.render(f'Game over. You scored: {snake.tail_length}. Press any key to play again',
                                        False, (0, 0, 0))
        pygame.display.update()
        