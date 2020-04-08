import pygame
from pygame import *
import os

pygame.mixer.pre_init(44100, -16, 2, 2048) # fix audio delay
pygame.init()

scr_size = (width,height) = (600,150)
FPS = 60
gravity = 0.6

# screen = pygame.display.set_mode(scr_size)

class Dino():
    def __init__(self,sizex=-1,sizey=-1):
        self.screen = pygame.display.set_mode(scr_size)
        self.images,self.rect = self.load_sprite_sheet('dino.png',5,1,sizex,sizey,-1)
        self.images1,self.rect1 = self.load_sprite_sheet('dino_ducking.png',2,1,59,sizey,-1)
        self.rect.bottom = int(0.98*height)
        self.rect.left = width / 15
        self.image = self.images[0]
        self.index = 0
        self.counter = 0
        self.score = 0
        self.isJumping = False
        self.isDead = False
        self.isDucking = False
        self.isBlinking = False
        self.movement = [0,0]
        self.jumpSpeed = 11.5

        self.stand_pos_width = self.rect.width
        self.duck_pos_width = self.rect1.width

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

    def checkbounds(self):
        if self.rect.bottom > int(0.98*height):
            self.rect.bottom = int(0.98*height)
            self.isJumping = False

    def update(self):
        if self.isJumping:
            self.movement[1] = self.movement[1] + gravity

        if self.isJumping:
            self.index = 0
        elif self.isBlinking:
            if self.index == 0:
                if self.counter % 400 == 399:
                    self.index = (self.index + 1)%2
            else:
                if self.counter % 20 == 19:
                    self.index = (self.index + 1)%2

        elif self.isDucking:
            if self.counter % 5 == 0:
                self.index = (self.index + 1)%2
        else:
            if self.counter % 5 == 0:
                self.index = (self.index + 1)%2 + 2

        if self.isDead:
           self.index = 4

        if not self.isDucking:
            self.image = self.images[self.index]
            self.rect.width = self.stand_pos_width
        else:
            self.image = self.images1[(self.index)%2]
            self.rect.width = self.duck_pos_width

        self.rect = self.rect.move(self.movement)
        self.checkbounds()

        if not self.isDead and self.counter % 7 == 6 and self.isBlinking == False:
            self.score += 1
            # if self.score % 100 == 0 and self.score != 0:
                # if pygame.mixer.get_init() != None:
                #     checkPoint_sound.play()

        self.counter = (self.counter + 1)
