import pygame
from pygame import *
import os, random
from dino import screen

pygame.mixer.pre_init(44100, -16, 2, 2048) # fix audio delay
pygame.init()

scr_size = (width,height) = (600,150)
FPS = 60
gravity = 0.6

black = (0,0,0)
white = (255,255,255)
# background_col = (235,235,235)
background_col = (255,255,255)

high_score = 0

screen = pygame.display.set_mode(scr_size)

class Ground():
    def __init__(self,speed=-5):
        self.image,self.rect = self.load_image('ground.png',-1,-1,-1)
        self.image1,self.rect1 = self.load_image('ground.png',-1,-1,-1)
        self.rect.bottom = height
        self.rect1.bottom = height
        self.rect1.left = self.rect.right
        self.speed = speed

    def load_image(
        self,
        name,
        sizex=-1,
        sizey=-1,
        colorkey=None,
        ):

        fullname = os.path.join('sprites', name)
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
        screen.blit(self.image,self.rect)
        screen.blit(self.image1,self.rect1)

    def update(self):
        self.rect.left += self.speed
        self.rect1.left += self.speed

        if self.rect.right < 0:
            self.rect.left = self.rect1.right

        if self.rect1.right < 0:
            self.rect1.left = self.rect.right
