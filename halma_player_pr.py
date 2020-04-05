import time
import copy
import sys
import random
from halma_model import HalmaModel


class HalmaPlayer02:
    nama = "Pemain"
    deskripsi = "Random Strategy"
    nomor = 1
    index = 0
    papan = []

    def __init__(self, nama):
        self.nama = nama
        self._ply = 3
        self._maxbreadth = 500
        self._maxbranch = 10 #max branch dalam satu ply
        self._loncat = 0
        self._geser = 0
        self._henti = 0
        self._inc = 1

    def setNomor(self, nomor):
        self.nomor = nomor
        self.index = nomor-1

    # mengembalikan semua kemungkikan main (geser / loncat) bidak di (x1, y1)
    def bisaMain(self, model, papan, x1, y1):
        geser = []
        loncat = {}
        # loncat_buffer = []
        baris = 0
        kolom = 0

        ip = self.index;
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
        loncat = self.loncatanPlus(model, papan, loncat)
        # print("THISDONE")
        # done getting the dictionary i wanted, now i need to sort it
        # to match the format specified

        loncat2 = self.sortLoncat(loncat)

        # print(x1, y1)
        # print(loncat2)
        # print("--------")
        # time.sleep(1)

        # loncat2 =

        return geser, loncat2

    def loncatanPlus(self, model, papan, loncat):
        loncat_buffer = []
        baris = 1
        stopCheck = False
        memory = (0,0)

        ip = self.index;


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
    def nextStep(self, model2, tujuan, asal, aksi, giliran):
        if model2.getGiliran() != giliran :
            model2.ganti(0)
        if (aksi == model2.A_LONCAT):
            # print("ASD",asal, tujuan, aksi)
            for xy in tujuan:
                valid = model2.mainLoncat(asal[0], asal[1], xy[0], xy[1])
                if (valid == model2.S_OK):
                    asal = xy # usulan solusi BUG#1
                    self._loncat += self._inc
        elif (aksi == model2.A_GESER):
            valid = model2.mainGeser(asal[0], asal[1], tujuan[0], tujuan[1])
            if (valid == model2.S_OK):
                self._geser += self._inc
        else:
            self._henti += self._inc

        return model2

    # untuk cari cabang suatu node
    def cariCabang(self, model, giliran):
        cabang = []
        papan = model.getPapan()
        b0 = model.getPosisiBidak(self.index)
        for b in b0:
            g, l = self.bisaMain(model, papan, b[0], b[1])
            asal = b

            udah = []
            for i in range(len(g)):
                kelar = False
                node = copy.deepcopy(model)
                aksi = model.A_GESER
                while not kelar:
                    x = random.randint(0,len(g)-1)
                    if x not in udah:
                        tujuan = g[x]
                        nextNode = self.nextStep(node, tujuan, asal, aksi, giliran)

                        udah.append(x)
                        cabang.append((nextNode, tujuan, asal, aksi))
                        kelar = True

            udah = []
            for i in range(len(l)):
                kelar = False
                node = copy.deepcopy(model)
                aksi = model.A_LONCAT
                while not kelar:
                    x = random.randint(0,len(l)-1)
                    if x not in udah:
                        tujuan = l[x] if type(l[x]) != tuple else [l[x]]
                        nextNode = self.nextStep(node, tujuan, asal, aksi, giliran)

                        udah.append(x)
                        cabang.append((nextNode, tujuan, asal, aksi))
                        kelar = True

        return cabang

    def updateDict(self, dict, k1, k2, isi):
        try:
            dict[k1][k2].update(isi)
        except:
            try:
                dict[k1][k2] = isi
            except:
                try:
                    dict[k1].update({k2:isi})
                except:
                    dict[k1] = {k2: isi}

    def evalFunc(self, node, giliran):
        return random.randint(0,100)

    def cariMax(self, evalScore):
        score = []
        max = -9999
        for i in evalScore:
            if (evalScore[i]["score"] > max):
                max = evalScore[i]["score"]
        #
        # for i in range(len(evalScore)):
        #     if (evalScore[i] >= max):
        #         score.append(evalScore[i])
        return max

    # Untuk cari value min
    def cariMin(self, evalScore):
        score = []
        min = 9999
        for i in evalScore:
            if (evalScore[i]["score"] < min):
                min = evalScore[i]["score"]

        # for i in range(len(evalScore)):
        #     if (evalScore[i] == min):
        #         score.append(evalScore[i])
        return min


    def main(self, model):
        time_start = time.process_time()

        #initialization
        # print(model.getPapan())
        time.sleep(1)
        model1 = copy.deepcopy(model)
        tree = {} # i: {j: {"node": node, "parent": (parent_i, parent_j), "tujuan": tujuan, "asal":asal, "aksi": aksi}}
        evalScore = {}
        tree[0] = {0: {"node": model1 }}

        giliran = self.nomor

        # search x ply
# cabang masih belum dapet semua euy
        for i in range(0, self._ply):
            no = 0
            if i % 2 == 0: #MAX
                giliran = self.nomor
            else: #MIN
                giliran = 1 - self.nomor

            udah = []

            for j in range(len(tree[i])):
                no2 = 0
                kelar = False #milih j dirandom, questionable tapi lur
                while not kelar:
                    x = random.randint(0, len(tree[i])-1)
                    if x not in udah:
                        parent = (i,x)
                        cabang = self.cariCabang(tree[i][x]["node"], giliran)
                        # print(parent, '----', cabang, '\r\n')
                        for k in range(len(cabang)): #lets only take x child per node
                            if no < self._maxbreadth:
                                if no2 < self._maxbranch:
                                    # parent = (i,j)
                                    isi = {"node": cabang[k][0], "parent": parent, "tujuan": cabang[k][1], "asal": cabang[k][2], "aksi": cabang[k][3]}
                                    self.updateDict(tree, i+1, no, isi)

                                    no += 1
                                    no2 +=1
                        udah.append(x)
                        kelar = True


        # evaluation function
        # print(tree)
        frontier = tree[self._ply]
        n = 0
        oldParent = None
        for i in range(len(frontier)):
            parent = frontier[i]["parent"]
            # print(parent)
            if self._ply % 2 == 1: #ujungnya max
                giliran = self.nomor
            else:
                giliran = 1-self.nomor

            if parent != oldParent:
                oldParent = parent
                n = 0
            else:
                n +=1

            isi = { n: {"i" : i, "score": self.evalFunc(frontier[i]["node"], giliran) } }
            # print(isi)
            self.updateDict(evalScore, parent[0], parent[1], isi)


#  Catatan : Cari loncatan ganda makan waktu buanyakk, enaknya gmn ya?
        # minimax + alpha beta pruning
        for parent_i in reversed(range(1, self._ply)):
            n = 0
            for parent_j in evalScore[parent_i]:
                parent2 = tree[parent_i][parent_j]["parent"]
                if parent_i % 2 == 0: #MAX
                    score = self.cariMax(evalScore[parent_i][parent_j])
                else:
                    score = self.cariMin(evalScore[parent_i][parent_j])

                isi = { n: {"i" : parent_j, "score": score } }
                self.updateDict(evalScore, parent2[0], parent2[1], isi)

                n += 1

        print("hSDf", evalScore)

        # move selection
        pilihan = []
        for j in evalScore[1]:
            for n in evalScore[1][j]:
                if evalScore[1][j][n]["score"] == evalScore[0][0][0]["score"]:
                    pilihan.append((tree[1][j]["tujuan"], tree[1][j]["asal"], tree[1][j]["aksi"]))


        print("time taken:", time.process_time() - time_start)

        # return
        if len(pilihan) > 0:
            pilih = random.randint(0,len(pilihan)-1)
            print(pilihan[pilih])
            # print(type(pilihan[pilih][0]) != tuple)

            if pilihan[pilih][2] == model.A_LONCAT:
                return (pilihan[pilih][0], pilihan[pilih][1], pilihan[pilih][2]) if type(pilihan[pilih][0]) != tuple else ([pilihan[pilih][0]], pilihan[pilih][1], pilihan[pilih][2])
            else:
                return [pilihan[pilih][0]], pilihan[pilih][1], pilihan[pilih][2]
        else:
            return None, None, model.A_BERHENTI
