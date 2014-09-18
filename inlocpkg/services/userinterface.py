# --- imports ---
import pygame
import time
import random
import serial
import threading

class UserInterface(threading.Thread):

    def __init__(self, screenSize, mapSizeM, bgimg, transmitters):
        # --- initialize game ---
        pygame.init()
        pygame.display.set_caption('BuildSys 2014: iBeacon Localization Primer')
        pygame.font.init()
        self.smallfont = pygame.font.Font(pygame.font.get_default_font(),14)
        self.mediumfont = pygame.font.Font(None,32)
        self.largefont = pygame.font.Font(None, 44)
        self.screenW=screenSize[0]
        self.screenH=screenSize[1]
        self.mapWidthM = mapSizeM[0]
        self.mapHeightM = mapSizeM[1]
        self.transmitters = transmitters
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


        # --- background ---
        bgimg=pygame.image.load(bgimg).convert()
        self.mapWidthPx = round( (1.0 - self.statsFramePerc)*self.screenW )
        self.mapHeightPx = round( (1.0 - self.titleFramePerc)*self.screenH )
        self.background=pygame.transform.scale (bgimg,(self.mapWidthPx,self.mapHeightPx))

        # --- misc. variables ---
        self.num_users = 0
        self.user_list = {}
        self.transmitter_list = {}

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

            self.draw_frame(self.user_list)

        pygame.quit()

    def quit(self):
        self.running = False

    def addUser(self, uid, impath):
        self.num_users += 1
        if uid in self.user_list:
            print("warning: attempted to add existing uid to UI list")
        else:
            self.user_list[uid] = self.UserSprite(uid,impath)

    def addTransmitter(self, major, minor, mxy, impath):
        if (major,minor) in self.transmitter_list:
            print("warning: attempted to add existing transmitter to UI list")
        else:
            pxy = self.userCoordsToPx(mxy)
            self.transmitter_list[(major,minor)] = self.TransmitterSprite(pxy, major, minor, impath)

    def moveUserMeters(self, uid, mxy):
        if uid not in self.user_list:
            print("warning: attempted to move a uid not found in UI user list")
        else:
            self.user_list[uid].setPosition(self.userCoordsToPx(mxy))

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
        title_str = "BuildSys 2014: An iBeacon Localization Primer"
        title = self.largefont.render(title_str, True, (0,0,0))
        self.screen.blit(title, (round(self.screenW/2)-300, 20) )

        # --- draw reception statistics frame ---
        stats_str = "Reception Statistics"
        stats = self.mediumfont.render(stats_str, True, (0,0,0))
        self.screen.blit(stats, (10, self.statsFrameRect[1]) )

        # --- draw beacon statistics frame ---
        stats_str = "Beacon Statistics"
        stats = self.mediumfont.render(stats_str, True, (0,0,0))
        self.screen.blit(stats, (10, self.statsFrameRect[1] + 200) )

        # --- draw map frame ---        
        # draw background
        self.screen.blit(self.background,self.mapFrameRect[0:2])

        # draw transmitters
        for MajMin in self.transmitter_list:
            self.screen.blit(self.transmitter_list[MajMin].image, self.transmitter_list[MajMin].xy)

        # draw users
        for uid in self.user_list:
            self.screen.blit(self.user_list[uid].image, self.user_list[uid].xy)

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


