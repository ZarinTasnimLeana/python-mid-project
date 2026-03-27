import pygame
from settings import *
from entities.player import Player
from entities.maze import Maze
from storage import Storage

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.running = True
        self.paused = False

        self.storage = Storage("data.json")
        self.data = self.storage.load()

        self.reset()

    def reset(self):
        self.maze = Maze(GRID_H, GRID_W)
        self.player = Player(1, 1)
        self.goal = (GRID_H - 2, GRID_W - 2)

        self.start_time = pygame.time.get_ticks()

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            self.running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False

            elif event.key == pygame.K_UP:
                self.player.move(-1, 0, self.maze)
            elif event.key == pygame.K_DOWN:
                self.player.move(1, 0, self.maze)
            elif event.key == pygame.K_LEFT:
                self.player.move(0, -1, self.maze)
            elif event.key == pygame.K_RIGHT:
                self.player.move(0, 1, self.maze)

    def update(self):
        if (self.player.x, self.player.y) == self.goal:
            time_taken = pygame.time.get_ticks() - self.start_time
            score = max(1, 10000 - time_taken)

            if score > self.data["high_score"]:
                self.data["high_score"] = score
                self.storage.save(self.data)

            print("YOU WIN! Score:", score)
            self.reset()

    def draw(self):
        self.screen.fill((200, 200, 200))

        # draw maze
        for i in range(self.maze.rows):
            for j in range(self.maze.cols):
                if self.maze.grid[i][j] == 1:
                    pygame.draw.rect(self.screen, (0, 0, 0),
                                     (j * GRID_SIZE, i * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # draw goal
        pygame.draw.rect(self.screen, (255, 0, 0),
                         (self.goal[1] * GRID_SIZE, self.goal[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # draw player
        self.player.draw(self.screen, GRID_SIZE)

        # show score
        font = pygame.font.SysFont(None, 30)
        text = font.render(f"High Score: {self.data['high_score']}", True, (0, 0, 0))
        self.screen.blit(text, (10, 10))

        pygame.display.flip()

    def run(self):
        while self.running:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                self.handle_events(event)

            self.update()
            self.draw()

        pygame.quit()