import pygame

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy, maze):
        nx = self.x + dx
        ny = self.y + dy

        if maze.is_walkable(nx, ny):
            self.x = nx
            self.y = ny

    def draw(self, screen, grid_size):
        pygame.draw.rect(screen, (0, 255, 0),
                         (self.y * grid_size, self.x * grid_size, grid_size, grid_size))