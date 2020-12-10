from django.db import models
import sys
import copy
from termcolor import colored, cprint

ktoJeNaTahu = False  # false = biely, true = cierny
klikolNaFigurku = False # false = neklikol, true = klikol
jeNutenyTah = False # false = neni nuteny tah, true = je nuteny tah

cb = "00400040004000404000400040004000004000400040004040404040404040404040404040404040401040104010401010401040104010404010401040104010"

#00100010001000101000100010001000001000100010001000000000000000000000000000000000200020002000200000200020002000202000200020002000
#value:
#0 = nic
#1 = player1
#2 = player2

#color:
#0 = nic
#1 = zelena
#2 = oranzova
#3 = cervena

# Create your models here.
class Game(models.Model):
    chessboard = models.CharField( max_length=128, default=cb)
    onTurn = models.BooleanField(default=False)
    clicked = models.BooleanField(default=False)
    necessary = models.BooleanField(default=False)
    player1 = models.CharField( max_length=50)
    player2 = models.CharField( max_length=50, null=True, blank=True)
    state = models.CharField( max_length=50, default="lobby")
    

    def click(self, tah):
        parse(self.chessboard)
        global ktoJeNaTahu 
        global klikolNaFigurku
        global jeNutenyTah 
        
        ktoJeNaTahu = self.onTurn
        klikolNaFigurku = self.clicked
        jeNutenyTah = self.necessary

        y = 0
        for i in range(8):
            if abeceda[i] == tah[1]:
                y = i
                break

        x = (8-int(tah[2]))
        who = tah[0]

        if jeNutenyTah == False:
            valid = zeleny(x, y, who)
        else:
            valid = cerveny(x, y, who)

        if valid == False:
            valid = clickPohyb(x, y)

        self.onTurn = ktoJeNaTahu
        self.clicked = klikolNaFigurku
        self.necessary = jeNutenyTah
        self.chessboard = returnString()
        self.save()
        return valid

    # def __str__(self):
    #     return f'Game {self.id}'

    # def get_value(self, x, y):
    #     return self.chessboard[(x+8*y)*2]

    # def get_color(self, x, y):
    #     return self.chessboard[(x+8*y)*2+1]

    # def set_value(self, x, y, value):
    #     self.chessboard[(x+8*y)*2] = value

    # def set_color(self, x, y, color):
    #     self.chessboard[(x+8*y)*2+1] = color

    # def get_move(self, x, y):
    #     s = list(self.chessboard)
    #     s[(x+8*y)*2+1] = '1'

    #     if self.get_value(x, y) == '1' :
    #         if 0 <= y+1 <8:
    #             if 0 <= x+1 <8:
    #                 if self.get_value(x+1, y+1) == '0':
    #                     s[(x+1+8*(y+1))*2+1] = '1'
    #                 elif self.get_value(x+1, y+1) == '2' and 0 <= y+2 <8 and 0 <= x+2 <8 and self.get_value(x+2, y+2) == '0':
    #                     s[(x+1+8*(y+1))*2+1] = '3'
    #                     s[(x+2+8*(y+2))*2+1] = '1'
    #             if 0 <= x-1 <8:
    #                 if self.get_value(x-1, y+1) == '0':
    #                     s[(x-1+8*(y+1))*2+1] = '1'
    #                 elif self.get_value(x-1, y+1) == '2' and 0 <= y+2 <8 and 0 <= x-2 <8 and self.get_value(x-2, y+2) == '0':
    #                     s[(x-1+8*(y+1))*2+1] = '3'
    #                     s[(x-2+8*(y+2))*2+1] = '1'
    #     elif self.get_value(x, y) == '2' :
    #         if 0 <= y-1 <8:
    #             if 0 <= x+1 <8:
    #                 if self.get_value(x+1, y-1) == '0':
    #                     s[(x+1+8*(y-1))*2+1] = '1'
    #                 elif self.get_value(x+1, y-1) == '1' and 0 <= y-2 <8 and 0 <= x+2 <8 and self.get_value(x+2, y-2) == '0':
    #                     s[(x+1+8*(y-1))*2+1] = '3'
    #                     s[(x+2+8*(y-2))*2+1] = '1'
    #             if 0 <= x-1 <8:
    #                 if self.get_value(x-1, y-1) == '0':
    #                     s[(x-1+8*(y-1))*2+1] = '1'
    #                 elif self.get_value(x-1, y-1) == '1' and 0 <= y-2 <8 and 0 <= x-2 <8 and self.get_value(x-2, y-2) == '0':
    #                     s[(x-1+8*(y-1))*2+1] = '3'
    #                     s[(x-2+8*(y-2))*2+1] = '1'

    #     return "".join(s)





# [x, y]
#--------------------------
# x je figurka
# x -> 0 = biela
#   -> 1 = cierna
#   -> 2 = zelena
#   -> 3 = cervena
#   -> 4 = ziadna
#--------------------------
# y je background
# y -> 0 = ziany/cierny
#   -> 1 = zelena/kliknuta figurka
#   -> 2 = cervena
#   -> 3 = bleda
#   -> 4 = tmave
#-------------------------

sachovnica = [[[4, 0], [1, 0], [4, 0], [1, 0], [4, 0], [1, 0], [4, 0], [1, 0]], # 8
            [[1, 0], [4, 0], [1, 0], [4, 0], [1, 0], [4, 0], [1, 0], [4, 0]], # 7
            [[4, 0], [1, 0], [4, 0], [1, 0], [4, 0], [1, 0], [4, 0], [1, 0]], # 6
            [[4, 0], [4, 0], [4, 0], [4, 0], [4, 0], [4, 0], [4, 0], [4, 0]], # 5
            [[4, 0], [4, 0], [4, 0], [4, 0], [4, 0], [4, 0], [4, 0], [4, 0]], # 4
            [[0, 0], [4, 0], [0, 0], [4, 0], [0, 0], [4, 0], [0, 0], [4, 0]], # 3
            [[4, 0], [0, 0], [4, 0], [0, 0], [4, 0], [0, 0], [4, 0], [0, 0]], # 2
            [[0, 0], [4, 0], [0, 0], [4, 0], [0, 0], [4, 0], [0, 0], [4, 0]]] # 1
            #    a       b       c       d       e       f       g       h

sachovnicaTmp = sachovnica

abeceda = ["a", "b", "c", "d", "e", "f", "g", "h"]

    # def parse(x):
    #     pole = []
    #     for i in range(8):
    #         podpole = []
    #         for j in range(8):
    #             ppolo = [x[8*i+j],x[8*i+j+1]]
    #             podpole.append(ppolo)
    #         pola.append(podpole)

        
    #     return pole

def parse(x):
    index = 0

    for i in range(8):
        for j in range(8):
            sachovnica[7-i][j][0] = int(x[index])
            sachovnica[7 - i][j][1] = int(x[index+1])
            index += 2

def returnString():
    msg = ""
    for i in range(8):
        for j in range(8):
            msg += str(sachovnica[7-i][j][0])
            msg += str(sachovnica[7 - i][j][1])
    return msg

def setColor(x, y):
    if sachovnica[x][y][1] == 0:
        resetColor()
    elif sachovnica[x][y][1] == 1:
        sys.stdout.write("\033[0;32m")
    elif sachovnica[x][y][1] == 2:
        sys.stdout.write("\033[1;31m")
    elif sachovnica[x][y][1] == 3:
        sys.stdout.write("\033[1;36m")
    elif sachovnica[x][y][1] == 4:
        sys.stdout.write("\033[;1m")

def resetColor():
    sys.stdout.write("\033[0;0m")

def printBoard():
    # Use a breakpoint in the code line below to debug your script.
    for i in range(8):
        for j in range(8):
            resetColor()
            print("|", end="")
            msg = "."

            setColor(i, j)
            if sachovnica[i][j][0] != 4:
                msg = sachovnica[i][j][0]

            print(msg, end="")

        print("|")
        print("----------------")


def isValid(tah):
    if len(tah) != 2:
        if tah[0] not in ["w", "b"]:
            print("Si kokot je len biely alebo cierny.")
            return False
        else:
            if (ktoJeNaTahu == False and tah[0] == "b") or (ktoJeNaTahu == True and tah[0] == "w"):
                print("nie si na tahu")
                return False

        if tah[1] not in ["a", "b", "c", "d", "e", "f", "g", "h"]:
            print("Ale chod do pice musi to byt od a-h")
            return False

        if int(tah[2]) > 8 or tah[2] == "0":
            print("Jebem to od 1-8.")
            return False
    else:
        print("Si kokot musi to mat 3 znaky [kto klikol] [pismeno] [cislo]")
        return False

    return True

def redToGreen():
    for i in range(8):
        for j in range(8):
            if sachovnica[i][j][0] == 3:
                sachovnica[i][j][0] = 2

            if sachovnica[i][j][1] == 2:
                sachovnica[i][j][1] = 1

def cleanBledaTmava():
    cleanBackground(3)
    cleanBackground(4)

def cleanZelene():
    cleanBackground(1)
    cleanFigurky(2)

def cleanCervene():
    cleanBackground(2)
    cleanFigurky(3)

def cleanFigurky(figurka):
    for i in range(8):
        for j in range(8):
            if sachovnica[i][j][0] == figurka:
                sachovnica[i][j][0] = 4

def cleanBackground(background):
    for i in range(8):
        for j in range(8):
            if sachovnica[i][j][1] == background:
                sachovnica[i][j][1] = 0

def setZeleneFigurky(x, y, who):
    if who == "w":
        if x-1 >= 0 and y+1 < 8:
            if sachovnica[x-1][y+1][0] not in [0, 1]:
                sachovnica[x-1][y+1][0] = 2

        if x-1 >= 0 and y-1 >= 0:
            if sachovnica[x-1][y-1][0] not in [0, 1]:
                sachovnica[x-1][y-1][0] = 2
    else:
        if x+1 < 8 and y+1 < 8:
            if sachovnica[x+1][y+1][0] not in [0, 1]:
                sachovnica[x+1][y+1][0] = 2


        if x+1 < 8 and y-1 >= 0:
            if sachovnica[x+1][y-1][0] not in [0, 1]:
                sachovnica[x+1][y-1][0] = 2


def setCervenyFigurky(x, y, who):
    if who == "w":
        if x - 2 >= 0 and y + 2 < 8:
            if sachovnica[x][y][0] in [0, 3]:
                if sachovnica[x - 1][y + 1][0] == 1:
                    if sachovnica[x - 2][y + 2][0] in [3, 4]:
                        sachovnica[x][y][1] = 2
                        sachovnica[x - 2][y + 2][0] = 3


        if x - 2 >= 0 and y - 2 >= 0:
            if sachovnica[x][y][0] in [0, 3]:
                if sachovnica[x - 1][y - 1][0] == 1:
                    if sachovnica[x - 2][y - 2][0] in [3, 4]:
                        sachovnica[x][y][1] = 2
                        sachovnica[x - 2][y - 2][0] = 3

    else:
        if x + 2 < 8 and y + 2 < 8:
            if sachovnica[x][y][0] in [1, 3]:
                if sachovnica[x + 1][y + 1][0] == 0:
                    if sachovnica[x + 2][y + 2][0] in [3, 4]:
                        sachovnica[x][y][1] = 2
                        sachovnica[x + 2][y + 2][0] = 3

        if x + 2 < 8 and y - 2 >= 0:
            if sachovnica[x][y][0] in [1, 3]:
                if sachovnica[x + 1][y - 1][0] == 0:
                    if sachovnica[x + 2][y - 2][0] in [3, 4]:
                        sachovnica[x][y][1] = 2
                        sachovnica[x + 2][y - 2][0] = 3



# Funkcia na zistenie ci sa ma nastavit/odnastavit zeleny background a figurky
def zeleny(x, y, who):
    global klikolNaFigurku

    if klikolNaFigurku == False:  # ak nema zakliknutu ziadnu figurku
        if who == "w" and sachovnica[x][y][0] == 0:  # ak je biely na rade a figurka je biela
            sachovnica[x][y][1] = 1
            setZeleneFigurky(x, y, who)

            klikolNaFigurku = True
            return True

        if who == "b" and sachovnica[x][y][0] == 1:  # ak je cierny na rade a figurka je cierna
            sachovnica[x][y][1] = 1
            setZeleneFigurky(x, y, who)

            klikolNaFigurku = True
            return True

    else:  # ak ma zakliknutu niaku figurku
        if who == "w" and sachovnica[x][y][0] == 0:  # ak je biely na rade a figurka je biela
            if sachovnica[x][y][1] == 1:  # ak figurka uz je zakliknuta
                sachovnica[x][y][1] = 0
                cleanZelene()

                klikolNaFigurku = False
                return True
            else:  # zaklikol novu figurku
                cleanBackground(1)
                cleanZelene()

                sachovnica[x][y][1] = 1
                setZeleneFigurky(x, y, who)
                return True

        if who == "b" and sachovnica[x][y][0] == 1:  # ak je cierny na rade a figurka je cierna
            if sachovnica[x][y][1] == 1:  # ak figurka uz je zakliknuta
                sachovnica[x][y][1] = 0
                cleanZelene()

                klikolNaFigurku = False
                return True
            else:  # zaklikol novu figurku
                cleanBackground(1)
                cleanZelene()

                sachovnica[x][y][1] = 1
                setZeleneFigurky(x, y, who)
                return True

    return False

def setCervene():
    global jeNutenyTah
    jeNutenyTah = False

    if ktoJeNaTahu == False:
        for x in range(8):
            for y in range(8):
                if x - 2 >= 0 and y + 2 < 8:
                    if sachovnica[x][y][0] in [0, 3]:
                        if sachovnica[x - 1][y + 1][0] == 1:
                            if sachovnica[x - 2][y + 2][0] in [3, 4]:

                                if sachovnica[x][y][0] != 3:
                                    sachovnica[x][y][1] = 2

                                sachovnica[x - 2][y + 2][0] = 3

                                jeNutenyTah = True

                if x - 2 >= 0 and y - 2 >= 0:
                    if sachovnica[x][y][0] in [0, 3]:
                        if sachovnica[x - 1][y - 1][0] == 1:
                            if sachovnica[x - 2][y - 2][0] in [3, 4]:

                                if sachovnica[x][y][0] != 3:
                                    sachovnica[x][y][1] = 2

                                sachovnica[x - 2][y - 2][0] = 3

                                jeNutenyTah = True
    else:
        for x in range(8):
            for y in range(8):
                if x + 2 < 8 and y + 2 < 8:
                    if sachovnica[x][y][0] in [1, 3]:
                        if sachovnica[x + 1][y + 1][0] == 0:
                            if sachovnica[x + 2][y + 2][0] in [3, 4]:

                                if sachovnica[x][y][0] != 3:
                                    sachovnica[x][y][1] = 2

                                sachovnica[x + 2][y + 2][0] = 3

                                jeNutenyTah = True

                if x + 2 < 8 and y - 2 >= 0:
                    if sachovnica[x][y][0] in [1, 3]:
                        if sachovnica[x + 1][y - 1][0] == 0:
                            if sachovnica[x+2][y-2][0] in [3, 4]:

                                if sachovnica[x][y][0] != 3:
                                    sachovnica[x][y][1] = 2

                                sachovnica[x + 2][y - 2][0] = 3

                                jeNutenyTah = True

def invertTah(x, y):
    who = "b"
    global ktoJeNaTahu

    if ktoJeNaTahu == True:
        who = "w"

    setCervenyFigurky(x, y, who)

    bool1 = False

    for i in range(8):
        for j in range(8):
            if sachovnica[i][j][0] == 3:
                bool1 = True
                break

    if bool1 == True:
        sachovnica[x][y][1] = 2

        ktoJeNaTahu = not ktoJeNaTahu
        return True

    return False




def clickPohyb(x, y):
    if sachovnica[x][y][0] == 2:
        for i in range(8):
            for j in range(8):
                if sachovnica[i][j][1] == 1:
                    sachovnica[x][y][0] = sachovnica[i][j][0]
                    sachovnica[i][j][0] = 4

                    cleanZelene()

                    cleanBledaTmava()

                    if jeNutenyTah == True:
                        sachovnica[int((x+i)/2)][int((y+j)/2)][0] = 4

                    sachovnica[x][y][1] = 3
                    sachovnica[i][j][1] = 4
                    break

        global ktoJeNaTahu
        ktoJeNaTahu = not ktoJeNaTahu

        bool1 = invertTah(x, y)

        if bool1 == False:
            setCervene()

        return True

    return False

def cerveny(x, y, who):
    global sachovnicaTmp
    global sachovnica

    if (sachovnica[x][y][1] == 2):
        sachovnicaTmp = sachovnica.copy()
        cleanCervene()
        setCervenyFigurky(x, y, who)
        sachovnica[x][y][1] = 1
        redToGreen()
        return True

    if (sachovnica[x][y][1] == 1):
        cleanZelene()
        setCervene()
        return True

    return False

    