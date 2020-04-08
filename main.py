import os
import sys
import pygame
import random
from pygame import *
import numpy as np
from dino import Dino
from cactus import Cactus
from crows import Crow
from ground import Ground
from scoreboard import Scoreboard

class env:
    def __init__(self):
        self.crow_height = 0.0
        self.i = 0
        self.high_score = 0
        self.nearest = 800
        self.t_reward = 0

        self.discrete_spaces = np.linspace(76, 640, num=100)

        self.action_complete = True

        self.old_states = []
        self.new_states = []

        pygame.mixer.pre_init(44100, -16, 2, 2048) # fix audio delay
        pygame.init()

        self.scr_size = (self.width,self.height) = (600,150)
        self.FPS = 60

        # background_col = (235,235,235)
        self.background_col = (255,255,255)

        self.screen = pygame.display.set_mode(self.scr_size)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("T-Rex Rush")

        temp_images,temp_rect = self.load_sprite_sheet('numbers.png',12,1,11,int(11*6/5),-1)
        self.HI_image = pygame.Surface((22,int(11*6/5)))
        self.HI_rect = self.HI_image.get_rect()
        self.HI_image.fill(self.background_col)
        self.HI_image.blit(temp_images[10],temp_rect)
        temp_rect.left += temp_rect.width
        self.HI_image.blit(temp_images[11],temp_rect)
        self.HI_rect.top = self.height*0.1
        self.HI_rect.left = self.width*0.73

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

    def introscreen(self):
        temp_dino = Dino(44,47)
        temp_dino.isBlinking = False
        gameStart = True


        temp_ground,temp_ground_rect = load_sprite_sheet('ground.png',15,1,-1,-1,-1)
        temp_ground_rect.left = width/20
        temp_ground_rect.bottom = height

        while not gameStart:
            if pygame.display.get_surface() == None:
                print("Couldn't load display surface")
                return True
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                            temp_dino.isJumping = True
                            temp_dino.isBlinking = False
                            temp_dino.movement[1] = -1*temp_dino.jumpSpeed

            temp_dino.update()

            if pygame.display.get_surface() != None:
                screen.fill(background_col)
                screen.blit(temp_ground[0],temp_ground_rect)
                if temp_dino.isBlinking:
                    pass
                    # screen.blit(logo,logo_rect)
                    # screen.blit(callout,callout_rect)
                temp_dino.draw()

                pygame.display.update()

            clock.tick(self.FPS)
            if temp_dino.isJumping == False and temp_dino.isBlinking == False:
                gameStart = True

    def reset(self):
        self.gamespeed = 4
        self.startMenu = False
        self.gameOver = False
        self.gameQuit = False
        self.playerDino = Dino(44,47)
        self.new_ground = Ground(-1*self.gamespeed)
        self.scb = Scoreboard()
        self.highsc = Scoreboard(self.width*0.78)
        self.counter = 0

        self.t_reward = 0

        self.nearest = 800
        self.action_complete = True

        self.cacti = pygame.sprite.Group()
        self.crows = pygame.sprite.Group()
        self.last_obstacle = pygame.sprite.Group()

        Cactus.containers = self.cacti
        Crow.containers = self.crows

        self.old_states.append(self.new_ground.speed)
        self.old_states.append(np.digitize(self.nearest, self.discrete_spaces))
        self.old_states.append(self.crow_height)
        self.old_states.append("Crouch" if self.playerDino.rect[2] != 44 else " standing")

        return self.old_states

    def play(self):
        for c in self.cacti:
            c.movement[0] = -1*self.gamespeed
            if pygame.sprite.collide_mask(self.playerDino,c):
                self.playerDino.isDead = True

        for p in self.crows:
            p.movement[0] = -1*self.gamespeed
            if pygame.sprite.collide_mask(self.playerDino,p):
                self.playerDino.isDead = True

        if len(self.cacti) < 2:
            if len(self.cacti) == 0:
                self.last_obstacle.empty()
                self.last_obstacle.add(Cactus(self.gamespeed,40,40))
            else:
                for l in self.last_obstacle:
                    if l.rect.right < self.width*0.7 and random.randrange(0,50) == 10:
                        self.last_obstacle.empty()
                        self.last_obstacle.add(Cactus(self.gamespeed, 40, 40))

        if len(self.crows) == 0 and random.randrange(0,200) == 10 and self.counter > 500:
            for l in self.last_obstacle:
                if l.rect.right < width*0.8:
                    self.last_obstacle.empty()
                    self.last_obstacle.add(Crow(self.gamespeed, 46, 40))

        self.playerDino.update()
        self.cacti.update()
        self.crows.update()
        self.new_ground.update()
        self.scb.update(self.playerDino.score)
        all_loc = []
        for c in self.cacti:
            if(c.rect.left < 72):
                all_loc.append(1000)
            else:
                all_loc.append(c.rect.left)

        h = []
        for p in self.crows:
            if(p.rect.left < 72):
                all_loc.append(1000)
            else:
                all_loc.append(p.rect.left)
                h.append(p.rect.centery)

        try:
            self.crow_height = min(h)
            self.nearest = min(all_loc)
        except:
            self.crow_height = 0.0
            if len(all_loc) == 0:
                self.t_reward += 99
                self.nearest = 800
            else:
                self.nearest = min(all_loc)

        self.new_states = []

        self.new_states.append(self.new_ground.speed)
        self.new_states.append(np.digitize(self.nearest, self.discrete_spaces))
        self.new_states.append(self.crow_height)
        # self.new_states.append("Jump" if self.playerDino.rect[1] != 100 else "running")
        self.new_states.append("Crouch" if self.playerDino.rect[2] != 44 else " standing")

        # if((0 < (100 - self.playerDino.rect[1]) <= 10) and self.i == 0):
        #     self.t_reward += 1
        #     self.new_states.append(self.t_reward)
        #     print("new__ states: ", self.new_states)
        if(self.playerDino.rect[1] == 100 and (self.playerDino.rect[2] == 44 or self.playerDino.rect[2] == 59)):
            self.i = 0
            self.action_complete = True
            # print("new states: ", self.new_states, self.action_complete)
        if(self.playerDino.rect[1] != 100):
            self.i += 1
        # print('Pos: ',playerDino.rect[1], playerDino.rect[2]) ## changes rect[1] - when jumping, rect[2] - when crouch
        self.highsc.update(self.high_score)

        if pygame.display.get_surface() != None:
            self.screen.fill(self.background_col)
            self.new_ground.draw()
            # clouds.draw(screen)
            self.scb.draw()
            if self.high_score != 0:
                self.highsc.draw()
                self.screen.blit(self.HI_image,self.HI_rect)
            self.cacti.draw(self.screen)
            self.crows.draw(self.screen)
            self.playerDino.draw()

            pygame.display.update()
        self.clock.tick(self.FPS)

        if self.playerDino.isDead:
            # print('Reward: -1000')

            # print("final_ states: ", self.new_states)
            print("<<<<<<GAME OVER>>>>>>>")
            self.gameOver = True
            # self.reset()

        if self.counter%700 == 699:
            self.new_ground.speed -= 1
            self.gamespeed += 1
            self.t_reward += 99

        self.counter = (self.counter + 1)

    def step(self, action): ## 0 - stay, 1 - jump, 2 - crouch, 3 - standup
        # while not self.gameQuit:
        #     while not self.gameOver:
        self.t_reward = 0
        if pygame.display.get_surface() == None:
            print("Couldn't load display surface")
            self.gameQuit = True
            self.gameOver = True
        else:
            if action == 1: ## event.key == pygame.K_SPACE
                self.action_complete = False
                if self.playerDino.rect.bottom == int(0.98*self.height):
                    self.playerDino.isJumping = True
                    # if pygame.mixer.get_init() != None:
                    #     jump_sound.play()
                    self.playerDino.movement[1] = -1*self.playerDino.jumpSpeed
                    # self.t_reward -= 36
                while True:
                    self.play()
                    if self.action_complete :
                        self.action_complete = False
                        break

            if action == 2:      ## event.key == pygame.K_DOWN
                if not (self.playerDino.isJumping and self.playerDino.isDead):
                    self.playerDino.isDucking = True

                self.play()

            if action == 3:
                self.playerDino.isDucking = False
                self.play()

            if action == 4:
                self.close()
                return 0, 0, True
            else:
                self.play()

        self.t_reward += 1

        if self.gameOver:

            self.t_reward -= 101

        return self.new_states, self.t_reward, self.gameOver

        # self.close()

    def close(self):
        pygame.quit()
        quit()



if __name__=='__main__':
    x = env()
    states = x.reset()
    print(states)
    i = 0
    # while True:
    x.play()
    while True:
        action = int(input('esxa: '))

        S_ , R,  D = x.step(action)
        if(action == 4):
            break
        print(states, S_, R, D)
        states = S_

        if D:
            states = x.reset()
            x.play()
