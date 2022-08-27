#!/usr/bin/python3
import pathlib, os, ast, calendar
from time import sleep
from datetime import datetime, date, timedelta

versie = """
versie: 1.21
Auteur: Maestraccio
Contact: maestraccio@musician.org
Catania 20220827

+-----"""
info1 = """
Iedere rekeningmap bestaat uit een rekeningnummer en een jaartal. In 
opzet bevat een map één kalenderjaar, hoewel het mogelijk is onbeperkt
door te schrijven; dit is door de gebruiker vrij te bepalen. In de
rekeningmap worden standaard de volgende bestanden aangemaakt:
    "alternatievenamen": de categorienamen bij de letters
    "header": rekeninggegevens en rekeninggebonden weergaveopties
    zes categoriebestanden "A"-"E" en "O" met de financiële mutaties

6 categorieën (uitbreid- en aanpasbaar):
A: saldo & inkomen: in principe positieve bedragen, budget negatief
B: vaste lasten   : verwachte en terugkerende uitgaven
C: boodschappen   : dagelijkse variabele uitgaven
D: reis & verblijf: reiskosten, brandstof, overnachtingen, enz.
E: leningen       : bedragen die worden voorgeschoten en terugbetaald
O: overig         : overige mutaties
Andere categorieën kunnen worden toegevoegd door een nieuwe mutatie 
toe te voegen of te wijzigen en toe te wijzen aan de nieuwe categorie.

"header" bevat 8 regels waarvan alleen de eerste drie worden getoond:
1: Beschrijving
2: Rekeninghouder
3: Plaats
4: Valuta (standaard "€")
5: Nulregels (standaard "Nee")
6: Ondermarkering (standaard "-100")
7: Bovenmarkering (standaard "100")
8: Kleur (standaard "Categorie")

+-----"""
info2 = """
PROGRAMMASTRUCTUUR:

0 Beheer
    0 Print versie en info
    1 Categoriebeheer
        1 Categorienaam wijzigen
        2 Maandbudget wijzigen
        3 Categorie verwijderen
    2 Wijzig rekeninggegevens
        1 Beschrijving
        2 Rekeninghouder
        3 Plaats
        4 Valuta (standaard = "€")
        5 Nulregels (standaard "Nee")
        6 Ondermarkering (standaard omkering van Bovenmarkering)
        7 Bovenmarkering (standaard omkering van Ondermarkering)
        8 Kleur (standaard = "Categorie")
    3 Toon of verberg rekening
    4 Wissel van rekening
    5 Nieuwe rekening toevoegen
    6 Verwijder rekening
1 Bekijken
    Datumselectie -> Categorieselectie -> Subselectie -> Print + ID
2 Toevoegen
    1 Nieuw
    2 Kopie (o.b.v. ID uit "1 Bekijken")
3 Wijzigen (o.b.v. ID uit "1 Bekijken")
    1 Datum (standaard = vandaag)
    2 Bedrag (standaard = 0.0, "+" of "-" = omkering)
    3 Wederpartij
    4 Betreft
    5 Categorie
4 Verwijderen (o.b.v. ID uit "1 Bekijken")
"""

basismap = os.path.dirname(os.path.realpath(__file__)) # de map waar het pythonscript in staat moet schrijfbaar zijn
os.chdir(basismap)

##### Alle mogelijke kleuren

ResetAll                = "\033[0m"
Vet                     = "\033[1m"
Vaag                    = "\033[2m"
Onderstrepen            = "\033[4m"
Knipperen               = "\033[5m"
Omkeren                 = "\033[7m"
Verborgen               = "\033[8m"
ResetVet                = "\033[21m"
ResetVaag               = "\033[22m"
ResetOnderstrepen       = "\033[24m"
ResetKnipperen          = "\033[25m"
ResetOmkeren            = "\033[27m"
ResetVerborgen          = "\033[28m"
Default                 = "\033[39m"
Zwart                   = "\033[30m"
Rood                    = "\033[31m"
Groen                   = "\033[32m"
Geel                    = "\033[33m"
Blauw                   = "\033[34m"
Magenta                 = "\033[35m"
Cyaan                   = "\033[36m"
LichtGrijs              = "\033[37m"
DonkerGrijs             = "\033[90m"
LichtRood               = "\033[91m"
LichtGroen              = "\033[92m"
LichtGeel               = "\033[93m"
LichtBlauw              = "\033[94m"
LichtMagenta            = "\033[95m"
LichtCyaan              = "\033[96m"
Wit                     = "\033[97m"
AchtergrondDefault      = "\033[49m"
AchtergrondZwart        = "\033[40m"
AchtergrondRood         = "\033[41m"
AchtergrondGroen        = "\033[42m"
AchtergrondGeel         = "\033[43m"
AchtergrondBlauw        = "\033[44m"
AchtergrondMagenta      = "\033[45m"
AchtergrondCyaan        = "\033[46m"
AchtergrondLichtGrijs   = "\033[47m"
AchtergrondDonkerGrijs  = "\033[100m"
AchtergrondLichtRood    = "\033[101m"
AchtergrondLichtGroen   = "\033[102m"
AchtergrondLichtGeel    = "\033[103m"
AchtergrondLichtBlauw   = "\033[104m"
AchtergrondLichtMagenta = "\033[105m"
AchtergrondLichtCyaan   = "\033[106m"
AchtergrondWit          = "\033[107m"
colgoed = LichtGroen
colmatig = Magenta
colslecht = LichtRood
colonbepaald = Blauw
coltoe = Groen
colkijk = LichtGeel
colanders = LichtCyaan
colweg= Rood
coltekst = LichtMagenta

#____     __   \/   ____      _  ____
# ||\    /|    ||    ||\    /|  /   \\
# ||\\  /||  / ||\\  ||\\  /|| || \/ ||
# || \\/ || || || || || \\/ || || || ||
# ||  \  || || || || ||  \  || || || ||
#_/\_   _/\_|| \/ ||_/\_   _/\_ \ || /
#            \\___/               ||
# Money In           Money Out    \/
logo = """
%s                ____     __   \/   %s____     __  ____
%s                 ||\    /|    ||    %s||\    /|  /   \\\\
%s                 ||\\\\  /||  %s/ %s||%s\\\\  %s||\\\\  /|| || %s\/%s ||
%s                 || \\\\/ || %s|| %s||%s || %s|| \\\\/ || || %s||%s ||
%s                 ||  \  || %s|| %s|| %s|| %s||  \  || || %s|| %s||
%s                _/\_   _/\_%s|| %s\/ %s||%s_/\_   _/\_ \ %s|| %s/
%s                            \\\\___/               ||
%s                 Money In           %sMoney Out    %s\/%s
""" % (colgoed,colslecht,colgoed,colslecht,colgoed,colonbepaald,colgoed,colonbepaald,colslecht,colonbepaald,colslecht,colgoed,colonbepaald,colgoed,colonbepaald,colslecht,colonbepaald,colslecht,colgoed,colonbepaald,colgoed,colonbepaald,colslecht,colonbepaald,colslecht,colgoed,colonbepaald,colgoed,colonbepaald,colslecht,colonbepaald,colslecht,colonbepaald,colgoed,colslecht,colonbepaald,ResetAll)

for i in logo:
    print(i,flush = True, end = "")
    sleep(0.001)

forn = "{0:>.2f}".format
fornum = "{0:>8.2f}".format
for3 = "{:3}".format
forc3 = "{:^3}".format
for4 = "{:4}".format
for5 = "{:5}".format
forc5 = "{:^5}".format
forr5 = "{:>5}".format
forc7 = "{:^7}".format
for8 = "{:8}".format
for10 = "{:10}".format
forc10 = "{:^10}".format
forr10 = "{:>10}".format
for12 = "{:12}".format
forc12 = "{:^12}".format
for15 = "{:15}".format
forc15 = "{:^15}".format
forc17 = "{:^17}".format
for18 = "{:18}".format
for19 = "{:19}".format
forc19 = "{:^19}".format
forr19 = "{:>19}".format
for20 = "{:20}".format
forc20 = "{:^20}".format
for25 = "{:25}".format
forc68 = "{:^68}".format
forc70 = "{:^70}".format
forc80 = "{:^80}".format # alleen als er een kleur en een ResetAll in zit
toplijn = "+"+"-"*10+"-"+"-"*12+"-"+"-"*17+"-"+"-"*20+"-"+"-"*5+"+"
pluslijn = "+"+"-"*10+"+"+"-"*12+"+"+"-"*17+"+"+"-"*20+"+"+"-"*5+"+"
lijst = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O"]
afsluitlijst = ["X","Q",":Q"]
jalijst = ["J","S","Y",":W"]
neelijst = ["N"]

strnu = str(date.today()).replace("-","")
nu = int(strnu)
print(LichtGeel+forc70(nu)+ResetAll)

##### hier volgen wat functies #####

def updatekleur():
    with open("header","r") as h:
        header = ast.literal_eval(h.read())
    if header["Kleur"] == "Alle":
        kleuren = {"ResetAll":"\033[0m","Omkeren":"\033[7m","Rood":"\033[31m","Groen":"\033[32m","Geel":"\033[33m","Blauw":"\033[34m","Magenta":"\033[35m","Cyaan":"\033[36m","LichtGrijs":"\033[37m","DonkerGrijs":"\033[90m","LichtRood":"\033[91m","LichtGroen":"\033[92m","LichtGeel":"\033[93m","LichtBlauw":"\033[94m","LichtMagenta":"\033[95m","LichtCyaan":"\033[96m","Wit":"\033[97m","colgoed":LichtGroen,"colslecht":LichtRood,"colonbepaald":Blauw}
        catcol = {"A":Rood,"B":Groen,"C":Geel,"D":Blauw,"E":Magenta,"F":Cyaan,"G":LichtGrijs,"H":DonkerGrijs,"I":LichtRood,"J":LichtGroen,"K":LichtGeel,"L":LichtBlauw,"M":LichtMagenta,"N":LichtCyaan,"O":Wit}
    elif header["Kleur"] == "Mono":
        kleuren = {"ResetAll":"\033[0m","Omkeren":"\033[7m","Rood":ResetAll,"Groen":ResetAll,"Geel":ResetAll,"Blauw":ResetAll,"Magenta":ResetAll,"Cyaan":ResetAll,"LichtGrijs":ResetAll,"DonkerGrijs":ResetAll,"LichtRood":ResetAll,"LichtGroen":ResetAll,"LichtGeel":ResetAll,"LichtBlauw":ResetAll,"LichtMagenta":ResetAll,"LichtCyaan":ResetAll,"Wit":ResetAll,"colgoed":LichtGroen,"colslecht":LichtRood,"colonbepaald":Blauw}
        catcol = {"A":Rood,"B":Groen,"C":Geel,"D":Blauw,"E":Magenta,"F":Cyaan,"G":LichtGrijs,"H":DonkerGrijs,"I":LichtRood,"J":LichtGroen,"K":LichtGeel,"L":LichtBlauw,"M":LichtMagenta,"N":LichtCyaan,"O":Wit}
    elif header["Kleur"] == "Regenboog":
        kleuren = {"ResetAll":"\033[0m","Omkeren":"\033[7m","Rood":"\033[31m","Groen":"\033[32m","Geel":"\033[33m","Blauw":"\033[34m","Magenta":"\033[35m","Cyaan":"\033[36m","LichtGrijs":"\033[37m","DonkerGrijs":"\033[90m","LichtRood":"\033[91m","LichtGroen":"\033[92m","LichtGeel":"\033[93m","LichtBlauw":"\033[94m","LichtMagenta":"\033[95m","LichtCyaan":"\033[96m","Wit":"\033[97m","colgoed":LichtGroen,"colslecht":LichtRood,"colonbepaald":Blauw}
        catcol = {"A":AchtergrondRood,"B":AchtergrondGeel,"C":AchtergrondLichtGeel,"D":AchtergrondGroen,"E":AchtergrondBlauw,"F":AchtergrondMagenta,"G":AchtergrondRood,"H":AchtergrondGeel,"I":AchtergrondLichtGeel,"J":AchtergrondGroen,"K":AchtergrondBlauw,"L":AchtergrondMagenta,"M":AchtergrondLichtGroen,"N":AchtergrondLichtRood,"O":AchtergrondMagenta}
    else:
        kleuren = {"ResetAll":"\033[0m","Omkeren":"\033[7m","Rood":ResetAll,"Groen":ResetAll,"Geel":ResetAll,"Blauw":ResetAll,"Magenta":ResetAll,"Cyaan":ResetAll,"LichtGrijs":ResetAll,"DonkerGrijs":ResetAll,"LichtRood":ResetAll,"LichtGroen":ResetAll,"LichtGeel":ResetAll,"LichtBlauw":ResetAll,"LichtMagenta":ResetAll,"LichtCyaan":ResetAll,"Wit":ResetAll,"colgoed":LichtGroen,"colslecht":LichtRood,"colonbepaald":Blauw}
        catcol = {"A":"\033[31m","B":"\033[32m","C":"\033[33m","D":"\033[34m","E":"\033[35m","F":"\033[36m","G":"\033[37m","H":"\033[90m","I":"\033[91m","J":"\033[92m","K":"\033[93m","L":"\033[94m","M":"\033[95m","N":"\033[96m","O":"\033[97m"}
    return kleuren,catcol

def rknngnlst():
    os.chdir(basismap)
    rekeningenlijst = []
    for d in os.listdir():
        if "@" in d:
            with open(os.path.join(d,"header"),"r") as h:
                header = ast.literal_eval(h.read())
            beschrijving = header["Beschrijving"]
            e = d+"@"+beschrijving
            rekeningenlijst.append(e.split("@"))
    rekeningenlijst = sorted(rekeningenlijst)
    reking = 1
    for i in rekeningenlijst:
        print("  "+colslecht+for3(str(reking))+ResetAll+colgoed+for20(i[0])+colonbepaald+i[1]+ResetAll+" "+colslecht+i[2]+ResetAll)
        reking += 1
    return rekeningenlijst

def rek():
    rek = "N"
    while rek == "N":
        rekening = input("Kies een %srekening%s om te gebruiken\n%s  : %s" % (colgoed,ResetAll,colslecht,colgoed))
        print(ResetAll, end = "")
        if rekening.upper() in afsluitlijst:
            exit()
        else:
            try:
                indrek = int(rekening)-1
                iban = rekeningenlijst[indrek][0]
                jaar = rekeningenlijst[indrek][1]
            except(Exception) as error:
                #print(error)
                indrek = 0
            finally:
                iban = rekeningenlijst[indrek][0]
                jaar = rekeningenlijst[indrek][1]
                werkmap = os.path.join(basismap,iban+"@"+jaar)
                os.chdir(werkmap)
                with open("header","r") as f:
                    header = ast.literal_eval(f.read())
                with open("alternatievenamen","r") as g:
                    alternatievenamenlijst = ast.literal_eval(g.read())
                return iban,jaar,header,alternatievenamenlijst,werkmap

def printheaderall():
    for k,v in header.items():
        if "markering" in k:
            v = header["Valuta"]+fornum(v)
        print(colslecht+for15(k),colonbepaald+":",colgoed+str(v)+ResetAll)

def printheader():
    regel = 0
    for k,v in header.items():
        print(colslecht+for15(k),colonbepaald+":",colgoed+v+ResetAll)
        regel += 1
        if regel == 3:
            break

def alt():
    alternatievenamenlijst = {}
    try:
        with open("alternatievenamen","r") as f:
            alternatievenamen = ast.literal_eval(f.read())
            for k,v in sorted(alternatievenamen.items()):
                with open(k,"r") as g:
                    lengte = ast.literal_eval(g.read())
                    tot = 0
                    for i in lengte[1:]:
                        tot = tot + i[1]
                    budget = lengte[0]
                    lencat = "items: "+forr5(str(len(lengte)-1))
                    col = catcol[k]
                    print(col+forc70(k+": "+forc17(v)+lencat)+ResetAll)
                    alternatievenamenlijst[k] = v
    except(Exception) as error:
        #print(error)
        pass

def nieuwerekening():
    nieuw = "Y"
    while nieuw == "Y":
        nieuwiban = input("Geef het %srekeningnummer%s (%sIBAN%s)\n  : %s" % (LichtGroen,ResetAll,LichtGroen,ResetAll,LichtGroen)).upper()
        print(ResetAll, end = "")
        if nieuwiban.upper() in afsluitlijst:
            os.chdir(os.path.join(basismap,iban+"@"+jaar))
            break
        nieuwjaar = input("Geef het %sjaar%s (%s\"YYYY\"%s)\n  : %s" % (LichtGroen,ResetAll,LichtGroen,ResetAll,LichtGroen)).upper()
        print(ResetAll, end = "")
        if nieuwjaar.upper() in afsluitlijst:
            os.chdir(os.path.join(basismap,iban+"@"+jaar))
            break
        try:
            if int(nieuwjaar) < 1000 or int(nieuwjaar) > 9999:
                nieuwjaar = strnu[:4]
        except(Exception) as error:
            #print(error)
            nieuwjaar = strnu[:4]
        print("Nieuwe rekening: %s@%s" % (nieuwiban,nieuwjaar))
        os.mkdir(nieuwiban+"@"+nieuwjaar)
        os.chdir(nieuwiban+"@"+nieuwjaar)
        nieuwheader = {'Beschrijving':'','Rekeninghouder':'','Plaats':'','Valuta':'€', 'Nulregels':'Nee','Ondermarkering':-100,'Bovenmarkering':100,'Kleur':'Categorie'}
        with open("header","w") as f:
            print(nieuwheader, file = f, end = "")
        nieuwalternatievenamenlijst = {'A':'saldo & inkomen','B':'vaste lasten','C':'boodschappen','D':'reis & verblijf','E':'leningen','O':'overig'}
        with open("alternatievenamen","w") as g:
            print(nieuwalternatievenamenlijst, file = g, end = "")
        for k,v in nieuwalternatievenamenlijst.items():
            with open(k,"w") as h:
                print([0.0], file = h, end = "")
        with open("A","w") as w:
            print([0.0, [11111111, 0.0, "Saldo", "Startsaldo"]], file = w, end = "")
        os.chdir(basismap)
        nieuw = "N"


##### Eerst moet je een rekening selecteren of aanmaken #####

reksel = "Y"
while reksel == "Y":
    try:
        print()
        rekeningenlijst = rknngnlst()
        print()
        if len(rekeningenlijst) == 0:
            nieuwerekening()
            rekeningenlijst = rknngnlst()
            ibanjaar = rek()
            iban = ibanjaar[0]
            jaar = ibanjaar[1]
            header = ibanjaar[2]
            alternatievenamenlijst = ibanjaar[3]
        elif len(rekeningenlijst) == 1:
            werkmap = str(pathlib.Path().absolute())+str(os.path.sep)+(rekeningenlijst[0][0]+"@"+rekeningenlijst[0][1])+str(os.path.sep)
            iban = rekeningenlijst[0][0]
            jaar = rekeningenlijst[0][1]
            os.chdir(werkmap)
            with open("header","r") as f:
                header = ast.literal_eval(f.read())
        else:
            ibanjaar = rek()
            iban = ibanjaar[0]
            jaar = ibanjaar[1]
            header = ibanjaar[2]
            werkmap = ibanjaar[3]
        kleur = updatekleur()
        Kleuren = kleur[0]
        globals().update(Kleuren)
        catcol = kleur[1]
        break
    except(Exception) as error:
        #print(error)
        pass

##### Hier worden de standaarwaarden overschreven met de aangepaste waarden in header

try:
    with open("header","r") as h:
        header = ast.literal_eval(h.read())
    for k,v in header.items():
        k = v
    globals().update(header)
except(Exception) as error:
    #print(error)
    nieuwheader = {'Beschrijving':'','Rekeninghouder':'','Plaats':'','Valuta':'€', 'Nulregels':'Nee','Ondermarkering':-100,'Bovenmarkering':100,'Kleur':'Categorie'}
    with open("header","w") as f:
        print(nieuwheader, file = f, end = "")
    with open("header","r") as h:
        header = ast.literal_eval(h.read())
    for k,v in header.items():
        k = v
    globals().update(header)
    #pass

print()
print(toplijn)
print()

##### HIER BEGINT HET PROGRAMMA #####

mimo = "Y"
while mimo == "Y":
#    if jaar == "":
#        print("%sMaak eerst in \"%s0 beheer%s\" een nieuwe rekening aan%s" % (colslecht,LichtMagenta,colslecht,ResetAll))
#    else:
    kleur = updatekleur()                     # hier past hij de kleurinstellingen van de rekening toe
    Kleuren = kleur[0]
    globals().update(Kleuren)
    catcol = kleur[1]
    with open("alternatievenamen","r") as a:  # hier haalt hij de dictionary uit het bestand met de alternatieve namen van de categorieën
        alternatievenamenlijst = ast.literal_eval(a.read())
    printheader()
    print()
    moni = 0.0                                # hier telt hij alle bedragen die hij kan vinden bij elkaar op
    for i in lijst:
        try:
            with open(i,"r") as f:
                inhoudvancategorie = ast.literal_eval(f.read())
                for j in inhoudvancategorie[1:]:
                    moni += j[1]
        except(Exception) as error:
            #print(error)
            pass
    print(LichtMagenta+forc70(iban+" "+Valuta+" "+fornum(moni))+ResetAll)
    alt()
    print()
    
##### Hier volgt het eerste keuzemenu #####

    keuze1 = input("Maak een keuze\n%s  0 Beheer%s\n%s >1 Bekijken%s\n%s  2 Toevoegen%s\n%s  3 Wijzigen%s\n%s  4 Verwijderen%s\n  : " % (LichtMagenta,ResetAll,LichtGeel,ResetAll,LichtGroen,ResetAll,LichtCyaan,ResetAll,LichtRood,ResetAll))
    if keuze1.upper() in afsluitlijst:
        print()
        print(toplijn)
        print()
        break
    elif keuze1 == "1" or keuze1 == "": # BEKIJKEN
        print()
        bekijken = "Y"
        while bekijken == "Y":
            budgetcheck = "N"
            dagsaldo = "N"
            col1 = LichtGeel
            keuze2 = input("%sMaak een datumselectie%s\n >1 %sÉén maand%s (incl. budgetanalyse)\n  2 %sAantal dagen geleden%s t/m vandaag\n  3 %sAantal maanden geleden%s t/m vandaag\n  4 %sEen datumbereik%s YYYYMMDD-YYYYMMDD\n  5 %sÉén dag%s YYYYMMDD (incl. dagsaldo)\n  : %s" % (col1,ResetAll,col1,ResetAll,col1,ResetAll,col1,ResetAll,col1,ResetAll,col1,ResetAll,col1))
            print(ResetAll, end = "")
            if keuze2.upper() in afsluitlijst:
                break
            else:
                if keuze2 == "2":
                    einddatum = nu
                    dagen = input("%sGeef het aantal dagen op%s\n  : %s" % (col1,ResetAll,col1))
                    print(ResetAll, end = "")
                    if dagen.upper() in afsluitlijst:
                        break
                    else:
                        try:
                            dagen = int(dagen)
                            startdatum = int(str(datetime.strptime(strnu,"%Y%m%d")-timedelta(days = dagen))[:10].replace("-",""))
                            print("Van %s%s%s tot %s%s%s" % (col1,startdatum,ResetAll,col1,einddatum,ResetAll))
                            aantaldagen = "Y"
                        except(Exception) as error:
                            #print(error)
                            dagen = 7
                            startdatum = int(str(datetime.strptime(strnu,"%Y%m%d")-timedelta(days = dagen))[:10].replace("-",""))
                            print("Van %s%s%s tot %s%s%s" % (col1,startdatum,ResetAll,col1,einddatum,ResetAll))
                            aantaldagen = "Y"
                elif keuze2 == "3":
                    einddatum = nu
                    maanden = input("%sGeef het aantal maanden op%s (max 3 jr)\n  : %s" % (col1,ResetAll,col1))
                    print(ResetAll, end = "")
                    if maanden.upper() in afsluitlijst:
                        break
                    else:
                        maandcheck = int(strnu[4:6])
                        try:
                            maanden = int(maanden)
                            if maanden < 0:
                                startdatum = int(strnu[:4]+"{:0>2}".format(str(maandcheck))+"01")
                                print("Van %s%s%s tot %s%s%s" % (col1,startdatum,ResetAll,col1,strnu,ResetAll))
                            elif maanden <= maandcheck:
                                startdatum = int(strnu[:4]+"{:0>2}".format(str(maandcheck-int(maanden)))+"01")
                                print("Van %s%s%s tot %s%s%s" % (col1,startdatum,ResetAll,col1,strnu,ResetAll))
                            elif maandcheck < maanden < maandcheck+12:
                                startdatum = int(str(int(strnu[:4])-1)+"{:0>2}".format(str(12+(maandcheck-maanden)))+"01")
                                print("Van %s%s%s tot %s%s%s" % (col1,startdatum,ResetAll,col1,strnu,ResetAll))
                            elif maandcheck < maanden < maandcheck+24:
                                startdatum = int(str(int(strnu[:4])-2)+"{:0>2}".format(str(12+(maandcheck-maanden+12)))+"01")
                                print("Van %s%s%s tot %s%s%s" % (col1,startdatum,ResetAll,col1,strnu,ResetAll))
                            elif maandcheck < maanden < maandcheck+36:
                                startdatum = int(str(int(strnu[:4])-3)+"{:0>2}".format(str(12+(maandcheck-maanden+24)))+"01")
                                print("Van %s%s%s tot %s%s%s" % (col1,startdatum,ResetAll,col1,strnu,ResetAll))
                            else:
                                startdatum = int(strnu[:4]+"{:0>2}".format(str(maandcheck))+"01")
                                print("Van %s%s%s tot %s%s%s" % (col1,startdatum,ResetAll,col1,strnu,ResetAll))
                        except(Exception) as error:
                            #print(error)
                            startdatum = int(strnu[:4]+"{:0>2}".format(str(maandcheck))+"01")
                            print("Van %s%s%s tot %s%s%s" % (col1,startdatum,ResetAll,col1,strnu,ResetAll))
                elif keuze2 == "4":
                    bereik = input("%sGeef het datumbereik op als \"YYYYMMDD-YYYYMMDD\"%s (of laat leeg)\n  : %s" % (col1,ResetAll,col1))
                    print(ResetAll, end = "")
                    if bereik.upper() in afsluitlijst:
                        break
                    else:
                        try:
                            startdatum = int(str(datetime.strptime(bereik[:8],"%Y%m%d"))[:10].replace("-",""))
                            einddatum = int(str(datetime.strptime(bereik[9:],"%Y%m%d"))[:10].replace("-",""))
                            print(col1+str(startdatum)+ResetAll+" - "+col1+str(einddatum)+ResetAll)
                        except(Exception) as error:
                            startdatum = 11111111
                            einddatum = 99999999
                            #print(error)
                elif keuze2 == "5":
                    dagsaldo = "Y"
                    dag = input("%sGeef de datum op als \"YYYYMMDD\"%s\n  : %s" % (col1,ResetAll,col1))
                    print(ResetAll, end = "")
                    if dag.upper() in afsluitlijst:
                        break
                    else:
                        try:
                            startdatum = int(str(datetime.strptime(dag[:8],"%Y%m%d"))[:10].replace("-",""))
                            einddatum = startdatum
                            print(col1+str(startdatum)+ResetAll+ResetAll)
                        except(Exception) as error:
                            startdatum = nu
                            einddatum = startdatum
                            #print(error)
                        for i in lijst:
                            try:
                                with open(i,"r") as f:
                                    inhoudvancategorie = ast.literal_eval(f.read())
                                    for j in inhoudvancategorie[1:]:
                                        if j[0] > einddatum:
                                            moni -= j[1]
                            except(Exception) as error:
                                #print(error)
                                pass

                else:
                    budgetcheck = "Y"
                    maanden = input("%sAantal maanden geleden%s (max 3 jr, mag ook \"0\" = deze maand zijn)\n  : %s" % (col1,ResetAll,col1))
                    print(ResetAll, end = "")
                    if maanden.upper() in afsluitlijst:
                        break
                    elif maanden == "":
                        maanden = 0
                    maandcheck = int(strnu[4:6])
                    try:
                        maanden = int(maanden)
                        if maanden < 0:
                            maanden = maanden * -1
                        if maanden <= maandcheck:
                            startdatum = int(strnu[:4]+"{:0>2}".format(str(maandcheck-int(maanden)))+"01")
                            einddatum = int(str(startdatum)[:6]+str(int(list(calendar.monthrange(int(str(startdatum)[:4]),int(str(startdatum)[4:6])))[1])))
                            print("Van %s%s%s tot %s%s%s" % (col1,startdatum,ResetAll,col1,einddatum,ResetAll))
                        elif maandcheck < maanden < maandcheck+12:
                            startdatum = int(str(int(strnu[:4])-1)+"{:0>2}".format(str(12+(maandcheck-maanden)))+"01")
                            einddatum = int(str(startdatum)[:6]+str(int(list(calendar.monthrange(int(str(startdatum)[:4]),int(str(startdatum)[4:6])))[1])))
                            print("Van %s%s%s tot %s%s%s" % (col1,startdatum,ResetAll,col1,strnu,ResetAll))
                        elif maandcheck < maanden < maandcheck+24:
                            startdatum = int(str(int(strnu[:4])-2)+"{:0>2}".format(str(12+(maandcheck-maanden+12)))+"01")
                            einddatum = int(str(startdatum)[:6]+str(int(list(calendar.monthrange(int(str(startdatum)[:4]),int(str(startdatum)[4:6])))[1])))
                            print("Van %s%s%s tot %s%s%s" % (col1,startdatum,ResetAll,col1,strnu,ResetAll))
                        elif maandcheck < maanden < maandcheck+36:
                            startdatum = int(str(int(strnu[:4])-3)+"{:0>2}".format(str(12+(maandcheck-maanden+24)))+"01")
                            einddatum = int(str(startdatum)[:6]+str(int(list(calendar.monthrange(int(str(startdatum)[:4]),int(str(startdatum)[4:6])))[1])))
                            print("Van %s%s%s tot %s%s%s" % (col1,startdatum,ResetAll,col1,strnu,ResetAll))
                        else:
                            startdatum = int(strnu[:4]+"{:0>2}".format(str(maandcheck-int(maanden)))+"01")
                            einddatum = int(str(startdatum)[:6]+str(int(list(calendar.monthrange(int(str(startdatum)[:4]),int(str(startdatum)[4:6])))[1])))
                            print("Van %s%s%s tot %s%s%s" % (col1,startdatum,ResetAll,col1,einddatum,ResetAll))
                    except(Exception) as error:
                        #print(error)
                        pass
                seldat = []
                for i in range(len(lijst)):
                    try:
                        with open(lijst[i],"r") as f:
                            cat = ast.literal_eval(f.read())
                            cat0 = cat[0]
                            cat1 = sorted(cat[1:])
                            for j in cat1:
                                if startdatum <= j[0] <= einddatum:
                                    j.append(lijst[i][-1].upper())
                                    seldat.append(j)
                    except(Exception) as error:
                        #print(error)
                        pass
                if budgetcheck == "Y":
                    maanddat = seldat
                    mcount = 0
                    mtot = 0.0
                    for i in maanddat:
                        mcount += 1
                        mtot += i[1]
                    if mtot >= 0:
                        colmtot = colgoed
                        mtot = colmtot+Valuta+fornum(mtot)+ResetAll
                    else:
                        colmtot = colslecht
                        mtot = colmtot+Valuta+fornum(mtot)+ResetAll
                    maandtotaallijst = {}
                    for i in lijst:
                        j1 = 0
                        for j in seldat:
                            if i in j[-1]:
                                j1 = j1 + j[1]
                                maandtotaallijst[i] = round(j1,2)
                            elif Nulregels == "Ja":
                                maandtotaallijst[i] = 0.0

                print("%sCategorie selecteren \"?\" of uitsluiten \"-?\"%s (optioneel)" % (col1,ResetAll))
                alt()
                keuze3 = input("  : ")
                selcat = []
                if keuze3.upper() in afsluitlijst:
                    break
                try:
                    if keuze3[0] != "-":
                        Katlijst = []
                        for j in seldat:
                            for i in keuze3:
                                if i.upper() in j[-1]:
                                    selcat.append(j)
                                    Katlijst.append(i.upper()) 
                                seldat = selcat
                        Katlijst= list(dict.fromkeys(Katlijst))
                        Kat = ", "+str(Katlijst).replace("[","").replace("]","").replace("\'","").replace(",","").replace(" ","")
                    elif keuze3[0] == "-" and len(keuze3) > 1:
                        Katlijst = []
                        for i in keuze3[1:]:
                            for j in seldat:
                                if i.upper() in j[-1]:
                                    selcat.append(j)
                                    Katlijst.append(i.upper()) 
                        for k in selcat:
                            seldat.remove(k)
                        Katlijst = list(dict.fromkeys(Katlijst))
                        Kat = ", zonder "+str(Katlijst).replace("[","").replace("]","").replace("\'","").replace(",","").replace(" ","")
                except(Exception) as error:
                    #print(error)
                    Kat = ""
                    pass
                seldat = sorted(seldat)
                sel = []
                keuze4 = input("%sSubselectie%s (optioneel)\n  1 bedrag\n  2 wederpartij\n  3 aantekening\n  : " % (col1,ResetAll))
                if keuze4.upper() in afsluitlijst:
                    break
                elif keuze4== "1":
                    sel3 = "bedrag"
                    bedrag = "N"
                    while bedrag == "N":
                        bedragv = input("Geef een bedrag \"%s##.##%s\" of bedragbereik \"%s##.## ##.##%s\" op\n  : " % (col1,ResetAll,col1,ResetAll)) 
                        if bedragv.upper() in afsluitlijst:
                            bedragv1 = -99999.99
                            bedragv2 = 99999.99
                            break
                        elif bedragv == "":
                            bedragv1 = -99999.99
                            bedragv2 = 99999.99
                            print(bedragv1,bedragv2)
                            bedrag = "Y"
                        else:
                            bedragv = " ".join(bedragv.split())
                            bereik = bedragv.split(" ")
                            if len(bereik) == 1:
                                try:
                                    bedragv1 = float(bereik[0])
                                    bedragv2 = bedragv1
                                    print(bedragv1,bedragv2)
                                    bedrag = "Y"
                                except(Exception) as error:
                                    #print(error)
                                    pass
                            else:
                                try:
                                    bedragv1 = float(bereik[0])
                                    bedragv2 = float(bereik[1])
                                    print(bedragv1,bedragv2)
                                    bedrag = "Y"
                                except(Exception) as error:
                                    #print(error)
                                    bedragv1 = -99999.99
                                    bedragv2 = 99999.99
                                    print(bedragv1,bedragv2)
                                    bedrag = "Y"
                    kop = ", %s van %s %s tot %s %s" % (sel3,Valuta,fornum(bedragv1),Valuta,fornum(bedragv2))
                    if bedragv1 == -99999.99 and bedragv2 == 99999.99:
                        kop = ", alle bedragen"
                    ID = 0
                    for i in seldat:
                        if bedragv1 <= i[1] <= bedragv2:
                            vier = i[4]+str(ID)
                            i.remove(i[4])
                            i.append(vier)
                            sel.append(i)
                            ID += 1
                elif keuze4 == "2":
                    sel3 = "wederpartij"
                    wederpartij = "N"
                    while wederpartij == "N":
                        wederpartijv = input("Geef een (deel van de) %swederpartij%s op\n  : " % (col1,ResetAll)).lower()
                        if wederpartijv.upper() in afsluitlijst:
                            wederpartijv = ""
                        wederpartij = "Y"
                    kop = ", %s *%s*" % (sel3,wederpartijv)
                    if wederpartijv == "":
                        kop = ", alle wederpartijen"
                    ID = 0
                    for i in seldat:
                        if wederpartijv in i[2].lower():
                            vier = i[4]+str(ID)
                            i.remove(i[4])
                            i.append(vier)
                            sel.append(i)
                            ID += 1
                elif keuze4 == "3":
                    sel3 = "aantekening"
                    aantekening = "N"
                    while aantekening == "N":
                        aantekeningv = input("Geef een (deel van de) %saantekening%s op\n  : " % (col1,ResetAll)).lower()
                        if aantekeningv.upper() in afsluitlijst:
                            aantekeningv = ""
                        aantekening = "Y"
                    kop = ", %s *%s*" % (sel3,aantekeningv)
                    if aantekeningv == "":
                        kop = ", alle aantekeningen"
                    ID = 0
                    for i in seldat:
                        if aantekeningv in i[3].lower():
                            vier = i[4]+str(ID)
                            i.remove(i[4])
                            i.append(vier)
                            sel.append(i)
                            ID += 1
                    kop = ", %s %s" % (sel3,aantekeningv)
                    if aantekeningv == "":
                        kop = ", alle aantekeningen"
                else:
                    sel3 = ""
                    kop = ", alles"
                    ID = 0
                    for i in seldat:
                        vier = i[4]+str(ID)
                        i.remove(i[4])
                        i.append(vier)
                        sel.append(i)
                        ID += 1

                # HIER KOMT DE TABEL

                print(toplijn)
                startdatumeinddatum = "%s-%s" % (startdatum,einddatum)
                if startdatum == 11111111 and einddatum == 99999999:
                    startdatumeinddatum = "alle data"
                print("|"+col1+forc68(startdatumeinddatum+Kat+kop)+ResetAll+"|")
                print(pluslijn)
                print("|"+col1+forc10("Datum")+ResetAll+"|"+col1+forc12("Bedrag")+ResetAll+"|"+col1+forc17("Wederpartij")+ResetAll+"|"+col1+forc20("Betreft")+ResetAll+"|"+col1+forc5("ID")+ResetAll+"|")
                print(pluslijn)
                for i in sel:
                    if i[1] < header['Ondermarkering']:
                        colc = colslecht+Omkeren
                    elif header['Ondermarkering'] <= i[1] < 0:
                        colc = colslecht
                    elif 0 <= i[1] < header['Bovenmarkering']:
                        colc = colgoed
                    else:
                        colc = colgoed+Omkeren
                    col = catcol[i[4][0]]
                    print("|",for8(str(i[0])),"|",colc+Valuta+ResetAll,fornum(i[1]),"|",for15(i[2]),"|",for18(i[3]),"|",col+for3(i[4])+ResetAll,"|")
                print(pluslijn)
                try:
                    mon = str(sel[0][0])[:6]
                except(Exception) as error:
                    #print(error)
                    mon = 0.0
                count = 0
                tot = 0.0
                for i in sel:
                    count += 1
                    tot += i[1]
                if tot >= 0:
                    coltot = colgoed
                    tot = coltot+Valuta+fornum(tot)+ResetAll
                else:
                    coltot = colslecht
                    tot = coltot+Valuta+fornum(tot)+ResetAll
                if count == 1:
                    regels = "regel"
                else:
                    regels = "regels"
                print(col1+forc80("Deze SELECTIE bevat %s %s voor een totaal van %s" % (str(count),regels,tot))+ResetAll)
                if budgetcheck == "Y":
                    try:
                        with open("alternatievenamen","r") as f:
                            alternatievenamenlijst = ast.literal_eval(f.read())
                            for k,v in alternatievenamenlijst.items():
                                with open(k,"r") as g:
                                    inhoudvancategorie = ast.literal_eval(g.read())
                                    budget = inhoudvancategorie[0]
                                    col = catcol[k]
                                    for i in maandtotaallijst:
                                        if k in i[-1]:
                                            if round(budget+maandtotaallijst[k],2) > 0.00:
                                                colsaldo = colgoed
                                            elif round(budget+maandtotaallijst[k],2) == 0.00:
                                                colsaldo = colonbepaald
                                            else:
                                                colsaldo = colslecht
                                            print(col+k,forc17(v),"bud %s" % (Valuta),fornum(budget),"Totaal %s" % (Valuta),fornum(maandtotaallijst[k])," Rest", colsaldo+Valuta,colsaldo+fornum(budget+maandtotaallijst[k]),ResetAll)
                        if mcount == 1:
                            regels = "regel"
                        else:
                            regels = "regels"
                        print(col1+forc80("Deze HELE MAAND bevat %s %s voor een totaal van %s" % (str(mcount),regels,mtot))+ResetAll)
                    except(Exception) as error:
                        print(colslecht+forc70("Er is geen rekening geselecteerd")+ResetAll)
                        #print(error)
                if dagsaldo == "Y":
                    print(col1+forc70("Dagsaldo op %s: %s %s" % (str(startdatum),Valuta,fornum(moni)))+ResetAll)
                bekijken = "N"
        print(toplijn)
        print()
    elif keuze1 == "2": # TOEVOEGEN
        print()
        col2 = LichtGroen
        keuze2 = input("%sNieuw item toevoegen of een kopie maken%s\n  1 %sNieuw%s\n  2 %sKopie%s\n  : %s" % (col2,ResetAll,col2,ResetAll,col2,ResetAll,col2))
        print(ResetAll, end = "")
        if keuze2.upper() in afsluitlijst:
            pass
        else:
            toe = "N"
            while toe == "N":
                if keuze2 == "2":
                    tekopieren = input("Welk ID wil je %skopieren%s\n  : " % (col2, ResetAll))
                    if tekopieren.upper() in afsluitlijst:
                        break
                    else:
                        try:
                            with open(tekopieren[0].upper(),"r") as f:
                                inhoudvancategorie = ast.literal_eval(f.read())
                            alternatievenaam = alternatievenamenlijst[tekopieren[0].upper()]
                            col = catcol[tekopieren[0].upper()]
                        except(Exception) as error:
                            #print(error)
                            pass
                        for i in sel:
                            if i[4] == tekopieren[0].upper()+tekopieren[1:]:
                                inhoudvancategorie.append(i[:4])
                                break
                        sortcat0 = inhoudvancategorie[0]
                        sortcat1 = sorted(inhoudvancategorie[1:])
                        inhoudvancategorie = [sortcat0]
                        for k in sortcat1:
                            inhoudvancategorie.append(k)
                        print("%s %s%d%s\n%s %s%s %s%s\n%s %s%s%s\n%s %s%s%s\n%s %s%s%s" % (for15("Datum: "),col2,i[0],ResetAll,for15("Bedrag: "),col2,Valuta,forn(i[1]),ResetAll,for15("Wederpartij: "),col2,i[2],ResetAll,for15("Betreft: "),col2,i[3],ResetAll,for15("Categorie: "),col,alternatievenaam,ResetAll))
                        with open(tekopieren[0].upper(),"w") as w:
                            print(inhoudvancategorie, file = w, end = "")
                    break
                else:
                    nieuw = []
                    try:
                        datum = input("%sDatum%s (YYYYMMDD) of %sCSV%s (datum,bedrag,wederpartij,betreft)\n  : %s" % (col2,ResetAll,col2,ResetAll,col2))
                        print(ResetAll, end = "")
                        if datum.upper() in afsluitlijst:
                            break
                        elif "," in datum:
                            csv = datum.split(",")
                            if len(csv) == 5:
                                try:
                                    csv = [csv[0],float(str(csv[1])+"."+str(csv[2])),csv[3],csv[4]]
                                except(Exception) as error:
                                    #print(error)
                                    break
                            if len(csv) == 4:
                                try:
                                    if csv[0] == "":
                                        csv[0] = strnu
                                    csv[0] = int(str(datetime.strptime(csv[0],"%Y%m%d")).replace("-","")[:8])
                                    if csv[1] == "":
                                        csv[1] = 0.0
                                    csv[1] = float(csv[1])
                                    if len(csv[2]) > 15:
                                        csv[2] = csv[2][:15]
                                    if len(csv[3]) > 18:
                                        csv[3] = csv[3][:18]
                                    for i in csv:
                                        nieuw.append(i)
                                except(Exception) as error:
                                    #print(error)
                                    pass
                            else:
                                break
                        else:
                            if datum == "":
                                datum = nu
                                print(col2+"    "+str(datum)+ResetAll)
                            else:
                                datumstr = datum.replace("-","").replace("/","").replace(" ","")
                                datum = int(str(datetime.strptime(datumstr,"%Y%m%d")).replace("-","")[:8])
                            nieuw.append(datum)
                            bedrag = input("%sBedrag%s\n  : %s" % (col2,ResetAll,col2)).replace(",",".").replace(Valuta,".").strip()
                            print(ResetAll, end = "")
                            if bedrag.upper() in afsluitlijst:
                                break
                            elif bedrag == "":
                                bedrag = 0.0
                                print(col2+"    "+forn(bedrag)+ResetAll)
                            else:
                                bedrag = float(bedrag)
                            nieuw.append(bedrag)
                            wederpartij = input("%sWederpartij%s\n  : %s" % (col2,ResetAll,col2))
                            print(ResetAll, end = "")
                            if wederpartij.upper() in afsluitlijst:
                                break
                            nieuw.append(wederpartij[:15])
                            betreft = input("%sBetreft%s\n  : %s" % (col2,ResetAll,col2))
                            print(ResetAll, end = "")
                            if betreft.upper() in afsluitlijst:
                                break
                            nieuw.append(betreft[:18])
                        print("%sCategorie%s (letter \"%s\"-\"%s\")" % (col2,ResetAll,lijst[0],lijst[-1]))
                        alt()
                        categorie = input("  : %s" % (col2))
                        print(ResetAll, end = "")
                        if categorie.upper() in afsluitlijst or categorie.upper() not in lijst:
                            break
                        else:
                            categorie = categorie.upper()
                        try:
                            with open(categorie,"r") as f:
                                inhoudvancategorie = ast.literal_eval(f.read())
                        except(Exception) as error:
                            #print(error)
                            nieuwecategorie = input("Geef de %snieuwe categorie%s %s een naam\n  : " % (col2,ResetAll,catcol[categorie]+categorie+ResetAll))
                            if nieuwecategorie.upper() in afsluitlijst:
                                break
                            else:
                                alternatievenamenlijst[categorie] = nieuwecategorie[:15].lower()
                                with open("alternatievenamen","w") as f:
                                    print(alternatievenamenlijst, file = f, end = "")
                                with open(categorie,"w") as f:
                                    print([0.0], file = f, end = "")
                                inhoudvancategorie = [0.0]
                        alternatievenaam = alternatievenamenlijst[categorie]
                        print(alternatievenaam)
                        col = catcol[categorie]
                        print("%s %s%d%s\n%s %s%s %s%s\n%s %s%s%s\n%s %s%s%s\n%s %s%s%s" % (for15("Datum: "),col2,nieuw[0],ResetAll,for15("Bedrag: "),col2,Valuta,forn(nieuw[1]),ResetAll,for15("Wederpartij: "),col2,nieuw[2],ResetAll,for15("Betreft: "),col2,nieuw[3],ResetAll,for15("Categorie: "),col,alternatievenaam,ResetAll))
                        inhoudvancategorie.append(nieuw)
                        inhoudvancategorie1 = sorted(inhoudvancategorie[1:])
                        inhoudvancategorie = [inhoudvancategorie[0]]
                        for i in inhoudvancategorie1:
                            inhoudvancategorie.append(i)
                        with open(categorie,"w") as f:
                            print(inhoudvancategorie, file = f, end = "")
                        toe = "Y"
                    except(Exception) as error:
                        #print(error)
                        break
        print()
        print(toplijn)
        print()
    elif keuze1 == "3": # WIJZIGEN
        print()
        col3 = LichtCyaan
        try:
            int(sel[0][0])
            wijzig = "N"
            while wijzig == "N":
                tewijzigen = input("Welk ID wil je %swijzigen%s\n  : %s" % (col3, ResetAll,col3))
                print(ResetAll, end = "")
                if tewijzigen.upper() in afsluitlijst:
                    del keuze1
                    break
                else:
                    if tewijzigen != "":
                        twloop = tewijzigen
                    elif tewijzigen == "":
                        try:
                            tewijzigen = twloop
                        except(Exception) as error:
                            #print(error)
                            pass
                    try:
                        with open(tewijzigen[0].upper(),"r") as f:
                            inhoudvancategorie = ast.literal_eval(f.read())
                        alternatievenaam = alternatievenamenlijst[tewijzigen[0].upper()]
                        col = catcol[tewijzigen[0].upper()]
                        for i in sel:
                            if i[4] == tewijzigen.upper():
                                wat = input("Wat wil je %swijzigen%s\n  %s1%s %s %s\n  %s2%s %s %s %s\n  %s3%s %s %s\n  %s4%s %s %s\n  %s5%s %s %s%s%s\n  : " % (col3,ResetAll,col3,ResetAll,for15("Datum:"),i[0],col3,ResetAll,for15("Bedrag:"),Valuta,i[1],col3,ResetAll,for15("Wederpartij:"),i[2],col3,ResetAll,for15("Betreft:"),i[3],col3,ResetAll,for15("Categorie:"),col,alternatievenaam,ResetAll))
                                if wat.upper() in afsluitlijst:
                                    break
                                elif wat == "1":
                                    try:
                                        datum = input("%sDatum%s (YYYYMMDD)\n  : %s" % (col3,ResetAll,col3))
                                        print(ResetAll, end = "")
                                        if datum.upper() in afsluitlijst:
                                            break
                                        elif datum == "":
                                            datum = nu
                                            print(col3+"    "+str(datum)+ResetAll)
                                        else:
                                            datumstr = datum.replace("-","").replace("/","").replace(" ","")
                                            datum = int(str(datetime.strptime(datumstr,"%Y%m%d")).replace("-","")[:8])
                                        for j in inhoudvancategorie[1:]:
                                            if i[:4] == j:
                                                inhoudvancategorie.remove(j)
                                                inhoudvancategorie.append([datum,i[1],i[2],i[3]])
                                                break
                                        with open(tewijzigen[0].upper(),"w") as f:
                                            print(inhoudvancategorie, file = f, end = "")
                                        print("%s %s%d%s\n%s %s%s %s%s\n%s %s%s%s\n%s %s%s%s\n%s %s%s%s" % (for15("Datum: "),col3,datum,ResetAll,for15("Bedrag: "),col3,Valuta,forn(i[1]),ResetAll,for15("Wederpartij: "),col3,i[2],ResetAll,for15("Betreft: "),col3,i[3],ResetAll,for15("Categorie: "),col,alternatievenaam,ResetAll))
                                    except(Exception) as error:
                                        #print(error)
                                        pass
                                elif wat == "2":
                                    try:
                                        bedrag = input("%sBedrag%s\n  : %s" % (col3,ResetAll,col3)).replace(",",".").replace(Valuta,".").strip()
                                        print(ResetAll, end = "")
                                        if bedrag.upper() in afsluitlijst:
                                            break
                                        elif bedrag == "":
                                            bedrag = 0.0
                                            print(col3+"    "+forn(bedrag)+ResetAll)
                                        elif bedrag == "+" or bedrag == "-":
                                            bedrag = i[1] * -1
                                        else:
                                            bedrag = float(bedrag)
                                        for j in inhoudvancategorie:
                                            if i[:4] == j:
                                                inhoudvancategorie.remove(j)
                                                i[1] = bedrag
                                                inhoudvancategorie.append(i[:4])
                                                break
                                        with open(tewijzigen[0].upper(),"w") as f:
                                            print(inhoudvancategorie, file = f, end = "")
                                        print("%s %s%d%s\n%s %s%s %s%s\n%s %s%s%s\n%s %s%s%s\n%s %s%s%s" % (for15("Datum: "),col3,i[0],ResetAll,for15("Bedrag: "),col3,Valuta,forn(bedrag),ResetAll,for15("Wederpartij: "),col3,i[2],ResetAll,for15("Betreft: "),col3,i[3],ResetAll,for15("Categorie: "),col,alternatievenaam,ResetAll))
                                    except(Exception) as error:
                                        #print(error)
                                        pass
                                elif wat == "3":
                                    wederpartij = input("%sWederpartij%s\n  : %s" % (col3,ResetAll,col3))
                                    print(ResetAll, end = "")
                                    if wederpartij.upper() in afsluitlijst:
                                        break
                                    for j in inhoudvancategorie:
                                        if i[:4] == j:
                                            inhoudvancategorie.remove(j)
                                            i[2] = wederpartij[:15]
                                            inhoudvancategorie.append(i[:4])
                                            break
                                    with open(tewijzigen[0].upper(),"w") as f:
                                        print(inhoudvancategorie, file = f, end = "")
                                        print("%s %s%d%s\n%s %s%s %s%s\n%s %s%s%s\n%s %s%s%s\n%s %s%s%s" % (for15("Datum: "),col3,i[0],ResetAll,for15("Bedrag: "),col3,Valuta,forn(i[1]),ResetAll,for15("Wederpartij: "),col3,wederpartij,ResetAll,for15("Betreft: "),col3,i[3],ResetAll,for15("Categorie: "),col,alternatievenaam,ResetAll))
                                elif wat == "4":
                                    betreft = input("%sBetreft%s\n  : %s" % (col3,ResetAll,col3))
                                    print(ResetAll, end = "")
                                    if betreft.upper() in afsluitlijst:
                                        break
                                    for j in inhoudvancategorie:
                                        if i[:4] == j:
                                            inhoudvancategorie.remove(j)
                                            i[3] = betreft[:18]
                                            inhoudvancategorie.append(i[:4])
                                            break
                                    with open(tewijzigen[0].upper(),"w") as f:
                                        print(inhoudvancategorie, file = f, end = "")
                                        print("%s %s%d%s\n%s %s%s %s%s\n%s %s%s%s\n%s %s%s%s\n%s %s%s%s" % (for15("Datum: "),col3,i[0],ResetAll,for15("Bedrag: "),col3,Valuta,forn(i[1]),ResetAll,for15("Wederpartij: "),col3,i[2],ResetAll,for15("Betreft: "),col3,betreft,ResetAll,for15("Categorie: "),col,alternatievenaam,ResetAll))
                                elif wat == "5":
                                    print("Naar welke categorie wil je %s overzetten" % (col+tewijzigen.upper()+ResetAll))
                                    alt()
                                    waar = input("  : ")
                                    if waar.upper() in afsluitlijst or waar.upper() not in lijst:
                                        break
                                    else:
                                        waar = waar.upper()
                                        try:
                                            with open(waar,"r") as f:
                                                inhoudvancategorie = ast.literal_eval(f.read())
                                        except(Exception) as error:
                                            #print(error)
                                            nieuwecategorie = input("Geef de %snieuwe categorie%s %s een naam\n  : " % (col3,ResetAll,catcol[waar]+waar+ResetAll))
                                            if nieuwecategorie.upper() in afsluitlijst:
                                                break
                                            else:
                                                alternatievenamenlijst[waar] = nieuwecategorie[:15].lower()
                                                with open("alternatievenamen","w") as f:
                                                    print(alternatievenamenlijst, file = f, end = "")
                                                with open(waar,"w") as f:
                                                    print([0.0], file = f, end = "")
                                                inhoudvancategorie = [0.0]
                                        alternatievenaam = alternatievenamenlijst[waar]
                                        print(catcol[waar]+"%s: " % waar+alternatievenaam+ResetAll)
                                        for i in sel:
                                            i4 = tewijzigen[0].upper()+tewijzigen[1:]
                                            if i4 == i[4]:
                                                inhoudvancategorie.append(i[:4])
                                                col = catcol[waar]
                                                print("%sHet ID is gewijzigd, genereer nieuwe %sID%s's!%s" % (colslecht,LichtGeel,colslecht,ResetAll))
                                                print("%s %s%d%s\n%s %s%s %s%s\n%s %s%s%s\n%s %s%s%s\n%s %s%s%s" % (for15("Datum: "),col3,i[0],ResetAll,for15("Bedrag: "),col3,Valuta,forn(i[1]),ResetAll,for15("Wederpartij: "),col3,i[2],ResetAll,for15("Betreft: "),col3,i[3],ResetAll,for15("Categorie: "),col,alternatievenaam,ResetAll))
                                                with open(waar.upper(),"w") as w:
                                                    print(inhoudvancategorie, file = w, end = "")
                                                with open(tewijzigen[0].upper(),"r") as r:
                                                    hierweg = ast.literal_eval(r.read())
                                                    hierweg.remove(i[:4])
                                                with open(tewijzigen[0].upper(),"w") as v:
                                                    print(hierweg, file = v, end = "")
                                                break
                    except(Exception) as error:
                        #print(error)
                        pass
                    print()
        except(Exception) as error:
            #print(error)
            print("%sEr is een ID nodig uit \"%s1 bekijken%s\"%s" % (colslecht,LichtGeel,colslecht,ResetAll))
        print()
        print(toplijn)
        print()
    elif keuze1 == "4": # VERWIJDEREN
        print()
        col4 = LichtRood
        try:
            int(sel[0][0])
            verwijder = "N"
            while verwijder == "N":
                teverwijderen = input("Welk ID wil je %sverwijderen%s\n  : " % (col4, ResetAll))
                if teverwijderen.upper() in afsluitlijst:
                    break
                else:
                    try:
                        with open(teverwijderen[0].upper(),"r") as f:
                            inhoudvancategorie = ast.literal_eval(f.read())
                        alternatievenaam = alternatievenamenlijst[teverwijderen[0].upper()]
                        col = catcol[teverwijderen[0].upper()]
                        for i in sel:
                            if i[4] == teverwijderen[0].upper()+teverwijderen[1:]:
                                wat = input("  %s %s\n  %s %s %s\n  %s %s\n  %s %s\n  %s %s\nBevestig\n  : %s" % (for15("Datum:"),col4+str(i[0])+ResetAll,for15("Bedrag:"),col4+Valuta,str(i[1])+ResetAll,for15("Wederpartij:"),col4+i[2]+ResetAll,for15("Betreft:"),col4+i[3]+ResetAll,for15("Categorie:"),col4+alternatievenaam,ResetAll))
                                if wat.upper() in jalijst:
                                    for j in inhoudvancategorie:
                                        if i[:4] == j:
                                            inhoudvancategorie.remove(j)
                                            break
                                    with open(teverwijderen[0].upper(),"w") as f:
                                        print(inhoudvancategorie, file = f, end = "")
                                        print("%sOK%s" % (col4,ResetAll))
                                    with open(teverwijderen[0].upper(),"w") as f:
                                        undo = input("(\"U\" voor \"undo\")")
                                        if undo.upper() == "U":
                                            inhoudvancategorie.append(j)
                                        print(inhoudvancategorie, file = f, end = "")
                                print()
                    except(Exception) as error:
                        #print(error)
                        pass
        except(Exception) as error:
            #print(error)
            print("%sEr is een ID nodig uit \"%s1 bekijken%s\"%s" % (colslecht,LichtGeel,colslecht,ResetAll))
        print()
        print(toplijn)
        print()
    elif keuze1 == "0": # BEHEER
        print()
        col5 = LichtMagenta
        beheer = "Y"
        while beheer == "Y":
            keuze2 = input("Maak een keuze\n  0 %sPrint versie en info%s\n >1 %sCategoriebeheer%s\n  2 %sWijzig rekeninggegevens%s\n  3 %sToon of verberg rekening%s\n  4 %sWissel van rekening%s(!)\n  5 %sNieuwe rekening toevoegen%s\n  6 %sVerwijder rekening%s\n  : " % (LichtGeel,ResetAll,LichtCyaan,ResetAll,Blauw,ResetAll,Geel,ResetAll,LichtMagenta,ResetAll,LichtGroen,ResetAll,LichtRood,ResetAll))
            if keuze2.upper() in afsluitlijst:
                break
            elif keuze2 == "2":
                if os.getcwd() == basismap:
                    print(colslecht+forc70("Er is geen rekening geselecteerd")+ResetAll)
                else:
                    headerloop = "Y"
                    while headerloop == "Y":
                        printheaderall()
                        hoe = header["Beschrijving"]
                        wie = header["Rekeninghouder"]
                        waar = header["Plaats"]
                        Valuta = header["Valuta"]
                        Nulregels = header["Nulregels"]
                        Ondermarkering = header["Ondermarkering"]
                        Bovenmarkering = header["Bovenmarkering"]
                        Kleur = header["Kleur"]
                        wat = input("Kies wat je wilt wijzigen\n  1 %sBeschrijving%s\n  2 %sRekeninghouder%s\n  3 %sPlaats%s\n  4 %sValuta%s\n  5 %sNulregels%s\n  6 %sOndermarkering%s\n  7 %sBovenmarkering%s\n  8 %sKleur%s\n  : " % (colslecht,ResetAll,colslecht,ResetAll,colslecht,ResetAll,colslecht,ResetAll,colslecht,ResetAll,colslecht,ResetAll,colslecht,ResetAll,colslecht,ResetAll))
                        if wat.upper() in afsluitlijst:
                            break
                        elif wat == "1":
                            hoe = input("Beschrijving\n  : %s" % (colgoed))
                            print(ResetAll, end = "")
                            if hoe.upper() in afsluitlijst:
                                break
                            header["Beschrijving"] = hoe
                        elif wat == "2":
                            wie = input("Rekeninghouder\n  : %s" % (colgoed))
                            print(ResetAll, end = "")
                            if wie.upper() in afsluitlijst:
                                break
                            header["Rekeninghouder"] = wie
                        elif wat == "3":
                            waar = input("Plaats\n  : %s" % (colgoed))
                            print(ResetAll, end = "")
                            if waar.upper() in afsluitlijst:
                                break
                            header["Plaats"] = waar
                        elif wat == "4":
                            Valuta = input("Valuta\n  : %s" % (colgoed))
                            print(ResetAll, end = "")
                            if Valuta.upper() in afsluitlijst:
                                break
                            header["Valuta"] = Valuta
                        elif wat == "5":
                            nuljanee = input("Nulregels\n  J Ja\n  N Nee\n  : %s" % (colgoed))
                            print(ResetAll, end = "")
                            if nuljanee.upper() in afsluitlijst:
                                break
                            elif nuljanee.upper() in jalijst:
                                header["Nulregels"] = "Ja"
                            else:
                                header["Nulregels"] = "Nee"
                        elif wat == "6":
                            Ondermarkering = input("Ondergrens voor markering %s\n  : %s" % (Omkeren+colslecht+Valuta+ResetAll,colgoed))
                            print(ResetAll, end = "")
                            if Ondermarkering.upper() in afsluitlijst:
                                break
                            else:
                                try:
                                    Ondermarkering = float(Ondermarkering)
                                except(Exception) as error:
                                    #print(error)
                                    Ondermarkering = header["Bovenmarkering"]*-1
                            header["Ondermarkering"] = Ondermarkering
                        elif wat == "7":
                            Bovenmarkering = input("Bovengrens voor markering %s\n  : %s" % (Omkeren+colgoed+Valuta+ResetAll,colgoed))
                            print(ResetAll, end = "")
                            if Bovenmarkering.upper() in afsluitlijst:
                                break
                            else:
                                try:
                                    Bovenmarkering = float(Bovenmarkering)
                                except(Exception) as error:
                                    #print(error)
                                    Bovenmarkering = header["Ondermarkering"]*-1
                            header["Bovenmarkering"] = Bovenmarkering
                        elif wat == "8":
                            Koeleur = input("Kleur\n%s  A Alles%s\n%s  C Categorie%s\n  M Mono\n%s  R %sR%se%sg%se%sn%sb%so%so%sg%s\n  : %s" % ("\033[95m","\033[0m","\033[31m","\033[0m","\033[45m","\033[41m","\033[43m","\033[103m","\033[42m","\033[44m","\033[45m","\033[41m","\033[43m","\033[103m","\033[0m",colgoed))
                            print(ResetAll, end = "")
                            if Koeleur.upper() in afsluitlijst:
                                break
                            elif Koeleur.upper() == "A":
                                header["Kleur"] = "Alle"
                            elif Koeleur.upper() == "C":
                                header["Kleur"] = "Categorie"
                            elif Koeleur.upper() == "M":
                                header["Kleur"] = "Mono"
                            elif Koeleur.upper() == "R":
                                header["Kleur"] = "Regenboog"
                        with open("header","w") as f:
                            print(header, file = f, end = "")
                        kleur = updatekleur()
                        Kleuren = kleur[0]
                        globals().update(Kleuren)
                        catcol = kleur[1]
            elif keuze2 == "3":
                if os.getcwd() == basismap:
                    print(colslecht+forc70("Er is geen rekening geselecteerd")+ResetAll)
                else:
                    os.chdir(basismap)
                    gtndrekeningenlijst = []
                    for d in os.listdir():
                        if "@" in d:
                            gtndrekeningenlijst.append(d.split("@"))
                    gtndrekeningenlijst = sorted(gtndrekeningenlijst)
                    vrbrgnrekeningenlijst = []
                    for d in os.listdir():
                        if "_" in d:
                            vrbrgnrekeningenlijst.append(d.split("_"))
                    vrbrgnrekeningenlijst = sorted(vrbrgnrekeningenlijst)
                    if len(vrbrgnrekeningenlijst) > 0:
                        print("%sVerborgen%s rekeningen:" % (colslecht,ResetAll))
                        for i in vrbrgnrekeningenlijst:
                            print("    "+colslecht+for20(i[0])+colonbepaald+i[1]+ResetAll)
                    if len(gtndrekeningenlijst) > 0:
                        print("%sGetoonde%s rekeningen:" % (colgoed,ResetAll))
                        reking = 1
                        for i in gtndrekeningenlijst:
                            print("    "+colgoed+for20(i[0])+colonbepaald+i[1]+ResetAll)
                            reking += 1
                    os.chdir(os.path.join(basismap,iban+"@"+jaar))
                    tov = input("Een %sverborgen rekening%s tonen of een %sgetoonde rekening%s verbergen\n  1 %stonen%s en ga erheen\n  2 %sverbergen%s\n  : %s" % (colslecht,ResetAll,colgoed,ResetAll,colgoed,ResetAll,colslecht,ResetAll,colgoed))
                    print(ResetAll, end = "")

                    if tov.upper() in afsluitlijst:
                        break
                    elif tov == "1":
                        os.chdir(basismap)
                        vrbrgnrekeningenlijst = []
                        for d in os.listdir():
                            if "_" in d:
                                vrbrgnrekeningenlijst.append(d.split("_"))
                        vrbrgnrekeningenlijst = sorted(vrbrgnrekeningenlijst)
                        if len(vrbrgnrekeningenlijst) == 0:
                            print("%sEr zijn geen verborgen rekeningen%s" % (colslecht,ResetAll))
                            os.chdir(os.path.join(basismap,iban+"@"+jaar))
                        else:
                            print("%sVerborgen%s rekeningen:" % (colslecht,ResetAll))
                            reking = 1
                            for i in vrbrgnrekeningenlijst:
                                print("  "+colslecht+for3(str(reking))+ResetAll+colgoed+for20(i[0])+colonbepaald+i[1]+ResetAll)
                                reking += 1
                            rekening = input("Kies een rekening\n%s  : %s" % (colslecht,colgoed))
                            print(ResetAll, end = "")
                            if rekening.upper() in afsluitlijst:
                                os.chdir(os.path.join(basismap,iban+"@"+jaar))
                                break
                            else:
                                try:
                                    toonrek = int(rekening)-1
                                    viban = vrbrgnrekeningenlijst[toonrek][0]
                                    vjaar = vrbrgnrekeningenlijst[toonrek][1]
                                    os.rename(os.path.join(basismap,viban+"_"+vjaar),os.path.join(basismap,viban+"@"+vjaar))
                                    os.chdir(os.path.join(basismap,viban+"@"+vjaar))
                                    with open("header","r") as h:
                                        header = ast.literal_eval(h.read())
                                    hoe = header["Beschrijving"]
                                    wie = header["Rekeninghouder"]
                                    waar = header["Plaats"]
                                    Valuta = header["Valuta"]
                                    Nulregels = header["Nulregels"]
                                    Ondermarkering = header["Ondermarkering"]
                                    Bovenmarkering = header["Bovenmarkering"]
                                    Kleur = header["Kleur"]
                                    kleur = updatekleur()
                                    Kleuren = kleur[0]
                                    globals().update(Kleuren)
                                    catcol = kleur[1]
                                    break
                                except(Exception) as error:
                                    os.chdir(os.path.join(basismap,iban+"@"+jaar))
                                    #print(error)
                                    #pass
                    elif tov == "2":
                        vrbrgn = "Y"
                        while vrbrgn == "Y":
                            os.chdir(basismap)
                            gtndrekeningenlijst = []
                            for d in os.listdir():
                                if "@" in d:
                                    gtndrekeningenlijst.append(d.split("@"))
                            gtndrekeningenlijst = sorted(gtndrekeningenlijst)
                            if len(gtndrekeningenlijst) == 1:
                                print("%sJe kunt niet de huidige rekening verbergen%s" % (colslecht,ResetAll))
                                os.chdir(os.path.join(basismap,iban+"@"+jaar))
                                break
                            else:
                                print("%sGetoonde%s rekeningen:" % (colgoed,ResetAll))
                                reking = 1
                                for i in gtndrekeningenlijst:
                                    print("  "+colslecht+for3(str(reking))+ResetAll+colgoed+for20(i[0])+colonbepaald+i[1]+ResetAll)
                                    reking += 1
                                rekening = input("Kies een rekening\n%s  : %s" % (colslecht,colgoed))
                                print(ResetAll, end = "")
                                if rekening.upper() in afsluitlijst:
                                    os.chdir(os.path.join(basismap,iban+"@"+jaar))
                                    break
                                else:
                                    try:
                                        toonrek = int(rekening)-1
                                        viban = gtndrekeningenlijst[toonrek][0]
                                        vjaar = gtndrekeningenlijst[toonrek][1]
                                        if viban == iban and vjaar == jaar:
                                            print("%sJe kunt niet de huidige rekening verbergen%s" % (colslecht,ResetAll))
                                            os.chdir(os.path.join(basismap,iban+"@"+jaar))
                                            break
                                        os.rename(os.path.join(basismap,viban+"@"+vjaar),os.path.join(basismap,viban+"_"+vjaar))
                                        os.chdir(os.path.join(basismap,iban+"@"+jaar))
                                        break
                                    except(Exception) as error:
                                        os.chdir(os.path.join(basismap,iban+"@"+jaar))
                                        #print(error)
                                        #pass
            elif keuze2 == "4":
                if os.getcwd() == basismap:
                    print(colslecht+forc70("Er is geen rekening geselecteerd")+ResetAll)
                else:
                    print("%sLET OP! Afbreken verlaat het programma%s" % (colslecht,ResetAll))
                    print("%sBeschikbare rekeningen:%s" % (colgoed,ResetAll))
                    rekeningenlijst = rknngnlst()
                    ibanjaar = rek()
                    iban = ibanjaar[0]
                    jaar = ibanjaar[1]
                    header = ibanjaar[2]
                    hoe = header["Beschrijving"]
                    wie = header["Rekeninghouder"]
                    waar = header["Plaats"]
                    Valuta = header["Valuta"]
                    Nulregels = header["Nulregels"]
                    Ondermarkering = header["Ondermarkering"]
                    Bovenmarkering = header["Bovenmarkering"]
                    Kleur = header["Kleur"]
                    kleur = updatekleur()
                    Kleuren = kleur[0]
                    globals().update(Kleuren)
                    catcol = kleur[1]
            elif keuze2 == "5":
                os.chdir(basismap)
                nieuwerekening()
                rekeningenlijst = rknngnlst()
                ibanjaar = rek()
                iban = ibanjaar[0]
                jaar = ibanjaar[1]
                header = ibanjaar[2]
                alternatievenamenlijst = ibanjaar[3]
                hoe = header["Beschrijving"]
                wie = header["Rekeninghouder"]
                waar = header["Plaats"]
                Valuta = header["Valuta"]
                Nulregels = header["Nulregels"]
                Ondermarkering = header["Ondermarkering"]
                Bovenmarkering = header["Bovenmarkering"]
                Kleur = header["Kleur"]
                kleur = updatekleur()
                Kleuren = kleur[0]
                globals().update(Kleuren)
                catcol = kleur[1]
            elif keuze2 == "6":
                if os.getcwd() == basismap:
                    print(colslecht+forc70("Er is geen rekening geselecteerd")+ResetAll)
                else:
                    os.chdir(basismap)
                    print("Kies een rekening")
                    rekeningenlijst = rknngnlst()
                    welk = input("  : ")
                    if welk.upper() in afsluitlijst:
                        os.chdir(os.path.join(basismap,iban+"@"+jaar))
                        break
                    try:
                        welk = int(welk)-1
                        viban = rekeningenlijst[welk][0]
                        vjaar = rekeningenlijst[welk][1]
                        if iban == viban and jaar == vjaar:
                            print("%sJe kunt niet de huidige rekening verwijderen%s" % (colslecht,ResetAll))
                            os.chdir(os.path.join(basismap,iban+"@"+jaar))
                            break
                        elif welk in range(len(rekeningenlijst)):
                            print(colslecht+rekeningenlijst[welk][0]+ResetAll)
                            try:
                                with open(rekeningenlijst[welk][0]+"@"+rekeningenlijst[welk][1]+str(os.path.sep)+"header","r") as h:
                                    headr = ast.literal_eval(h.read())
                                    for k,v in headr.items():
                                        print(colonbepaald+for15(k),":",colgoed+v+ResetAll)
                            except(Exception) as error:
                                #print(error)
                                pass
                            oknok = input("%sOK%s of %sNiet OK%s\n%s  1 OK%s\n%s >2 Niet OK%s\n  : " % (colgoed,ResetAll,colslecht,ResetAll,colgoed,ResetAll,colslecht,ResetAll))
                            if oknok == "1":
                                os.chdir(rekeningenlijst[welk][0]+"@"+rekeningenlijst[welk][1])
                                for f in os.listdir():
                                    os.remove(f)
                                os.chdir(basismap)
                                os.rmdir(rekeningenlijst[welk][0]+"@"+rekeningenlijst[welk][1])
                                rekeningenlijst.remove(rekeningenlijst[welk])
                                rekeningenlijst = rknngnlst()
                                os.chdir(os.path.join(basismap,iban+"@"+jaar))
                    except(Exception) as error:
                        #print(error)
                        os.chdir(os.path.join(basismap,iban+"@"+jaar))
            elif keuze2 == "0":
                input(versie)
                input(info1)
                print(info2)
                input(toplijn)
                print()
            elif keuze2 == "1" or keuze2 == "":
                if os.getcwd() == basismap:
                    print(colslecht+forc70("Er is geen rekening geselecteerd")+ResetAll)
                else:
                    catbeheer = "Y"
                    while catbeheer == "Y":
                        print("Kies een categorie")
                        alt()
                        kategorie = input("  : ")
                        if kategorie.upper() in afsluitlijst:
                            break
                        else:
                            if kategorie.upper() in lijst:
                                try:
                                    with open(kategorie.upper(),"r") as c:
                                        kat = ast.literal_eval(c.read())
                                        budget = kat[0]
                                    col = catcol[kategorie.upper()]
                                    wat = input("Kies\n  1 %sCategorienaam%s wijzigen (nu %s)\n  2 %sMaandbudget%s wijzigen (nu %s)\n  3 %sCategorie verwijderen%s\n  : " % (LichtCyaan,ResetAll,col+alternatievenamenlijst[kategorie.upper()]+ResetAll,LichtCyaan,ResetAll,col+Valuta+fornum(budget)+ResetAll,colslecht,ResetAll))
                                    if wat.upper() in afsluitlijst:
                                        break
                                    elif wat == "1":
                                        hoedan = input("Geef de nieuwe %scategorienaam%s (max 15)\n  : %s" % (LichtCyaan,ResetAll,col))
                                        print(ResetAll, end = "")
                                        if hoedan.upper() in afsluitlijst:
                                            break
                                        else:
                                            with open("alternatievenamen","w") as f:
                                                alternatievenamenlijst[kategorie.upper()] = hoedan.lower()[:15]
                                                print(alternatievenamenlijst, file = f, end = "")
                                    elif wat == "2":
                                        budlijst = []
                                        for k,v in alternatievenamenlijst.items():
                                            with open(k,"r") as f:
                                                cat = ast.literal_eval(f.read())
                                                budlijst.append(cat[0])
                                                print(k,forc17(v),Valuta,fornum(cat[0]))
                                        balans = 0
                                        for i in budlijst:
                                            balans += i 
                                        if balans == 0:
                                            colbal = colgoed
                                        else:
                                            colbal = colslecht
                                        print(colbal+forr19("BALANS ="),Valuta,fornum(round(balans,2))+ResetAll)
                                        hoeveeldan = input("Geef het nieuwe %smaandbudget%s voor %s: %s\n  : %s" % (LichtCyaan,ResetAll,col+kategorie.upper(),alternatievenamenlijst[kategorie.upper()]+ResetAll,col))
                                        print(ResetAll, end = "")
                                        if hoeveeldan.upper() in afsluitlijst:
                                            break
                                        else:
                                            try:
                                                kat[0] = float(hoeveeldan)
                                                with open(kategorie.upper(),"w") as f:
                                                    print(kat, file = f, end = "")
                                            except(Exception) as error:
                                                #print(error)
                                                pass
                                        budlijst = []
                                        for k,v in alternatievenamenlijst.items():
                                            with open(k,"r") as f:
                                                cat = ast.literal_eval(f.read())
                                                budlijst.append(cat[0])
                                        balans = 0
                                        for i in budlijst:
                                            balans += i 
                                        if balans == 0:
                                            colbal = colgoed
                                        else:
                                            colbal = colslecht
                                        print(colbal+forr19("BALANS ="),Valuta,fornum(round(balans,2))+ResetAll)

                                    elif wat == "3":
                                        oknok = input("%sOK%s of %sNiet OK%s\n%s  1 OK%s\n%s >2 Niet OK%s\n  : " % (colgoed,ResetAll,colslecht,ResetAll,colgoed,ResetAll,colslecht,ResetAll))
                                        if oknok == "1":
                                            os.remove(kategorie.upper())
                                            del alternatievenamenlijst[kategorie.upper()]
                                            with open("alternatievenamen","w") as f:
                                                print(alternatievenamenlijst, file = f, end = "")
                                except(Exception) as error:
                                    #print(error)
                                    pass
        print()
        print(toplijn)
        print()
