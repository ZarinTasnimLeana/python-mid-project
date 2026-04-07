import random
import pygame

class Coin:
    def __init__(self, maze):
        while True:
            x = random.randint(1, maze.rows - 2)
            y = random.randint(1, maze.cols - 2)

            if maze.grid[x][y] == 0:
                self.x = x
                self.y = y
                break

    def draw(self, screen, grid_size):
        pygame.draw.circle(
            screen,
            (255, 215, 0),
            (
                self.y * grid_size + grid_size // 2,
                self.x * grid_size + grid_size // 2
            ),
            grid_size // 4
        )