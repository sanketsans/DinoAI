import pygame
from pygame import *
import os, random

pygame.mixer.pre_init(44100, -16, 2, 2048) # fix audio delay
pygame.init()

class Ground():
    def __init__(self,speed=-5):
        self.scr_size = (600,150)
        self.width = 600
        self.height = 150

        self.screen = pygame.display.set_mode(self.scr_size)
        self.image,self.rect = self.load_image('ground.png',-1,-1,-1)
        self.image1,self.rect1 = self.load_image('ground.png',-1,-1,-1)
        self.rect.bottom = self.height
        self.rect1.bottom = self.height
        self.rect1.left = self.rect.right
        self.speed = speed

    def load_image(
        self,
        name,
        sizex=-1,
        sizey=-1,
        colorkey=None,
        ):

        fullname = os.path.join('sprites_copy', name)
        image = pygame.image.load(fullname)
        image = image.convert()
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, RLEACCEL)

        if sizex != -1 or sizey != -1:
            image = pygame.transform.scale(image, (sizex, sizey))

        return (image, image.get_rect())

    def draw(self):
        self.screen.blit(self.image,self.rect)
        self.screen.blit(self.image1,self.rect1)

    def update(self):
        self.rect.left += self.speed
        self.rect1.left += self.speed

        if self.rect.right < 0:
            self.rect.left = self.rect1.right

        if self.rect1.right < 0:
            self.rect1.left = self.rect.right
