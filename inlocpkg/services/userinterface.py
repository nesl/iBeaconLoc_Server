# --- imports ---
import pygame
import time
import random
import serial
import threading

class UserInterface(threading.Thread):

    def __init__(self, screenW, screenH, bgimg):
        # --- initialize game ---
        pygame.init()
        pygame.display.set_caption('BuildSys 2014: iBeacon Localization Primer')
        pygame.font.init()
        self.mediumfont = pygame.font.Font(pygame.font.get_default_font(),18)
        self.screenW=screenW
        self.screenH=screenH
        self.screen=pygame.display.set_mode((screenW,screenH))

        # --- background ---
        bgimg=pygame.image.load (bgimg).convert()
        self.background=pygame.transform.scale (bgimg,(screenW,screenH))

        # --- misc. variables ---
        self.num_users = 0
        self.sprite_list = []

        # -- game state --
        self.running = True

        # initialize super thread
        super(UserInterface,self).__init__()

    def run(self):
        # --- fire up the game ---
        while self.running:

            # -- check for pygame events --
            for event in pygame.event.get():
                # key press
                if event.type == pygame.KEYDOWN:
                    pass
                    #if event.key == pygame.K_q:

                # check for UI exit
                if event.type == pygame.QUIT:
                    self.running=False
                    break

            self.draw_frame(self.sprite_list)
            self.update_sprites()

        pygame.quit()

    def quit(self):
        self.running = False

    def addUser(self, user, impath):
        self.num_users += 1
        self.sprite_list.append( self.UserSprite(user, impath) )

    def draw_frame(self, alist):

        # draw background
        pygame.draw.rect(self.screen,(0,0,0),self.screen.get_rect())
        self.screen.blit(self.background,(0,0))

        # draw users
        for user in self.sprite_list:
            self.screen.blit(user.image, user.xy)

        # draw user statistics
        # packets per second

        pygame.display.flip()

    def update_sprites(self):
        for sprite in self.sprite_list:
                sprite.update()

    # =============== SPRITE CLASSES ================
    # --- RECTANGLE CLASS FOR COLLISION DETECTION ---
    class Rectangle:
        def __init__(self,x,y,width,height):
            self.left = x
            self.top = y
            self.bottom = y+height
            self.right = x+width

        def isTouching(rect2):
            return not (self.right < rect2.left or self.left > rect2.right or self.bottom < rect2.top or self.top > rect2.bottom)

    # --- GENERIC SPRITE CLASS ---
    class Sprite:
        def __init__(self,image_path):
            self.xy=(0,0)
            self.image=pygame.image.load(image_path)
            self.image=pygame.transform.scale(self.image,(30,30))
            self.width=32
            self.height=32
            self.description='generic'
        def setPosition(self, xy):
            self.xy = xy


    # --- USER SPRITE CLASS ---
    class UserSprite(Sprite):
        def __init__(self,user,img):
            self.user = user
            self.img = img
            self.description = 'User ' + str(user.uid)
            super(UserInterface.UserSprite, self).__init__(img)
            self.image=pygame.transform.scale(self.image, (32, 32))

        def update(self):
            pass



