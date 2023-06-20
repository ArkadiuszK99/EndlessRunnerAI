import pygame
import os
from bullet import Bullet

character_walk_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","character_walk.png")).convert_alpha())
character_crouch_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","character_crouch.png")).convert_alpha())

startingY = 630

class Character:
    
    def __init__(self):
        
        self.x = 0
        self.y = startingY
        self.img = character_walk_img
        self.jumpCount = 0
        self.crouchCount = 0
        self.bullets = []
        

    def jump(self):
        
        self.jumpCount = 40

    def crouch(self):
        
        self.crouchCount = 80

    def shot(self):
        self.bullets.append(Bullet(self.x, self.y + 20))

    def move(self):
        
        #jump
        if self.jumpCount > 0:
            self.y -= 5
            self.jumpCount -= 1

        #fall
        if self.jumpCount == 0 and self.y < startingY:
            self.y += 5

        #crouch
        if self.crouchCount > 0:
            self.img = character_crouch_img
            self.crouchCount -= 1
            self.y = 650

            if self.crouchCount == 0:
                self.img = character_walk_img
                self.y = startingY

    def draw(self, win):
        
        win.blit(self.img, (self.x, self.y))

    def get_mask(self):
        
        return pygame.mask.from_surface(self.img)