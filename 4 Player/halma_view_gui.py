# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 07:23:50 2020

@author: Mursito
@author: Toro

"""

import pygame
import time

from halma_model import HalmaModel
from halma_player import HalmaPlayer
from halma_view import HalmaView

### ----- VARIABLE DECLARATION ----- ###
# Set the color variable
black = (0, 0, 0)
white = (255, 255, 255)
grey = (192, 192, 192)
dark_grey = (48, 48, 48)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
yellow = (255, 255, 0)

pcolors=[red, blue, green, yellow]

class HalmaViewGui(HalmaView):

    # Constructor
    def __init__(self, title):
        super().__init__(title)

        self.positions = {}
        self.thePiece = 0
        self.gameStatus = False
        self.giliran = 1
        self.nkotak = 10
        self.linewidth = 40/self.nkotak #if(self.nkotak == 10) else 2.5 if(self.nkotak == 16) else 0

        ### ----- INITILIAZE pygame ----- ###
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 680))
        pygame.display.set_caption(title)

        # UI Variables
        ### ----- CREATE GAME OBJECTS ----- ###
        # Create board with gridlines
        self.board = pygame.Surface((616, 616))
        self.board.fill(dark_grey)
        for i in range(1, self.nkotak):
            pygame.draw.rect(self.board, grey, (0, i*(580/self.nkotak) + (i-1)*self.linewidth, 616, self.linewidth)) # (surface, color, (posisi x, posisi y, lebar, tinggi))
            pygame.draw.rect(self.board, grey, (i*(580/self.nkotak) + (i-1)*self.linewidth, 0, self.linewidth, 616))

        # CREATE PIECES
        ## Create First Player Pieces (Red)
        self.pieces=[]
        for i in range(4):
            s = pygame.Surface(((580/self.nkotak), (580/self.nkotak)))
            s.fill(dark_grey)
            pygame.draw.circle(s, pcolors[i], (int(580/self.nkotak/2), int(580/self.nkotak/2)), int(580/self.nkotak/2 - 3))
            self.pieces.append(s)

        # CREATE PLAYER INFORMATION
        self.playerInformation = pygame.Surface((400, 576))
        self.playerInformation.fill(white)
        ## Create font objects
        self.font = pygame.font.Font('freesansbold.ttf', 32) # (font file, size)
        self.fontSmall = pygame.font.Font('freesansbold.ttf', 16)
        ## Create text suface objects,
        self.tPlayerTurn = self.font.render('PLAYER ' + str(self.giliran) + ' TURN', True, blue, green)
        self.tPlayer1 = self.fontSmall.render('PLAYER1', True, green, blue) #(the text, True, text colour, background color)
        self.tPlayer1Name = self.font.render('AMBIS', True, green, blue)
        self.tPlayer1Points = self.fontSmall.render('PLAYER1POINTS' + '/15', True, green, blue)
        self.tPlayer2 = self.fontSmall.render('PLAYER2', True, green, blue)
        self.tPlayer2Name = self.font.render('GENIUS', True, green, blue)
        self.tPlayer2Points = self.fontSmall.render('PLAYER2POINTS' + '/15', True, green, blue)
        #-----#
        self.bStart = self.font.render('START', True, green, blue)
        self.bExit = self.font.render('EXIT', True, green, blue)
        ## Create rectangular border for the objects
        self.tPlayerTurnR = self.tPlayerTurn.get_rect()
        self.tPlayer1R = self.tPlayer1.get_rect()
        self.tPlayer1NameR = self.tPlayer1Name.get_rect()
        self.tPlayer1PointsR = self.tPlayer1Points.get_rect()
        self.tPlayer2R = self.tPlayer2.get_rect()
        self.tPlayer2NameR = self.tPlayer2Name.get_rect()
        self.tPlayer2PointsR = self.tPlayer2Points.get_rect()
        #-----#
        self.bStartR = self.bStart.get_rect()
        self.bExitR = self.bExit.get_rect()
        ## Set the center of the rectangular object.
        self.tPlayerTurnR.center = (640, 30)
        self.tPlayer1R = (800, 80)
        self.tPlayer1NameR.center = (1000, 112 + 16)
        self.tPlayer1PointsR = (800, 144)
        self.tPlayer2R = (800, 176)
        self.tPlayer2NameR.center = (1000, 208 + 16)
        self.tPlayer2PointsR = (800, 240)
        #-----#
        self.bStartR = (800, 540)
        self.bExitR = (1000, 540)


    def gambarPapan(self):
        self.screen.blit(self.board, (105, 60))

    def gambarBidak(self, model):
        nkotak = model.getUkuran()
        for x in range(nkotak):
            for y in range(nkotak):
                bxy = model.getBidak(x,y)
                if (bxy > 0):
                    p = (bxy // 100) - 1
                    self.screen.blit(self.pieces[p], (105 + x*((580/self.nkotak)+self.linewidth), 60 + y*((580/self.nkotak)+self.linewidth)))

    # mulai main 2 pemain
    def tampilAwal(self, model):
        super().tampilAwal(model)
        # RENDER THE GAME
        # Clear the screen
        self.screen.fill(black)

        self.gambarPapan()
        self.gambarBidak(model)

        # Render Player Information
        self.screen.blit(self.playerInformation, (800, 80))
        # Render the text
        self.screen.blit(self.tPlayerTurn, self.tPlayerTurnR)
        self.screen.blit(self.tPlayer1, self.tPlayer1R)
        self.screen.blit(self.tPlayer1Name, self.tPlayer1NameR)
        self.screen.blit(self.tPlayer1Points, self.tPlayer1PointsR)
        self.screen.blit(self.tPlayer2, self.tPlayer2R)
        self.screen.blit(self.tPlayer2Name, self.tPlayer2NameR)
        self.screen.blit(self.tPlayer2Points, self.tPlayer2PointsR)
        self.screen.blit(self.bStart, self.bStartR)
        self.screen.blit(self.bExit, self.bExitR)
        pygame.display.update()

    # tampilkan pemain yang aktif
    def tampilMulai(self, model):
        super().tampilMulai(model)

    # tampilkan geser
    def tampilGeser(self, model, x1, y1, x2, y2):
        super().tampilGeser(model, x1, y1, x2, y2)
        self.gambarPapan()
        self.gambarBidak(model)
        pygame.display.update()

    # tampilkan loncat
    def tampilLoncat(self, model, x1, y1, x3, y3):
        super().tampilLoncat(model, x1, y1, x3, y3)
        self.gambarPapan()
        self.gambarBidak(model)
        pygame.display.update()

    # tampilkan pemain selesai aktif
    # dan sisa waktu
    def tampilHenti(self, model):
        super().tampilHenti(model)

    # tampilkan pergantian pemain
    def tampilGanti(self, model):
        super().tampilGanti(model)

    # tampilkan game selesai
    def tampilAkhir(self, model, status):
        super().tampilAkhir(model, status)
