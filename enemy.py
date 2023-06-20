import pygame
import os
from obstacle import Obstacle

pygame.font.init()

WIN_WIDTH = 600
WIN_HEIGHT = 800
FLOOR = 730
STAT_FONT = pygame.font.SysFont("comicsans", 50)
END_FONT = pygame.font.SysFont("comicsans", 70)

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Endless runner")

enemy_img = pygame.transform.scale(pygame.image.load(os.path.join("imgs","enemy1.png")).convert_alpha(), (60, 100))

class Enemy(Obstacle):

    def __init__(self, x, height):
        super().__init__(x, height)
        self.img = pygame.transform.flip(enemy_img, True, False)
        self.killed = False
        self.height = 600
        self.isEnemy = True
        self.hitbox = (self.x, self.height, 60, 100)
