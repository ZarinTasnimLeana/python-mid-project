import random

class Maze:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[1 for _ in range(cols)] for _ in range(rows)]
        self.generate()

    def generate(self):
        def carve(x, y):
            dirs = [(2,0), (-2,0), (0,2), (0,-2)]
            random.shuffle(dirs)

            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                if 0 < nx < self.rows and 0 < ny < self.cols and self.grid[nx][ny] == 1:
                    self.grid[nx][ny] = 0
                    self.grid[x + dx//2][y + dy//2] = 0
                    carve(nx, ny)

        self.grid[1][1] = 0
        carve(1, 1)

    def is_walkable(self, x, y):
        return 0 <= x < self.rows and 0 <= y < self.cols and self.grid[x][y] == 0