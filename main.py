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

pygame.mixer.pre_init(44100, -16, 2, 2048) # fix audio delay
pygame.init()

scr_size = (width,height) = (600,150)
FPS = 60

# background_col = (235,235,235)
background_col = (255,255,255)

high_score = 0

screen = pygame.display.set_mode(scr_size)
clock = pygame.time.Clock()
pygame.display.set_caption("T-Rex Rush")

def load_sprite_sheet(
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

def introscreen():
    temp_dino = Dino(44,47)
    temp_dino.isBlinking = False
    gameStart = True

    # callout,callout_rect = load_image('call_out.png',196,45,-1)
    # callout_rect.left = width*0.05
    # callout_rect.top = height*0.4

    temp_ground,temp_ground_rect = load_sprite_sheet('ground.png',15,1,-1,-1,-1)
    temp_ground_rect.left = width/20
    temp_ground_rect.bottom = height

    # logo,logo_rect = load_image('/home/sans/Music/Chrome-T-Rex-Rush/sprites_copy/logo.png',240,40,-1)
    # logo_rect.centerx = width*0.6
    # logo_rect.centery = height*0.6
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

        clock.tick(FPS)
        if temp_dino.isJumping == False and temp_dino.isBlinking == False:
            gameStart = True

discrete_spaces = np.linspace(76, 640, num=100)
print(discrete_spaces)

class env:
    def __init__(self):
        self.crow_height = 0.0
        self.i = 0
        self.high_score = 0
        self.nearest = 800

        self.discrete_spaces = np.linspace(76, 640, num=100)

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
        self.HI_rect.top = height*0.1
        self.HI_rect.left = width*0.73

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

        self.cacti = pygame.sprite.Group()
        self.crows = pygame.sprite.Group()
        self.last_obstacle = pygame.sprite.Group()

        Cactus.containers = self.cacti
        Crow.containers = self.crows

        self.old_states.append(self.new_ground.speed)
        self.old_states.append(np.digitize(self.nearest, self.discrete_spaces))
        self.old_states.append(self.crow_height)
        self.old_states.append("Jump" if self.playerDino.rect[1] != 100 else "running")
        self.old_states.append("Crouch" if self.playerDino.rect[2] != 44 else " standing")

        return self.old_states

    def step(self, action): ## 0 - stay, 1 - jump, 2 - crouch, 3 - standup
        # while not self.gameQuit:
        #     while not self.gameOver:
        if pygame.display.get_surface() == None:
            print("Couldn't load display surface")
            self.gameQuit = True
            self.gameOver = True
        else:
            if action == 1: ## event.key == pygame.K_SPACE
                if self.playerDino.rect.bottom == int(0.98*self.height):
                    self.playerDino.isJumping = True
                    # if pygame.mixer.get_init() != None:
                    #     jump_sound.play()
                    self.playerDino.movement[1] = -1*self.playerDino.jumpSpeed

            if action == 2:      ## event.key == pygame.K_DOWN
                if not (self.playerDino.isJumping and self.playerDino.isDead):
                    self.playerDino.isDucking = True

            if action == 3:
                self.playerDino.isDucking = False

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

        self.old_states = []
        try:
            # nearest = min(all_loc)
            self.old_states.append(self.new_ground.speed)
            self.old_states.append(np.digitize(self.nearest, self.discrete_spaces))
            self.old_states.append(self.crow_height)
            self.old_states.append("Jump" if self.playerDino.rect[1] != 100 else "running")
            self.old_states.append("Crouch" if self.playerDino.rect[2] != 44 else " standing")
            # print('ground: {} nearest position {} '.format(new_ground.speed, np.digitize(nearest,discrete_spaces)), nearest)
        except Exception as e:
            pass
            # print('ground: {} nearest position {} '.format(new_ground.speed, 0))

        if((0 < (100 - self.playerDino.rect[1]) <= 10) and self.i == 1):
            print("old_ states: ", self.old_states, self.playerDino.rect)
        if(self.playerDino.rect[1] == 100 and(self.playerDino.rect[2] == 44 or self.playerDino.rect[2] == 59)):
            print('old states: ', self.old_states)

        self.playerDino.update()
        self.cacti.update()
        self.crows.update()
        # clouds.update()
        self.new_ground.update()
        self.scb.update(self.playerDino.score)
        # print('Reward: ', 1)
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
        except:
            self.crow_height = 0.0

        self.new_states = []
        try:
            self.nearest = min(all_loc)
            self.new_states.append(self.new_ground.speed)
            self.new_states.append(np.digitize(self.nearest, self.discrete_spaces))
            self.new_states.append(self.crow_height)
            self.new_states.append("Jump" if self.playerDino.rect[1] != 100 else "running")
            self.new_states.append("Crouch" if self.playerDino.rect[2] != 44 else " standing")
            # states.append(playerDino.movement[1])
            # print('ground: {} nearest position {} '.format(new_ground.speed, np.digitize(nearest,discrete_spaces)), nearest, playerDino.rect[2])
        except:
            pass
            # print('ground: {} nearest position {} '.format(new_ground.speed, 0))
        if((0 < (100 - self.playerDino.rect[1]) <= 10) and self.i == 0):
            print("new states: ", self.new_states)
        if(self.playerDino.rect[1] == 100 and (self.playerDino.rect[2] == 44 or self.playerDino.rect[2] == 59)):
            self.i = 0
            print("new states: ", self.new_states)
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
        clock.tick(self.FPS)

        if self.playerDino.isDead:
            print('Reward: -100')
            print("<<<<<<GAME OVER>>>>>>>")
            self.playerDino.isDead = True
            self.gameOver = False
            self.reset()

        if self.counter%700 == 699:
            self.new_ground.speed -= 1
            self.gamespeed += 1

        self.counter = (self.counter + 1)

        # self.close()

    def close(self):
        pygame.quit()
        quit()

crow_height = 0.0
i = 0

def gameplay():
    global high_score, crow_height, i
    gamespeed = 4
    startMenu = False
    gameOver = False
    gameQuit = False
    playerDino = Dino(44,47)
    new_ground = Ground(-1*gamespeed)
    scb = Scoreboard()
    highsc = Scoreboard(width*0.78)
    counter = 0

    cacti = pygame.sprite.Group()
    crows = pygame.sprite.Group()
    last_obstacle = pygame.sprite.Group()

    Cactus.containers = cacti
    Crow.containers = crows

    temp_images,temp_rect = load_sprite_sheet('numbers.png',12,1,11,int(11*6/5),-1)
    HI_image = pygame.Surface((22,int(11*6/5)))
    HI_rect = HI_image.get_rect()
    HI_image.fill(background_col)
    HI_image.blit(temp_images[10],temp_rect)
    temp_rect.left += temp_rect.width
    HI_image.blit(temp_images[11],temp_rect)
    HI_rect.top = height*0.1
    HI_rect.left = width*0.73

    nearest = 800
    while not gameQuit:
        while not gameOver:
            if pygame.display.get_surface() == None:
                print("Couldn't load display surface")
                gameQuit = True
                gameOver = True
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameQuit = True
                        gameOver = True

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            if playerDino.rect.bottom == int(0.98*height):
                                playerDino.isJumping = True
                                # if pygame.mixer.get_init() != None:
                                #     jump_sound.play()
                                playerDino.movement[1] = -1*playerDino.jumpSpeed

                        if event.key == pygame.K_DOWN:
                            if not (playerDino.isJumping and playerDino.isDead):
                                playerDino.isDucking = True

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_UP:
                            playerDino.isDucking = False
            for c in cacti:
                c.movement[0] = -1*gamespeed
                if pygame.sprite.collide_mask(playerDino,c):
                    playerDino.isDead = True

            for p in crows:
                p.movement[0] = -1*gamespeed
                if pygame.sprite.collide_mask(playerDino,p):
                    playerDino.isDead = True

            if len(cacti) < 2:
                if len(cacti) == 0:
                    last_obstacle.empty()
                    last_obstacle.add(Cactus(gamespeed,40,40))
                else:
                    for l in last_obstacle:
                        if l.rect.right < width*0.7 and random.randrange(0,50) == 10:
                            last_obstacle.empty()
                            last_obstacle.add(Cactus(gamespeed, 40, 40))

            if len(crows) == 0 and random.randrange(0,200) == 10 and counter > 500:
                for l in last_obstacle:
                    if l.rect.right < width*0.8:
                        last_obstacle.empty()
                        last_obstacle.add(Crow(gamespeed, 46, 40))

            old_states = []
            try:
                # nearest = min(all_loc)
                old_states.append(new_ground.speed)
                old_states.append(np.digitize(nearest, discrete_spaces))
                old_states.append(crow_height)
                old_states.append("Jump" if playerDino.rect[1] != 100 else "running")
                old_states.append("Crouch" if playerDino.rect[2] != 44 else " standing")
                # print('ground: {} nearest position {} '.format(new_ground.speed, np.digitize(nearest,discrete_spaces)), nearest)
            except Exception as e:
                pass
                # print('ground: {} nearest position {} '.format(new_ground.speed, 0))

            if((0 < (100 - playerDino.rect[1]) <= 10) and i == 1):
                print("old_ states: ", old_states, playerDino.rect)
            if(playerDino.rect[1] == 100 and(playerDino.rect[2] == 44 or playerDino.rect[2] == 59)):
                print('old states: ', old_states)

            playerDino.update()
            cacti.update()
            crows.update()
            # clouds.update()
            new_ground.update()
            scb.update(playerDino.score)
            # print('Reward: ', 1)
            all_loc = []
            for c in cacti:
                if(c.rect.left < 72):
                    all_loc.append(1000)
                else:
                    all_loc.append(c.rect.left)

            h = []
            for p in crows:
                if(p.rect.left < 72):
                    all_loc.append(1000)
                else:
                    all_loc.append(p.rect.left)
                    h.append(p.rect.centery)

            try:
                crow_height = min(h)
            except:
                crow_height = 0.0

            states = []
            try:
                nearest = min(all_loc)
                states.append(new_ground.speed)
                states.append(np.digitize(nearest, discrete_spaces))
                states.append("Jump" if playerDino.rect[1] != 100 else "running")
                states.append("Crouch" if playerDino.rect[2] != 44 else " standing")
                # states.append(playerDino.movement[1])
                # print('ground: {} nearest position {} '.format(new_ground.speed, np.digitize(nearest,discrete_spaces)), nearest, playerDino.rect[2])
            except:
                pass
                # print('ground: {} nearest position {} '.format(new_ground.speed, 0))
            if((0 < (100 - playerDino.rect[1]) <= 10) and i == 0):
                print("new states: ", states)
            if(playerDino.rect[1] == 100 and (playerDino.rect[2] == 44 or playerDino.rect[2] == 59)):
                i = 0
                print("new states: ", states)
            if(playerDino.rect[1] != 100):
                i += 1
            # print('Pos: ',playerDino.rect[1], playerDino.rect[2]) ## changes rect[1] - when jumping, rect[2] - when crouch
            highsc.update(high_score)

            if pygame.display.get_surface() != None:
                screen.fill(background_col)
                new_ground.draw()
                # clouds.draw(screen)
                scb.draw()
                if high_score != 0:
                    highsc.draw()
                    screen.blit(HI_image,HI_rect)
                cacti.draw(screen)
                crows.draw(screen)
                playerDino.draw()

                pygame.display.update()
            clock.tick(FPS)

            if playerDino.isDead:
                print('Reward: -100')
                print("<<<<<<GAME OVER>>>>>>>")
                playerDino.isDead = True
                gameOver = False
                gameplay()

            if counter%700 == 699:
                new_ground.speed -= 1
                gamespeed += 1

            counter = (counter + 1)

            # action = input('next action')
        if gameQuit:
            break

    pygame.quit()
    quit()

def main():
    x = env()
    states = x.reset()
    print(states)
    while True:
        act = int(input('action: '))
        x.step(act)
    # isGameQuit = introscreen()
    # if not isGameQuit:
    #     gameplay()

main()
