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

class DinoGameEnv:
    def __init__(self):
        self.crow_height = 0.0
        self.i = 0
        self.high_score = 0
        self.nearest = 800
        self.second_nearest = 1000
        self.t_reward = 0

        self.discrete_spaces = np.linspace(0, 640, num=100)

        self.action_complete = True

        self.old_states = []
        self.new_states = []

        self.allow_rendering = False

        pygame.mixer.pre_init(44100, -16, 2, 2048) # fix audio delay
        pygame.init()

        self.scr_size = (self.width,self.height) = (600,150)
        self.FPS = 60

        # background_col = (235,235,235)
        self.background_col = (255,255,255)

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.scr_size)
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

    def render(self):
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
        self.second_nearest = 1000
        self.action_complete = True

        self.cacti = pygame.sprite.Group()
        self.crows = pygame.sprite.Group()
        self.last_obstacle = pygame.sprite.Group()

        Cactus.containers = self.cacti
        Crow.containers = self.crows

        self.old_states = []
        self.new_states = []

        self.old_states.append(self.new_ground.speed/-self.gamespeed)
        self.old_states.append(np.digitize(self.nearest, self.discrete_spaces))
        self.old_states.append(np.digitize(self.second_nearest, self.discrete_spaces))
        self.old_states.append(self.crow_height)
        # self.old_states.append("Crouch" if self.playerDino.rect[2] != 44 else " standing")
        self.old_states.append(0 if self.playerDino.rect[2] != 44 else 1)

        self.play()

        return np.array(self.old_states, dtype=np.float64)

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

        if len(self.crows) == 0 and random.randrange(0,200) == 10 and self.counter > 1:
            for l in self.last_obstacle:
                if l.rect.right < self.width*0.8:
                    self.last_obstacle.empty()
                    self.last_obstacle.add(Crow(self.gamespeed, 46, 40))

        self.playerDino.update()
        self.cacti.update()
        self.crows.update()
        self.new_ground.update()
        self.scb.update(self.playerDino.score)

        all_loc = []
        for c in self.cacti:
            # print(self.playerDino.rect.width, c.rect.width)
            all_loc.append(c.rect.left)
            # if(c.rect.left < 72):
            #     all_loc.append(1000)
            # else:
            #     all_loc.append(c.rect.left)

        h = []
        for p in self.crows:
            all_loc.append(p.rect.left)
            # print(p.rect.width)
            # if(p.rect.left < 72):
            #     all_loc.append(1000)
            # else:
            #     all_loc.append(p.rect.left)
            #     h.append(p.rect.centery)

        print(self.playerDino.rect.right, all_loc, self.new_ground.rect.right, self.new_ground.rect.left)

        try:
            self.crow_height = min(h)
            self.nearest = min(all_loc)
        except:
            self.crow_height = 0.0
            if len(all_loc) == 0:
                self.nearest = 800
            else:
                self.nearest = min(all_loc)

        self.new_states = []

        self.new_states.append(self.new_ground.speed/-self.gamespeed)
        self.new_states.append(np.digitize(self.nearest, self.discrete_spaces))
        if(len(all_loc) > 1):
            all_loc.remove(self.nearest)
            self.second_nearest = min(all_loc)
            self.new_states.append(np.digitize(self.second_nearest, self.discrete_spaces) - np.digitize(self.nearest, self.discrete_spaces))
        else:
            self.second_nearest = 1000
            self.new_states.append(np.digitize(self.second_nearest, self.discrete_spaces))
        self.new_states.append(self.crow_height)
        # self.new_states.append("Jump" if self.playerDino.rect[1] != 100 else "running")
        # self.new_states.append("Crouch" if self.playerDino.rect[2] != 44 else " standing")
        self.new_states.append(0 if self.playerDino.rect[2] != 44 else 1)

        # if((0 < (100 - self.playerDino.rect[1]) <= 10) and self.i == 0):
        #     self.t_reward += 1
        #     self.new_states.append(self.t_reward)
        #     print("new__ states: ", self.new_states)
        if(self.playerDino.rect[1] == 100 and (self.playerDino.rect[2] == 44 or self.playerDino.rect[2] == 59)):
            self.i = 0
            self.action_complete = True

        if(self.playerDino.rect[1] != 100):
            self.i += 1

        self.highsc.update(self.high_score)

        if self.allow_rendering:
            self.render()

        self.clock.tick(self.FPS)

        if self.playerDino.isDead:
            # print('Reward: -1000')

            # print("final_ states: ", self.new_states)
            # print("<<<<<<GAME OVER>>>>>>>")
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
        if True:
            if action == 0: ## event.key == pygame.K_SPACE
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

            if action == 1:      ## event.key == pygame.K_DOWN
                if not (self.playerDino.isJumping and self.playerDino.isDead):
                    self.playerDino.isDucking = True

                self.play()

            if action == 2:
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

        return np.array(self.new_states, dtype=np.float64), self.t_reward, self.gameOver

        # self.close()

    def close(self):
        pygame.display.quit()
        pygame.quit()
        quit()


if __name__=='__main__':

    ## SAMPLE RUN OF THE ENV
    x = DinoGameEnv()
    states = x.reset()
    print(states)

    x.allow_rendering = True

    while True:
        # action = np.random.choice(np.arange(0,4))
        action = int(input('input action: '))

        S_ , R,  D = x.step(action)

        if(action == 4):
            x.close()
            break

        print(states, S_, R, D)

        if D:
            states = x.reset()
            # x.play()
        else:
            states = S_
