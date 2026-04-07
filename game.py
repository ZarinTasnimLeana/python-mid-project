import pygame
from settings import *
from entities.player import Player
from entities.maze import Maze
from storage import Storage
from entities.coin import Coin


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.running = True

        self.storage = Storage("data.json")
        self.data = self.storage.load()

        self.reset()

    def reset(self):
        self.maze = Maze(GRID_H, GRID_W)
        self.player = Player(1, 1)
        self.goal = (GRID_H - 2, GRID_W - 2)

        self.coins = [Coin(self.maze) for _ in range(5)]
        self.score = 0

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
        # Coin collection
        for coin in self.coins[:]:
            if (self.player.x, self.player.y) == (coin.x, coin.y):
                self.coins.remove(coin)
                self.score += 10

        # Win condition
        if (self.player.x, self.player.y) == self.goal:
            time_taken = pygame.time.get_ticks() - self.start_time
            score = max(1, 100 - time_taken)

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
                    pygame.draw.rect(
                        self.screen,
                        (0, 0, 0),
                        (j * GRID_SIZE, i * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                    )

        # draw coins
        for coin in self.coins:
            coin.draw(self.screen, GRID_SIZE)

        # draw goal
        pygame.draw.rect(
            self.screen,
            (255, 0, 0),
            (self.goal[1] * GRID_SIZE, self.goal[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        )

        # draw player
        self.player.draw(self.screen, GRID_SIZE)

         
        font = pygame.font.SysFont(None, 30)

        # background box
        pygame.draw.rect(self.screen, (0, 0, 0), (5, 5, 220, 70))

        # score text
        score_text = font.render(
            f"Score: {self.score}", True, (255, 255, 255)
        )
        self.screen.blit(score_text, (10, 10))

        
       
        pygame.display.flip()

    def run(self):
        while self.running:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                self.handle_events(event)

            self.update()
            self.draw()

        pygame.quit()
