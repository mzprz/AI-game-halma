# -*- coding: utf-8 -*-
"""
Program utama, bekerja sebagai controller

@author: Mursito
"""

import pygame

from halma_model import HalmaModel
from halma_view_gui import HalmaViewGui
from halma_player import HalmaPlayer

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
    layar.tampilAkhir(model, valid)
    pygame.time.delay(3000)
    pygame.quit();
        

p1=HalmaPlayer("Pintar")
p2=HalmaPlayer("Cerdas")

halma(p1, p2)


