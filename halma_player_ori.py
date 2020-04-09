# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 08:04:48 2020

@author: Mursito
"""

import random
from halma_model import HalmaModel
import _pickle as cPickle
import time

class HalmaState:
    def __init__(self, node, tujuan, asal, aksi ):
        self.asal = asal
        self.tujuan = tujuan
        self.aksi = aksi
        self.node = self.deepcopy(node)
        self.cabangList = []
        self.prevMove = []
        self.score = None

    def addPrev(self, prev):
        if type(prev) == list:
            self.prevMove += prev
        else:
            self.prevMove.append(prev)

    def getPrev(self):
        return self.prevMove

    def deepcopy(self, model):
        return cPickle.loads(cPickle.dumps(model, -1))

    def addCabang(self, cabang):
        self.cabangList.append(cabang)

    def getCabang(self):
        return self.cabangList

    def getFrom(self):
        return self.asal

    def getTo(self):
        return self.tujuan

    def getNode(self):
        return self.node

    def setScore(self,score):
        self.score = score

    def getScore(self):
        return self.score

    def getReturn(self):
        if self.aksi == self.node.A_GESER:
            return ([self.tujuan], self.asal, self.aksi)
        else:
            return (self.tujuan, self.asal, self.aksi)


class HalmaPlayer:
    nama = "Pemain"
    deskripsi = "Random Strategy"
    nomor = 1
    index = 0
    papan = []

    def __init__(self, nama):
        self.nama = nama
        self._ply = 3
        self._childMax = 30

    def setNomor(self, nomor):
        self.nomor = nomor
        self.index = nomor-1

    # mengembalikan semua kemungkikan main (geser / loncat) bidak di (x1, y1)
    def bisaMain(self, model, papan, ip, x1, y1):
        geser = []
        loncat = []
        dTujuan = model.dalamTujuan(ip, x1, y1)
        for a in model.ARAH:
            x2 = x1 + a[0]
            y2 = y1 + a[1]
            #print((x2, y2), end="")
            if model.dalamPapan(x2, y2):
                if (papan[x2][y2] == 0):
                    if not dTujuan or model.dalamTujuan(ip, x2, y2):
                        geser.append((x2,y2))
                else:
                    x3 = x2 + a[0]
                    y3 = y2 + a[1]
                    #print((x3, y3), end="")
                    if model.dalamPapan(x3, y3):
                        if (papan[x3][y3] == 0):
                            if not dTujuan or model.dalamTujuan(ip, x3, y3):
                                loncat.append((x3,y3))

        return geser, loncat

    # mensimulasikan next step kalo disi)ilakukan aksi tertentu thd papan
    def nextStep(self, model2, tujuan, asal, aksi, index):

        if model2.getGiliran() != index :
            model2.ganti(0)

        # print("IGLGIGE", giliran-1, model2.getGiliran())
        if (aksi == model2.A_LONCAT):
            # print("ASD",asal, tujuan, aksi)
            for xy in tujuan:
                valid = model2.mainLoncat(asal[0], asal[1], xy[0], xy[1])
                if (valid == model2.S_OK):
                    asal = xy # usulan solusi BUG#1
                    # self._loncat += self._inc
        elif (aksi == model2.A_GESER):
            valid = model2.mainGeser(asal[0], asal[1], tujuan[0], tujuan[1])
            if (valid == model2.S_OK):
                pass
                # self._geser += self._inc
        else:
            pass
            # self._henti += self._inc

        return model2

    # untuk cari cabang suatu node
    def cariCabang(self, state, maxPlayer):
        model = state.getNode()
        papan = model.getPapan()
        index = self.index if maxPlayer else 1-self.index
        # print(index)
        # print("time taken:", time.process_time() - time_start)
        b0 = model.getPosisiBidak(index)
        # print("ASD", b0)
        for b in b0:
            # print(b)
            g, l = self.bisaMain(model, papan, index, b[0], b[1])
            asal = b

            for i in range(len(l)):
                addOK = True
                node = self.deepcopy(model)
                aksi = model.A_LONCAT
                tujuan = l[i] if type(l[i]) != tuple else [l[i]]
                if len(state.getPrev())>0:
                    for prev in state.getPrev():
                        if tujuan == prev.getFrom():
                            addOK = False
                            break
                if addOK:
                    nextNode = self.nextStep(node, tujuan, asal, aksi, index)
                    cabang = HalmaState(nextNode, tujuan, asal, aksi)
                    state.addCabang(cabang)
                    cabang.addPrev(state)
                    cabang.addPrev(state.getPrev())


            for i in range(len(g)):
                addOK = True
                node = self.deepcopy(model)
                aksi = model.A_GESER
                tujuan = g[i]
                if len(state.getPrev())>0:
                    for prev in state.getPrev():
                        if tujuan == prev.getFrom():
                            addOK = False
                            break
                if addOK:
                    nextNode = self.nextStep(node, tujuan, asal, aksi, index)
                    cabang = HalmaState(nextNode, tujuan, asal, aksi)
                    state.addCabang(cabang)
                    cabang.addPrev(state)
                    cabang.addPrev(state.getPrev())

        # for cabang in state.getCabang():
        #     if cabang.aksi == model.A_LONCAT:
        #         self._prev = cabang.getPrev()
        #         buffer = cabang.getTo()
        #         print(cabang.getFrom())
        #         print(cabang.getTo())
        #         a = self.cekJump(cabang, cabang.getFrom(), cabang.getTo()[0], model, papan, index) # cek lompatan lanjutannya ada ape engga
        #         buffer += a
        #         print("A", buffer)
                # kalo ada brti di state ini cabangnya nambah



        return state.getCabang()

    def cekJump(self, cabang, xy0, xy1, model, papan, index):
        _, loncat = self.bisaMain(model, papan, index, xy1[0], xy1[1])

        if len(loncat)>0:
            for xy2 in loncat:
                if xy2 != xy0:
                    print("1",loncat)
                    loncat2 = self.cekJump(cabang, xy1, xy2, model, papan, index)
                    if len(loncat2)>0:
                        for xy3 in loncat2:
                            if xy3 != xy1:
                                print("2",loncat2)
                                loncat.append(xy3)

        time.sleep(1)
        return loncat


    def evalFunc(self, state, maxPlayer):
        return random.randint(0,100)

    def minimax(self, state, depth, alpha, beta, maxPlayer):
        if depth == 0 or state.getNode().akhir():
            return self.evalFunc(state, maxPlayer)

        if maxPlayer:
            maxEval = -9999
            cabang = self.cariCabang(state, True)
            childCount = 0
            for child in cabang:
                if childCount < self._childMax:
                    eval = self.minimax(child, depth-1, alpha, beta, False)
                    child.setScore(eval)
                    maxEval = max(maxEval,eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
                childCount +=1
            return maxEval
        else:
            minEval = 9999
            cabang = self.cariCabang(state, False)
            childCount = 0
            for child in cabang:
                if childCount < self._childMax:
                    eval = self.minimax(child, depth-1, alpha, beta, True)
                    child.setScore(eval)
                    minEval = min(minEval,eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
                childCount +=1
            return minEval



    def deepcopy(self, model):
        return cPickle.loads(cPickle.dumps(model, -1))

    def main(self, model):
        time_start = time.process_time()

        initState = HalmaState(model, None, None, None)
        pilihan = []

        eval = self.minimax(initState, self._ply, -9999, 9999, True)

        for child in initState.getCabang():
            if child.getScore() == eval:
                pilihan.append(child)

        print("time taken:", time.process_time() - time_start)

        if len(pilihan) > 0:
            pilih = random.randint(0,len(pilihan)-1)
            print( pilihan[pilih].getReturn())
            return pilihan[pilih].getReturn()
        else:
            return None, None, model.A_BERHENTI

        # return None, None, model.A_HENTI
