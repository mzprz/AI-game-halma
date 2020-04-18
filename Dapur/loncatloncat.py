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
