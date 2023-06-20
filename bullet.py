import pygame
import os

bullet_img = pygame.transform.scale(pygame.image.load(os.path.join("imgs","bullet.png")).convert_alpha(), (20, 10))

class Bullet(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.vel = 8
        self.img = bullet_img

    def move(self):
        self.x += self.vel

    def draw(self, win):    
        win.blit(self.img, (self.x, self.y))
    
    def get_mask(self):
        
        return pygame.mask.from_surface(self.img)