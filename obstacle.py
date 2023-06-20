import pygame
import random
import os

pygame.font.init() 


WIN_WIDTH = 1000
WIN_HEIGHT = 800
FLOOR = 730
STAT_FONT = pygame.font.SysFont("comicsans", 50)
END_FONT = pygame.font.SysFont("comicsans", 70)

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Endless runner")

obstacle_img = pygame.transform.scale(pygame.image.load(os.path.join("imgs","box.png")).convert_alpha(), (100, 140))

class Obstacle():
    
    VEL = 5

    def __init__(self, x, height):
    
        self.x = x
        self.height = height
        self.img = obstacle_img
        self.passed = False
        self.set_height()
        self.isEnemy = False
        self.removed = False

    def set_height(self):
        
        if random.uniform(0, 1) < 0.5:
            self.height = 500
        else:
            self.height = 600

    def move(self):
        
        self.x -= self.VEL

    def draw(self, win):
        
        win.blit(self.img, (self.x, self.height))


    def collide(self, object, win):
        
        object_mask = object.get_mask()
        obstacle_mask = pygame.mask.from_surface(self.img)
        obstacle_offset = (self.x - object.x, self.height - round(object.y))

        obstacle_point = object_mask.overlap(obstacle_mask, obstacle_offset)

        if obstacle_point:
            return True

        return False

    def get_data(self):
        data = [self.x, self.height]
        return data