import pygame
from pygame import *
import os, random

pygame.mixer.pre_init(44100, -16, 2, 2048) # fix audio delay
pygame.init()


# screen = pygame.display.set_mode(scr_size)

class Crow(pygame.sprite.Sprite):
    def __init__(self,speed=5,sizex=-1,sizey=-1):
        self.scr_size = (600,150)
        self.width = 600
        self.height = 150

        self.screen = pygame.display.set_mode(self.scr_size)
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.images,self.rect = self.load_sprite_sheet('ptera.png',2,1,sizex,sizey,-1)
        self.crow_height = [self.height*0.82,self.height*0.75,self.height*0.60,self.height*0.45]
        self.crow_height_index = 3 #random.choice((0,3)) ## random.randrange(0,4)
        self.rect.centery = self.crow_height[self.crow_height_index]
        self.rect.left = self.width + self.rect.width
        self.image = self.images[0]
        self.movement = [-1*speed,0]
        self.index = 0
        self.counter = 0

    def load_sprite_sheet(
            self,
            sheetname,
            nx,
            ny,
            scalex = -1,
            scaley = -1,
            colorkey = None,
            ):
        fullname = os.path.join('sprites_copy',sheetname)
        sheet = pygame.image.load(fullname)
        sheet = sheet.convert()

        sheet_rect = sheet.get_rect()

        sprites = []

        sizex = sheet_rect.width/nx
        sizey = sheet_rect.height/ny

        for i in range(0,ny):
            for j in range(0,nx):
                rect = pygame.Rect((j*sizex,i*sizey,sizex,sizey))
                image = pygame.Surface(rect.size)
                image = image.convert()
                image.blit(sheet,(0,0),rect)

                if colorkey is not None:
                    if colorkey is -1:
                        colorkey = image.get_at((0,0))
                    image.set_colorkey(colorkey,RLEACCEL)

                if scalex != -1 or scaley != -1:
                    image = pygame.transform.scale(image,(scalex,scaley))

                sprites.append(image)

        sprite_rect = sprites[0].get_rect()

        return sprites,sprite_rect

    def draw(self):
        self.screen.blit(self.image,self.rect)

    def update(self):
        if self.counter % 10 == 0:
            self.index = (self.index+1)%2
        self.image = self.images[self.index]
        self.rect = self.rect.move(self.movement)
        self.counter = (self.counter + 1)
        if self.rect.right < 0:
            self.kill()
