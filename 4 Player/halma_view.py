# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 07:23:50 2020

Congklak Board Game

@author: Mursito
"""

from halma_model import HalmaModel
from halma_player import HalmaPlayer

S_AKSI = ["Geser", "Loncat", "Henti"]

class HalmaView:
    indent = ""

    def __init__(self, title):
        print(title)        

    # mulai main 2 pemain
    def tampilAwal(self, model):
        print("Ukuran   :", model.getUkuran())
        print("Bidak    :", model.getJumlahBidak())
        for i in range(model.getJumlahPemain()):
            print("Pemain ",i," : ", model.getPemain(i).nama)
        print()
        print("Bidak \tAksi \tDari \tKe")

    def tampilMulai(self, model):
        # nothing 
       self.indent = "" 

    def tampilGeser(self, model, x1, y1, x2, y2):
        print(model.getBidak(x2,y2),'\t', S_AKSI[model.A_GESER],'\t',(x1,y1),'\t',(x2,y2))

    def tampilLoncat(self, model, x1, y1, x3, y3):
        print(self.indent,model.getBidak(x3,y3),'\t', S_AKSI[model.A_LONCAT],'\t',(x1,y1),'\t',(x3,y3))
        if (self.indent == ""):
            self.indent = " "
        
    def tampilHenti(self, model):
        self.indent = ""
        
    def tampilGanti(self, model):
        self.indent = ""

    def tampilAkhir(self, model, status):
        print("SELESAI")
        p = model.getPemain(model.getGiliran())
        teman = model.getTeman(model.getGiliran())
        p1 = model.getPemain(teman);
        nregu = p.nama + " & " + p1.nama
        if (status == model.S_OK):
            print("Pemenang : ", nregu)            
        elif (status == model.S_ILLEGAL):
            print(nregu, "KALAH karena salah jalan")
        elif (status == model.S_TIMEOUT):
            print(nregu, "KALAH karena kehabisan waktu")
    
