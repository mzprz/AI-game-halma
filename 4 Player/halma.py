# -*- coding: utf-8 -*-
"""
Program utama, bekerja sebagai controller

@author: Mursito
"""

import pygame
import time

from halma_model import HalmaModel
from halma_view_gui import HalmaViewGui
from halma_player import HalmaPlayer

from halma_player_01_A import HalmaPlayer011
from halma_player_02_A import HalmaPlayer02
from halma_player_03_A import HalmaPlayer03
from halma_player_04_A import HalmaPlayer04

model = HalmaModel()
layar = HalmaViewGui("HALMA")

def halma(p1, p2):
    valid = model.S_OK
    model.awal(p1, p2)
    layar.tampilAwal(model)
    while (valid==model.S_OK):
        pygame.time.delay(100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
                raise SystemExit
        
        model.mainMulai()
        layar.tampilMulai(model)
        g = model.getGiliran()
        p = model.getPemain(g)
        tujuan, asal, aksi = p.main(model)
        selesai = model.getWaktu()
        if (aksi == model.A_LONCAT):
            for xy in tujuan:
                valid = model.mainLoncat(asal[0], asal[1], xy[0], xy[1])
                if (valid == model.S_OK):
                    layar.tampilLoncat(model, asal[0], asal[1], xy[0], xy[1])
                asal = xy
        elif (aksi == model.A_GESER):
            valid = model.mainGeser(asal[0], asal[1], tujuan[0][0], tujuan[0][1])
            if (valid == model.S_OK):
                layar.tampilGeser(model, asal[0], asal[1], tujuan[0][0], tujuan[0][1])        
        else:
            layar.tampilHenti(model)
        if model.akhir():
            break
        valid = model.ganti(selesai)
        if valid:
            layar.tampilGanti(model)
        time.sleep(1)
        
    layar.tampilAkhir(model, valid)
    pygame.time.delay(3000)
    pygame.quit();
        
p1=HalmaPlayer011("REGU-01")
p2=HalmaPlayer02("REGU-02")
p3=HalmaPlayer03("REGU-03")
p4=HalmaPlayer04("REGU-04")

halma(p1, p3)


