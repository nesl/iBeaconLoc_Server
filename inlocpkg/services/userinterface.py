# --- imports ---
import pygame
import time
import random
import serial
import threading
from ..constants import parameters
from .estimator import *

class UserInterface(threading.Thread):

    def __init__(self, screenSize, mapSizeM, transmitters, users, bgimg):
        # --- initialize game ---
        pygame.init()
        pygame.display.set_caption('BuildSys 2014: iBeacon Localization Primer')
        pygame.font.init()
        self.smallfont = pygame.font.SysFont("helvetica",24)
        self.mediumfont = pygame.font.SysFont("helvetica",28)
        self.largefont = pygame.font.SysFont("helvetica", 38)
        self.largefont.set_italic(True)
        self.mediumfont.set_bold(True)
        self.screenW=screenSize[0]
        self.screenH=screenSize[1]
        self.mapWidthM = mapSizeM[0]
        self.mapHeightM = mapSizeM[1]
        self.managed_transmitters = transmitters
        self.managed_users = users
        self.screen=pygame.display.set_mode((self.screenW,self.screenH))

        # calculate ui borders, the layout is something like this:
        #
        #        _________________________________
        #       |___________TITLE BAR____________|   (title %)
        #       |          |                     |       of
        #       |          |                     |       |
        #       |          |                     |       |
        #       |          |                     |       |
        #       |  STATS   |         MAP         |       |
        #       |          |                     |       |
        #       |          |                     |       |
        #       |          |                     |       |
        #       |__________|_____________________|       v
        #
        #         (stats %)   of ---------------->

        self.titleFramePerc = 0.15
        self.statsFramePerc = 0.33
        self.titleFrameRect = (0,0,round(self.titleFramePerc*self.screenH), self.screenW)
        self.statsFrameRect = (0, round(self.titleFramePerc*self.screenH),round(self.statsFramePerc*self.screenW),self.screenH)
        self.mapFrameRect = (self.statsFrameRect[2], self.statsFrameRect[1], self.screenW, self.screenH)
        self.frameBgColor = (255,255,255)
        self.fontColor = (0,0,0)
        self.user1Color = (0,0,255)
        self.user2Color = (255,0,0)
        self.fullscreen = False


        # --- background ---
        bgimg=pygame.image.load(bgimg).convert()
        self.mapWidthPx = round( (1.0 - self.statsFramePerc)*self.screenW )
        self.mapHeightPx = round( (1.0 - self.titleFramePerc)*self.screenH )
        self.background=pygame.transform.scale (bgimg,(self.mapWidthPx,self.mapHeightPx))

        # --- misc. variables ---
        self.user_sprite_list = {}
        self.transmitter_sprite_list = {}

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
                    #if event.key == pygame.K_f:

                # check for UI exit
                if event.type == pygame.QUIT:
                    self.running=False
                    break

            self.draw_frame(self.user_sprite_list)

        pygame.quit()

    def quit(self):
        self.running = False

    def addUser(self, uid, impath):
        if uid in self.user_sprite_list:
            print("warning: attempted to add existing uid to UI list")
        else:
            self.user_sprite_list[uid] = self.UserSprite(uid,impath)
            self.user_sprite_list[uid].setPosition(self.userCoordsToPx((0,0)))

    def addTransmitter(self, major, minor, mxy, impath):
        if (major,minor) in self.transmitter_sprite_list:
            print("warning: attempted to add existing transmitter to UI list")
        else:
            pxy = self.userCoordsToPx(mxy)
            self.transmitter_sprite_list[(major,minor)] = self.TransmitterSprite(pxy, major, minor, impath)

    def moveUserMeters(self, uid, mxy):
        if uid not in self.user_sprite_list:
            print("warning: attempted to move a uid not found in UI user list")
        else:
            self.user_sprite_list[uid].setPosition(self.userCoordsToPx(mxy))

    def userCoordsToPx(self, mxy):
        # x between 0 and screenW-1
        dpx = round( max(0, min(self.mapWidthPx*mxy[0]/self.mapWidthM, self.screenW) ))
        # y between 0 and screenH-1
        dpy = round( max(0, min(self.mapHeightPx*mxy[1]/self.mapHeightM, self.screenH) ))
        # account for weird x,y coordinates in ui
        px = self.mapFrameRect[0] + dpx
        py = self.screenH - dpy
        return (px,py)


    def draw_frame(self, alist):

        # draw background
        pygame.draw.rect(self.screen, self.frameBgColor, self.screen.get_rect())

        # --- draw title frame ---
        temp_str = "BuildSys 2014: An iBeacon Localization Primer"
        temp_mod = self.largefont.render(temp_str, True, (0,0,0))
        self.screen.blit(temp_mod, (round(self.screenW/2)-400, 20) )

        # --- draw reception statistics frame ---
        temp_str = "Reception Statistics"
        temp_mod = self.mediumfont.render(temp_str, True, self.fontColor)
        self.screen.blit(temp_mod, (10, self.statsFrameRect[1]) )
        temp_str = "User 1"
        temp_mod = self.smallfont.render(temp_str, True, self.user1Color)
        self.screen.blit(temp_mod, (160, self.statsFrameRect[1] + 40))
        temp_str = "User 2"
        temp_mod = self.smallfont.render(temp_str, True, self.user2Color)
        self.screen.blit(temp_mod, (300, self.statsFrameRect[1] + 40))
        temp_str = "PPS"
        temp_mod = self.smallfont.render(temp_str, True, self.fontColor)
        self.screen.blit(temp_mod, (20, self.statsFrameRect[1] + 70))
        if 1 not in self.managed_users:
            temp_str = "n/a"
        else:
            pps = self.managed_users[1].getPacketsPerSec()
            temp_str = "{:.1f}".format(pps) 
        temp_mod = self.smallfont.render(temp_str, True, self.fontColor)
        self.screen.blit(temp_mod, (180, self.statsFrameRect[1] + 70))
        if 2 not in self.managed_users:
            temp_str = "n/a"
        else:
            pps = self.managed_users[2].getPacketsPerSec()
            temp_str = "{:.1f}".format(pps) 
        temp_mod = self.smallfont.render(temp_str, True, self.fontColor)
        self.screen.blit(temp_mod, (320, self.statsFrameRect[1] + 70))

        # --- draw user preferences frame ---
        temp_str = "User Settings"
        temp_mod = self.mediumfont.render(temp_str, True, self.fontColor)
        self.screen.blit(temp_mod, (10, self.statsFrameRect[1] + 160) )
        temp_str = "User 1"
        temp_mod = self.smallfont.render(temp_str, True, self.user1Color)
        self.screen.blit(temp_mod, (160, self.statsFrameRect[1] + 200))
        temp_str = "User 2"
        temp_mod = self.smallfont.render(temp_str, True, self.user2Color)
        self.screen.blit(temp_mod, (300, self.statsFrameRect[1] + 200))
        temp_str = "Power"
        temp_mod = self.smallfont.render(temp_str, True, self.fontColor)
        self.screen.blit(temp_mod, (20, self.statsFrameRect[1] + 230))
        if 1 not in self.managed_users:
            temp_str = "n/a"
        else:
            power = self.managed_users[1].getPowerFilter()
            temp_str = str(power)
        temp_mod = self.smallfont.render(temp_str, True, self.fontColor)
        self.screen.blit(temp_mod, (180, self.statsFrameRect[1] + 230))
        if 2 not in self.managed_users:
            temp_str = "n/a"
        else:
            power = self.managed_users[2].getPowerFilter()
            temp_str = str(power)
        temp_mod = self.smallfont.render(temp_str, True, self.fontColor)
        self.screen.blit(temp_mod, (320, self.statsFrameRect[1] + 230))

        temp_str = "Rate"
        temp_mod = self.smallfont.render(temp_str, True, self.fontColor)
        self.screen.blit(temp_mod, (20, self.statsFrameRect[1] + 260))
        if 1 not in self.managed_users:
            temp_str = "n/a"
        else:
            rate = self.managed_users[1].getRateThrottle()
            temp_str = str(rate)
        temp_mod = self.smallfont.render(temp_str, True, self.fontColor)
        self.screen.blit(temp_mod, (180, self.statsFrameRect[1] + 260))
        if 2 not in self.managed_users:
            temp_str = "n/a"
        else:
            rate = self.managed_users[2].getRateThrottle()
            temp_str = str(rate)
        temp_mod = self.smallfont.render(temp_str, True, self.fontColor)
        self.screen.blit(temp_mod, (320, self.statsFrameRect[1] + 260))

        # --- draw power consumption frame ---
        temp_str = "Est. Power Consumption"
        temp_mod = self.mediumfont.render(temp_str, True, self.fontColor)
        self.screen.blit(temp_mod, (10, self.statsFrameRect[1] + 340) )
        temp_str = "User 1"
        temp_mod = self.smallfont.render(temp_str, True, self.user1Color)
        self.screen.blit(temp_mod, (160, self.statsFrameRect[1] + 380))
        temp_str = "User 2"
        temp_mod = self.smallfont.render(temp_str, True, self.user2Color)
        self.screen.blit(temp_mod, (300, self.statsFrameRect[1] + 380))
        temp_str = "Pow. (mW)"
        temp_mod = self.smallfont.render(temp_str, True, self.fontColor)
        self.screen.blit(temp_mod, (20, self.statsFrameRect[1] + 410))
        if 1 not in self.managed_users:
            temp_str = "n/a"
        else:
            power1 = estimatePowerConsumption(self.managed_users[1].getPowerFilter(), \
                                          self.managed_users[1].getRateThrottle() )
            power1_ma = round(1000*power1, 2)
            temp_str = str(power1_ma)
        temp_mod = self.smallfont.render(temp_str, True, self.fontColor)
        self.screen.blit(temp_mod, (180, self.statsFrameRect[1] + 410))
        if 2 not in self.managed_users:
            temp_str = "n/a"
        else:
            power2 = estimatePowerConsumption(self.managed_users[2].getPowerFilter(), \
                                          self.managed_users[2].getRateThrottle() )
            power2_ma = round(1000*power2,2)
            temp_str = str(power2_ma)
        temp_mod = self.smallfont.render(temp_str, True, self.fontColor)
        self.screen.blit(temp_mod, (320, self.statsFrameRect[1] + 410))

        temp_str = "Life (yrs)"
        temp_mod = self.smallfont.render(temp_str, True, self.fontColor)
        self.screen.blit(temp_mod, (20, self.statsFrameRect[1] + 440))
        if 1 not in self.managed_users:
            temp_str = "n/a"
        else:
            life = estimateLifetimeYears(parameters.BATTERYCAP_2AA, power1)
            life = round(life,2)
            temp_str = str(life)
        temp_mod = self.smallfont.render(temp_str, True, self.fontColor)
        self.screen.blit(temp_mod, (180, self.statsFrameRect[1] + 440))
        if 2 not in self.managed_users:
            temp_str = "n/a"
        else:
            life = estimateLifetimeYears(parameters.BATTERYCAP_2AA, power2)
            life = round(life,2)
            temp_str = str(life)
        temp_mod = self.smallfont.render(temp_str, True, self.fontColor)
        self.screen.blit(temp_mod, (320, self.statsFrameRect[1] + 440))


        #life_est = estimateLifetimeMonths( BATTERYCAP_2AA, pow_est)


        # --- draw map frame ---        
        # draw background
        self.screen.blit(self.background,self.mapFrameRect[0:2])

        # draw transmitters
        for MajMin in self.transmitter_sprite_list:
            xy = self.transmitter_sprite_list[MajMin].xy
            self.screen.blit(self.transmitter_sprite_list[MajMin].image, xy)
            minor_str = str(self.transmitter_sprite_list[MajMin].minor)
            minor = self.smallfont.render(minor_str, True, self.fontColor)
            self.screen.blit(minor, (xy[0]-20, xy[1]))

        # draw users
        for uid in self.user_sprite_list:
            self.screen.blit(self.user_sprite_list[uid].image, self.user_sprite_list[uid].xy)

        # draw user statistics
        # packets per second

        pygame.display.flip()

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
        def setPosition(self, xy):
            self.xy = xy


    # --- USER SPRITE ---
    class UserSprite(Sprite):
        def __init__(self,uid,img):
            self.img = img
            self.uid = uid
            super(UserInterface.UserSprite, self).__init__(img)
            self.image=pygame.transform.scale(self.image, (32, 32))

        def update(self):
            pass

    # --- TRANSMITTER SPRITE ---
    class TransmitterSprite(Sprite):
        def __init__(self, xy, major, minor, img):
            super(UserInterface.TransmitterSprite, self).__init__(img)      
            self.img = img
            self.major = major
            self.minor = minor
            self.image=pygame.transform.scale(self.image, (24, 24))
            self.xy = xy

        def update(self):
            pass


