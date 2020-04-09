import time
import copy
import sys
import _pickle as cPickle
import random
import gc

# tambahin kode untuk opsi berhenti masukin ply satu lur (tujuan = asal), biar ikut dicek eval Funct nya
class HalmaPlayer02:
    nama = "Pemain"
    deskripsi = "Kelompok 2"
    nomor = 1
    index = 0
    papan = []

    def __init__(self, nama):
        self.nama = nama
        self._ply = 3
        self.pilihan = []
        self._childMax = 25

    def setNomor(self, nomor):
        self.nomor = nomor
        self.index = nomor-1

    # mengembalikan semua kemungkikan main (geser / loncat) bidak di (x1, y1)
    def bisaMain(self, model, papan, ip, x1, y1):
        geser = []
        loncat = {}
        # loncat_buffer = []
        baris = 0
        kolom = 0

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
                                try:
                                    loncat[baris].update( { kolom: {"xy": (x3,y3) } })
                                except:
                                    loncat[baris] = { kolom: { "xy": (x3,y3) } }
                                kolom += 1
        # print("THISDONE")
        loncat = self.loncatanPlus(model, papan, loncat, ip)
        # print("THISDONE")
        # done getting the dictionary i wanted, now i need to sort it
        # to match the format specified

        loncat2 = self.sortLoncat(loncat)

        # print(x1, y1)
        # print(loncat2)
        # print("--------")
        # time.sleep(1)

        # loncat2 =
        # print("GESER", geser)
        # print("LONCAT", loncat2)

        return geser, loncat2

    def loncatanPlus(self, model, papan, loncat, ip):
        loncat_buffer = []
        baris = 1
        stopCheck = False
        memory = (0,0)

        baris = 0
        while stopCheck == False:
            try:
                kolom = 0
                for i in range(len(loncat[baris])): #untuk semua elemen dalam satu baris
                    x1 = loncat[baris][i]["xy"][0]
                    y1 = loncat[baris][i]["xy"][1]
                    dTujuan = model.dalamTujuan(ip, x1, y1)
                    for a in model.ARAH:
                        x2 = x1 + a[0]
                        y2 = y1 + a[1]
                        #print((x2, y2), end="")
                        if model.dalamPapan(x2, y2):
                            # print("xy", x2, y2, papan[x2][y2])
                            if (papan[x2][y2] == 0):
                                pass
                            else:
                                x3 = x2 + a[0]
                                y3 = y2 + a[1]
                                # print("xy3", x3, y3, papan[x3][y3])
                                if model.dalamPapan(x3, y3) and (x3,y3) not in memory:
                                    if (papan[x3][y3] == 0):
                                        if not dTujuan or model.dalamTujuan(ip, x3, y3):
                                            # print("BLAST")
                                            try:
                                                # print("BLAST2")
                                                loncat[baris+1].update( { kolom: {"xy": (x3,y3), "parent":(x1,y1) } })
                                            except:
                                                # print("BLAST3")
                                                loncat[baris+1] = { kolom: { "xy": (x3,y3), "parent":(x1,y1) } }
                                            # print(baris, kolom)
                                            kolom +=1
                                            # gc.disable()
                                            memory.append((x1,y1))
                baris += 1
            except:
                # print(sys.exc_info())
                stopCheck = True

        return loncat

    def sortLoncat(self, loncat):

        # sort dari frontier ujung ke parent ujung

        buffer = []
        loncat2 = []
        no = 0
        baris = len(loncat)-1 if len(loncat) > 0 else None #baris terakhir
        # print(loncat)
        if baris != None:
            # print(loncat[baris])
            for kolom in range(len(loncat[baris])): #untuk semua kolom dalam baris terakhir
                if baris > 0:
                    # print("BLAST")
                    buffer = [loncat[baris][kolom]["xy"], loncat[baris][kolom]["parent"]] #tambahkan xy tersebut dan parentnya
                    # cari ke atas, kalau xy itu ada di buffer = tambahkan parentnya ke buffer
                    for i in reversed(range(len(loncat)-1)):
                        # print("BLAST2")
                        for j in range(len(loncat[i])):
                            # print("MEH", loncat[i][j]["xy"])

                            if (loncat[i][j]["xy"] in buffer):
                                if("parent" in loncat[i][j].keys()):
                                    buffer.append(loncat[i][j]["parent"])
                            else:
                                if (i==0):
                                    loncat2.append(loncat[i][j]["xy"])

                    buffer2 = buffer[::-1]

                    loncat2.append(buffer2)

                    for i in range(1,len(buffer2)):
                        buffer3 = buffer2[:i]
                        # print("ASD", buffer3)
                        loncat2.append(buffer3)
                else :
                    loncat2.append(loncat[baris][kolom]["xy"])


        # print(loncat2)

        return loncat2

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
    def cariCabang(self, model, maxPlayer):
        cabang = []
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
                node = self.deepcopy(model)
                aksi = model.A_LONCAT
                tujuan = l[i] if type(l[i]) != tuple else [l[i]]
                nextNode = self.nextStep(node, tujuan, asal, aksi, index)

                cabang.append((nextNode, tujuan, asal, aksi))

            for i in range(len(g)):
                node = self.deepcopy(model)
                aksi = model.A_GESER
                tujuan = g[i]
                nextNode = self.nextStep(node, tujuan, asal, aksi, index)

                cabang.append((nextNode, tujuan, asal, aksi))

        return cabang

    def evalFunc(self, node, maxPlayer):
        score = 0
        w0 = 0.1
        w1 = 1
        w2 = 0.1
        w3 = 1
        index = self.index if maxPlayer else 1-self.index
        ladder03 = self.evalFuncLadder(node,index,0,3)
        ladder12 = 0 #self.evalFuncLadder(node,index,1,2)

        # print("CENTROID = ", self.evalCentroid(node, index))
        # print("TARGET = ", self.evalFuncTarget(node,index))
        # print("TARGET2 = ", self.evalFuncTarget(node,1-index))
        # print("LADDER03 = ", ladder03)
        # print("LADDER12 = ", ladder12)
        # print("--------")

        centroid = self.evalCentroid(node, index)
        score += centroid * w0 if index == 1 else -centroid*w0
        score += self.evalFuncTarget(node,index) * w1
        score -= self.evalFuncTarget(node,1-index) * w2
        score +=  max(ladder03, ladder12) * w3

        # print("Score:", score)

        return score

    def evalCentroid(self, node, giliran):
        papan = self.papanBiner(node,giliran,1,0)
        c = 0
        # print("AS", papan)
        for i in range(len(papan)):
            for j in range(len(papan[i])):
                if papan[i][j] == 1:
                    c += node.getUkuran()-j-i
                    # print("i",i,"j",j, "score:", j+i)

        return c

    def papanBiner(self, node, giliran, a, b):
        papan = node.getPapan()
        papan_biner = self.deepcopy(papan)

        for i in range(len(papan)):
            for j in range(len(papan)):
                if int(str(papan[i][j])[:1]) == giliran+1:
                    papan_biner [i][j] = a
                elif int(str(papan[i][j])[:1]) == 1-giliran + 1:
                    papan_biner [i][j] = b
                else:
                    papan_biner [i][j] = 0
        return papan_biner

    def evalFuncTarget(self, node, giliran):
        score = 0
        papan = node.getPapan()

        for i in range(len(papan)):
            for j in range(len(papan[i])):
                if papan[i][j] // 100 == giliran+1:
                    if node.dalamTujuan(giliran,i,j):
                        score +=1

        return score

    def buildArmyType(self, no):
        ladder = [[0]*no for i in range(no)]
        x = 0
        for i in range(len(ladder)):
            for j in range(len(ladder[i])):
                if i%2==0:
                    ladder[i][j] = x
                else:
                    ladder[i][j] = x+2
                x = 0 if(x==1) else 1
        return ladder

    def evalFuncLadder(self, node, giliran, no1, no2):
        papan = self.papanBiner(node,giliran, 1, 1)
        no = node.getUkuran()
        c = [[0]*no for i in range(no)]
        ladder = self.buildArmyType(no)

        for i in range(len(ladder)):
            for j in range(len(ladder[i])):
                if ladder[i][j] == no1 or ladder[i][j] == no2:
                    if not node.dalamTujuan(0, i, j) and not node.dalamTujuan(1,i,j):
                        ladder[i][j] = 1
                else:
                    ladder[i][j] = 0

        # print(ladder)

        for i in range(len(papan)):
            for j in range(len(papan[i])):
                c[i][j] = papan[i][j] & ladder[i][j]

        # print("C", c)

        return sum([sum(c[i]) for i in range(len(c))])

    def minimax(self, position, depth, alpha, beta, maxPlayer):
        if depth == 0 or position.akhir():
            return self.evalFunc(position, maxPlayer)

        if maxPlayer:
            maxEval = -9999
            cabang = self.cariCabang(position, True)
            childCount = 0
            for child in cabang:
                if childCount < self._childMax:
                    eval = self.minimax(child[0], depth-1, alpha, beta, False)
                    # these two lines is somehow the problem
                    if depth == self._ply and maxEval >= eval:
                        gc.disable()
                        self.pilihan.append((child[1],child[2],child[3])) #awalnya append diganti =

                    maxEval = max(maxEval,eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
                childCount +=1
            return maxEval
        else:
            minEval = 9999
            cabang = self.cariCabang(position, False)
            childCount = 0
            for child in cabang:
                if childCount < self._childMax:
                    eval = self.minimax(child[0], depth-1, alpha, beta, True)
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

        #initialization
        self.pilihan = []
        initPos = self.deepcopy(model)

        evalScore = self.minimax(initPos, self._ply, -9999, 9999, True)
        print(evalScore)
        print("time taken:", time.process_time() - time_start)
        #
        print(self.pilihan)
        if len(self.pilihan) > 0:
            pilih = random.randint(0,len(self.pilihan)-1)
            print(self.pilihan[pilih])
            # print(type(pilihan[pilih][0]) != tuple)

            if self.pilihan[pilih][2] == model.A_LONCAT:
                return (self.pilihan[pilih][0], self.pilihan[pilih][1], self.pilihan[pilih][2]) if type(self.pilihan[pilih][0]) != tuple else ([self.pilihan[pilih][0]], self.pilihan[pilih][1], self.pilihan[pilih][2])
            else:
                return [self.pilihan[pilih][0]], self.pilihan[pilih][1], self.pilihan[pilih][2]
        else:
            return None, None, model.A_BERHENTI
