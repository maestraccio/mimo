#!/usr/bin/python3
import pathlib, os, ast, calendar
from time import sleep
from datetime import datetime, date, timedelta

bouw = "2.29"
plaats = "Amersfoort"
hardedatum = "20221219"

versie = """
Versie: %s
Auteur: Maestraccio
Contact: maestraccio@musician.org
%s %s

+-----""" % (bouw,plaats,hardedatum)
versieEN = """
Versione: %s
Writer: Maestraccio
Contact: maestraccio@musician.org
%s %s

+-----""" % (bouw,plaats,hardedatum)
versieIT = """
Versione: %s
Scrittore: Maestraccio
Recapiti: maestraccio@musician.org
%s %s

+-----""" % (bouw,plaats,hardedatum)
info1 = """
Iedere rekeningmapnaam bestaat uit een rekeningnummer en een jaartal.
In opzet bevat een map één kalenderjaar, hoewel het mogelijk is om
onbeperkt door te schrijven; dit is door de gebruiker vrij te bepalen.
In de rekeningmap worden standaard de volgende bestanden aangemaakt:
  - zes categoriebestanden "A"-"E" en "O" met de financiële mutaties
  - "alternatievenamen": de Nederlandse categorienamen bij die letters
  - "header": rekeninggegevens en rekeninggebonden weergaveopties

6 categorieën (uitbreid- en aanpasbaar):
A: saldo & inkomen: in principe positieve bedragen, budget negatief
B: vaste lasten   : verwachte en terugkerende uitgaven
C: boodschappen   : dagelijkse variabele uitgaven
D: reis & verblijf: reiskosten, brandstof, overnachtingen, enz.
E: leningen       : bedragen die worden voorgeschoten en terugbetaald
O: overig         : overige mutaties
Andere categorieën kunnen worden toegevoegd door een nieuwe mutatie 
toe te voegen of te wijzigen en toe te wijzen aan de nieuwe categorie.
Het aanpasbare startsaldo "0.0" staat in "A" op datum "11111111".

"header" bevat 10 items waarvan alleen de eerste drie worden getoond:
 1: Beschrijving
 2: Rekeninghouder
 3: Plaats
 4: Taal
 5: Valuta (standaard "€")
 6: Nulregels (standaard "Nee")
 7: Markering Laag >< Hoog (standaard "-100 >< 100")
 8: Kleur (standaard "Categorie")
 9: Datumformaat (standaard "JJJJMMDD")
10: Print maandoverzicht naar bestand (standaard "Nee")

+-----"""
info1EN = """
Every account folder name is formed by an account number and a year.
It is intended for details of one calendar year, although the user can
decide otherwise and continue adding details to the same folder. In
this account folder the following files are created by default:
  - six category files "A"-"E" and "O" with financial mutations
  - "alternatievenamen": the Dutch category names to those letters
  - "header": account details and account related interface options

6 categories (expandable and adjustable, translated from Dutch names):
A: funds & income : intentionally positive amounts, budget negative
B: fixed costs    : expected and repeated expenses
C: groceries      : daily variable expenses
D: travel & stay  : traveling costs, fuel, hotel stays, etc.
E: loans          : expenses to be returned and vice versa
O: other          : other mutations
Other categories can be added by adding a new mutation or making a
copy and assigning it to a new to be made category.
The customizable starting balance "0.0" is in "A" on date "11111111".

"header" contains 10 items of which only the first three are shown:
 1: Description
 2: Account holder
 3: City
 4: Language
 5: Currency (default "€")
 6: Zero lines (default "No")
 7: Marking Low >< High (default "-100 >< 100")
 8: Colour (default "Category")
 9: Date formatting (default "YYYYMMDD")
10: Print month overview to file (default "No")

+-----"""
info1IT = """
Il nome di ogni cartella del conto contiene un numero di conto ed un
anno. Questa cartella è destinata ad elementi di un anno solare,
sebbene l'utente possa decidere diversamente e continuare ad aggiun-
gere elementi nella stessa cartella. In questa cartella del conto
vengono creati i seguenti file per impostazione predefinita:
  - sei file di categoria "A"-"E" e "O" con mutazioni finanziarie
  - "alternatievenamen": i nomi delle categorie (NL) a queste lettere
  - "header": dettagli del conto ed opzioni dell'interfaccia relative
        al conto

6 categorie (espandibili e regolabili, nomi olandesi del file):
A: saldo & reddito: importi intenzionalmente positivi, budget negativo
B: costi fissi: spese previste e ripetute
C: spese: spese variabili giornaliere/alimentari
D: viaggioalloggio: spese di viaggio, carburante, soggiorni, ecc.
E: prestiti: spese da restituire e viceversa
O: altro: atre mutazioni
È possibile aggiungere altre categorie aggiungendo una nuova muta-
zione o effettuando a copiarla ed assegnarla ad una nuova categoria
da fare.
Il personalizzabile saldo iniziale "0.0" è in "A" su data "11111111".

"header" contiene 10 elementi di cui vengono mostrati solo i primi
tre:
 1: Descrizione
 2: Intestatario
 3: Città
 4: Lingua
 5: Valuta (predefinito "€")
 6: Linee a zero (predefinito "No")
 7: Indicazione Inferiore >< Superiore (predefinito "-100 >< 100")
 8: Colore (predefinito "Categoria")
 9: Formato data (predefinito "AAAAMMGG")
10: Stampa riepilogo mensile in file (predefinito "No") 

+-----"""
info2 = """
PROGRAMMASTRUCTUUR:

0 Beheer rekeningopties
    0 Print versie en info
    1 Categoriebeheer
        1 Categorienaam wijzigen
        2 Maandbudget wijzigen
        3 Categorie verwijderen
    2 Rekeninginstellingen aanpassen
        1 Beschrijving
        2 Rekeninghouder
        3 Plaats
        4 Taal (standaard = "NL")
        5 Valuta (standaard = "€")
        6 Nulregels (standaard "Nee")
        7 Markering Laag >< Hoog (Laag standaard omkering van Hoog)
        8 Kleur (standaard = "Categorie")
        9 Datumformaat (standaard = "JJJJMMDD")
        10: Print maandoverzicht naar bestand (standaard "Nee")
    3 Toon of verberg rekening
    4 Wissel van zichtbare rekening
    5 Nieuwe rekening toevoegen
    6 Verwijder rekening
    7 Instellingen overzetten
1 Mutaties bekijken
    Datumselectie -> Categorieselectie -> Subselectie -> Toon + ID
2 Mutatie toevoegen
    1 Nieuw
    2 Kopie naar vandaag
    3 Kopie naar andere rekening
3 Mutatie wijzigen
    1 Datum (standaard = vandaag)
    2 Bedrag (standaard = "0.0", "+" of "-" = omkering)
    3 Wederpartij
    4 Betreft
    5 Categorie
4 Mutatie verwijderen
5 Spaarpotten
    1 Bekijk spaarpotten
    2 Wijzig spaarpot
        1 Naam
        2 Waarde
    3 Voeg nieuwe spaarpot toe
    4 Verwijder spaarpot

Keuzes moeten worden bevestigd met "Enter".
"Terug" of "Verlaten" met "Q" (of "X").
"Terug naar hoofdmenu" met "QQ", "Nu afsluiten" met "QQQ".
"""
info2EN = """
PROGRAM STRUCTURE:

0 Manage account options
    0 Print version and info
    1 Category management
        1 Modify category name
        2 Modify month budget
        3 Remove category
    2 Alter account settings
        1 Description
        2 Account holder
        3 City
        4 Language (default "NL")
        5 Currency (default "€")
        6 Zero lines (default "No")
        7 Marking Lower >< Upper (by default one inversion of other)
        8 Colour (default = "Category")
        9 Date formatting (default = "YYYYMMDD")
        10: Print month overview to file (default "No")
    3 Show or hide account
    4 Switch visible account (!)
    5 Add new account
    6 Delete account
    7 Transfer account settings
1 View mutations
    Date selection -> Category selection -> Subselection -> Show + ID
2 Add mutation
    1 New
    2 Copy to today
    3 Copy to another account
3 Modify mutation
    1 Date (default = today)
    2 Amount (default = "0.0", "+" or "-" = opposite)
    3 Other party
    4 About
    5 Category
4 Remove mutation
5 Piggy banks
    1 View piggy banks
    2 Modify piggy bank
        1 Name
        2 Value
    3 Add new piggy bank
    4 Remove piggy bank

Choices must be confirmed with "Enter".
"Back" or "Abort" with "Q" (or "X").
"Back to main menu" with "QQ", "Exit now" with "QQQ".
"""
info2IT = """
STRUTTURA DEL PROGRAMMA:

0 Gestire opzioni del conto
    0 Print versione ed info
    1 Gestione categorie
        1 Modificare nome di categoria
        2 Modificare budget mensile
        3 Eliminare categoria
    2 Modificare impostazioni del conto
        1 Descrizione
        2 Intestatario
        3 Città
        4 Lingua (predefinito "NL")
        5 Valuta (predefinito "€")
        6 Linee a zero (predefinito "No")
        7 Indicazione Inf. >< Sup. (Inf. predefinito inverso di Sup.)
        8 Colore (predefinito = "Categoria")
        9 Formato data (predefinito "AAAAMMGG")
        10: Stampa riepilogo mensile in file (predefinito "No") 
    3 Mostrare o nascondere conto
    4 Passare ad un altro conto visibile
    5 Aggiungere un nuovo conto
    6 Eliminare conto
    7 Trasferire impostazioni
1 Vedere mutazioni
    Selezione data > Selezione categoria > Sottoselezione > Mostra+ID
2 Aggiungere mutazione
    1 Nuova
    2 Copia colla data di oggi
    3 Copia su un altro conto
3 Modificare mutazione
    1 Data (impostazione predefinita = oggi)
    2 Somma (predefinito = "0.0", "+" o "-" = inversione)
    3 Controparte
    4 Riguarda
    5 Categoria
4 Rimuovere mutazione
5 Salvadanai
    1 Vedere salvadanai
    2 Modificare salvadanaio
        1 Nome
        2 Valore
    3 Aggiungere salvadanaio
    4 Rimuovere salvadanaio

Le scelte devono essere confermate con "Invio".
"Indietro" o "Annulla" con "Q" (o "X").
"Tornare al menu principale" con "QQ", "Uscire ora" con "QQQ".
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
forc5 = "{:^5}".format
forr7 = "{:>7}".format
for8 = "{:8}".format
forc10 = "{:^10}".format
forc12 = "{:^12}".format
for15 = "{:15}".format
forc15 = "{:^15}".format
forc17 = "{:^17}".format
for18 = "{:18}".format
forr19 = "{:>19}".format
for20 = "{:20}".format
forc20 = "{:^20}".format
forl20 = "{:<20}".format
forr20 = "{:>20}".format
forl25 = "{:<25}".format
forr25 = "{:>25}".format
forc68 = "{:^68}".format
forl35 = "{:<35}".format
forr35 = "{:>35}".format
forr37 = "{:>37}".format
forc70 = "{:^70}".format
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

def updatetaal():
    with open("header","r") as h:
        header = ast.literal_eval(h.read())
    return header["Taal"]

def updatedat():
    with open("header","r") as h:
        header = ast.literal_eval(h.read())
    return header["Datumformaat"]


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
    os.chdir(basismap)
    rek = "N"
    while rek == "N":
        rekening = input("%s  : %s" % (colslecht,colgoed))
        print(ResetAll, end = "")
        if rekening.upper() in afsluitlijst:
            break
        elif len(rekening) == 2 and rekening.upper()[0] in afsluitlijst and rekening.upper()[1] in afsluitlijst:
            break
        elif len(rekening) == 3 and rekening.upper()[0] in afsluitlijst and rekening.upper()[2] in afsluitlijst:
            doei()
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

            #            if formaat == "1":
            #                header["Datumformaat"] = "DDMMYYYY"
            #            elif formaat == "2":
            #                header["Datumformaat"] = "DD-MM-YY"
            #            elif formaat == "3":
            #                header["Datumformaat"] = "DD/MM/YY"
            #            elif formaat == "4":
            #                header["Datumformaat"] = "DDmmm\'YY"
            #            elif formaat == "5":
            #                header["Datumformaat"] = "DD-mmmYY"
            #            elif len(formaat) == 2 and formaat.upper()[0] in afsluitlijst and formaat.upper()[1] in afsluitlijst:
            #                headerloop = "Q"
            #                break
            #            elif len(formaat) == 3 and formaat.upper()[0] in afsluitlijst and formaat.upper()[2] in afsluitlijst:
            #                doei()
            #            else:
            #                header["Datumformaat"] = "YYYYMMDD"
def printheaderall():
    for k,v in header.items():
        if Taal == "EN":
            if k == "Markering L><H":
                v = header["Valuta"]+fornum(v[0])+ResetAll+" >< "+colgoed+header["Valuta"]+fornum(v[1])
            print(colslecht+for15(k.replace("Beschrijving","Description").replace("Rekeninghouder","Account holder").replace("Plaats","City").replace("Taal","Language").replace("Valuta","Currency").replace("Nulregels","Zero lines").replace("Markering L><H","Marking L><U").replace("Kleur","Colour").replace("Datumformaat","Date formatting").replace("Print","Print")),colonbepaald+":",colgoed+v+ResetAll)
        elif Taal == "IT":
            if k == "Markering L><H":
                v = header["Valuta"]+fornum(v[0])+ResetAll+" >< "+colgoed+header["Valuta"]+fornum(v[1])
            if k == "Datumformaat":
                v = v.replace("DDMMYYYY","GGMMAAAA").replace("DD-MM-YY","GG-MM-YY").replace("DD/MM/YY","GG/MM/AA").replace("DDmmm\'YY","GGmmm\'AA").replace("DD-mmmYY","GG-mmmAA").replace("YYYYMMDD","AAAAMMGG")
            print(colslecht+for15(k.replace("Beschrijving","Descrizione").replace("Rekeninghouder","Intestatario").replace("Plaats","Città").replace("Taal","Lingua").replace("Valuta","Valuta").replace("Nulregels","Linee a zero").replace("Markering L><H","Indicaz. I><S").replace("Kleur","Colore").replace("Datumformaat","Formato data").replace("Print","Stampa")),colonbepaald+":",colgoed+v+ResetAll)
        else:
            if k == "Markering L><H":
                v = header["Valuta"]+fornum(v[0])+ResetAll+" >< "+colgoed+header["Valuta"]+fornum(v[1])
            if k == "Datumformaat":
                v = v.replace("DDMMYYYY","DDMMJJJJ").replace("DD-MM-YY","DD-MM-JJ").replace("DD/MM/YY","DD/MM/JJ").replace("DDmmm\'YY","DDmmm\'JJ").replace("DD-mmmYY","DD-mmmJJ").replace("YYYYMMDD","JJJJMMDD")
            print(colslecht+for15(k),colonbepaald+":",colgoed+v+ResetAll)

def printheader():
    regel = 0
    for k,v in header.items():
        if Taal == "EN":
            if k == "Markering L><H":
                v = header["Valuta"]+fornum(v[0])+" >< "+header["Valuta"]+fornum(v[1])
            print(colslecht+for15(k.replace("Beschrijving","Description").replace("Rekeninghouder","Account holder").replace("Plaats","City").replace("Taal","Language").replace("Valuta","Currency").replace("Nulregels","Zero lines").replace("Markering L><H","Marking L><U").replace("Kleur","Colour").replace("Datumformaat","Date formatting").replace("Print","Print")),colonbepaald+":",colgoed+v+ResetAll)
        elif Taal == "IT":
            if k == "Markering L><H":
                v = header["Valuta"]+fornum(v[0])+" >< "+header["Valuta"]+fornum(v[1])
            if k == "Datumformaat":
                v = v.replace("DDMMYYYY","GGMMAAAA").replace("DD-MM-YY","GG-MM-YY").replace("DD/MM/YY","GG/MM/AA").replace("DDmmm\'YY","GGmmm\'AA").replace("DD-mmmYY","GG-mmmAA").replace("YYYYMMDD","AAAAMMGG")
            print(colslecht+for15(k.replace("Beschrijving","Descrizione").replace("Rekeninghouder","Intestatario").replace("Plaats","Città").replace("Taal","Lingua").replace("Valuta","Valuta").replace("Nulregels","Linee a zero").replace("Markering L><H","Indicaz. I><S").replace("Kleur","Colore").replace("Datumformaat","Formato data").replace("Print","Stampa")),colonbepaald+":",colgoed+v+ResetAll)
        else:
            if k == "Markering L><H":
                v = header["Valuta"]+fornum(v[0])+" >< "+header["Valuta"]+fornum(v[1])
            if k == "Datumformaat":
                v = v.replace("DDMMYYYY","DDMMJJJJ").replace("DD-MM-YY","DD-MM-JJ").replace("DD/MM/YY","DD/MM/JJ").replace("DDmmm\'YY","DDmmm\'JJ").replace("DD-mmmYY","DD-mmmJJ").replace("YYYYMMDD","JJJJMMDD")
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
                        if i[0] > int(strnu[:6]+"00"):
                            tot = tot + i[1]
                    budget = lengte[0]
                    col = catcol[k]
                    if Taal == "EN":
                        v = v.replace("saldo & inkomen","funds & income").replace("vaste lasten","fixed costs").replace("boodschappen","groceries").replace("reis & verblijf","travel & stay").replace("leningen","loans").replace("overig","other")
                    elif Taal == "IT":
                        v = v.replace("saldo & inkomen","saldo & reddito").replace("vaste lasten","costi fissi").replace("boodschappen","spese").replace("reis & verblijf","viaggioalloggio").replace("leningen","prestiti").replace("overig","altro")
                    print(col+forc70(forl20(k+": "+forc15(v))+forr20(Valuta+fornum(tot)+"/"+fornum(budget)))+ResetAll)
                    alternatievenamenlijst[k] = v
    except(Exception) as error:
        #print(error)
        pass

def nieuwerekening():
    Taal = updatetaal()
    os.chdir(basismap)
    nieuw = "Y"
    while nieuw == "Y":
        if Taal == "EN":
            nieuwetaal = input("Choose your %slanguage%s\n >1 NL\n  2 EN\n  3 IT\n  : %s" % (colgoed,ResetAll,colgoed))
        elif Taal == "IT":
            nieuwetaal = input("Scegli la tua %slingua%s\n >1 NL\n  2 EN\n  3 IT\n  : %s" % (colgoed,ResetAll,colgoed))
        else:
            nieuwetaal = input("Kies de %staal%s\n >1 NL\n  2 EN\n  3 IT\n  : %s" % (colgoed,ResetAll,colgoed))
        print(ResetAll, end = "")
        if nieuwetaal.upper() in afsluitlijst:
            break
        elif nieuwetaal == "2":
            Taal = "EN"
        elif nieuwetaal == "3":
            Taal = "IT"
        else:
            Taal = "NL"
        if Taal == "EN":
            nieuwiban = input("Enter the %saccount number%s (%sIBAN%s)\n  : %s" % (LichtGroen,ResetAll,LichtGroen,ResetAll,LichtGroen)).upper()
        elif Taal == "IT":
            nieuwiban = input("Inserisci il %snumero di conto%s (%sIBAN%s)\n  : %s" % (LichtGroen,ResetAll,LichtGroen,ResetAll,LichtGroen)).upper()
        else:
            nieuwiban = input("Geef het %srekeningnummer%s (%sIBAN%s)\n  : %s" % (LichtGroen,ResetAll,LichtGroen,ResetAll,LichtGroen)).upper()
        print(ResetAll, end = "")
        if nieuwiban.upper() in afsluitlijst:
            os.chdir(os.path.join(basismap,iban+"@"+jaar))
            break
        if Taal == "EN":
            nieuwjaar = input("Enter the %syear%s (%s\"YYYY\"%s)\n  : %s" % (LichtGroen,ResetAll,LichtGroen,ResetAll,LichtGroen)).upper()
        elif Taal == "IT":
            nieuwjaar = input("Inserisci l\'%sanno%s (%s\"AAAA\"%s)\n  : %s" % (LichtGroen,ResetAll,LichtGroen,ResetAll,LichtGroen)).upper()
        else:
            nieuwjaar = input("Geef het %sjaar%s (%s\"JJJJ\"%s)\n  : %s" % (LichtGroen,ResetAll,LichtGroen,ResetAll,LichtGroen)).upper()
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
        if Taal == "EN":
            print("New account: %s%s@%s%s" % (colgoed,nieuwiban,nieuwjaar,ResetAll))
        elif Taal == "IT":
            print("Nuovo conto: %s%s@%s%s" % (colgoed,nieuwiban,nieuwjaar,ResetAll))
        else:
            print("Nieuwe rekening: %s%s@%s%s" % (colgoed,nieuwiban,nieuwjaar,ResetAll))
        os.mkdir(nieuwiban+"@"+nieuwjaar)
        os.chdir(nieuwiban+"@"+nieuwjaar)
        nieuwheader = {'Beschrijving':'','Rekeninghouder':'','Plaats':'','Taal':Taal,'Valuta':'€', 'Nulregels':'Nee','Markering L><H': [-100,100],'Kleur':'Categorie','Datumformaat':'YYYYMMDD','Print':'Nee'}
        with open("header","w") as f:
            print(nieuwheader, file = f, end = "")
        nieuwalternatievenamenlijst = {'A':'saldo & inkomen','B':'vaste lasten','C':'boodschappen','D':'reis & verblijf','E':'leningen','O':'overig'}
        with open("alternatievenamen","w") as g:
            print(nieuwalternatievenamenlijst, file = g, end = "")
        for k,v in nieuwalternatievenamenlijst.items():
            with open(k,"w") as h:
                print([0.0], file = h, end = "")
        with open("A","w") as w:
            if Taal == "EN":
                print([0.0, [11111111, 0.0, "Balance", "StartingBalance"]], file = w, end = "")
            elif Taal == "IT":
                print([0.0, [11111111, 0.0, "Saldo", "SaldoIniziale"]], file = w, end = "")
            else:
                print([0.0, [11111111, 0.0, "Saldo", "Startsaldo"]], file = w, end = "")
        nieuw = "N"
    os.chdir(basismap)

def doei():
    print()
    try:
        if Taal == "EN":
            print(coltekst+forc70("Thank you for having used mimo an have a nice day")+ResetAll)
        elif Taal == "IT":
            print(coltekst+forc70("Grazie per aver usato mimo ed una buona giornata")+ResetAll)
        else:
            print(coltekst+forc70("Bedankt voor het gebruiken van mimo en nog een fijne dag")+ResetAll)
    except:
        pass
    print(toplijn)
    print()
    exit()

##### Eerst moet je een rekening selecteren of aanmaken #####

print()
rekeningenlijst = rknngnlst()
if len(rekeningenlijst) == 0:
    nieuwetaal = input("Choose your language\n >1 NL\n  2 EN\n  3 IT\n  : %s" % (colgoed))
    print(ResetAll, end = "")
    if nieuwetaal.upper() in afsluitlijst:
        doei()
    elif nieuwetaal == "2":
        Taal = "EN"
    elif nieuwetaal == "3":
        Taal = "IT"
    else:
        Taal = "NL"
    if Taal == "EN":
        input(info1EN)
        print(info2EN)
        input(toplijn)
        print()
    elif Taal == "IT":
        input(info1IT)
        print(info2IT)
        input(toplijn)
        print()
    else:
        input(info1)
        print(info2)
        input(toplijn)
        print()
    if Taal == "EN":
        nieuwiban = input("Enter the %saccount number%s (%sIBAN%s)\n  : %s" % (LichtGroen,ResetAll,LichtGroen,ResetAll,LichtGroen)).upper()
    elif Taal == "IT":
        nieuwiban = input("Inserisci il %snumero di conto%s (%sIBAN%s)\n  : %s" % (LichtGroen,ResetAll,LichtGroen,ResetAll,LichtGroen)).upper()
    else:
        nieuwiban = input("Geef het %srekeningnummer%s (%sIBAN%s)\n  : %s" % (LichtGroen,ResetAll,LichtGroen,ResetAll,LichtGroen)).upper()
    print(ResetAll, end = "")
    if nieuwiban.upper() in afsluitlijst:
        doei()
    if Taal == "EN":
        nieuwjaar = input("Enter the %syear%s (%s\"YYYY\"%s)\n  : %s" % (LichtGroen,ResetAll,LichtGroen,ResetAll,LichtGroen)).upper()
    elif Taal == "IT":
        nieuwjaar = input("Inserisci l\'%sanno%s (%s\"AAAA\"%s)\n  : %s" % (LichtGroen,ResetAll,LichtGroen,ResetAll,LichtGroen)).upper()
    else:
        nieuwjaar = input("Geef het %sjaar%s (%s\"JJJJ\"%s)\n  : %s" % (LichtGroen,ResetAll,LichtGroen,ResetAll,LichtGroen)).upper()
    print(ResetAll, end = "")
    if nieuwjaar.upper() in afsluitlijst:
        doei()
    try:
        if int(nieuwjaar) < 1000 or int(nieuwjaar) > 9999:
            nieuwjaar = strnu[:4]
    except(Exception) as error:
        #print(error)
        nieuwjaar = strnu[:4]
    if Taal == "EN":
        print("New account: %s%s@%s%s" % (colgoed,nieuwiban,nieuwjaar,ResetAll))
    elif Taal == "IT":
        print("Nuovo conto: %s%s@%s%s" % (colgoed,nieuwiban,nieuwjaar,ResetAll))
    else:
        print("Nieuwe rekening: %s%s@%s%s" % (colgoed,nieuwiban,nieuwjaar,ResetAll))
    os.mkdir(nieuwiban+"@"+nieuwjaar)
    os.chdir(nieuwiban+"@"+nieuwjaar)
    nieuwheader = {'Beschrijving':'','Rekeninghouder':'','Plaats':'','Taal':Taal,'Valuta':'€','Nulregels':'Nee','Markering L><H':[-100,100],'Kleur':'Categorie','Datumformaat':'YYYYMMDD','Print':'Nee'}
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
    rekeningenlijst = [[nieuwiban,nieuwjaar]]
if len(rekeningenlijst) == 1:
    os.chdir(basismap)
    for d in os.listdir():
        if "@" in d:
            werkmap = os.path.join(basismap,d)
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
    Taal = updatetaal()
    kleur = updatekleur()
    Kleuren = kleur[0]
    globals().update(Kleuren)
    catcol = kleur[1]

##### Hier worden de standaarwaarden overschreven met de aangepaste waarden in header

try:
    with open("header","r") as h:
        header = ast.literal_eval(h.read())
    for k,v in header.items():
        k = v
    globals().update(header)
except(Exception) as error:
    #print(error)
    nieuwheader = {'Beschrijving':'','Rekeninghouder':'','Plaats':'','Taal':Taal,'Valuta':'€','Nulregels':'Nee','Markering L><H':[-100,100],'Kleur':'Categorie','Datumformaat':'YYYYMMDD','Print':'Nee'}
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
sel = []
mimo = "Y"
while mimo == "Y":
    strnu = str(date.today()).replace("-","") # hier haalt hij de datum van vandaag op, voor als het programma openstaat om middernacht
    nu = int(strnu)
    print(LichtGeel+forc70(nu)+ResetAll)
    Taal = updatetaal()
    Datumopmaak = updatedat()
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
    col5 = Groen
    try:
        spaartotaal = 0
        with open("A","r") as a:
            gebudgetteerd = ast.literal_eval(a.read())[0]*-1
        with open("spaarpotten","r") as s:
            spaar = ast.literal_eval(s.read())
            for i,j in spaar.items():
                spaartotaal += j
        if moni-spaartotaal < gebudgetteerd:
            col5 = Rood
            tekort = col5+Valuta+fornum(moni-gebudgetteerd-spaartotaal)+ResetAll
            if Taal == "EN":
                print(col5+forc70("You have dropped below recommended buffer size. Check your piggy banks.")+ResetAll)
                print(forr37("Total budget            : ")+Valuta+fornum(gebudgetteerd))
                print(forr37("Total in all piggy banks: ")+Valuta+fornum(spaartotaal))
                print(forr37("Short                   : ")+tekort)
            elif Taal == "IT":
                print(col5+forc70("Sei sceso sotto la cifra di buffer raccomandato. Controlla salvadanai.")+ResetAll)
                print(forr37("Totale budgettato         : ")+Valuta+fornum(gebudgetteerd))
                print(forr37("Totale di tutti salvadanai: ")+Valuta+fornum(spaartotaal))
                print(forr37("Disavanzo                 : ")+tekort)
            else:
                print(col5+forc70("Je bent onder je aanbevolen buffer gezakt. Controleer je spaarpotten.")+ResetAll)
                print(forr37("Totaal gebudgetteerd      : ")+Valuta+fornum(gebudgetteerd))
                print(forr37("Totaal in alle spaarpotten: ")+Valuta+fornum(spaartotaal))
                print(forr37("Tekort                    : ")+tekort)
            print()
    except(Exception) as error:
        print(error)
        pass
    if sel == []:
        col1 = LichtGeel
        dagen = 7
        startdatum = int(str(datetime.strptime(strnu,"%Y%m%d")-timedelta(days = dagen))[:10].replace("-",""))
        einddatum = nu
        index = 0
        for i in range(len(lijst)):
            try:
                with open(lijst[i],"r") as f:
                    cat = ast.literal_eval(f.read())
                    cat1 = sorted(cat[1:])
                    for j in cat1:
                        if startdatum <= j[0] <= einddatum:
                            j.append(lijst[i][-1].upper()+str(index))
                            sel.append(j)
                            index += 1
            except(Exception) as error:
                #print(error)
                pass
        sel = sorted(sel)
        print(toplijn)
        startdatumeinddatum = "%s-%s" % (startdatum,einddatum)
        print("|"+col1+forc68(startdatumeinddatum)+ResetAll+"|")
        print(pluslijn)
        if Taal == "EN":
            print("|"+col1+forc10("Date")+ResetAll+"|"+col1+forc12("Amount")+ResetAll+"|"+col1+forc17("Other party")+ResetAll+"|"+col1+forc20("About")+ResetAll+"|"+col1+forc5("ID")+ResetAll+"|")
        elif Taal == "IT":
            print("|"+col1+forc10("Data")+ResetAll+"|"+col1+forc12("Somma")+ResetAll+"|"+col1+forc17("Controparte")+ResetAll+"|"+col1+forc20("Riguarda")+ResetAll+"|"+col1+forc5("ID")+ResetAll+"|")
        else:
            print("|"+col1+forc10("Datum")+ResetAll+"|"+col1+forc12("Bedrag")+ResetAll+"|"+col1+forc17("Wederpartij")+ResetAll+"|"+col1+forc20("Betreft")+ResetAll+"|"+col1+forc5("ID")+ResetAll+"|")
        print(pluslijn)
        for i in sel:
            if i[1] <= header['Markering L><H'][0]:
                colc = colslecht+Omkeren
            elif header['Markering L><H'][0] <= i[1] < 0:
                colc = colslecht
            elif 0 <= i[1] < header['Markering L><H'][1]:
                colc = colgoed
            else:
                colc = colgoed+Omkeren
            col = catcol[i[4][0]]
            yymd = i[0]
            if Datumformaat == "DDMMYYYY":
                yymd = str(yymd)[6:]+str(yymd)[4:6]+str(yymd)[:4]
            elif Datumformaat == "DD-MM-YY":
                yymd = str(yymd)[6:]+"-"+str(yymd)[4:6]+"-"+str(yymd)[2:4]
            elif Datumformaat == "DD/MM/YY":
                yymd = str(yymd)[6:]+"/"+str(yymd)[4:6]+"/"+str(yymd)[2:4]
            elif Datumformaat == "DD-mmmYY":
                if Taal == "EN":
                    yymd = str(yymd)[6:]+"-"+str(yymd)[4:6].replace("01","Jan").replace("02","Feb").replace("03","Mar").replace("04","Apr").replace("05","May").replace("06","Jun").replace("07","Jul").replace("08","Aug").replace("09","Sep").replace("10","Oct").replace("11","Nov").replace("12","Dec")+str(yymd)[2:4]
                elif Taal == "IT":
                    yymd = str(yymd)[6:]+"-"+str(yymd)[4:6].replace("01","gen").replace("02","feb").replace("03","mar").replace("04","apr").replace("05","mag").replace("06","giu").replace("07","lug").replace("08","ago").replace("09","set").replace("10","ott").replace("11","nov").replace("12","dic")+str(yymd)[2:4]
                else:
                    yymd = str(yymd)[6:]+"-"+str(yymd)[4:6].replace("01","jan").replace("02","feb").replace("03","mrt").replace("04","apr").replace("05","mei").replace("06","jun").replace("07","jul").replace("08","aug").replace("09","sep").replace("10","okt").replace("11","nov").replace("12","dec")+str(yymd)[2:4]
            elif Datumformaat == "DDmmm\'YY":
                if Taal == "EN":
                    yymd = str(yymd)[6:]+str(yymd)[4:6].replace("01","Jan").replace("02","Feb").replace("03","Mar").replace("04","Apr").replace("05","May").replace("06","Jun").replace("07","Jul").replace("08","Aug").replace("09","Sep").replace("10","Oct").replace("11","Nov").replace("12","Dec")+"'"+str(yymd)[2:4]
                elif Taal == "IT":
                    yymd = str(yymd)[6:]+str(yymd)[4:6].replace("01","gen").replace("02","feb").replace("03","mar").replace("04","apr").replace("05","mag").replace("06","giu").replace("07","lug").replace("08","ago").replace("09","set").replace("10","ott").replace("11","nov").replace("12","dic")+"'"+str(yymd)[2:4]
                else:
                    yymd = str(yymd)[6:]+str(yymd)[4:6].replace("01","jan").replace("02","feb").replace("03","mrt").replace("04","apr").replace("05","mei").replace("06","jun").replace("07","jul").replace("08","aug").replace("09","sep").replace("10","okt").replace("11","nov").replace("12","dec")+"'"+str(yymd)[2:4]
            print("|",for8(str(yymd)),"|",colc+Valuta+ResetAll,fornum(i[1]),"|",for15(i[2]),"|",for18(i[3]),"|",col+for3(i[4])+ResetAll,"|")
        print(pluslijn)
        print()

##### Hier volgt het eerste keuzemenu #####

    if Taal == "EN":
        keuze1 = input("Make a choice\n%s  0 Manage account options%s\n%s >1 View mutations%s\n%s  2 Add mutation%s\n%s  3 Modify mutation%s\n%s  4 Remove mutation%s\n%s  5 Piggy banks%s\n  : " % (LichtMagenta,ResetAll,LichtGeel,ResetAll,LichtGroen,ResetAll,LichtCyaan,ResetAll,LichtRood,ResetAll,col5,ResetAll))
    elif Taal == "IT":
        keuze1 = input("Scegli\n%s  0 Gestire opzioni del conto%s\n%s >1 Vedere mutazioni%s\n%s  2 Aggiungere mutazione%s\n%s  3 Modificare mutazione%s\n%s  4 Cancellare mutazione%s\n%s  5 Salvadanai%s\n  : " % (LichtMagenta,ResetAll,LichtGeel,ResetAll,LichtGroen,ResetAll,LichtCyaan,ResetAll,LichtRood,ResetAll,col5,ResetAll))
    else:
        keuze1 = input("Maak een keuze\n%s  0 Beheer rekeningopties%s\n%s >1 Mutaties bekijken%s\n%s  2 Mutatie toevoegen%s\n%s  3 Mutatie wijzigen%s\n%s  4 Mutatie verwijderen%s\n%s  5 Spaarpotten%s\n  : " % (LichtMagenta,ResetAll,LichtGeel,ResetAll,LichtGroen,ResetAll,LichtCyaan,ResetAll,LichtRood,ResetAll,col5,ResetAll))
    if keuze1.upper() in afsluitlijst:
        doei()
    elif len(keuze1) == 2 and keuze1.upper()[0] in afsluitlijst and keuze1.upper()[1] in afsluitlijst:
        pass
    elif len(keuze1) == 3 and keuze1.upper()[0] in afsluitlijst and keuze1.upper()[2] in afsluitlijst:
        doei()
    elif keuze1 == "1" or keuze1 == "": # BEKIJKEN
        print()
        bekijken = "Y"
        while bekijken == "Y":
            budgetcheck = "N"
            dagsaldo = "N"
            col1 = LichtGeel
            if Taal == "EN":
                keuze2 = input("%sSelect a date option%s\n >1 %sOne month%s (incl. budget analysis)\n  2 %sNumber of days ago%s till today\n  3 %sNumber of months ago%s till today\n  4 %sA date range%s YYYYMMDD-YYYYMMDD\n  5 %sOne day%s YYYYMMDD (incl. day balance)\n  : %s" % (col1,ResetAll,col1,ResetAll,col1,ResetAll,col1,ResetAll,col1,ResetAll,col1,ResetAll,col1))
            elif Taal == "IT":
                keuze2 = input("%sSeleziona data%s\n >1 %sUn mese%s (incl. analisi di budget)\n  2 %sNumero di giorni fa%s fino ad oggi\n  3 %sNumero di mesi fa%s fino ad oggi\n  4 %sUn intervallo di date%s AAAAMMGG-AAAAMMGG\n  5 %sUn giorno%s AAAAMMGG (incl. saldo giornaliero)\n  : %s" % (col1,ResetAll,col1,ResetAll,col1,ResetAll,col1,ResetAll,col1,ResetAll,col1,ResetAll,col1))
            else:
                keuze2 = input("%sMaak een datumselectie%s\n >1 %sÉén maand%s (incl. budgetanalyse)\n  2 %sAantal dagen geleden%s t/m vandaag\n  3 %sAantal maanden geleden%s t/m vandaag\n  4 %sEen datumbereik%s JJJJMMDD-JJJJMMDD\n  5 %sÉén dag%s JJJJMMDD (incl. dagsaldo)\n  : %s" % (col1,ResetAll,col1,ResetAll,col1,ResetAll,col1,ResetAll,col1,ResetAll,col1,ResetAll,col1))
            print(ResetAll, end = "")
            if keuze2.upper() in afsluitlijst:
                break
            elif len(keuze2) == 2 and keuze2.upper()[0] in afsluitlijst and keuze2.upper()[1] in afsluitlijst:
                break
            elif len(keuze2) == 3 and keuze2.upper()[0] in afsluitlijst and keuze2.upper()[2] in afsluitlijst:
                doei()
            else:
                if keuze2 == "2":
                    einddatum = nu
                    if Taal == "EN":
                        dagen = input("%sEnter the number of days%s\n  : %s" % (col1,ResetAll,col1))
                    elif Taal == "IT":
                        dagen = input("%sInserisci il numero di giorni%s\n  : %s" % (col1,ResetAll,col1))
                    else:
                        dagen = input("%sGeef het aantal dagen op%s\n  : %s" % (col1,ResetAll,col1))
                    print(ResetAll, end = "")
                    if dagen.upper() in afsluitlijst:
                        break
                    elif len(dagen) == 2 and dagen.upper()[0] in afsluitlijst and dagen.upper()[1] in afsluitlijst:
                        break
                    elif len(dagen) == 3 and dagen.upper()[0] in afsluitlijst and dagen.upper()[2] in afsluitlijst:
                        doei()
                    else:
                        try:
                            dagen = int(dagen)
                            startdatum = int(str(datetime.strptime(strnu,"%Y%m%d")-timedelta(days = dagen))[:10].replace("-",""))
                            if Taal == "EN":
                                print("From %s%s%s to %s%s%s" % (col1,startdatum,ResetAll,col1,einddatum,ResetAll))
                            elif Taal == "IT":
                                print("Da %s%s%s a %s%s%s" % (col1,startdatum,ResetAll,col1,einddatum,ResetAll))
                            else:
                                print("Van %s%s%s tot %s%s%s" % (col1,startdatum,ResetAll,col1,einddatum,ResetAll))
                            aantaldagen = "Y"
                        except(Exception) as error:
                            #print(error)
                            dagen = 7
                            startdatum = int(str(datetime.strptime(strnu,"%Y%m%d")-timedelta(days = dagen))[:10].replace("-",""))
                            if Taal == "EN":
                                print("From %s%s%s to %s%s%s" % (col1,startdatum,ResetAll,col1,einddatum,ResetAll))
                            elif Taal == "IT":
                                print("Da %s%s%s a %s%s%s" % (col1,startdatum,ResetAll,col1,einddatum,ResetAll))
                            else:
                                print("Van %s%s%s tot %s%s%s" % (col1,startdatum,ResetAll,col1,einddatum,ResetAll))
                            aantaldagen = "Y"
                elif keuze2 == "3":
                    einddatum = nu
                    if Taal == "EN":
                        maanden = input("%sEnter the number of months%s\n  : %s" % (col1,ResetAll,col1))
                    elif Taal == "IT":
                        maanden = input("%sInserisci il numero di mesi%s\n  : %s" % (col1,ResetAll,col1))
                    else:
                        maanden = input("%sGeef het aantal maanden op%s (max 3 jr)\n  : %s" % (col1,ResetAll,col1))
                    print(ResetAll, end = "")
                    if maanden.upper() in afsluitlijst:
                        break
                    elif len(maanden) == 2 and maanden.upper()[0] in afsluitlijst and maanden.upper()[1] in afsluitlijst:
                        break
                    elif len(maanden) == 3 and maanden.upper()[0] in afsluitlijst and maanden.upper()[2] in afsluitlijst:
                        doei()
                    else:
                        maandcheck = int(strnu[4:6])
                        try:
                            maanden = int(maanden)
                            if maanden < 0:
                                startdatum = int(strnu[:4]+"{:0>2}".format(str(maandcheck))+"01")
                                if Taal == "EN":
                                    print("From %s%s%s to %s%s%s" % (col1,startdatum,ResetAll,col1,strnu,ResetAll))
                                elif Taal == "IT":
                                    print("Da %s%s%s a %s%s%s" % (col1,startdatum,ResetAll,col1,strnu,ResetAll))
                                else:
                                    print("Van %s%s%s tot %s%s%s" % (col1,startdatum,ResetAll,col1,strnu,ResetAll))
                            elif maanden <= maandcheck:
                                startdatum = int(strnu[:4]+"{:0>2}".format(str(maandcheck-int(maanden)))+"01")
                                if Taal == "EN":
                                    print("From %s%s%s to %s%s%s" % (col1,startdatum,ResetAll,col1,strnu,ResetAll))
                                elif Taal == "IT":
                                    print("Da %s%s%s a %s%s%s" % (col1,startdatum,ResetAll,col1,strnu,ResetAll))
                                else:
                                    print("Van %s%s%s tot %s%s%s" % (col1,startdatum,ResetAll,col1,strnu,ResetAll))
                            elif maandcheck < maanden < maandcheck+12:
                                startdatum = int(str(int(strnu[:4])-1)+"{:0>2}".format(str(12+(maandcheck-maanden)))+"01")
                                if Taal == "EN":
                                    print("From %s%s%s to %s%s%s" % (col1,startdatum,ResetAll,col1,strnu,ResetAll))
                                elif Taal == "IT":
                                    print("Da %s%s%s a %s%s%s" % (col1,startdatum,ResetAll,col1,strnu,ResetAll))
                                else:
                                    print("Van %s%s%s tot %s%s%s" % (col1,startdatum,ResetAll,col1,strnu,ResetAll))
                            elif maandcheck < maanden < maandcheck+24:
                                startdatum = int(str(int(strnu[:4])-2)+"{:0>2}".format(str(12+(maandcheck-maanden+12)))+"01")
                                if Taal == "EN":
                                    print("From %s%s%s to %s%s%s" % (col1,startdatum,ResetAll,col1,strnu,ResetAll))
                                elif Taal == "IT":
                                    print("Da %s%s%s a %s%s%s" % (col1,startdatum,ResetAll,col1,strnu,ResetAll))
                                else:
                                    print("Van %s%s%s tot %s%s%s" % (col1,startdatum,ResetAll,col1,strnu,ResetAll))
                            elif maandcheck < maanden < maandcheck+36:
                                startdatum = int(str(int(strnu[:4])-3)+"{:0>2}".format(str(12+(maandcheck-maanden+24)))+"01")
                                if Taal == "EN":
                                    print("From %s%s%s to %s%s%s" % (col1,startdatum,ResetAll,col1,strnu,ResetAll))
                                elif Taal == "IT":
                                    print("Da %s%s%s a %s%s%s" % (col1,startdatum,ResetAll,col1,strnu,ResetAll))
                                else:
                                    print("Van %s%s%s tot %s%s%s" % (col1,startdatum,ResetAll,col1,strnu,ResetAll))
                            else:
                                startdatum = int(strnu[:4]+"{:0>2}".format(str(maandcheck))+"01")
                                if Taal == "EN":
                                    print("From %s%s%s to %s%s%s" % (col1,startdatum,ResetAll,col1,strnu,ResetAll))
                                elif Taal == "IT":
                                    print("Da %s%s%s a %s%s%s" % (col1,startdatum,ResetAll,col1,strnu,ResetAll))
                                else:
                                    print("Van %s%s%s tot %s%s%s" % (col1,startdatum,ResetAll,col1,strnu,ResetAll))
                        except(Exception) as error:
                            #print(error)
                            startdatum = int(strnu[:4]+"{:0>2}".format(str(maandcheck))+"01")
                            if Taal == "EN":
                                print("From %s%s%s to %s%s%s" % (col1,startdatum,ResetAll,col1,strnu,ResetAll))
                            elif Taal == "IT":
                                print("Da %s%s%s a %s%s%s" % (col1,startdatum,ResetAll,col1,strnu,ResetAll))
                            else:
                                print("Van %s%s%s tot %s%s%s" % (col1,startdatum,ResetAll,col1,strnu,ResetAll))
                elif keuze2 == "4":
                    if Taal == "EN":
                        bereik = input("%sEnter the date range like \"YYYYMMDD-YYYYMMDD\"%s\n  : %s" % (col1,ResetAll,col1))
                    elif Taal == "IT":
                        bereik = input("%sInserisci l\'intervallo come \"AAAAMMGG-AAAAMMGG\"%s\n  : %s" % (col1,ResetAll,col1))
                    else:
                        bereik = input("%sGeef het datumbereik op als \"JJJJMMDD-JJJJMMDD\"%s\n  : %s" % (col1,ResetAll,col1))
                    print(ResetAll, end = "")
                    if bereik.upper() in afsluitlijst:
                        break
                    elif len(bereik) == 2 and bereik.upper()[0] in afsluitlijst and bereik.upper()[1] in afsluitlijst:
                        break
                    elif len(bereik) == 3 and bereik.upper()[0] in afsluitlijst and bereik.upper()[2] in afsluitlijst:
                        doei()
                    else:
                        try:
                            if len(bereik) < 10:
                                startdatum = int(str(datetime.strptime(bereik[:8],"%Y%m%d"))[:10].replace("-",""))
                                einddatum = nu
                            else:
                                startdatum = int(str(datetime.strptime(bereik[:8],"%Y%m%d"))[:10].replace("-",""))
                                einddatum = int(str(datetime.strptime(bereik[9:],"%Y%m%d"))[:10].replace("-",""))
                            print(col1+str(startdatum)+ResetAll+" - "+col1+str(einddatum)+ResetAll)
                        except(Exception) as error:
                            startdatum = 11111112
                            einddatum = 99999999
                            print(col1+str(startdatum)+ResetAll+" - "+col1+str(einddatum)+ResetAll)
                            #print(error)
                        if startdatum == einddatum:
                            dagsaldo = "Y"
                elif keuze2 == "5":
                    dagsaldo = "Y"
                    if Taal == "EN":
                        dag = input("%sEnter the date like \"YYYYMMDD\"%s\n  : %s" % (col1,ResetAll,col1))
                    elif Taal == "IT":
                        dag = input("%sInserisci la data come \"AAAAMMGG\"%s\n  : %s" % (col1,ResetAll,col1))
                    else:
                        dag = input("%sGeef de datum op als \"JJJJMMDD\"%s\n  : %s" % (col1,ResetAll,col1))
                    print(ResetAll, end = "")
                    if dag.upper() in afsluitlijst:
                        break
                    elif len(dag) == 2 and dag.upper()[0] in afsluitlijst and dag.upper()[1] in afsluitlijst:
                        break
                    elif len(dag) == 3 and dag.upper()[0] in afsluitlijst and dag.upper()[2] in afsluitlijst:
                        doei()
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
                    if Taal == "EN":
                        maanden = input("%sNumber of months ago%s (max. 3 yrs)\n  : %s" % (col1,ResetAll,col1))
                    elif Taal == "IT":
                        maanden = input("%sNumero di mesi fa%s (mass. 3 anni)\n  : %s" % (col1,ResetAll,col1))
                    else:
                        maanden = input("%sAantal maanden geleden%s (max. 3 jr)\n  : %s" % (col1,ResetAll,col1))
                    print(ResetAll, end = "")
                    if maanden.upper() in afsluitlijst:
                        break
                    elif len(maanden) == 2 and maanden.upper()[0] in afsluitlijst and maanden.upper()[1] in afsluitlijst:
                        break
                    elif len(maanden) == 3 and maanden.upper()[0] in afsluitlijst and maanden.upper()[2] in afsluitlijst:
                        doei()
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
                            if Taal == "EN":
                                print("From %s%s%s to %s%s%s" % (col1,startdatum,ResetAll,col1,einddatum,ResetAll))
                            elif Taal == "IT":
                                print("Da %s%s%s a %s%s%s" % (col1,startdatum,ResetAll,col1,einddatum,ResetAll))
                            else:
                                print("Van %s%s%s tot %s%s%s" % (col1,startdatum,ResetAll,col1,einddatum,ResetAll))
                        elif maandcheck < maanden < maandcheck+12:
                            startdatum = int(str(int(strnu[:4])-1)+"{:0>2}".format(str(12+(maandcheck-maanden)))+"01")
                            einddatum = int(str(startdatum)[:6]+str(int(list(calendar.monthrange(int(str(startdatum)[:4]),int(str(startdatum)[4:6])))[1])))
                            if Taal == "EN":
                                print("From %s%s%s to %s%s%s" % (col1,startdatum,ResetAll,col1,strnu,ResetAll))
                            elif Taal == "IT":
                                print("Da %s%s%s a %s%s%s" % (col1,startdatum,ResetAll,col1,strnu,ResetAll))
                            else:
                                print("Van %s%s%s tot %s%s%s" % (col1,startdatum,ResetAll,col1,strnu,ResetAll))
                        elif maandcheck < maanden < maandcheck+24:
                            startdatum = int(str(int(strnu[:4])-2)+"{:0>2}".format(str(12+(maandcheck-maanden+12)))+"01")
                            einddatum = int(str(startdatum)[:6]+str(int(list(calendar.monthrange(int(str(startdatum)[:4]),int(str(startdatum)[4:6])))[1])))
                            if Taal == "EN":
                                print("From %s%s%s to %s%s%s" % (col1,startdatum,ResetAll,col1,strnu,ResetAll))
                            elif Taal == "IT":
                                print("Da %s%s%s a %s%s%s" % (col1,startdatum,ResetAll,col1,strnu,ResetAll))
                            else:
                                print("Van %s%s%s tot %s%s%s" % (col1,startdatum,ResetAll,col1,strnu,ResetAll))
                        elif maandcheck < maanden < maandcheck+36:
                            startdatum = int(str(int(strnu[:4])-3)+"{:0>2}".format(str(12+(maandcheck-maanden+24)))+"01")
                            einddatum = int(str(startdatum)[:6]+str(int(list(calendar.monthrange(int(str(startdatum)[:4]),int(str(startdatum)[4:6])))[1])))
                            if Taal == "EN":
                                print("From %s%s%s to %s%s%s" % (col1,startdatum,ResetAll,col1,strnu,ResetAll))
                            elif Taal == "IT":
                                print("Da %s%s%s a %s%s%s" % (col1,startdatum,ResetAll,col1,strnu,ResetAll))
                            else:
                                print("Van %s%s%s tot %s%s%s" % (col1,startdatum,ResetAll,col1,strnu,ResetAll))
                        else:
                            startdatum = int(strnu[:4]+"{:0>2}".format(str(maandcheck-int(maanden)))+"01")
                            einddatum = int(str(startdatum)[:6]+str(int(list(calendar.monthrange(int(str(startdatum)[:4]),int(str(startdatum)[4:6])))[1])))
                            if Taal == "EN":
                                print("From %s%s%s to %s%s%s" % (col1,startdatum,ResetAll,col1,einddatum,ResetAll))
                            elif Taal == "IT":
                                print("Da %s%s%s a %s%s%s" % (col1,startdatum,ResetAll,col1,einddatum,ResetAll))
                            else:
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
                    mndtot = 0.0
                    for i in maanddat:
                        mcount += 1
                        mndtot += i[1]
                    if mndtot >= 0:
                        colmtot = colgoed
                    else:
                        colmtot = colslecht
                    mtot = colmtot+Valuta+fornum(mndtot)+ResetAll
                    maandtotaallijst = {}
                    if Nulregels == "Ja":
                        for k in alternatievenamenlijst:
                            maandtotaallijst[k] = 0.0
                    for i in lijst:
                        j1 = 0
                        for j in seldat:
                            if i in j[-1]:
                                j1 = j1 + j[1]
                                maandtotaallijst[i] = round(j1,2)

                if Taal == "EN":
                    print("%sCategory selection \"?\" or exclusion \"-?\"\nor all \"+\"%s to group by category" % (col1,ResetAll))
                elif Taal == "IT":
                    print("%sSeleziona categoria \"?\" o escludi \"-?\"\no tutte \"+\"%s per ragruppare per categoria" % (col1,ResetAll))
                else:
                    print("%sCategorie selecteren \"?\" of uitsluiten \"-?\"\nof alle \"+\"%s om te groeperen per categorie" % (col1,ResetAll))
                alt()
                keuze3 = input("  : ")
                katsel = "N"
                selcat = []
                if keuze3.upper() in afsluitlijst:
                    break
                elif len(keuze3) == 2 and keuze3.upper()[0] in afsluitlijst and keuze3.upper()[1] in afsluitlijst:
                    break
                elif len(keuze3) == 3 and keuze3.upper()[0] in afsluitlijst and keuze3.upper()[2] in afsluitlijst:
                    doei()
                elif keuze3 == "+":
                    keuze3 = "".join(map(str,lijst)) # voor copy-paste voor andere toepassingen map() toegevoegd (lijst is alleen str)
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
                        if Taal == "EN":
                            Kat = ", without "+str(Katlijst).replace("[","").replace("]","").replace("\'","").replace(",","").replace(" ","")
                        if Taal == "IT":
                            Kat = ", senza "+str(Katlijst).replace("[","").replace("]","").replace("\'","").replace(",","").replace(" ","")
                        else:
                            Kat = ", zonder "+str(Katlijst).replace("[","").replace("]","").replace("\'","").replace(",","").replace(" ","")
                    katsel = "Y"
                except(Exception) as error:
                    #print(error)
                    Kat = ""
                    pass
                if katsel == "N":
                    seldat = sorted(seldat)
                sel = []
                if Taal == "EN":
                    keuze4 = input("%sSubselection%s\n  1 Amount\n  2 Other party\n  3 Note\n  : " % (col1,ResetAll))
                elif Taal == "IT":
                    keuze4 = input("%sSottoselezione%s\n  1 Somma\n  2 Controparte\n  3 Annotazione\n  : " % (col1,ResetAll))
                else:
                    keuze4 = input("%sSubselectie%s\n  1 Bedrag\n  2 Wederpartij\n  3 Aantekening\n  : " % (col1,ResetAll))
                if keuze4.upper() in afsluitlijst:
                    break
                elif len(keuze4) == 2 and keuze4.upper()[0] in afsluitlijst and keuze4.upper()[1] in afsluitlijst:
                    break
                elif len(keuze4) == 3 and keuze4.upper()[0] in afsluitlijst and keuze4.upper()[2] in afsluitlijst:
                    doei()
                elif keuze4== "1":
                    sel3 = "bedrag"
                    bedrag = "N"
                    while bedrag == "N":
                        if Taal == "EN":
                            bedragv = input("Enter an amount \"%s##.##%s\" or amount range \"%s##.## ##.##%s\"\n  : " % (col1,ResetAll,col1,ResetAll)) 
                        elif Taal == "IT":
                            bedragv = input("Inserisci una somma \"%s##.##%s\" o intervallo di somme \"%s##.## ##.##%s\"\n  : " % (col1,ResetAll,col1,ResetAll)) 
                        else:
                            bedragv = input("Geef een bedrag \"%s##.##%s\" of bedragbereik \"%s##.## ##.##%s\" op\n  : " % (col1,ResetAll,col1,ResetAll)) 
                        if bedragv.upper() in afsluitlijst:
                            bedragv1 = -99999.99
                            bedragv2 = 99999.99
                            break
                        elif len(bedragv) == 2 and bedragv.upper()[0] in afsluitlijst and bedragv.upper()[1] in afsluitlijst:
                            bedrag = "Q"
                            break
                        elif len(bedragv) == 3 and bedragv.upper()[0] in afsluitlijst and bedragv.upper()[2] in afsluitlijst:
                            doei()
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
                    if bedrag == "Q":
                        break
                    if Taal == "EN":
                        kop = ", %s from %s %s to %s %s" % (sel3,Valuta,fornum(bedragv1),Valuta,fornum(bedragv2))
                    elif Taal == "IT":
                        kop = ", %s da %s %s a %s %s" % (sel3,Valuta,fornum(bedragv1),Valuta,fornum(bedragv2))
                    else:
                        kop = ", %s van %s %s tot %s %s" % (sel3,Valuta,fornum(bedragv1),Valuta,fornum(bedragv2))
                    if bedragv1 == -99999.99 and bedragv2 == 99999.99:
                        if Taal == "EN":
                            kop = ", all amounts"
                        elif Taal == "IT":
                            kop = ", tutte le somme"
                        else:
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
                        if Taal == "EN":
                            wederpartijv = input("Enter a (part of the) %sother party%s\n  : " % (col1,ResetAll)).lower()
                        elif Taal == "IT":
                            wederpartijv = input("Inserisci (parte della) %scontroparte%s\n  : " % (col1,ResetAll)).lower()
                        else:
                            wederpartijv = input("Geef een (deel van de) %swederpartij%s op\n  : " % (col1,ResetAll)).lower()
                        wederpartij = "Y"
                        if wederpartijv.upper() in afsluitlijst:
                            wederpartijv = ""
                        elif len(wederpartijv) == 2 and wederpartijv.upper()[0] in afsluitlijst and wederpartijv.upper()[1] in afsluitlijst:
                            wederpartij = "Q"
                            break
                        elif len(wederpartijv) == 3 and wederpartijv.upper()[0] in afsluitlijst and wederpartijv.upper()[2] in afsluitlijst:
                            doei()
                    if wederpartij == "Q":
                        break
                    kop = ", %s *%s*" % (sel3,wederpartijv)
                    if wederpartijv == "":
                        if Taal == "EN":
                            kop = ", all other parties"
                        elif Taal == "IT":
                            kop = ", tutte le controparti"
                        else:
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
                        if Taal == "EN":
                            aantekeningv = input("Enter a (part of the) %snote%s\n  : " % (col1,ResetAll)).lower()
                        elif Taal == "IT":
                            aantekeningv = input("Inserisci (parte dell') %sannotazione%s\n  : " % (col1,ResetAll)).lower()
                        else:
                            aantekeningv = input("Geef een (deel van de) %saantekening%s op\n  : " % (col1,ResetAll)).lower()
                        aantekening = "Y"
                        if aantekeningv.upper() in afsluitlijst:
                            aantekeningv = ""
                        elif len(aantekeningv) == 2 and aantekeningv.upper()[0] in afsluitlijst and aantekeningv.upper()[1] in afsluitlijst:
                            aantekening = "Q"
                            break
                        elif len(aantekeningv) == 3 and aantekeningv.upper()[0] in afsluitlijst and aantekeningv.upper()[2] in afsluitlijst:
                            doei()
                    if aantekening == "Q":
                        break
                    kop = ", %s *%s*" % (sel3,aantekeningv)
                    if aantekeningv == "":
                        if Taal == "EN":
                            kop = ", all notes"
                        elif Taal == "IT":
                            kop = ", tutte le annotazioni"
                        else:
                            kop = ", alle aantekeningen"
                    ID = 0
                    for i in seldat:
                        if aantekeningv in i[3].lower():
                            vier = i[4]+str(ID)
                            i.remove(i[4])
                            i.append(vier)
                            sel.append(i)
                            ID += 1
                    if Taal == "EN":
                        kop = ", %s %s" % ("note: ",aantekeningv)
                    elif Taal == "IT":
                        kop = ", %s %s" % ("annotazione: ",aantekeningv)
                    else:
                        kop = ", %s %s" % ("aantekening: ",aantekeningv)
                else:
                    sel3 = ""
                    if Taal == "EN":
                        kop = ""
                    elif Taal == "IT":
                        kop = ""
                    else:
                        kop = ""
                    ID = 0
                    for i in seldat:
                        vier = i[4]+str(ID)
                        i.remove(i[4])
                        i.append(vier)
                        sel.append(i)
                        ID += 1

                # HIER WORDT HET MAANDOVERZICHT NAAR HET BESTAND GEPRINT

                if header["Print"] == "Ja" and budgetcheck == "Y":
                    with open(os.path.join(os.path.expanduser("~"),iban+"."+str(startdatum)[:6]+".txt"),"w") as p:
                        print(toplijn, file = p)
                    with open(os.path.join(os.path.expanduser("~"),iban+"."+str(startdatum)[:6]+".txt"),"a") as p:
                        startdatumeinddatum = "%s-%s" % (startdatum,einddatum)
                        if startdatum == 11111111 and einddatum == 99999999:
                            if Taal == "EN":
                                startdatumeinddatum = "all dates"
                            elif Taal == "IT":
                                startdatumeinddatum = "tutte le date"
                            else:
                                startdatumeinddatum = "alle data"
                        print("|"+forc68(startdatumeinddatum+Kat+kop)+"|", file = p)
                        print(pluslijn, file = p)
                        if Taal == "EN":
                            print("|"+forc10("Date")+"|"+forc12("Amount")+"|"+forc17("Other party")+"|"+forc20("About")+"|"+forc5("ID")+"|", file = p)
                        elif Taal == "IT":
                            print("|"+forc10("Data")+"|"+forc12("Somma")+"|"+forc17("Controparte")+"|"+forc20("Riguarda")+"|"+forc5("ID")+"|", file = p)
                        else:
                            print("|"+forc10("Datum")+"|"+forc12("Bedrag")+"|"+forc17("Wederpartij")+"|"+forc20("Betreft")+"|"+forc5("ID")+"|", file = p)
                        print(pluslijn, file = p)
                        for i in sel:
                            if i[1] <= header['Markering L><H'][0]:
                                colc = colslecht+Omkeren
                            elif header['Markering L><H'][0] <= i[1] < 0:
                                colc = colslecht
                            elif 0 <= i[1] < header['Markering L><H'][1]:
                                colc = colgoed
                            else:
                                colc = colgoed+Omkeren
                            col = catcol[i[4][0]]
                            yymd = i[0]
                            if Datumformaat == "DDMMYYYY":
                                yymd = str(yymd)[6:]+str(yymd)[4:6]+str(yymd)[:4]
                            elif Datumformaat == "DD-MM-YY":
                                yymd = str(yymd)[6:]+"-"+str(yymd)[4:6]+"-"+str(yymd)[2:4]
                            elif Datumformaat == "DD/MM/YY":
                                yymd = str(yymd)[6:]+"/"+str(yymd)[4:6]+"/"+str(yymd)[2:4]
                            elif Datumformaat == "DD-mmmYY":
                                if Taal == "EN":
                                    yymd = str(yymd)[6:]+"-"+str(yymd)[4:6].replace("01","Jan").replace("02","Feb").replace("03","Mar").replace("04","Apr").replace("05","May").replace("06","Jun").replace("07","Jul").replace("08","Aug").replace("09","Sep").replace("10","Oct").replace("11","Nov").replace("12","Dec")+str(yymd)[2:4]
                                elif Taal == "IT":
                                    yymd = str(yymd)[6:]+"-"+str(yymd)[4:6].replace("01","gen").replace("02","feb").replace("03","mar").replace("04","apr").replace("05","mag").replace("06","giu").replace("07","lug").replace("08","ago").replace("09","set").replace("10","ott").replace("11","nov").replace("12","dic")+str(yymd)[2:4]
                                else:
                                    yymd = str(yymd)[6:]+"-"+str(yymd)[4:6].replace("01","jan").replace("02","feb").replace("03","mrt").replace("04","apr").replace("05","mei").replace("06","jun").replace("07","jul").replace("08","aug").replace("09","sep").replace("10","okt").replace("11","nov").replace("12","dec")+str(yymd)[2:4]
                            elif Datumformaat == "DDmmm\'YY":
                                if Taal == "EN":
                                    yymd = str(yymd)[6:]+str(yymd)[4:6].replace("01","Jan").replace("02","Feb").replace("03","Mar").replace("04","Apr").replace("05","May").replace("06","Jun").replace("07","Jul").replace("08","Aug").replace("09","Sep").replace("10","Oct").replace("11","Nov").replace("12","Dec")+"'"+str(yymd)[2:4]
                                elif Taal == "IT":
                                    yymd = str(yymd)[6:]+str(yymd)[4:6].replace("01","gen").replace("02","feb").replace("03","mar").replace("04","apr").replace("05","mag").replace("06","giu").replace("07","lug").replace("08","ago").replace("09","set").replace("10","ott").replace("11","nov").replace("12","dic")+"'"+str(yymd)[2:4]
                                else:
                                    yymd = str(yymd)[6:]+str(yymd)[4:6].replace("01","jan").replace("02","feb").replace("03","mrt").replace("04","apr").replace("05","mei").replace("06","jun").replace("07","jul").replace("08","aug").replace("09","sep").replace("10","okt").replace("11","nov").replace("12","dec")+"'"+str(yymd)[2:4]
                            print("|",for8(str(yymd)),"|",Valuta,fornum(i[1]),"|",for15(i[2]),"|",for18(i[3]),"|",for3(i[4]),"|", file = p)
                        print(pluslijn, file = p)
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
                            if Taal == "EN":
                                regels = "line"
                            elif Taal == "IT":
                                regels = "linea"
                            else:
                                regels = "regel"
                        else:
                            if Taal == "EN":
                                regels = "lines"
                            elif Taal == "IT":
                                regels = "linee"
                            else:
                                regels = "regels"
                        #if Taal == "EN":
                        #    print("    This SELECTION counts %s %s with a total of %s" % (str(count),regels,tot.replace(colgoed,"").replace(colslecht,"").replace(ResetAll,"")), file = p)
                        #elif Taal == "IT":
                        #    print("    Questa SELEZIONE contiene %s %s per un totale di %s" % (str(count),regels,tot.replace(colgoed,"").replace(colslecht,"").replace(ResetAll,"")), file = p)
                        #else:
                        #    print("    Deze SELECTIE bevat %s %s voor een totaal van %s" % (str(count),regels,tot.replace(colgoed,"").replace(colslecht,"").replace(ResetAll,"")), file = p)
                        if budgetcheck == "Y":
                            try:
                                with open("alternatievenamen","r") as f:
                                    alternatievenamenlijst = ast.literal_eval(f.read())
                                    totbud = 0
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
                                                    try:
                                                        if k == "A":
                                                            colpos = colslecht
                                                            colneg = colgoed
                                                        else:
                                                            colpos = colgoed
                                                            colneg = colslecht
                                                        if maandtotaallijst[k]/budget < -1:
                                                            print(k+": "+Valuta+fornum(maandtotaallijst[k])+"/"+fornum(budget)+" |"+"+"*25+"|+"+forr7(int(round(((maandtotaallijst[k]/budget)+1)*-100,0)))+"%"+" ("+Valuta+fornum(budget+maandtotaallijst[k])+")", file = p)
                                                        else:
                                                            print(k+": "+Valuta+fornum(maandtotaallijst[k])+"/"+fornum(budget)+" |"+forl25("-"*int(round(maandtotaallijst[k]/budget*-25,0)))+"|-"+forr7(int(round(((maandtotaallijst[k]/budget)+1)*-100,0)))+"%"+" ("+Valuta+fornum(budget+maandtotaallijst[k])+")", file = p)
                                                    except(Exception) as error:
                                                        if maandtotaallijst[k] != 0:
                                                            print(k+": "+Valuta+fornum(maandtotaallijst[k])+"/"+fornum(budget)+" |"+forl25("."*25)+"|X"+forr7(" ")+" "+" ("+Valuta+fornum(budget+maandtotaallijst[k])+")", file = p)
                                                        else:
                                                            print(k+": "+Valuta+fornum(maandtotaallijst[k])+"/"+fornum(budget)+" |"+forl25(" "*25)+"|="+forr7(" ")+" "+" ("+Valuta+fornum(budget+maandtotaallijst[k])+")", file = p)
                                budtot = 0
                                for i in lijst:
                                    try:
                                        with open(i,"r") as r:
                                            inhoudvancategorie = ast.literal_eval(r.read())
                                            if inhoudvancategorie[0] < 0:
                                                budtot += inhoudvancategorie[0]*-1
                                    except(Exception) as error:
                                        pass
                                if mndtot < 0:
                                    print(forc5(int(round(mndtot/budtot*100,0)))+"% |"+forr25("-"*int(round(mndtot/budtot*-25,0)))+"|"+" "*25+"|", file = p)
                                elif mndtot > 0:
                                    print(forc5(" ")+"|"+" "*25+"|"+forl25("+"*int(round(mndtot/budtot*25,0)))+"|"+forc5(int(round(mndtot/budtot*100,0)))+"%", file = p)
                                else:
                                    print(forc5(" ")+" "*24+"-=+"+" "*24+forc5(int(round(mndtot/budtot*100,0)))+"%", file = p)
                                if mcount == 1:
                                    if Taal == "EN":
                                        regels = "line"
                                    elif Taal == "IT":
                                        regels = "linea"
                                    else:
                                        regels = "regel"
                                else:
                                    if Taal == "EN":
                                        regels = "lines"
                                    elif Taal == "IT":
                                        regels = "linee"
                                    else:
                                        regels = "regels"
                                if Taal == "EN":
                                    print("    This WHOLE MONTH counts %s %s with a total of %s" % (str(mcount),regels,mtot.replace(colgoed,"").replace(colslecht,"").replace(ResetAll,"")), file = p)
                                elif Taal == "IT":
                                    print("    Questo INTERO MESE contiene %s %s per un totale di %s" % (str(mcount),regels,mtot.replace(colgoed,"").replace(colslecht,"").replace(ResetAll,"")), file = p)
                                else:
                                    print("    Deze HELE MAAND bevat %s %s voor een totaal van %s" % (str(mcount),regels,mtot.replace(colgoed,"").replace(colslecht,"").replace(ResetAll,"")), file = p)
                            except(Exception) as error:
                                pass

                # HIER KOMT DE TABEL OP HET SCHERM

                print(toplijn)
                startdatumeinddatum = "%s-%s" % (startdatum,einddatum)
                if startdatum == 11111111 and einddatum == 99999999:
                    if Taal == "EN":
                        startdatumeinddatum = "all dates"
                    elif Taal == "IT":
                        startdatumeinddatum = "tutte le date"
                    else:
                        startdatumeinddatum = "alle data"
                print("|"+col1+forc68(startdatumeinddatum+Kat+kop)+ResetAll+"|")
                print(pluslijn)
                if Taal == "EN":
                    print("|"+col1+forc10("Date")+ResetAll+"|"+col1+forc12("Amount")+ResetAll+"|"+col1+forc17("Other party")+ResetAll+"|"+col1+forc20("About")+ResetAll+"|"+col1+forc5("ID")+ResetAll+"|")
                elif Taal == "IT":
                    print("|"+col1+forc10("Data")+ResetAll+"|"+col1+forc12("Somma")+ResetAll+"|"+col1+forc17("Controparte")+ResetAll+"|"+col1+forc20("Riguarda")+ResetAll+"|"+col1+forc5("ID")+ResetAll+"|")
                else:
                    print("|"+col1+forc10("Datum")+ResetAll+"|"+col1+forc12("Bedrag")+ResetAll+"|"+col1+forc17("Wederpartij")+ResetAll+"|"+col1+forc20("Betreft")+ResetAll+"|"+col1+forc5("ID")+ResetAll+"|")
                print(pluslijn)
                for i in sel:
                    if i[1] <= header['Markering L><H'][0]:
                        colc = colslecht+Omkeren
                    elif header['Markering L><H'][0] <= i[1] < 0:
                        colc = colslecht
                    elif 0 <= i[1] < header['Markering L><H'][1]:
                        colc = colgoed
                    else:
                        colc = colgoed+Omkeren
                    col = catcol[i[4][0]]
                    yymd = i[0]
                    if Datumformaat == "DDMMYYYY":
                        yymd = str(yymd)[6:]+str(yymd)[4:6]+str(yymd)[:4]
                    elif Datumformaat == "DD-MM-YY":
                        yymd = str(yymd)[6:]+"-"+str(yymd)[4:6]+"-"+str(yymd)[2:4]
                    elif Datumformaat == "DD/MM/YY":
                        yymd = str(yymd)[6:]+"/"+str(yymd)[4:6]+"/"+str(yymd)[2:4]
                    elif Datumformaat == "DD-mmmYY":
                        if Taal == "EN":
                            yymd = str(yymd)[6:]+"-"+str(yymd)[4:6].replace("01","Jan").replace("02","Feb").replace("03","Mar").replace("04","Apr").replace("05","May").replace("06","Jun").replace("07","Jul").replace("08","Aug").replace("09","Sep").replace("10","Oct").replace("11","Nov").replace("12","Dec")+str(yymd)[2:4]
                        elif Taal == "IT":
                            yymd = str(yymd)[6:]+"-"+str(yymd)[4:6].replace("01","gen").replace("02","feb").replace("03","mar").replace("04","apr").replace("05","mag").replace("06","giu").replace("07","lug").replace("08","ago").replace("09","set").replace("10","ott").replace("11","nov").replace("12","dic")+str(yymd)[2:4]
                        else:
                            yymd = str(yymd)[6:]+"-"+str(yymd)[4:6].replace("01","jan").replace("02","feb").replace("03","mrt").replace("04","apr").replace("05","mei").replace("06","jun").replace("07","jul").replace("08","aug").replace("09","sep").replace("10","okt").replace("11","nov").replace("12","dec")+str(yymd)[2:4]
                    elif Datumformaat == "DDmmm\'YY":
                        if Taal == "EN":
                            yymd = str(yymd)[6:]+str(yymd)[4:6].replace("01","Jan").replace("02","Feb").replace("03","Mar").replace("04","Apr").replace("05","May").replace("06","Jun").replace("07","Jul").replace("08","Aug").replace("09","Sep").replace("10","Oct").replace("11","Nov").replace("12","Dec")+"'"+str(yymd)[2:4]
                        elif Taal == "IT":
                            yymd = str(yymd)[6:]+str(yymd)[4:6].replace("01","gen").replace("02","feb").replace("03","mar").replace("04","apr").replace("05","mag").replace("06","giu").replace("07","lug").replace("08","ago").replace("09","set").replace("10","ott").replace("11","nov").replace("12","dic")+"'"+str(yymd)[2:4]
                        else:
                            yymd = str(yymd)[6:]+str(yymd)[4:6].replace("01","jan").replace("02","feb").replace("03","mrt").replace("04","apr").replace("05","mei").replace("06","jun").replace("07","jul").replace("08","aug").replace("09","sep").replace("10","okt").replace("11","nov").replace("12","dec")+"'"+str(yymd)[2:4]
                    print("|",for8(str(yymd)),"|",colc+Valuta+ResetAll,fornum(i[1]),"|",for15(i[2]),"|",for18(i[3]),"|",col+for3(i[4])+ResetAll,"|")
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
                    if Taal == "EN":
                        regels = "line"
                    elif Taal == "IT":
                        regels = "linea"
                    else:
                        regels = "regel"
                else:
                    if Taal == "EN":
                        regels = "lines"
                    elif Taal == "IT":
                        regels = "linee"
                    else:
                        regels = "regels"
                if Taal == "EN":
                    print(col1+"    This SELECTION counts %s %s with a total of %s" % (str(count),regels,tot)+ResetAll)
                elif Taal == "IT":
                    print(col1+"    Questa SELEZIONE contiene %s %s per un totale di %s" % (str(count),regels,tot)+ResetAll)
                else:
                    print(col1+"    Deze SELECTIE bevat %s %s voor een totaal van %s" % (str(count),regels,tot)+ResetAll)
                if budgetcheck == "Y":
                    try:
                        with open("alternatievenamen","r") as f:
                            alternatievenamenlijst = ast.literal_eval(f.read())
                            totbud = 0
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
                                            try:
                                                if k == "A":
                                                    colpos = colslecht
                                                    colneg = colgoed
                                                else:
                                                    colpos = colgoed
                                                    colneg = colslecht
                                                if maandtotaallijst[k]/budget < -1:
                                                    print(col+k+": "+Valuta+fornum(maandtotaallijst[k])+"/"+fornum(budget)+" |"+"+"*25+"|+"+forr7(int(round(((maandtotaallijst[k]/budget)+1)*-100,0)))+"%"+colneg+" ("+Valuta+fornum(budget+maandtotaallijst[k])+")"+ResetAll)
                                                else:
                                                    print(col+k+": "+Valuta+fornum(maandtotaallijst[k])+"/"+fornum(budget)+" |"+forl25("-"*int(round(maandtotaallijst[k]/budget*-25,0)))+"|-"+forr7(int(round(((maandtotaallijst[k]/budget)+1)*-100,0)))+"%"+colpos+" ("+Valuta+fornum(budget+maandtotaallijst[k])+")"+ResetAll)
                                            except(Exception) as error:
                                                if maandtotaallijst[k] != 0:
                                                    print(col+k+": "+Valuta+fornum(maandtotaallijst[k])+"/"+fornum(budget)+" |"+forl25("."*25)+"|X"+forr7(" ")+" "+colneg+" ("+Valuta+fornum(budget+maandtotaallijst[k])+")"+ResetAll)
                                                else:
                                                    print(col+k+": "+Valuta+fornum(maandtotaallijst[k])+"/"+fornum(budget)+" |"+forl25(" "*25)+"|="+forr7(" ")+" "+colpos+" ("+Valuta+fornum(budget+maandtotaallijst[k])+")"+ResetAll)
                        budtot = 0
                        for i in lijst:
                            try:
                                with open(i,"r") as r:
                                    inhoudvancategorie = ast.literal_eval(r.read())
                                    if inhoudvancategorie[0] < 0:
                                        budtot += inhoudvancategorie[0]*-1
                            except(Exception) as error:
                                pass
                        if mndtot < 0:
                            if int(round(mndtot/budtot*100,0)) >= -100:
                                print(colslecht+forc5(int(round(mndtot/budtot*100,0)))+"% |"+forr25("-"*int(round(mndtot/budtot*-25,0)))+"|"+colgoed+" "*25+"|"+ResetAll)
                            else:
                                print(colslecht+forc5(int(round(mndtot/budtot*100,0)))+"% |"+forr25("="*25)+"|"+colgoed+" "*25+"|"+ResetAll)
                        elif mndtot > 0:
                            if int(round(mndtot/budtot*100,0)) <= 100:
                                print(colslecht+forc5(" ")+"|"+" "*25+colgoed+"|"+forl25("+"*int(round(mndtot/budtot*25,0)))+"|"+forc5(int(round(mndtot/budtot*100,0)))+"%"+ResetAll)
                            else:
                                print(colslecht+forc5(" ")+"|"+" "*25+colgoed+"|"+forl25("#"*25)+"|"+forc5(int(round(mndtot/budtot*100,0)))+"%"+ResetAll)

                        else:
                            print(colgoed+forc5(" ")+" "*24+"-=+"+" "*24+forc5(int(round(mndtot/budtot*100,0)))+"%"+ResetAll)
                        if mcount == 1:
                            if Taal == "EN":
                                regels = "line"
                            elif Taal == "IT":
                                regels = "linea"
                            else:
                                regels = "regel"
                        else:
                            if Taal == "EN":
                                regels = "lines"
                            elif Taal == "IT":
                                regels = "linee"
                            else:
                                regels = "regels"
                        if Taal == "EN":
                            print(col1+"    This WHOLE MONTH counts %s %s with a total of %s" % (str(mcount),regels,mtot)+ResetAll)
                        elif Taal == "IT":
                            print(col1+"    Questo INTERO MESE contiene %s %s per un totale di %s" % (str(mcount),regels,mtot)+ResetAll)
                        else:
                            print(col1+"    Deze HELE MAAND bevat %s %s voor een totaal van %s" % (str(mcount),regels,mtot)+ResetAll)
                    except(Exception) as error:
                        pass
                if dagsaldo == "Y":
                    if Taal == "EN":
                        print(col1+forc70("Day balance on %s: %s %s" % (str(startdatum),Valuta,fornum(moni)))+ResetAll)
                    elif Taal == "IT":
                        print(col1+forc70("Saldo giornaliero a %s: %s %s" % (str(startdatum),Valuta,fornum(moni)))+ResetAll)
                    else:
                        print(col1+forc70("Dagsaldo op %s: %s %s" % (str(startdatum),Valuta,fornum(moni)))+ResetAll)
                bekijken = "N"
        if bekijken == "Q":
            break
        print(toplijn)
        print()

    elif keuze1 == "2": # TOEVOEGEN
        print()
        col2 = LichtGroen
        if Taal == "EN":
            keuze2 = input("%sAdd a new mutation or make a copy of a known ID%s\n >1 %sNew%s\n  2 %sCopy to today%s\n  3 %sCopy to other account%s\n  : %s" % (col2,ResetAll,col2,ResetAll,col2,ResetAll,col2,ResetAll,col2))
        elif Taal == "IT":
            keuze2 = input("%sAggiungi una nuova mutazione o fai una copia di un ID conosciuto%s\n >1 %sNuovo%s\n  2 %sCopia colla data di oggi%s\n  3 %sCopia su un altro conto%s\n  : %s" % (col2,ResetAll,col2,ResetAll,col2,ResetAll,col2,ResetAll,col2))
        else:
            keuze2 = input("%sNieuwe mutatie toevoegen of een kopie van een bekend ID maken%s\n >1 %sNieuw%s\n  2 %sKopie naar vandaag%s\n  3 %sKopie naar andere rekening%s\n  : %s" % (col2,ResetAll,col2,ResetAll,col2,ResetAll,col2,ResetAll,col2))
        print(ResetAll, end = "")
        if keuze2.upper() in afsluitlijst:
            pass
        elif len(keuze2) == 2 and keuze2.upper()[0] in afsluitlijst and keuze2.upper()[1] in afsluitlijst:
            pass
        elif len(keuze2) == 3 and keuze2.upper()[0] in afsluitlijst and keuze2.upper()[2] in afsluitlijst:
            doei()
        else:
            toe = "N"
            while toe == "N":
                if keuze2 == "2":
                    if Taal == "EN":
                        tekopieren = input("Which ID do you want to %scopy to today%s\n  : " % (col2, ResetAll))
                    elif Taal == "IT":
                        tekopieren = input("Di quale ID vuoi fare una %scopia colla data di oggi%s\n  : " % (col2, ResetAll))
                    else:
                        tekopieren = input("Welk ID wil je %skopieren naar vandaag%s\n  : " % (col2, ResetAll))
                    if tekopieren.upper() in afsluitlijst:
                        break
                    elif len(tekopieren) == 2 and tekopieren.upper()[0] in afsluitlijst and tekopieren.upper()[1] in afsluitlijst:
                        toe = "Q"
                        break
                    elif len(tekopieren) == 3 and tekopieren.upper()[0] in afsluitlijst and tekopieren.upper()[2] in afsluitlijst:
                        doei()
                    else:
                        try:
                            with open(tekopieren[0].upper(),"r") as f:
                                inhoudvancategorie = ast.literal_eval(f.read())
                            alternatievenaam = alternatievenamenlijst[tekopieren[0].upper()]
                            col = catcol[tekopieren[0].upper()]
                        except(Exception) as error:
                            #print(error)
                            pass
                        try:
                            for i in sel:
                                if i[4] == tekopieren[0].upper()+tekopieren[1:]:
                                    i[0] = nu
                                    inhoudvancategorie.append(i[:4])
                                    break
                            sortcat0 = inhoudvancategorie[0]
                            sortcat1 = sorted(inhoudvancategorie[1:])
                            inhoudvancategorie = [sortcat0]
                            for k in sortcat1:
                                inhoudvancategorie.append(k)
                            if Taal == "EN":
                                alternatievenaam= alternatievenaam.replace("saldo & inkomen","funds & income").replace("vaste lasten","fixed costs").replace("boodschappen","groceries").replace("reis & verblijf","travel & stay").replace("leningen","loans").replace("overig","other")
                                print("%s %s%d%s\n%s %s%s %s%s\n%s %s%s%s\n%s %s%s%s\n%s %s%s%s" % (for15("Date: "),col2,i[0],ResetAll,for15("Amount: "),col2,Valuta,forn(i[1]),ResetAll,for15("Other party: "),col2,i[2],ResetAll,for15("About: "),col2,i[3],ResetAll,for15("Category: "),col,alternatievenaam,ResetAll))
                            elif Taal == "IT":
                                alternatievenaam = alternatievenaam.replace("saldo & inkomen","saldo & reddito").replace("vaste lasten","costi fissi").replace("boodschappen","spese").replace("reis & verblijf","viaggioalloggio").replace("leningen","prestiti").replace("overig","altro")
                                print("%s %s%d%s\n%s %s%s %s%s\n%s %s%s%s\n%s %s%s%s\n%s %s%s%s" % (for15("Data: "),col2,i[0],ResetAll,for15("Somma: "),col2,Valuta,forn(i[1]),ResetAll,for15("Controparte: "),col2,i[2],ResetAll,for15("Riguarda: "),col2,i[3],ResetAll,for15("Categoria: "),col,alternatievenaam,ResetAll))
                            else:
                                print("%s %s%d%s\n%s %s%s %s%s\n%s %s%s%s\n%s %s%s%s\n%s %s%s%s" % (for15("Datum: "),col2,i[0],ResetAll,for15("Bedrag: "),col2,Valuta,forn(i[1]),ResetAll,for15("Wederpartij: "),col2,i[2],ResetAll,for15("Betreft: "),col2,i[3],ResetAll,for15("Categorie: "),col,alternatievenaam,ResetAll))
                            with open(tekopieren[0].upper(),"w") as w:
                                print(inhoudvancategorie, file = w, end = "")
                        except(Exception) as error:
                            pass
                    break
                if keuze2 == "3":
                    if Taal == "EN":
                        tekopieren = input("Which ID do you want to %scopy to another account%s\n  : " % (col2, ResetAll))
                    elif Taal == "IT":
                        tekopieren = input("Di quale ID vuoi fare una %scopia su un altro conto%s\n  : " % (col2, ResetAll))
                    else:
                        tekopieren = input("Welk ID wil je %skopieren naar een andere rekening%s\n  : " % (col2, ResetAll))
                    if tekopieren.upper() in afsluitlijst:
                        break
                    elif len(tekopieren) == 2 and tekopieren.upper()[0] in afsluitlijst and tekopieren.upper()[1] in afsluitlijst:
                        break
                    elif len(tekopieren) == 3 and tekopieren.upper()[0] in afsluitlijst and tekopieren.upper()[2] in afsluitlijst:
                        doei()
                    else:
                        col = catcol[tekopieren.upper()[0]]
                        os.chdir(basismap)
                        if Taal == "EN":
                            print("To which account do you want to %scopy %s%s%s" % (col2,col,tekopieren.upper(),ResetAll))
                        elif Taal == "IT":
                            print("In quale conto vuoi fare una %scopia di %s%s%s" % (col2,col,tekopieren.upper(),ResetAll))
                        else:
                            print("Naar welke rekening wil je %s%s%s kopieren%s" % (col,tekopieren.upper(),col2,ResetAll))
                        rekeningenlijst = rknngnlst()
                        welk = input("  : ")
                        if welk.upper() in afsluitlijst:
                            os.chdir(os.path.join(basismap,iban+"@"+jaar))
                            break
                        elif len(welk) == 2 and welk.upper()[0] in afsluitlijst and welk.upper()[1] in afsluitlijst:
                            os.chdir(os.path.join(basismap,iban+"@"+jaar))
                            break
                        elif len(welk) == 3 and welk.upper()[0] in afsluitlijst and welk.upper()[2] in afsluitlijst:
                            doei()
                        try:
                            welk = int(welk)-1
                            viban = rekeningenlijst[welk][0]
                            vjaar = rekeningenlijst[welk][1]
                            try:
                                with open(os.path.join(viban+"@"+vjaar,tekopieren[0].upper()),"r") as f:
                                    inhoudvancategoriev = ast.literal_eval(f.read())
                            except(Exception) as error:
                                #print(error)
                                inhoudvancategoriev = [0.0]
                                with open(os.path.join(viban+"@"+vjaar,tekopieren[0].upper()),"w") as w:
                                    print(inhoudvancategoriev, file = w, end = "")
                            alternatievenaam = alternatievenamenlijst[tekopieren[0].upper()]
                            col = catcol[tekopieren[0].upper()]
                        except(Exception) as error:
                            #print(error)
                            pass
                        try:
                            for i in sel:
                                if i[4] == tekopieren[0].upper()+tekopieren[1:]:
                                    inhoudvancategoriev.append(i[:4])
                                    break
                            sortcat0 = inhoudvancategoriev[0]
                            sortcat1 = sorted(inhoudvancategoriev[1:])
                            inhoudvancategoriev = [sortcat0]
                            for k in sortcat1:
                                inhoudvancategoriev.append(k)
                            if Taal == "EN":
                                alternatievenaam= alternatievenaam.replace("saldo & inkomen","funds & income").replace("vaste lasten","fixed costs").replace("boodschappen","groceries").replace("reis & verblijf","travel & stay").replace("leningen","loans").replace("overig","other")
                                print("%s %s%d%s\n%s %s%s %s%s\n%s %s%s%s\n%s %s%s%s\n%s %s%s%s" % (for15("Date: "),col2,i[0],ResetAll,for15("Amount: "),col2,Valuta,forn(i[1]),ResetAll,for15("Other party: "),col2,i[2],ResetAll,for15("About: "),col2,i[3],ResetAll,for15("Category: "),col,alternatievenaam,ResetAll))
                            elif Taal == "IT":
                                alternatievenaam = alternatievenaam.replace("saldo & inkomen","saldo & reddito").replace("vaste lasten","costi fissi").replace("boodschappen","spese").replace("reis & verblijf","viaggioalloggio").replace("leningen","prestiti").replace("overig","altro")
                                print("%s %s%d%s\n%s %s%s %s%s\n%s %s%s%s\n%s %s%s%s\n%s %s%s%s" % (for15("Data: "),col2,i[0],ResetAll,for15("Somma: "),col2,Valuta,forn(i[1]),ResetAll,for15("Controparte: "),col2,i[2],ResetAll,for15("Riguarda: "),col2,i[3],ResetAll,for15("Categoria: "),col,alternatievenaam,ResetAll))
                            else:
                                print("%s %s%d%s\n%s %s%s %s%s\n%s %s%s%s\n%s %s%s%s\n%s %s%s%s" % (for15("Datum: "),col2,i[0],ResetAll,for15("Bedrag: "),col2,Valuta,forn(i[1]),ResetAll,for15("Wederpartij: "),col2,i[2],ResetAll,for15("Betreft: "),col2,i[3],ResetAll,for15("Categorie: "),col,alternatievenaam,ResetAll))
                            with open(os.path.join(viban+"@"+vjaar,tekopieren[0].upper()),"w") as w:
                                print(inhoudvancategoriev, file = w, end = "")
                        except(Exception) as error:
                            #print(error)
                            pass
                        os.chdir(iban+"@"+jaar)
                    break
                else:
                    nieuw = []
                    try:
                        if Taal == "EN":
                            datum = input("%sDate%s (YYYYMMDD) or %sCSV%s (date,amount,other party,about)\n  : %s" % (col2,ResetAll,col2,ResetAll,col2))
                        elif Taal == "IT":
                            datum = input("%sData%s (AAAAMMGG) o %sCSV%s (data,somma,controparte,riguarda)\n  : %s" % (col2,ResetAll,col2,ResetAll,col2))
                        else:
                            datum = input("%sDatum%s (JJJJMMDD) of %sCSV%s (datum,bedrag,wederpartij,betreft)\n  : %s" % (col2,ResetAll,col2,ResetAll,col2))
                        print(ResetAll, end = "")
                        if datum.upper() in afsluitlijst:
                            break
                        elif len(datum) == 2 and datum.upper()[0] in afsluitlijst and datum.upper()[1] in afsluitlijst:
                            break
                        elif len(datum) == 3 and datum.upper()[0] in afsluitlijst and datum.upper()[2] in afsluitlijst:
                            doei()
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
                            if Taal == "EN":
                                bedrag = input("%sAmount%s\n  : %s" % (col2,ResetAll,col2)).replace(",",".").replace(Valuta,"").strip()
                            elif Taal == "IT":
                                bedrag = input("%sSomma%s\n  : %s" % (col2,ResetAll,col2)).replace(",",".").replace(Valuta,"").strip()
                            else:
                                bedrag = input("%sBedrag%s\n  : %s" % (col2,ResetAll,col2)).replace(",",".").replace(Valuta,"").strip()
                            print(ResetAll, end = "")
                            if bedrag.upper() in afsluitlijst:
                                break
                            elif len(bedrag) == 2 and bedrag.upper()[0] in afsluitlijst and bedrag.upper()[1] in afsluitlijst:
                                break
                            elif len(bedrag) == 3 and bedrag.upper()[0] in afsluitlijst and bedrag.upper()[2] in afsluitlijst:
                                doei()
                            elif bedrag == "":
                                bedrag = 0.0
                                print(col2+"    "+forn(bedrag)+ResetAll)
                            else:
                                bedrag = float(bedrag)
                            nieuw.append(bedrag)
                            if Taal == "EN":
                                wederpartij = input("%sOther party%s\n  : %s" % (col2,ResetAll,col2))
                            elif Taal == "IT":
                                wederpartij = input("%sControparte%s\n  : %s" % (col2,ResetAll,col2))
                            else:
                                wederpartij = input("%sWederpartij%s\n  : %s" % (col2,ResetAll,col2))
                            print(ResetAll, end = "")
                            if wederpartij.upper() in afsluitlijst:
                                break
                            elif len(wederpartij) == 2 and wederpartij.upper()[0] in afsluitlijst and wederpartij.upper()[1] in afsluitlijst:
                                break
                            elif len(wederpartij) == 3 and wederpartij.upper()[0] in afsluitlijst and wederpartij.upper()[2] in afsluitlijst:
                                doei()
                            nieuw.append(wederpartij[:15])
                            if Taal == "EN":
                                betreft = input("%sAbout%s\n  : %s" % (col2,ResetAll,col2))
                            elif Taal == "IT":
                                betreft = input("%sRiguarda%s\n  : %s" % (col2,ResetAll,col2))
                            else:
                                betreft = input("%sBetreft%s\n  : %s" % (col2,ResetAll,col2))
                            print(ResetAll, end = "")
                            if betreft.upper() in afsluitlijst:
                                break
                            elif len(betreft) == 2 and betreft.upper()[0] in afsluitlijst and betreft.upper()[1] in afsluitlijst:
                                break
                            elif len(betreft) == 3 and betreft.upper()[0] in afsluitlijst and betreft.upper()[2] in afsluitlijst:
                                doei()
                            nieuw.append(betreft[:18])
                        if Taal == "EN":
                            print("%sCategory%s (letter \"%s\"-\"%s\")" % (col2,ResetAll,lijst[0],lijst[-1]))
                        elif Taal == "IT":
                            print("%sCategoria%s (lettera \"%s\"-\"%s\")" % (col2,ResetAll,lijst[0],lijst[-1]))
                        else:
                            print("%sCategorie%s (letter \"%s\"-\"%s\")" % (col2,ResetAll,lijst[0],lijst[-1]))
                        alt()
                        categorie = input("  : %s" % (col2))
                        print(ResetAll, end = "")
                        if categorie.upper() in afsluitlijst or categorie.upper() not in lijst:
                            break
                        elif len(categorie) == 2 and categorie.upper()[0] in afsluitlijst and categorie.upper()[1] in afsluitlijst:
                            break
                        elif len(categorie) == 3 and categorie.upper()[0] in afsluitlijst and categorie.upper()[2] in afsluitlijst:
                            doei()
                        else:
                            categorie = categorie.upper()
                        try:
                            with open(categorie,"r") as f:
                                inhoudvancategorie = ast.literal_eval(f.read())
                        except(Exception) as error:
                            #print(error)
                            if Taal == "EN":
                                nieuwecategorie = input("Give the %snew category%s %s a name\n  : " % (col2,ResetAll,catcol[categorie]+categorie+ResetAll))
                            elif Taal == "IT":
                                nieuwecategorie = input("Dai la %snuova categoria%s %s un nome\n  : " % (col2,ResetAll,catcol[categorie]+categorie+ResetAll))
                            else:
                                nieuwecategorie = input("Geef de %snieuwe categorie%s %s een naam\n  : " % (col2,ResetAll,catcol[categorie]+categorie+ResetAll))
                            if nieuwecategorie.upper() in afsluitlijst:
                                break
                            elif len(nieuwecategorie) == 2 and nieuwecategorie.upper()[0] in afsluitlijst and nieuwecategorie.upper()[1] in afsluitlijst:
                                break
                            elif len(nieuwecategorie) == 3 and nieuwecategorie.upper()[0] in afsluitlijst and nieuwecategorie.upper()[2] in afsluitlijst:
                                doei()
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
                        if Taal == "EN":
                            print("%s %s%d%s\n%s %s%s %s%s\n%s %s%s%s\n%s %s%s%s\n%s %s%s%s" % (for15("Date: "),col2,nieuw[0],ResetAll,for15("Amount: "),col2,Valuta,forn(nieuw[1]),ResetAll,for15("Other party: "),col2,nieuw[2],ResetAll,for15("About: "),col2,nieuw[3],ResetAll,for15("Category: "),col,alternatievenaam,ResetAll))
                        elif Taal == "IT":
                            print("%s %s%d%s\n%s %s%s %s%s\n%s %s%s%s\n%s %s%s%s\n%s %s%s%s" % (for15("Data: "),col2,nieuw[0],ResetAll,for15("Somma: "),col2,Valuta,forn(nieuw[1]),ResetAll,for15("Controparte: "),col2,nieuw[2],ResetAll,for15("Riguarda: "),col2,nieuw[3],ResetAll,for15("Categoria: "),col,alternatievenaam,ResetAll))
                        else:
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
            if toe == "Q":
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
                if Taal == "EN":
                    tewijzigen = input("Which ID do you want to %smodify%s\n  : %s" % (col3, ResetAll,col3))
                elif Taal == "IT":
                    tewijzigen = input("Quale ID vuoi %modificare%s\n  : %s" % (col3, ResetAll,col3))
                else:
                    tewijzigen = input("Welk ID wil je %swijzigen%s\n  : %s" % (col3, ResetAll,col3))
                print(ResetAll, end = "")
                if tewijzigen.upper() in afsluitlijst:
                    del keuze1
                    break
                elif len(tewijzigen) == 2 and tewijzigen.upper()[0] in afsluitlijst and tewijzigen.upper()[1] in afsluitlijst:
                    del keuze1
                    break
                elif len(tewijzigen) == 3 and tewijzigen.upper()[0] in afsluitlijst and tewijzigen.upper()[2] in afsluitlijst:
                    doei()
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
                                if Taal == "EN":
                                    alternatievenaam= alternatievenaam.replace("saldo & inkomen","funds & income").replace("vaste lasten","fixed costs").replace("boodschappen","groceries").replace("reis & verblijf","travel & stay").replace("leningen","loans").replace("overig","other")
                                    wat = input("What do you want to %schange%s\n  %s1%s %s %s\n  %s2%s %s %s %s\n  %s3%s %s %s\n  %s4%s %s %s\n  %s5%s %s %s%s%s\n  : " % (col3,ResetAll,col3,ResetAll,for15("Date: "),i[0],col3,ResetAll,for15("Amount: "),Valuta,i[1],col3,ResetAll,for15("Other party: "),i[2],col3,ResetAll,for15("About: "),i[3],col3,ResetAll,for15("Category: "),col,alternatievenaam,ResetAll))
                                elif Taal == "IT":
                                    alternatievenaam = alternatievenaam.replace("saldo & inkomen","saldo & reddito").replace("vaste lasten","costi fissi").replace("boodschappen","spese").replace("reis & verblijf","viaggioalloggio").replace("leningen","prestiti").replace("overig","altro")
                                    wat = input("Cosa vuoi %smodificare%s\n  %s1%s %s %s\n  %s2%s %s %s %s\n  %s3%s %s %s\n  %s4%s %s %s\n  %s5%s %s %s%s%s\n  : " % (col3,ResetAll,col3,ResetAll,for15("Data: "),i[0],col3,ResetAll,for15("Somma: "),Valuta,i[1],col3,ResetAll,for15("Controparte: "),i[2],col3,ResetAll,for15("Riguarda: "),i[3],col3,ResetAll,for15("Categoria: "),col,alternatievenaam,ResetAll))
                                else:
                                    wat = input("Wat wil je %swijzigen%s\n  %s1%s %s %s\n  %s2%s %s %s %s\n  %s3%s %s %s\n  %s4%s %s %s\n  %s5%s %s %s%s%s\n  : " % (col3,ResetAll,col3,ResetAll,for15("Datum: "),i[0],col3,ResetAll,for15("Bedrag: "),Valuta,i[1],col3,ResetAll,for15("Wederpartij: "),i[2],col3,ResetAll,for15("Betreft: "),i[3],col3,ResetAll,for15("Categorie: "),col,alternatievenaam,ResetAll))
                                if wat.upper() in afsluitlijst:
                                    break
                                elif len(wat) == 2 and wat.upper()[0] in afsluitlijst and wat.upper()[1] in afsluitlijst:
                                    break
                                elif len(wat) == 3 and wat.upper()[0] in afsluitlijst and wat.upper()[2] in afsluitlijst:
                                    doei()
                                elif wat == "1":
                                    try:
                                        if Taal == "EN":
                                            datum = input("%sDate%s (YYYYMMDD)\n  : %s" % (col3,ResetAll,col3))
                                        elif Taal == "IT":
                                            datum = input("%sData%s (AAAAMMGG)\n  : %s" % (col3,ResetAll,col3))
                                        else:
                                            datum = input("%sDatum%s (JJJJMMDD)\n  : %s" % (col3,ResetAll,col3))
                                        print(ResetAll, end = "")
                                        if datum.upper() in afsluitlijst:
                                            break
                                        elif len(datum) == 2 and datum.upper()[0] in afsluitlijst and datum.upper()[1] in afsluitlijst:
                                            break
                                        elif len(datum) == 3 and datum.upper()[0] in afsluitlijst and datum.upper()[2] in afsluitlijst:
                                            doei()
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
                                        if Taal == "EN":
                                            print("%s %s%d%s\n%s %s%s %s%s\n%s %s%s%s\n%s %s%s%s\n%s %s%s%s" % (for15("Date: "),col3,datum,ResetAll,for15("Amount: "),col3,Valuta,forn(i[1]),ResetAll,for15("Other party: "),col3,i[2],ResetAll,for15("About: "),col3,i[3],ResetAll,for15("Category: "),col,alternatievenaam,ResetAll))
                                        elif Taal == "IT":
                                            print("%s %s%d%s\n%s %s%s %s%s\n%s %s%s%s\n%s %s%s%s\n%s %s%s%s" % (for15("Data: "),col3,datum,ResetAll,for15("Somma: "),col3,Valuta,forn(i[1]),ResetAll,for15("Controparte: "),col3,i[2],ResetAll,for15("Riguarda: "),col3,i[3],ResetAll,for15("Categoria: "),col,alternatievenaam,ResetAll))
                                        else:
                                            print("%s %s%d%s\n%s %s%s %s%s\n%s %s%s%s\n%s %s%s%s\n%s %s%s%s" % (for15("Datum: "),col3,datum,ResetAll,for15("Bedrag: "),col3,Valuta,forn(i[1]),ResetAll,for15("Wederpartij: "),col3,i[2],ResetAll,for15("Betreft: "),col3,i[3],ResetAll,for15("Categorie: "),col,alternatievenaam,ResetAll))
                                    except(Exception) as error:
                                        #print(error)
                                        pass
                                elif wat == "2":
                                    try:
                                        if Taal == "EN":
                                            bedrag = input("%sAmount%s\n  : %s" % (col3,ResetAll,col3)).replace(",",".").replace(Valuta,"").strip()
                                        elif Taal == "IT":
                                            bedrag = input("%sSomma%s\n  : %s" % (col3,ResetAll,col3)).replace(",",".").replace(Valuta,"").strip()
                                        else:
                                            bedrag = input("%sBedrag%s\n  : %s" % (col3,ResetAll,col3)).replace(",",".").replace(Valuta,"").strip()
                                        print(ResetAll, end = "")
                                        if bedrag.upper() in afsluitlijst:
                                            break
                                        elif len(bedrag) == 2 and bedrag.upper()[0] in afsluitlijst and bedrag.upper()[1] in afsluitlijst:
                                            break
                                        elif len(bedrag) == 3 and bedrag.upper()[0] in afsluitlijst and bedrag.upper()[2] in afsluitlijst:
                                            doei()
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
                                        if Taal == "EN":
                                            print("%s %s%d%s\n%s %s%s %s%s\n%s %s%s%s\n%s %s%s%s\n%s %s%s%s" % (for15("Date: "),col3,i[0],ResetAll,for15("Amount: "),col3,Valuta,forn(bedrag),ResetAll,for15("Other party: "),col3,i[2],ResetAll,for15("About: "),col3,i[3],ResetAll,for15("Category: "),col,alternatievenaam,ResetAll))
                                        elif Taal == "IT":
                                            print("%s %s%d%s\n%s %s%s %s%s\n%s %s%s%s\n%s %s%s%s\n%s %s%s%s" % (for15("Data: "),col3,i[0],ResetAll,for15("Somma: "),col3,Valuta,forn(bedrag),ResetAll,for15("Controparte: "),col3,i[2],ResetAll,for15("Riguarda: "),col3,i[3],ResetAll,for15("Categoria: "),col,alternatievenaam,ResetAll))
                                        else:
                                            print("%s %s%d%s\n%s %s%s %s%s\n%s %s%s%s\n%s %s%s%s\n%s %s%s%s" % (for15("Datum: "),col3,i[0],ResetAll,for15("Bedrag: "),col3,Valuta,forn(bedrag),ResetAll,for15("Wederpartij: "),col3,i[2],ResetAll,for15("Betreft: "),col3,i[3],ResetAll,for15("Categorie: "),col,alternatievenaam,ResetAll))
                                    except(Exception) as error:
                                        #print(error)
                                        pass
                                elif wat == "3":
                                    if Taal == "EN":
                                        wederpartij = input("%sOther party%s\n  : %s" % (col3,ResetAll,col3))
                                    elif Taal == "IT":
                                        wederpartij = input("%sControparte%s\n  : %s" % (col3,ResetAll,col3))
                                    else:
                                        wederpartij = input("%sWederpartij%s\n  : %s" % (col3,ResetAll,col3))
                                    print(ResetAll, end = "")
                                    if wederpartij.upper() in afsluitlijst:
                                        break
                                    elif len(wederpartij) == 2 and wederpartij.upper()[0] in afsluitlijst and wederpartij.upper()[1] in afsluitlijst:
                                        break
                                    elif len(wederpartij) == 3 and wederpartij.upper()[0] in afsluitlijst and wederpartij.upper()[2] in afsluitlijst:
                                        doei()
                                    for j in inhoudvancategorie:
                                        if i[:4] == j:
                                            inhoudvancategorie.remove(j)
                                            i[2] = wederpartij[:15]
                                            inhoudvancategorie.append(i[:4])
                                            break
                                    with open(tewijzigen[0].upper(),"w") as f:
                                        print(inhoudvancategorie, file = f, end = "")
                                    if Taal == "EN":
                                        print("%s %s%d%s\n%s %s%s %s%s\n%s %s%s%s\n%s %s%s%s\n%s %s%s%s" % (for15("Date: "),col3,i[0],ResetAll,for15("Amount: "),col3,Valuta,forn(i[1]),ResetAll,for15("Other party: "),col3,wederpartij,ResetAll,for15("About: "),col3,i[3],ResetAll,for15("Category: "),col,alternatievenaam,ResetAll))
                                    elif Taal == "IT":
                                        print("%s %s%d%s\n%s %s%s %s%s\n%s %s%s%s\n%s %s%s%s\n%s %s%s%s" % (for15("Data: "),col3,i[0],ResetAll,for15("Somma: "),col3,Valuta,forn(i[1]),ResetAll,for15("Controparte: "),col3,wederpartij,ResetAll,for15("Riguarda: "),col3,i[3],ResetAll,for15("Categoria: "),col,alternatievenaam,ResetAll))
                                    else:
                                        print("%s %s%d%s\n%s %s%s %s%s\n%s %s%s%s\n%s %s%s%s\n%s %s%s%s" % (for15("Datum: "),col3,i[0],ResetAll,for15("Bedrag: "),col3,Valuta,forn(i[1]),ResetAll,for15("Wederpartij: "),col3,wederpartij,ResetAll,for15("Betreft: "),col3,i[3],ResetAll,for15("Categorie: "),col,alternatievenaam,ResetAll))
                                elif wat == "4":
                                    if Taal == "EN":
                                        betreft = input("%sAbout%s\n  : %s" % (col3,ResetAll,col3))
                                    elif Taal == "IT":
                                        betreft = input("%sRiguarda%s\n  : %s" % (col3,ResetAll,col3))
                                    else:
                                        betreft = input("%sBetreft%s\n  : %s" % (col3,ResetAll,col3))
                                    print(ResetAll, end = "")
                                    if betreft.upper() in afsluitlijst:
                                        break
                                    elif len(betreft) == 2 and betreft.upper()[0] in afsluitlijst and betreft.upper()[1] in afsluitlijst:
                                        break
                                    elif len(betreft) == 3 and betreft.upper()[0] in afsluitlijst and betreft.upper()[2] in afsluitlijst:
                                        doei()
                                    for j in inhoudvancategorie:
                                        if i[:4] == j:
                                            inhoudvancategorie.remove(j)
                                            i[3] = betreft[:18]
                                            inhoudvancategorie.append(i[:4])
                                            break
                                    with open(tewijzigen[0].upper(),"w") as f:
                                        print(inhoudvancategorie, file = f, end = "")
                                    if Taal == "EN":
                                        print("%s %s%d%s\n%s %s%s %s%s\n%s %s%s%s\n%s %s%s%s\n%s %s%s%s" % (for15("Date: "),col3,i[0],ResetAll,for15("Amount: "),col3,Valuta,forn(i[1]),ResetAll,for15("Other party: "),col3,i[2],ResetAll,for15("About: "),col3,betreft,ResetAll,for15("Category: "),col,alternatievenaam,ResetAll))
                                    elif Taal == "IT":
                                        print("%s %s%d%s\n%s %s%s %s%s\n%s %s%s%s\n%s %s%s%s\n%s %s%s%s" % (for15("Data: "),col3,i[0],ResetAll,for15("Somma: "),col3,Valuta,forn(i[1]),ResetAll,for15("Controparte: "),col3,i[2],ResetAll,for15("Riguarda: "),col3,betreft,ResetAll,for15("Categoria: "),col,alternatievenaam,ResetAll))
                                    else:
                                        print("%s %s%d%s\n%s %s%s %s%s\n%s %s%s%s\n%s %s%s%s\n%s %s%s%s" % (for15("Datum: "),col3,i[0],ResetAll,for15("Bedrag: "),col3,Valuta,forn(i[1]),ResetAll,for15("Wederpartij: "),col3,i[2],ResetAll,for15("Betreft: "),col3,betreft,ResetAll,for15("Categorie: "),col,alternatievenaam,ResetAll))
                                elif wat == "5":
                                    if Taal == "EN":
                                        print("To which category do you want to transfer %s" % (col+tewijzigen.upper()+ResetAll))
                                    elif Taal == "IT":
                                        print("In quale categoria vuoi trasferire %s" % (col+tewijzigen.upper()+ResetAll))
                                    else:
                                        print("Naar welke categorie wil je %s overzetten" % (col+tewijzigen.upper()+ResetAll))
                                    alt()
                                    waar = input("  : ")
                                    if waar.upper() in afsluitlijst or waar.upper() not in lijst:
                                        break
                                    elif len(waar) == 2 and waar.upper()[0] in afsluitlijst and waar.upper()[1] in afsluitlijst:
                                        break
                                    elif len(waar) == 3 and waar.upper()[0] in afsluitlijst and waar.upper()[2] in afsluitlijst:
                                        doei()
                                    else:
                                        waar = waar.upper()
                                        try:
                                            with open(waar,"r") as f:
                                                inhoudvancategorie = ast.literal_eval(f.read())
                                        except(Exception) as error:
                                            #print(error)
                                            if Taal == "EN":
                                                nieuwecategorie = input("Give the %snew category%s %s a name\n  : " % (col3,ResetAll,catcol[waar]+waar+ResetAll))
                                            elif Taal == "IT":
                                                nieuwecategorie = input("Dai la %snuova categoria%s %s un nome\n  : " % (col3,ResetAll,catcol[waar]+waar+ResetAll))
                                            else:
                                                nieuwecategorie = input("Geef de %snieuwe categorie%s %s een naam\n  : " % (col3,ResetAll,catcol[waar]+waar+ResetAll))
                                            if nieuwecategorie.upper() in afsluitlijst:
                                                break
                                            elif len(nieuwecategorie) == 2 and nieuwecategorie.upper()[0] in afsluitlijst and nieuwecategorie.upper()[1] in afsluitlijst:
                                                break
                                            elif len(nieuwecategorie) == 3 and nieuwecategorie.upper()[0] in afsluitlijst and nieuwecategorie.upper()[2] in afsluitlijst:
                                                doei()
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
                                                if Taal == "EN":
                                                    print("%sThe ID changed, generate new %sID%s's!%s" % (colslecht,LichtGeel,colslecht,ResetAll))
                                                elif Taal == "IT":
                                                    print("%sL\'ID è cambiato, genera nuovi %sID%s!%s" % (colslecht,LichtGeel,colslecht,ResetAll))
                                                else:
                                                    print("%sHet ID is gewijzigd, genereer nieuwe %sID%s's!%s" % (colslecht,LichtGeel,colslecht,ResetAll))
                                                if Taal == "EN":
                                                    alternatievenaam= alternatievenaam.replace("saldo & inkomen","funds & income").replace("vaste lasten","fixed costs").replace("boodschappen","groceries").replace("reis & verblijf","travel & stay").replace("leningen","loans").replace("overig","other")
                                                    print("%s %s%d%s\n%s %s%s %s%s\n%s %s%s%s\n%s %s%s%s\n%s %s%s%s" % (for15("Date: "),col3,i[0],ResetAll,for15("Amount: "),col3,Valuta,forn(i[1]),ResetAll,for15("Other party: "),col3,i[2],ResetAll,for15("About: "),col3,i[3],ResetAll,for15("Category: "),col,alternatievenaam,ResetAll))
                                                elif Taal == "IT":
                                                    alternatievenaam = alternatievenaam.replace("saldo & inkomen","saldo & reddito").replace("vaste lasten","costi fissi").replace("boodschappen","spese").replace("reis & verblijf","viaggioalloggio").replace("leningen","prestiti").replace("overig","altro")
                                                    print("%s %s%d%s\n%s %s%s %s%s\n%s %s%s%s\n%s %s%s%s\n%s %s%s%s" % (for15("Data: "),col3,i[0],ResetAll,for15("Somma: "),col3,Valuta,forn(i[1]),ResetAll,for15("Controparte: "),col3,i[2],ResetAll,for15("Riguarda: "),col3,i[3],ResetAll,for15("Categoria: "),col,alternatievenaam,ResetAll))
                                                else:
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
            pass
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
                if Taal == "EN":
                    teverwijderen = input("Which ID do you want to %sremove%s\n  : " % (col4, ResetAll))
                elif Taal == "IT":
                    teverwijderen = input("Quale ID vuoi %srimuovere%s\n  : " % (col4, ResetAll))
                else:
                    teverwijderen = input("Welk ID wil je %sverwijderen%s\n  : " % (col4, ResetAll))
                if teverwijderen.upper() in afsluitlijst:
                    break
                elif len(teverwijderen) == 2 and teverwijderen.upper()[0] in afsluitlijst and teverwijderen.upper()[1] in afsluitlijst:
                    break
                elif len(teverwijderen) == 3 and teverwijderen.upper()[0] in afsluitlijst and teverwijderen.upper()[2] in afsluitlijst:
                    doei()
                else:
                    try:
                        with open(teverwijderen[0].upper(),"r") as f:
                            inhoudvancategorie = ast.literal_eval(f.read())
                        alternatievenaam = alternatievenamenlijst[teverwijderen[0].upper()]
                        col = catcol[teverwijderen[0].upper()]
                        for i in sel:
                            if i[4] == teverwijderen[0].upper()+teverwijderen[1:]:
                                if Taal == "EN":
                                    alternatievenaam= alternatievenaam.replace("saldo & inkomen","funds & income").replace("vaste lasten","fixed costs").replace("boodschappen","groceries").replace("reis & verblijf","travel & stay").replace("leningen","loans").replace("overig","other")
                                    wat = input("  %s %s\n  %s %s %s\n  %s %s\n  %s %s\n  %s %s\nConfirm\n  : %s" % (for15("Date: "),col4+str(i[0])+ResetAll,for15("Amount: "),col4+Valuta,str(i[1])+ResetAll,for15("Other party: "),col4+i[2]+ResetAll,for15("About: "),col4+i[3]+ResetAll,for15("Category: "),col4+alternatievenaam,ResetAll))
                                elif Taal == "IT":
                                    alternatievenaam = alternatievenaam.replace("saldo & inkomen","saldo & reddito").replace("vaste lasten","costi fissi").replace("boodschappen","spese").replace("reis & verblijf","viaggioalloggio").replace("leningen","prestiti").replace("overig","altro")
                                    wat = input("  %s %s\n  %s %s %s\n  %s %s\n  %s %s\n  %s %s\nConferma\n  : %s" % (for15("Data: "),col4+str(i[0])+ResetAll,for15("Somma: "),col4+Valuta,str(i[1])+ResetAll,for15("Controparte: "),col4+i[2]+ResetAll,for15("Riguarda: "),col4+i[3]+ResetAll,for15("Categoria: "),col4+alternatievenaam,ResetAll))
                                else:
                                    wat = input("  %s %s\n  %s %s %s\n  %s %s\n  %s %s\n  %s %s\nBevestig\n  : %s" % (for15("Datum: "),col4+str(i[0])+ResetAll,for15("Bedrag: "),col4+Valuta,str(i[1])+ResetAll,for15("Wederpartij: "),col4+i[2]+ResetAll,for15("Betreft: "),col4+i[3]+ResetAll,for15("Categorie: "),col4+alternatievenaam,ResetAll))
                                if wat.upper() in jalijst:
                                    for j in inhoudvancategorie:
                                        if i[:4] == j:
                                            inhoudvancategorie.remove(j)
                                            break
                                    with open(teverwijderen[0].upper(),"w") as f:
                                        print(inhoudvancategorie, file = f, end = "")
                                        if Taal == "EN":
                                            print("%sOK%s" % (col4,ResetAll))
                                        elif Taal == "IT":
                                            print("%sOK%s" % (col4,ResetAll))
                                        else:
                                            print("%sOK%s" % (col4,ResetAll))
                                    with open(teverwijderen[0].upper(),"w") as f:
                                        if Taal == "EN":
                                            undo = input("(\"U\" for \"undo\")")
                                        elif Taal == "IT":
                                            undo = input("(\"U\" per \"undo\")")
                                        else:
                                            undo = input("(\"U\" voor \"undo\")")
                                        if undo.upper() == "U":
                                            inhoudvancategorie.append(j)
                                        print(inhoudvancategorie, file = f, end = "")
                                elif len(wat) == 2 and wat.upper()[0] in afsluitlijst and wat.upper()[1] in afsluitlijst:
                                    verwijder = "Q"
                                    break
                                elif len(wat) == 3 and wat.upper()[0] in afsluitlijst and wat.upper()[2] in afsluitlijst:
                                    doei()
                                print()
                    except(Exception) as error:
                        #print(error)
                        pass
                if verwijder == "Q":
                    break
        except(Exception) as error:
            pass
        print()
        print(toplijn)
        print()

    elif keuze1 == "5": # SPAARPOTTEN
        print()
        spaarpotten = "Y"
        while spaarpotten == "Y":
            spaartotaal = 0
            with open("A","r") as a:
                Uitgaven = ast.literal_eval(a.read())[0]
            try:
                with open("spaarpotten","r") as s:
                    spaar = ast.literal_eval(s.read())
                    spaartel = 0
                    for i,j in spaar.items():
                        spaartel += 1
                        spaartotaal += j
                    if Taal == "EN":
                        print("    Total in piggy banks: %s" % (col5+Valuta+fornum(spaartotaal)+ResetAll))
                        print("    %s is reserved for monthly expenses" % (col5+Valuta+fornum(Uitgaven*-1)+ResetAll))
                        print("    Remains %s unpiggied" % (col5+Valuta+fornum(moni-spaartotaal+Uitgaven)+ResetAll))
                        print("    A buffer of %s on payday (i.p) is recommended" % (col5+Valuta+fornum(Uitgaven*-1)+ResetAll))
                    elif Taal == "IT":
                        print("    Totale in salvadanai: %s" % (col5+Valuta+fornum(spaartotaal)+ResetAll))
                        print("    %s è riservato per spese mensili" % (col5+Valuta+fornum(Uitgaven*-1)+ResetAll))
                        print("    Rimane %s nonsalvadanato" % (col5+Valuta+fornum(moni-spaartotaal+Uitgaven)+ResetAll))
                        print("    Un buffer di %s su giorno di paga (s.p.) è raccomandato" % (col5+Valuta+fornum(Uitgaven*-1)+ResetAll))
                    else:
                        print("    Totaal in spaarpotten: %s" % (col5+Valuta+fornum(spaartotaal)+ResetAll))
                        print("    %s is gereserveerd voor maandelijkse uitgaven" % (col5+Valuta+fornum(Uitgaven*-1)+ResetAll))
                        print("    Er blijft %s ongespaarpot over" % (col5+Valuta+fornum(moni-spaartotaal+Uitgaven)+ResetAll))
                        print("    Een buffer van %s op betaaldag wordt (i.m.) aanbevolen" % (col5+Valuta+fornum(Uitgaven*-1)+ResetAll))
                    print()
            except(Exception) as error:
                print(error)
                if Taal == "EN":
                    print("There are no piggy banks (yet)")
                    print()
                elif Taal == "IT":
                    print("Non ci sono (ancora) salvadanai")
                    print()
                else:
                    print("Er zijn (nog) geen spaarpotten")
                    print()
            if moni-Uitgaven < spaartotaal:
                col5 = Rood
            if Taal == "EN":
                keuze2 = input("%s Make a choice%s\n  >1 %sView piggy banks%s\n   2 %sModify piggy bank%s\n   3 %sAdd new piggy bank%s\n   4 %sRemove piggy bank%s\n   : " % (col5,ResetAll,LichtGeel,ResetAll,LichtCyaan,ResetAll,LichtGroen,ResetAll,LichtRood,ResetAll))
            elif Taal == "IT":
                keuze2 = input("%s Fai una scelta%s\n  >1 %sVedere salvadanai%s\n   2 %sModificare salvadanaio%s\n   3 %sAggiungere salvadanaio%s\n   4 %sEliminare salvadanaio%s\n   : " % (col5,ResetAll,LichtGeel,ResetAll,LichtCyaan,ResetAll,LichtGroen,ResetAll,LichtRood,ResetAll))
            else:
                keuze2 = input("%s Maak een keuze%s\n  >1 %sBekijk spaarpotten%s\n   2 %sWijzig spaarpot%s\n   3 %sVoeg nieuwe spaarpot toe%s\n   4 %sVerwijder spaarpot%s\n   : " % (col5,ResetAll,LichtGeel,ResetAll,LichtCyaan,ResetAll,LichtGroen,ResetAll,LichtRood,ResetAll))
            if keuze2.upper() in afsluitlijst:
                break
            elif len(keuze2) == 2 and keuze2.upper()[0] in afsluitlijst and keuze2.upper()[1] in afsluitlijst:
                break
            elif len(keuze2) == 3 and keuze2.upper()[0] in afsluitlijst and keuze2.upper()[2] in afsluitlijst:
                doei()
            elif keuze2 == "2":
                potwijzig = "Y"
                while potwijzig == "Y":
                    if Taal == "EN":
                        print("  Which %spiggy bank%s do you want to %smodify%s" % (col5,ResetAll,LichtCyaan,ResetAll))
                    elif Taal == "IT":
                        print("  Quale %ssalvadanaio%s vuoi %smodificare%s" % (col5,ResetAll,LichtCyaan,ResetAll))
                    else:
                        print("  Welke %sspaarpot%s wil je %swijzigen%s" % (col5,ResetAll,LichtCyaan,ResetAll))
                    spaartel = 0
                    try:
                        with open("spaarpotten","r") as s:
                            spaar = ast.literal_eval(s.read())
                            spaarlijst = []
                            for i,j in spaar.items():
                                spaartel += 1
                                if Taal == "EN":
                                    print("%s %s contains %s" % (spaartel,col5+for15(i)+ResetAll,Valuta+fornum(j)))
                                elif Taal == "IT":
                                    print("%s %s contiene %s" % (spaartel,col5+for15(i)+ResetAll,Valuta+fornum(j)))
                                else:
                                    print("%s %s bevat %s" % (spaartel,col5+for15(i)+ResetAll,Valuta+fornum(j)))
                                spaarlijst.append(i)
                        keuze3 = input("    : ")
                        if keuze3.upper() in afsluitlijst:
                            break
                        elif len(keuze3) == 2 and keuze3.upper()[0] in afsluitlijst and keuze3.upper()[1] in afsluitlijst:
                            spaarpotten = "N"
                            break
                        elif len(keuze3) == 3 and keuze3.upper()[0] in afsluitlijst and keuze3.upper()[2] in afsluitlijst:
                            doei()
                        else:
                            try:
                                keuze3 = int(keuze3)-1
                                if keuze3 in range(spaartel):
                                    if Taal == "EN":
                                        keuze4 = input("   What do you want to modify\n     1 Name   %s\n    >2 Value %s\n     : " % (col5+for15(spaarlijst[keuze3])+ResetAll,col5+Valuta+fornum(spaar[spaarlijst[keuze3]])+ResetAll))
                                    elif Taal == "IT":
                                        keuze4 = input("   Cosa vuoi modificare\n     1 Nome   %s\n    >2 Valore %s\n     : " % (col5+for15(spaarlijst[keuze3])+ResetAll,col5+Valuta+fornum(spaar[spaarlijst[keuze3]])+ResetAll))
                                    else:
                                        keuze4 = input("   Wat wil je wijzigen\n     1 Naam   %s\n    >2 Waarde %s\n     : " % (col5+for15(spaarlijst[keuze3])+ResetAll,col5+Valuta+fornum(spaar[spaarlijst[keuze3]])+ResetAll))
                                    if keuze4.upper() in afsluitlijst:
                                        break
                                    elif len(keuze4) == 2 and keuze4.upper()[0] in afsluitlijst and keuze4.upper()[1] in afsluitlijst:
                                        spaarpotten = "N"
                                        break
                                    elif len(keuze4) == 3 and keuze4.upper()[0] in afsluitlijst and keuze4.upper()[2] in afsluitlijst:
                                        doei()
                                    elif keuze4 == "1":
                                        if Taal == "EN":
                                            nieuwekey = input("    Rename this piggy bank %s\n      : %s" % (col5+for15(spaarlijst[keuze3])+ResetAll,col5))[:15]
                                        elif Taal == "IT":
                                            nieuwekey = input("    Rinomina questo salvadanaio %s\n      : %s" % (col5+for15(spaarlijst[keuze3])+ResetAll,col5))[:15]
                                        else:
                                            nieuwekey = input("    Geef deze spaarpot %s een nieuwe naam\n      : %s" % (col5+for15(spaarlijst[keuze3])+ResetAll,col5))[:15]
                                        print(ResetAll, end = "")
                                        if nieuwekey.upper() in afsluitlijst:
                                            break
                                        elif len(nieuwekey) == 2 and nieuwekey.upper()[0] in afsluitlijst and nieuwekey.upper()[1] in afsluitlijst:
                                            spaarpotten = "N"
                                            break
                                        elif len(nieuwekey) == 3 and nieuwekey.upper()[0] in afsluitlijst and nieuwekey.upper()[2] in afsluitlijst:
                                            doei()
                                        spaar[nieuwekey] = spaar[spaarlijst[keuze3]]
                                        del spaar[spaarlijst[keuze3]]
                                        with open("spaarpotten","w") as s:
                                            print(spaar, file = s, end = "")
                                    else:
                                        inspaarpotlijst = []
                                        for i,j in spaar.items():
                                            if i != spaarlijst[keuze3]:
                                                inspaarpotlijst.append(j)
                                        inspaarpot = 0
                                        for i in inspaarpotlijst:
                                            inspaarpot += i
                                        beschikbaar = round(moni,2) + Uitgaven - inspaarpot
                                        nieuwewaarde = "Y"
                                        while nieuwewaarde == "Y":
                                            if Taal == "EN":
                                                nieuwevalue = input("    Enter a new value\n      : %s" % (col5))
                                            elif Taal == "IT":
                                                nieuwevalue = input("    Inserire un nuovo valore\n      : %s" % (col5))
                                            else:
                                                nieuwevalue = input("    Geef een nieuwe waarde op\n      : %s" % (col5))
                                            print(ResetAll, end = "")
                                            if nieuwevalue.upper() in afsluitlijst:
                                                break
                                            elif len(nieuwevalue) == 2 and nieuwevalue.upper()[0] in afsluitlijst and nieuwevalue.upper()[1] in afsluitlijst:
                                                spaarpotten = "N"
                                                potwijzig = "N"
                                                break
                                            elif len(nieuwevalue) == 3 and nieuwevalue.upper()[0] in afsluitlijst and nieuwevalue.upper()[2] in afsluitlijst:
                                                doei()
                                            try:
                                                nieuwevalue = round(float(nieuwevalue),2)
                                                if nieuwevalue > beschikbaar:
                                                    if Taal == "EN":
                                                        print("%sThat is too much to set aside%s" % (colslecht,ResetAll))
                                                    elif Taal == "IT":
                                                        print("%sQuesto è troppo per mettere da parte%s" % (colslecht,ResetAll))
                                                    else:
                                                        print("%sDat is teveel om weg te zetten%s" % (colslecht,ResetAll))
                                                elif nieuwevalue < 0:
                                                    if Taal == "EN":
                                                        print("%sThat is too little to set aside%s" % (colslecht,ResetAll))
                                                    elif Taal == "IT":
                                                        print("%sQuesto è troppo poco per mettere da parte%s" % (colslecht,ResetAll))
                                                    else:
                                                        print("%sDat is te weinig om weg te zetten%s" % (colslecht,ResetAll))
                                                else:
                                                    spaar[spaarlijst[keuze3]] = nieuwevalue
                                                    with open("spaarpotten","w") as s:
                                                        print(spaar, file = s, end = "")
                                                    if Taal == "EN":
                                                        print("%s contains %s" % (col5+for15(spaarlijst[keuze3])+ResetAll,Valuta+fornum(spaar[spaarlijst[keuze3]])))
                                                    elif Taal == "IT":
                                                        print("%s contiene %s" % (col5+for15(spaarlijst[keuze3])+ResetAll,Valuta+fornum(spaar[spaarlijst[keuze3]])))
                                                    else:
                                                        print("%s bevat %s" % (col5+for15(spaarlijst[keuze3])+ResetAll,Valuta+fornum(spaar[spaarlijst[keuze3]])))
                                                    break
                                            except:
                                                if Taal == "EN":
                                                    print("%sThat is not a valid value%s" % (colslecht,ResetAll))
                                                elif Taal == "IT":
                                                    print("%sQuesto non è un valore valido%s" % (colslecht,ResetAll))
                                                else:
                                                    print("%sDat is geen geldige waarde%s" % (colslecht,ResetAll))
                                else:
                                    if Taal == "EN":
                                        print("That piggy bank doesn't exist (yet)")
                                    elif Taal == "IT":
                                        print("Questo salvadanaio non existe (ancora)")
                                    else:
                                        print("Die spaarpot bestaat (nog) niet")
                            except(Exception) as error:
                                print(error)
                    except(Exception) as error:
                        pass
            elif keuze2 == "3":
                potnieuw = "Y"
                while potnieuw == "Y":
                    try:
                        with open("spaarpotten","r") as s:
                            spaar = ast.literal_eval(s.read())
                            spaarlijst = []
                            for i,j in spaar.items():
                                if Taal == "EN":
                                    print("%s contains %s" % (col5+for15(i)+ResetAll,Valuta+fornum(j)))
                                elif Taal == "IT":
                                    print("%s contiene %s" % (col5+for15(i)+ResetAll,Valuta+fornum(j)))
                                else:
                                    print("%s bevat %s" % (col5+for15(i)+ResetAll,Valuta+fornum(j)))
                                spaarlijst.append(i)
                    except:
                        spaar = {}
                        spaarlijst = []
                    if Taal == "EN":
                        nieuwespaarpot = input("  Enter the %sname%s of the new piggy bank\n    : %s" % (col5,ResetAll,col5))[:15]
                        print(ResetAll, end = "")
                    elif Taal == "IT":
                        nieuwespaarpot = input("  Inserisci il %snome%s del nuovo salvadanaio\n    : %s" % (col5,ResetAll,col5))[:15]
                        print(ResetAll, end = "")
                    else:
                        nieuwespaarpot = input("  Typ de %snaam%s van de nieuwe spaarpot\n    : %s" % (col5,ResetAll,col5))[:15]
                        print(ResetAll, end = "")
                    if nieuwespaarpot.upper() in afsluitlijst:
                        break
                    elif len(nieuwespaarpot) == 2 and nieuwespaarpot.upper()[0] in afsluitlijst and nieuwespaarpot.upper()[1] in afsluitlijst:
                        spaarpotten = "N"
                        break
                    elif len(nieuwespaarpot) == 3 and nieuwespaarpot.upper()[0] in afsluitlijst and nieuwespaarpot.upper()[2] in afsluitlijst:
                        doei()
                    else:
                        with open("A","r") as a:
                            Uitgaven = ast.literal_eval(a.read())[0]
                        inspaarpotlijst = []
                        for i,j in spaar.items():
                            inspaarpotlijst.append(j)
                        inspaarpot = 0
                        for i in inspaarpotlijst:
                            inspaarpot += i
                        beschikbaar = round(moni,2) + Uitgaven - inspaarpot
                        nieuwewaarde = "Y"
                        while nieuwewaarde == "Y":
                            if Taal == "EN":
                                nieuwevalue = input("  Enter a new value\n    : %s" % (col5))
                            elif Taal == "IT":
                                nieuwevalue = input("  Inserire un nuovo valore\n    : %s" % (col5))
                            else:
                                nieuwevalue = input("  Geef een nieuwe waarde op\n    : %s" % (col5))
                            print(ResetAll, end = "")
                            if nieuwevalue.upper() in afsluitlijst:
                                break
                            elif len(nieuwevalue) == 2 and nieuwevalue.upper()[0] in afsluitlijst and nieuwevalue.upper()[1] in afsluitlijst:
                                spaarpotten = "N"
                                potnieuw = "N"
                                break
                            elif len(nieuwevalue) == 3 and nieuwevalue.upper()[0] in afsluitlijst and nieuwevalue.upper()[2] in afsluitlijst:
                                doei()
                            try:
                                nieuwevalue = round(float(nieuwevalue),2)
                                if nieuwevalue > beschikbaar:
                                    if Taal == "EN":
                                        print("%sThat is too much to set aside%s" % (colslecht,ResetAll))
                                    elif Taal == "IT":
                                        print("%sQuesto è troppo per mettere da parte%s" % (colslecht,ResetAll))
                                    else:
                                        print("%sDat is teveel om weg te zetten%s" % (colslecht,ResetAll))
                                elif nieuwevalue < 0:
                                    if Taal == "EN":
                                        print("%sThat is too little to set aside%s" % (colslecht,ResetAll))
                                    elif Taal == "IT":
                                        print("%sQuesto è troppo poco per mettere da parte%s" % (colslecht,ResetAll))
                                    else:
                                        print("%sDat is te weinig om weg te zetten%s" % (colslecht,ResetAll))
                                else:
                                    spaar[nieuwespaarpot] = nieuwevalue
                                    with open("spaarpotten","w") as s:
                                        print(spaar, file = s, end = "")
                                    if Taal == "EN":
                                        print("%s contains %s" % (col5+for15(nieuwespaarpot)+ResetAll,Valuta+fornum(nieuwevalue)))
                                    elif Taal == "IT":
                                        print("%s contiene %s" % (col5+for15(nieuwespaarpot)+ResetAll,Valuta+fornum(nieuwevalue)))
                                    else:
                                        print("%s bevat %s" % (col5+for15(nieuwespaarpot)+ResetAll,Valuta+fornum(nieuwevalue)))
                                    break
                            except:
                                if Taal == "EN":
                                    print("%sThat is not a valid value%s" % (colslecht,ResetAll))
                                elif Taal == "IT":
                                    print("%sQuesto non è un valore valido%s" % (colslecht,ResetAll))
                                else:
                                    print("%sDat is geen geldige waarde%s" % (colslecht,ResetAll))
            elif keuze2 == "4":
                potverwijder = "Y"
                while potverwijder == "Y":
                    if Taal == "EN":
                        print("  Which %spiggy bank%s do you want to %sremove%s" % (col5,ResetAll,colslecht,ResetAll))
                    elif Taal == "IT":
                        print("  Quale %ssalvadanaio%s vuoi %seliminare%s" % (col5,ResetAll,colslecht,ResetAll))
                    else:
                        print("  Welke %sspaarpot%s wil je %sverwijderen%s" % (col5,ResetAll,colslecht,ResetAll))
                    spaartel = 0
                    try:
                        with open("spaarpotten","r") as s:
                            spaar = ast.literal_eval(s.read())
                            spaarlijst = []
                            for i,j in spaar.items():
                                spaartel += 1
                                if Taal == "EN":
                                    print("%s %s contains %s" % (spaartel,col5+for15(i)+ResetAll,Valuta+fornum(j)))
                                elif Taal == "IT":
                                    print("%s %s contiene %s" % (spaartel,col5+for15(i)+ResetAll,Valuta+fornum(j)))
                                else:
                                    print("%s %s bevat %s" % (spaartel,col5+for15(i)+ResetAll,Valuta+fornum(j)))
                                spaarlijst.append(i)
                        keuze3 = input("    : ")
                        if keuze3.upper() in afsluitlijst:
                            break
                        elif len(keuze3) == 2 and keuze3.upper()[0] in afsluitlijst and keuze3.upper()[1] in afsluitlijst:
                            spaarpotten = "N"
                            break
                        elif len(keuze3) == 3 and keuze3.upper()[0] in afsluitlijst and keuze3.upper()[2] in afsluitlijst:
                            doei()
                        else:
                            keuze3 = int(keuze3)-1
                            if keuze3 in range(spaartel):
                                del spaar[spaarlijst[keuze3]]
                                if len(spaar) == 0:
                                    os.remove("spaarpotten")
                                else:
                                    with open("spaarpotten","w") as s:
                                        print(spaar, file = s, end = "")
                    except:
                        pass
            else:
                try:
                    with open("spaarpotten","r") as s:
                        print()
                        spaar = ast.literal_eval(s.read())
                        spaartel = 0
                        spaartotaal = 0
                        for i,j in spaar.items():
                            spaartel += 1
                            spaartotaal += j
                            if Taal == "EN":
                                print("%s %s contains %s" % (spaartel,col5+for15(i)+ResetAll,Valuta+fornum(j)))
                            elif Taal == "IT":
                                print("%s %s contiene %s" % (spaartel,col5+for15(i)+ResetAll,Valuta+fornum(j)))
                            else:
                                print("%s %s bevat %s" % (spaartel,col5+for15(i)+ResetAll,Valuta+fornum(j)))
                        print()
                except(Exception) as error:
                    pass

    elif keuze1 == "0": # BEHEER
        print()
        col5 = LichtMagenta
        beheer = "Y"
        while beheer == "Y":
            if Taal == "EN":
                keuze2 = input("Make a choice\n  0 %sPrint version and info%s\n >1 %sCategory management%s\n  2 %sModify account settings%s\n  3 %sShow or hide account%s\n  4 %sSwitch visible account%s (!)\n  5 %sAdd new account%s\n  6 %sDelete account%s\n  7 %sTransfer account settings%s\n  : " % (LichtGeel,ResetAll,LichtCyaan,ResetAll,Blauw,ResetAll,Geel,ResetAll,LichtMagenta,ResetAll,LichtGroen,ResetAll,LichtRood,ResetAll,Magenta,ResetAll))
            elif Taal == "IT":
                keuze2 = input("Fai una scelta\n  0 %sPrint versione ed info%s\n >1 %sGestire categorie%s\n  2 %sModificare impostazioni del conto%s\n  3 %sEsporre o nascondere conto%s\n  4 %sPassare ad un\'altro conto visibile%s (!)\n  5 %sAggiungere un nuovo conto%s\n  6 %sEliminare un conto%s\n  7 %sTrasferire impostazioni%s\n  : " % (LichtGeel,ResetAll,LichtCyaan,ResetAll,Blauw,ResetAll,Geel,ResetAll,LichtMagenta,ResetAll,LichtGroen,ResetAll,LichtRood,ResetAll,Magenta,ResetAll))
            else:
                keuze2 = input("Maak een keuze\n  0 %sPrint versie en info%s\n >1 %sCategoriebeheer%s\n  2 %sRekeninginstellingen aanpassen%s\n  3 %sToon of verberg rekening%s\n  4 %sWissel van zichtbare rekening%s (!)\n  5 %sNieuwe rekening toevoegen%s\n  6 %sVerwijder rekening%s\n  7 %sInstellingen overzetten%s\n  : " % (LichtGeel,ResetAll,LichtCyaan,ResetAll,Blauw,ResetAll,Geel,ResetAll,LichtMagenta,ResetAll,LichtGroen,ResetAll,LichtRood,ResetAll,Magenta,ResetAll))
            if keuze2.upper() in afsluitlijst:
                break
            elif len(keuze2) == 2 and keuze2.upper()[0] in afsluitlijst and keuze2.upper()[1] in afsluitlijst:
                break
            elif len(keuze2) == 3 and keuze2.upper()[0] in afsluitlijst and keuze2.upper()[2] in afsluitlijst:
                doei()
            elif keuze2 == "2":
                headerloop = "Y"
                while headerloop == "Y":
                    #printheaderall()
                    hoe = header["Beschrijving"]
                    wie = header["Rekeninghouder"]
                    waar = header["Plaats"]
                    Taal = header["Taal"]
                    Valuta = header["Valuta"]
                    Nulregels = header["Nulregels"]
                    MarkeringLH = header["Markering L><H"]
                    Kleur = header["Kleur"]
                    Datumformaat = header["Datumformaat"]
                    Print = header["Print"]
                    if Taal == "EN":
                        Nulregels = Nulregels.replace("Ja","Yes").replace("Nee","No")
                        Print = Print.replace("Ja","Yes").replace("Nee","No")
                        Kleur = Kleur.replace("Alle","All").replace("Categorie","Category").replace("Mono","Mono").replace("Regenboog","Rainbow")
                    elif Taal == "IT":
                        Nulregels = Nulregels.replace("Ja","Sì").replace("Nee","No")
                        Print = Print.replace("Ja","Sì").replace("Nee","No")
                        Kleur = Kleur.replace("Alle","Tutti").replace("Categorie","Categoria").replace("Mono","Mono").replace("Regenboog","Arcobaleno")
                    if Taal == "EN":
                        if Datumformaat == "DDMMYYYY":
                            yymd = strnu[6:]+strnu[4:6]+strnu[:4]
                        elif Datumformaat == "DD-MM-YY":
                            yymd = strnu[6:]+"-"+strnu[4:6]+"-"+strnu[2:4]
                        elif Datumformaat == "DD/MM/YY":
                            yymd = strnu[6:]+"/"+strnu[4:6]+"/"+strnu[2:4]
                        elif Datumformaat == "DDmmm\'YY":
                            yymd = strnu[6:]+strnu[4:6].replace("01","Jan").replace("02","Feb").replace("03","Mar").replace("04","Apr").replace("05","May").replace("06","Jun").replace("07","Jul").replace("08","Aug").replace("09","Sep").replace("10","Oct").replace("11","Nov").replace("12","Dec")+"'"+strnu[2:4]
                        elif Datumformaat == "DD-mmmYY":
                            yymd = strnu[6:]+"-"+strnu[4:6].replace("01","Jan").replace("02","Feb").replace("03","Mar").replace("04","Apr").replace("05","May").replace("06","Jun").replace("07","Jul").replace("08","Aug").replace("09","Sep").replace("10","Oct").replace("11","Nov").replace("12","Dec")+strnu[2:4]
                        else:
                            yymd = strnu
                        wat = input("Choose what you want to %smodify%s\n  1 %s\n  2 %s\n  3 %s\n  4 %s\n  5 %s\n  6 %s\n  7 %s\n  8 %s\n  9 %s\n 10 %s\n  : " % (Blauw,ResetAll,colslecht+for15("Description")+ResetAll+colgoed+for15(hoe)+ResetAll, colslecht+for15("Account holder")+ResetAll+colgoed+for15(wie)+ResetAll, colslecht+for15("City")+ResetAll+colgoed+for15(waar)+ResetAll, colslecht+for15("Language")+ResetAll+colgoed+for15(Taal)+ResetAll, colslecht+for15("Currency")+ResetAll+colgoed+for15(Valuta)+ResetAll, colslecht+for15("Zero lines")+ResetAll+colgoed+for15(Nulregels)+ResetAll, colslecht+for15("Marking L><U")+ResetAll+colgoed+Valuta+fornum(MarkeringLH[0])+ResetAll+" >< "+colgoed+Valuta+fornum(MarkeringLH[1])+ResetAll, colslecht+for15("Colour")+ResetAll+colgoed+for15(Kleur)+ResetAll, colslecht+for15("Date formatting")+ResetAll+colgoed+for15(Datumformaat)+for15(yymd)+ResetAll, colslecht+for15("Print to file")+ResetAll+colgoed+for15(Print)+ResetAll))
                    elif Taal == "IT":
                        if Datumformaat == "DDMMYYYY":
                            Datumformaat = "GGMMAAAA"
                            yymd = strnu[6:]+strnu[4:6]+strnu[:4]
                        elif Datumformaat == "DD-MM-YY":
                            Datumformaat = "GG-MM-AA"
                            yymd = strnu[6:]+"-"+strnu[4:6]+"-"+strnu[2:4]
                        elif Datumformaat == "DD/MM/YY":
                            Datumformaat = "GG/MM/AA"
                            yymd = strnu[6:]+"/"+strnu[4:6]+"/"+strnu[2:4]
                        elif Datumformaat == "DDmmm\'YY":
                            Datumformaat = "GGmmm'\AA"
                            yymd = strnu[6:]+strnu[4:6].replace("01","gen").replace("02","feb").replace("03","mar").replace("04","apr").replace("05","mag").replace("06","giu").replace("07","lug").replace("08","ago").replace("09","set").replace("10","ott").replace("11","nov").replace("12","dic")+"'"+strnu[2:4]
                        elif Datumformaat == "DD-mmmYY":
                            Datumformaat = "GG-mmmAA"
                            yymd = strnu[6:]+"-"+strnu[4:6].replace("01","gen").replace("02","feb").replace("03","mar").replace("04","apr").replace("05","mag").replace("06","giu").replace("07","lug").replace("08","ago").replace("09","set").replace("10","ott").replace("11","nov").replace("12","dic")+strnu[2:4]
                        else:
                            Datumformaat = "AAAAMMGG"
                            yymd = strnu
                        wat = input("Scegli cosa vuoi %smodificare%s\n  1 %s\n  2 %s\n  3 %s\n  4 %s\n  5 %s\n  6 %s\n  7 %s\n  8 %s\n  9 %s\n 10 %s\n  : " % (Blauw,ResetAll,colslecht+for15("Descrizione")+ResetAll+colgoed+for15(hoe)+ResetAll, colslecht+for15("Intestatario")+ResetAll+colgoed+for15(wie)+ResetAll, colslecht+for15("Città")+ResetAll+colgoed+for15(waar)+ResetAll, colslecht+for15("Lingua")+ResetAll+colgoed+for15(Taal)+ResetAll, colslecht+for15("Valuta")+ResetAll+colgoed+for15(Valuta)+ResetAll, colslecht+for15("Linee a zero")+ResetAll+colgoed+for15(Nulregels)+ResetAll, colslecht+for15("Indicaz. I><S")+ResetAll+colgoed+Valuta+fornum(MarkeringLH[0])+ResetAll+" >< "+colgoed+Valuta+fornum(MarkeringLH[1])+ResetAll, colslecht+for15("Colore")+ResetAll+colgoed+for15(Kleur)+ResetAll, colslecht+for15("Formato data")+ResetAll+colgoed+for15(Datumformaat)+for15(yymd)+ResetAll, colslecht+for15("Stampa file")+ResetAll+colgoed+for15(Print)+ResetAll))
                    else:
                        if Datumformaat == "DDMMYYYY":
                            Datumformaat = "DDMMJJJJ"
                            yymd = strnu[6:]+strnu[4:6]+strnu[:4]
                        elif Datumformaat == "DD-MM-YY":
                            Datumformaat = "DD-MM-JJ"
                            yymd = strnu[6:]+"-"+strnu[4:6]+"-"+strnu[2:4]
                        elif Datumformaat == "DD/MM/YY":
                            Datumformaat = "DD/MM/JJ"
                            yymd = strnu[6:]+"/"+strnu[4:6]+"/"+strnu[2:4]
                        elif Datumformaat == "DDmmm\'YY":
                            Datumformaat = "DDmmm\'JJ"
                            yymd = strnu[6:]+strnu[4:6].replace("01","jan").replace("02","feb").replace("03","mrt").replace("04","apr").replace("05","mei").replace("06","jun").replace("07","jul").replace("08","aug").replace("09","sep").replace("10","okt").replace("11","nov").replace("12","dec")+"'"+strnu[2:4]
                        elif Datumformaat == "DD-mmmYY":
                            Datumformaat = "DD-mmmJJ"
                            yymd = strnu[6:]+"-"+strnu[4:6].replace("01","jan").replace("02","feb").replace("03","mrt").replace("04","apr").replace("05","mei").replace("06","jun").replace("07","jul").replace("08","aug").replace("09","sep").replace("10","okt").replace("11","nov").replace("12","dec")+strnu[2:4]
                        else:
                            Datumformaat = "JJJJMMDD"
                            yymd = strnu
                        wat = input("Kies wat je wilt %saanpassen%s\n  1 %s\n  2 %s\n  3 %s\n  4 %s\n  5 %s\n  6 %s\n  7 %s\n  8 %s\n  9 %s\n 10 %s\n  : " % (Blauw,ResetAll,colslecht+for15("Beschrijving")+ResetAll+colgoed+for15(hoe)+ResetAll, colslecht+for15("Rekeninghouder")+ResetAll+colgoed+for15(wie)+ResetAll, colslecht+for15("Plaats")+ResetAll+colgoed+for15(waar)+ResetAll, colslecht+for15("Taal")+ResetAll+colgoed+for15(Taal)+ResetAll, colslecht+for15("Valuta")+ResetAll+colgoed+for15(Valuta)+ResetAll, colslecht+for15("Nulregels")+ResetAll+colgoed+for15(Nulregels)+ResetAll, colslecht+for15("Markering L><H")+ResetAll+colgoed+Valuta+fornum(MarkeringLH[0])+ResetAll+" >< "+colgoed+Valuta+fornum(MarkeringLH[1])+ResetAll, colslecht+for15("Kleur")+ResetAll+colgoed+for15(Kleur)+ResetAll, colslecht+for15("Datumformaat")+ResetAll+colgoed+for15(Datumformaat)+for15(yymd)+ResetAll, colslecht+for15("Print naar file")+ResetAll+colgoed+for15(Print)+ResetAll))
                    if wat.upper() in afsluitlijst:
                        break
                    elif len(wat) == 2 and wat.upper()[0] in afsluitlijst and wat.upper()[1] in afsluitlijst:
                        headerloop = "Q"
                        break
                    elif len(wat) == 3 and wat.upper()[0] in afsluitlijst and wat.upper()[2] in afsluitlijst:
                        doei()
                    elif wat == "1":
                        if Taal == "EN":
                            hoe = input("Description\n  : %s" % (colgoed))
                        elif Taal == "IT":
                            hoe = input("Descrizione\n  : %s" % (colgoed))
                        else:
                            hoe = input("Beschrijving\n  : %s" % (colgoed))
                        print(ResetAll, end = "")
                        if hoe.upper() in afsluitlijst:
                            break
                        elif len(hoe) == 2 and hoe.upper()[0] in afsluitlijst and hoe.upper()[1] in afsluitlijst:
                            headerloop = "Q"
                            break
                        elif len(hoe) == 3 and hoe.upper()[0] in afsluitlijst and hoe.upper()[2] in afsluitlijst:
                            doei()
                        header["Beschrijving"] = hoe
                    elif wat == "2":
                        if Taal == "EN":
                            wie = input("Account holder\n  : %s" % (colgoed))
                        elif Taal == "IT":
                            wie = input("Intestatario\n  : %s" % (colgoed))
                        else:
                            wie = input("Rekeninghouder\n  : %s" % (colgoed))
                        print(ResetAll, end = "")
                        if wie.upper() in afsluitlijst:
                            break
                        elif len(wie) == 2 and wie.upper()[0] in afsluitlijst and wie.upper()[1] in afsluitlijst:
                            headerloop = "Q"
                            break
                        elif len(wie) == 3 and wie.upper()[0] in afsluitlijst and wie.upper()[2] in afsluitlijst:
                            doei()
                        header["Rekeninghouder"] = wie
                    elif wat == "3":
                        if Taal == "EN":
                            waar = input("City\n  : %s" % (colgoed))
                        elif Taal == "IT":
                            waar = input("Città\n  : %s" % (colgoed))
                        else:
                            waar = input("Plaats\n  : %s" % (colgoed))
                        print(ResetAll, end = "")
                        if waar.upper() in afsluitlijst:
                            break
                        elif len(waar) == 2 and waar.upper()[0] in afsluitlijst and waar.upper()[1] in afsluitlijst:
                            headerloop = "Q"
                            break
                        elif len(waar) == 3 and waar.upper()[0] in afsluitlijst and waar.upper()[2] in afsluitlijst:
                            doei()
                        header["Plaats"] = waar
                    elif wat == "4":
                        if Taal == "EN":
                            taal = input("Language\n >1 NL\n  2 EN\n  3 IT\n  : %s" % (colgoed))
                        elif Taal == "IT":
                            taal = input("Lingua\n >1 NL\n  2 EN\n  3 IT\n  : %s" % (colgoed))
                        else:
                            taal = input("Taal\n >1 NL\n  2 EN\n  3 IT\n  : %s" % (colgoed))
                        print(ResetAll, end = "")
                        if taal.upper() in afsluitlijst:
                            break
                        elif len(taal) == 2 and taal.upper()[0] in afsluitlijst and taal.upper()[1] in afsluitlijst:
                            headerloop = "Q"
                            break
                        elif len(taal) == 3 and taal.upper()[0] in afsluitlijst and taal.upper()[2] in afsluitlijst:
                            doei()
                        elif taal == "2":
                            Taal = "EN"
                        elif taal == "3":
                            Taal = "IT"
                        else:
                            Taal = "NL"
                        header["Taal"] = Taal
                    elif wat == "5":
                        if Taal == "EN":
                            Valuta = input("Currency\n  : %s" % (colgoed))
                        elif Taal == "IT":
                            Valuta = input("Valuta\n  : %s" % (colgoed))
                        else:
                            Valuta = input("Valuta\n  : %s" % (colgoed))
                        print(ResetAll, end = "")
                        if Valuta.upper() in afsluitlijst:
                            break
                        elif len(Valuta) == 2 and Valuta.upper()[0] in afsluitlijst and Valuta.upper()[1] in afsluitlijst:
                            headerloop = "Q"
                            break
                        elif len(Valuta) == 3 and Valuta.upper()[0] in afsluitlijst and Valuta.upper()[2] in afsluitlijst:
                            doei()
                        header["Valuta"] = Valuta
                    elif wat == "6":
                        if Taal == "EN":
                            nuljanee = input("Zero lines\n  Y Yes\n >N No\n  : %s" % (colgoed))
                        elif Taal == "IT":
                            nuljanee = input("Linee a zero\n  S Si\n >N No\n  : %s" % (colgoed))
                        else:
                            nuljanee = input("Nulregels\n  J Ja\n >N Nee\n  : %s" % (colgoed))
                        print(ResetAll, end = "")
                        if nuljanee.upper() in afsluitlijst:
                            break
                        elif len(nuljanee) == 2 and nuljanee.upper()[0] in afsluitlijst and nuljanee.upper()[1] in afsluitlijst:
                            headerloop = "Q"
                            break
                        elif len(nuljanee) == 3 and nuljanee.upper()[0] in afsluitlijst and nuljanee.upper()[2] in afsluitlijst:
                            doei()
                        elif nuljanee.upper() in jalijst:
                            header["Nulregels"] = "Ja"
                        else:
                            header["Nulregels"] = "Nee"
                    elif wat == "7":
                        if Taal == "EN":
                            Ondermarkering = input("Lower limit for marking %s\n  : %s" % (Omkeren+colslecht+Valuta+ResetAll,colgoed))
                        elif Taal == "IT":
                            Ondermarkering = input("Limite inferiore per indicazione %s\n  : %s" % (Omkeren+colslecht+Valuta+ResetAll,colgoed))
                        else:
                            Ondermarkering = input("Ondergrens voor markering %s\n  : %s" % (Omkeren+colslecht+Valuta+ResetAll,colgoed))
                        print(ResetAll, end = "")
                        if Ondermarkering.upper() in afsluitlijst:
                            break
                        elif len(Ondermarkering) == 2 and Ondermarkering.upper()[0] in afsluitlijst and Ondermarkering.upper()[1] in afsluitlijst:
                            headerloop = "Q"
                            break
                        elif len(Ondermarkering) == 3 and Ondermarkering.upper()[0] in afsluitlijst and Ondermarkering.upper()[2] in afsluitlijst:
                            doei()
                        elif Ondermarkering == "":
                            Ondermarkering = header["Markering L><H"][0]
                        else:
                            try:
                                Ondermarkering = round(float(Ondermarkering),2)
                            except(Exception) as error:
                                #print(error)
                                Ondermarkering = header["Markering L><H"][1] * -1
                        header["Markering L><H"][0] = Ondermarkering
                        if Taal == "EN":
                            Bovenmarkering = input("Upper limit for marking %s\n  : %s" % (Omkeren+colgoed+Valuta+ResetAll,colgoed))
                        elif Taal == "IT":
                            Bovenmarkering = input("Limite superiore per indicazione %s\n  : %s" % (Omkeren+colgoed+Valuta+ResetAll,colgoed))
                        else:
                            Bovenmarkering = input("Bovengrens voor markering %s\n  : %s" % (Omkeren+colgoed+Valuta+ResetAll,colgoed))
                        print(ResetAll, end = "")
                        if Bovenmarkering.upper() in afsluitlijst:
                            break
                        elif len(Bovenmarkering) == 2 and Bovenmarkering.upper()[0] in afsluitlijst and Bovenmarkering.upper()[1] in afsluitlijst:
                            headerloop = "Q"
                            break
                        elif len(Bovenmarkering) == 3 and Bovenmarkering.upper()[0] in afsluitlijst and Bovenmarkering.upper()[2] in afsluitlijst:
                            doei()
                        elif Bovenmarkering == "":
                            Bovenmarkering = header["Markering L><H"][1]
                        else:
                            try:
                                Bovenmarkering = round(float(Bovenmarkering),2)
                            except(Exception) as error:
                                #print(error)
                                Bovenmarkering = header["Markering L><H"][0] * -1
                        header["Markering L><H"][1] = Bovenmarkering
                    elif wat == "8":
                        if Taal == "EN":
                            Koeleur = input("Colour\n%s  1 All%s\n%s  2 Category%s\n  3 Mono\n%s  4 %sR%sa%si%sn%sb%so%sw%s\n  : %s" % ("\033[95m","\033[0m","\033[31m","\033[0m","\033[45m","\033[41m","\033[43m","\033[103m","\033[42m","\033[44m","\033[45m","\033[41m","\033[0m",colgoed))
                        elif Taal == "IT":
                            Koeleur = input("Colore\n%s  1 Tutti%s\n%s  2 Categoria%s\n  3 Mono\n%s  4 %sA%sr%sc%so%sb%sa%sl%se%sn%so%s\n  : %s" % ("\033[95m","\033[0m","\033[31m","\033[0m","\033[45m","\033[41m","\033[43m","\033[103m","\033[42m","\033[44m","\033[45m","\033[41m","\033[43m","\033[103m","\033[42m","\033[0m",colgoed))
                        else:
                            Koeleur = input("Kleur\n%s  1 Alles%s\n%s  2 Categorie%s\n  3 Mono\n%s  4 %sR%se%sg%se%sn%sb%so%so%sg%s\n  : %s" % ("\033[95m","\033[0m","\033[31m","\033[0m","\033[45m","\033[41m","\033[43m","\033[103m","\033[42m","\033[44m","\033[45m","\033[41m","\033[43m","\033[103m","\033[0m",colgoed))
                        print(ResetAll, end = "")
                        if Koeleur.upper() in afsluitlijst:
                            break
                        elif len(Koeleur) == 2 and Koeleur.upper()[0] in afsluitlijst and Koeleur.upper()[1] in afsluitlijst:
                            headerloop = "Q"
                            break
                        elif len(Koeleur) == 3 and Koeleur.upper()[0] in afsluitlijst and Koeleur.upper()[2] in afsluitlijst:
                            doei()
                        elif Koeleur.upper() == "1":
                            header["Kleur"] = "Alle"
                        elif Koeleur.upper() == "2":
                            header["Kleur"] = "Categorie"
                        elif Koeleur.upper() == "3":
                            header["Kleur"] = "Mono"
                        elif Koeleur.upper() == "4":
                            header["Kleur"] = "Regenboog"
                    elif wat == "9":
                        if Taal == "EN":
                            yymd4 = strnu[6:]+strnu[4:6].replace("01","Jan").replace("02","Feb").replace("03","Mar").replace("04","Apr").replace("05","May").replace("06","Jun").replace("07","Jul").replace("08","Aug").replace("09","Sep").replace("10","Oct").replace("11","Nov").replace("12","Dec")+"'"+strnu[2:4]
                            yymd5 = strnu[6:]+"-"+strnu[4:6].replace("01","Jan").replace("02","Feb").replace("03","Mar").replace("04","Apr").replace("05","May").replace("06","Jun").replace("07","Jul").replace("08","Aug").replace("09","Sep").replace("10","Oct").replace("11","Nov").replace("12","Dec")+strnu[2:4]
                            formaat = input("Choose your preferred date formatting\n >0 YYYYMMDD (%s)\n  1 DDMMYYYY (%s)\n  2 DD-MM-YY (%s)\n  3 DD/MM/YY (%s)\n  4 DDmmm\'YY (%s)\n  5 DD-mmmYY (%s)\n  :%s" % (strnu,strnu[6:]+strnu[4:6]+strnu[:4],strnu[6:]+"-"+strnu[4:6]+"-"+strnu[2:4],strnu[6:]+"/"+strnu[4:6]+"/"+strnu[2:4],yymd4,yymd5,colgoed))
                        elif Taal == "IT":
                            yymd4 = strnu[6:]+strnu[4:6].replace("01","gen").replace("02","feb").replace("03","mar").replace("04","apr").replace("05","mag").replace("06","giu").replace("07","lug").replace("08","ago").replace("09","set").replace("10","ott").replace("11","nov").replace("12","dic")+"'"+strnu[2:4]
                            yymd5 = strnu[6:]+"-"+strnu[4:6].replace("01","gen").replace("02","feb").replace("03","mar").replace("04","apr").replace("05","mag").replace("06","giu").replace("07","lug").replace("08","ago").replace("09","set").replace("10","ott").replace("11","nov").replace("12","dic")+strnu[2:4]
                            formaat = input("Scegli il tuo formato data preferito\n >0 AAAAMMGG (%s)\n  1 GGMMAAAA (%s)\n  2 GG-MM-AA (%s)\n  3 GG/MM/AA (%s)\n  4 GGmmm\'AA (%s)\n  5 GG-mmmAA (%s)\n  :%s" % (strnu,strnu[6:]+strnu[4:6]+strnu[:4],strnu[6:]+"-"+strnu[4:6]+"-"+strnu[2:4],strnu[6:]+"/"+strnu[4:6]+"/"+strnu[2:4],yymd4,yymd5,colgoed))
                        else:
                            yymd4 = strnu[6:]+strnu[4:6].replace("01","jan").replace("02","feb").replace("03","mrt").replace("04","apr").replace("05","mei").replace("06","jun").replace("07","jul").replace("08","aug").replace("09","sep").replace("10","okt").replace("11","nov").replace("12","dec")+"'"+strnu[2:4]
                            yymd5 = strnu[6:]+"-"+strnu[4:6].replace("01","jan").replace("02","feb").replace("03","mrt").replace("04","apr").replace("05","mei").replace("06","jun").replace("07","jul").replace("08","aug").replace("09","sep").replace("10","okt").replace("11","nov").replace("12","dec")+strnu[2:4]
                            formaat = input("Kies je voorkeursdatumformaat\n >0 JJJJMMDD (%s)\n  1 DDMMJJJJ (%s)\n  2 DD-MM-JJ (%s)\n  3 DD/MM/JJ (%s)\n  4 DDmmm\'JJ (%s)\n  5 DD-mmmJJ (%s)\n  :%s" % (strnu,strnu[6:]+strnu[4:6]+strnu[:4],strnu[6:]+"-"+strnu[4:6]+"-"+strnu[2:4],strnu[6:]+"/"+strnu[4:6]+"/"+strnu[2:4],yymd4,yymd5,colgoed))
                        print(ResetAll, end = "")
                        if formaat == "1":
                            header["Datumformaat"] = "DDMMYYYY"
                        elif formaat == "2":
                            header["Datumformaat"] = "DD-MM-YY"
                        elif formaat == "3":
                            header["Datumformaat"] = "DD/MM/YY"
                        elif formaat == "4":
                            header["Datumformaat"] = "DDmmm\'YY"
                        elif formaat == "5":
                            header["Datumformaat"] = "DD-mmmYY"
                        elif len(formaat) == 2 and formaat.upper()[0] in afsluitlijst and formaat.upper()[1] in afsluitlijst:
                            headerloop = "Q"
                            break
                        elif len(formaat) == 3 and formaat.upper()[0] in afsluitlijst and formaat.upper()[2] in afsluitlijst:
                            doei()
                        else:
                            header["Datumformaat"] = "YYYYMMDD"
                    elif wat == "10":
                        if Taal == "EN":
                            printjanee = input("Print month overview to file\n  Y Yes\n >N No\n  : %s" % (colgoed))
                        elif Taal == "IT":
                            printjanee = input("Stampa riepilogo mensile in file\n  S Si\n >N No\n  : %s" % (colgoed))
                        else:
                            printjanee = input("Print maandoverzicht naar bestand\n  J Ja\n >N Nee\n  : %s" % (colgoed))
                        print(ResetAll, end = "")
                        if printjanee.upper() in afsluitlijst:
                            break
                        elif len(printjanee) == 2 and printjanee.upper()[0] in afsluitlijst and printjanee.upper()[1] in afsluitlijst:
                            headerloop = "Q"
                            break
                        elif len(printjanee) == 3 and printjanee.upper()[0] in afsluitlijst and printjanee.upper()[2] in afsluitlijst:
                            doei()
                        elif printjanee.upper() in jalijst:
                            header["Print"] = "Ja"
                        else:
                            header["Print"] = "Nee"
                    with open("header","w") as f:
                        print(header, file = f, end = "")
                    kleur = updatekleur()
                    Kleuren = kleur[0]
                    globals().update(Kleuren)
                    catcol = kleur[1]
                if headerloop == "Q":
                    break
            elif keuze2 == "3":
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
                    if Taal == "EN":
                        print("%sHidden%s accounts:" % (colslecht,ResetAll))
                    elif Taal == "IT":
                        print("Conti %snascosti%s:" % (colslecht,ResetAll))
                    else:
                        print("%sVerborgen%s rekeningen:" % (colslecht,ResetAll))
                    for i in vrbrgnrekeningenlijst:
                        print("    "+colslecht+for20(i[0])+colonbepaald+i[1]+ResetAll)
                if len(gtndrekeningenlijst) > 0:
                    if Taal == "EN":
                        print("%sShown%s accounts:" % (colgoed,ResetAll))
                    elif Taal == "IT":
                        print("Conti %sesposti%s:" % (colgoed,ResetAll))
                    else:
                        print("%sGetoonde%s rekeningen:" % (colgoed,ResetAll))
                    reking = 1
                    for i in gtndrekeningenlijst:
                        print("    "+colgoed+for20(i[0])+colonbepaald+i[1]+ResetAll)
                        reking += 1
                os.chdir(os.path.join(basismap,iban+"@"+jaar))
                if Taal == "EN":
                    tov = input("Show a %shidden account%s or hide a %sshown account%s\n  1 %sShow%s and go\n  2 %sHide%s\n  : %s" % (colslecht,ResetAll,colgoed,ResetAll,colgoed,ResetAll,colslecht,ResetAll,colgoed))
                elif Taal == "IT":
                    tov = input("Esporre un %sconto nascosto%s o nascondere un %sconto esposto%s\n  1 %sEspondi%s e vai\n  2 %sNascondi%s\n  : %s" % (colslecht,ResetAll,colgoed,ResetAll,colgoed,ResetAll,colslecht,ResetAll,colgoed))
                else:
                    tov = input("Een %sverborgen rekening%s tonen of een %sgetoonde rekening%s verbergen\n  1 %sTonen%s en ga erheen\n  2 %sVerbergen%s\n  : %s" % (colslecht,ResetAll,colgoed,ResetAll,colgoed,ResetAll,colslecht,ResetAll,colgoed))
                print(ResetAll, end = "")

                if tov.upper() in afsluitlijst:
                    break
                elif len(tov) == 2 and tov.upper()[0] in afsluitlijst and tov.upper()[1] in afsluitlijst:
                    break
                elif len(tov) == 3 and tov.upper()[0] in afsluitlijst and tov.upper()[2] in afsluitlijst:
                    doei()
                elif tov == "1":
                    os.chdir(basismap)
                    vrbrgnrekeningenlijst = []
                    for d in os.listdir():
                        if "_" in d:
                            vrbrgnrekeningenlijst.append(d.split("_"))
                    vrbrgnrekeningenlijst = sorted(vrbrgnrekeningenlijst)
                    if len(vrbrgnrekeningenlijst) == 0:
                        if Taal == "EN":
                            print("%sThere are no accounts hidden%s" % (colslecht,ResetAll))
                        elif Taal == "IT":
                            print("%sNon ci son conti nascosti%s" % (colslecht,ResetAll))
                        else:
                            print("%sEr zijn geen verborgen rekeningen%s" % (colslecht,ResetAll))
                        os.chdir(os.path.join(basismap,iban+"@"+jaar))
                    else:
                        if Taal == "EN":
                            print("%sHidden%s accounts:" % (colslecht,ResetAll))
                        elif Taal == "IT":
                            print("Conti %snascosti%s:" % (colslecht,ResetAll))
                        else:
                            print("%sVerborgen%s rekeningen:" % (colslecht,ResetAll))
                        reking = 1
                        for i in vrbrgnrekeningenlijst:
                            print("  "+colslecht+for3(str(reking))+ResetAll+colgoed+for20(i[0])+colonbepaald+i[1]+ResetAll)
                            reking += 1
                        if Taal == "EN":
                            rekening = input("Choose an account\n%s  : %s" % (colslecht,colgoed))
                        elif Taal == "IT":
                            rekening = input("Scegli un conto\n%s  : %s" % (colslecht,colgoed))
                        else:
                            rekening = input("Kies een rekening\n%s  : %s" % (colslecht,colgoed))
                        print(ResetAll, end = "")
                        if rekening.upper() in afsluitlijst:
                            os.chdir(os.path.join(basismap,iban+"@"+jaar))
                            break
                        elif len(rekening) == 2 and rekening.upper()[0] in afsluitlijst and rekening.upper()[1] in afsluitlijst:
                            os.chdir(os.path.join(basismap,iban+"@"+jaar))
                            break
                        elif len(rekening) == 3 and rekening.upper()[0] in afsluitlijst and rekening.upper()[2] in afsluitlijst:
                            doei()
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
                                Taal = header["Taal"]
                                Valuta = header["Valuta"]
                                Nulregels = header["Nulregels"]
                                MarkeringLH = header["Markering L><H"]
                                Kleur = header["Kleur"]
                                kleur = updatekleur()
                                Kleuren = kleur[0]
                                globals().update(Kleuren)
                                catcol = kleur[1]
                                iban = viban
                                jaar = vjaar
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
                            if Taal == "EN":
                                print("%sYou cannot hide the account you are currently using%s" % (colslecht,ResetAll))
                            elif Taal == "IT":
                                print("%sNon si può nascondere il conto attualmente in uso%s" % (colslecht,ResetAll))
                            else:
                                print("%sJe kunt niet de rekening verbergen die je nu gebruikt%s" % (colslecht,ResetAll))
                            os.chdir(os.path.join(basismap,iban+"@"+jaar))
                            break
                        else:
                            if Taal == "EN":
                                print("%sShown%s accounts:" % (colgoed,ResetAll))
                            elif Taal == "IT":
                                print("Conti %sesposti%s:" % (colgoed,ResetAll))
                            else:
                                print("%sGetoonde%s rekeningen:" % (colgoed,ResetAll))
                            reking = 1
                            for i in gtndrekeningenlijst:
                                print("  "+colslecht+for3(str(reking))+ResetAll+colgoed+for20(i[0])+colonbepaald+i[1]+ResetAll)
                                reking += 1
                            if Taal == "EN":
                                rekening = input("Choose an account\n%s  : %s" % (colslecht,colgoed))
                            elif Taal == "IT":
                                rekening = input("Scegli un conto\n%s  : %s" % (colslecht,colgoed))
                            else:
                                rekening = input("Kies een rekening\n%s  : %s" % (colslecht,colgoed))
                            print(ResetAll, end = "")
                            if rekening.upper() in afsluitlijst:
                                os.chdir(os.path.join(basismap,iban+"@"+jaar))
                                break
                            elif len(rekening) == 2 and rekening.upper()[0] in afsluitlijst and rekening.upper()[1] in afsluitlijst:
                                os.chdir(os.path.join(basismap,iban+"@"+jaar))
                                break
                            elif len(rekening) == 3 and rekening.upper()[0] in afsluitlijst and rekening.upper()[2] in afsluitlijst:
                                doei()
                            else:
                                try:
                                    toonrek = int(rekening)-1
                                    viban = gtndrekeningenlijst[toonrek][0]
                                    vjaar = gtndrekeningenlijst[toonrek][1]
                                    if viban == iban and vjaar == jaar:
                                        if Taal == "EN":
                                            print("%sYou cannot hide the account you are currently using%s" % (colslecht,ResetAll))
                                        elif Taal == "IT":
                                            print("%sNon si può nascondere il conto attualmente in uso%s" % (colslecht,ResetAll))
                                        else:
                                            print("%sJe kunt niet de rekening verbergen die je nu gebruikt%s" % (colslecht,ResetAll))
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
                if Taal == "EN":
                    print("%sATTENTION! Abort will exit the program%s" % (colslecht,ResetAll))
                elif Taal == "IT":
                    print("%sATTENZIONE! Interrompere esce dal programma%s" % (colslecht,ResetAll))
                else:
                    print("%sLET OP! Afbreken verlaat het programma%s" % (colslecht,ResetAll))
                if Taal == "EN":
                    print("%sAvailable visible accounts:%s" % (colgoed,ResetAll))
                elif Taal == "IT":
                    print("%sConti visibili disponibili:%s" % (colgoed,ResetAll))
                else:
                    print("%sBeschikbare zichtbare rekeningen:%s" % (colgoed,ResetAll))
                rekeningenlijst = rknngnlst()
                ibanjaar = rek()
                iban = ibanjaar[0]
                jaar = ibanjaar[1]
                header = ibanjaar[2]
                hoe = header["Beschrijving"]
                wie = header["Rekeninghouder"]
                waar = header["Plaats"]
                Taal = header["Taal"]
                Valuta = header["Valuta"]
                Nulregels = header["Nulregels"]
                MarkeringLH = header["Markering L><H"]
                Kleur = header["Kleur"]
                kleur = updatekleur()
                Kleuren = kleur[0]
                globals().update(Kleuren)
                catcol = kleur[1]
            elif keuze2 == "5":
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
                Taal = header["Taal"]
                Valuta = header["Valuta"]
                Nulregels = header["Nulregels"]
                MarkeringLH = header["Markering L><H"]
                Kleur = header["Kleur"]
                kleur = updatekleur()
                Kleuren = kleur[0]
                globals().update(Kleuren)
                catcol = kleur[1]
            elif keuze2 == "6":
                os.chdir(basismap)
                if Taal == "EN":
                    print("Choose an account")
                elif Taal == "IT":
                    print("Scegli un conto")
                else:
                    print("Kies een rekening")
                rekeningenlijst = rknngnlst()
                welk = input("  : ")
                if welk.upper() in afsluitlijst:
                    os.chdir(os.path.join(basismap,iban+"@"+jaar))
                    break
                elif len(welk) == 2 and welk.upper()[0] in afsluitlijst and welk.upper()[1] in afsluitlijst:
                    os.chdir(os.path.join(basismap,iban+"@"+jaar))
                    break
                elif len(welk) == 3 and welk.upper()[0] in afsluitlijst and welk.upper()[2] in afsluitlijst:
                    doei()
                try:
                    welk = int(welk)-1
                    viban = rekeningenlijst[welk][0]
                    vjaar = rekeningenlijst[welk][1]
                    if iban == viban and jaar == vjaar:
                        if Taal == "EN":
                            print("%sYou cannot delete the account you are currently using%s" % (colslecht,ResetAll))
                        elif Taal == "IT":
                            print("%sNon si può eliminare il conto attualmente in uso%s" % (colslecht,ResetAll))
                        else:
                            print("%sJe kunt niet de rekening verwijderen die je nu gebruikt%s" % (colslecht,ResetAll))
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
                        if Taal == "EN":
                            oknok = input("%sOK%s or %sNot OK%s\n%s  1 OK%s\n%s >2 Not OK%s\n  : " % (colgoed,ResetAll,colslecht,ResetAll,colgoed,ResetAll,colslecht,ResetAll))
                        elif Taal == "IT":
                            oknok = input("%sOK%s o %sNon OK%s\n%s  1 OK%s\n%s >2 Non OK%s\n  : " % (colgoed,ResetAll,colslecht,ResetAll,colgoed,ResetAll,colslecht,ResetAll))
                        else:
                            oknok = input("%sOK%s of %sNiet OK%s\n%s  1 OK%s\n%s >2 Niet OK%s\n  : " % (colgoed,ResetAll,colslecht,ResetAll,colgoed,ResetAll,colslecht,ResetAll))
                        if oknok == "1":
                            os.chdir(rekeningenlijst[welk][0]+"@"+rekeningenlijst[welk][1])
                            for f in os.listdir():
                                os.remove(f)
                            os.chdir(basismap)
                            os.rmdir(rekeningenlijst[welk][0]+"@"+rekeningenlijst[welk][1])
                            rekeningenlijst.remove(rekeningenlijst[welk])
                            rekeningenlijst = rknngnlst()
                        elif len(oknok) == 2 and welk.upper()[0] in afsluitlijst and welk.upper()[1] in afsluitlijst:
                            os.chdir(os.path.join(basismap,iban+"@"+jaar))
                            break
                        elif len(oknok) == 3 and welk.upper()[0] in afsluitlijst and welk.upper()[2] in afsluitlijst:
                            doei()
                        os.chdir(os.path.join(basismap,iban+"@"+jaar))
                except(Exception) as error:
                    #print(error)
                    os.chdir(os.path.join(basismap,iban+"@"+jaar))
            elif keuze2 == "7":
                os.chdir(basismap)
                if Taal == "EN":
                    print("Choose an account to %stransfer your current settings%s to" % (Magenta,ResetAll))
                elif Taal == "IT":
                    print("Scegli un conto per %strasferirci su le impostazioni correnti%s" % (Magenta,ResetAll))
                else:
                    print("Kies een rekening om de %shuidige instellingen naar over te zetten%s" % (Magenta,ResetAll))
                rekeningenlijst = rknngnlst()
                welk = input("  : ")
                if welk.upper() in afsluitlijst:
                    os.chdir(os.path.join(basismap,iban+"@"+jaar))
                    break
                elif len(welk) == 2 and welk.upper()[0] in afsluitlijst and welk.upper()[1] in afsluitlijst:
                    os.chdir(os.path.join(basismap,iban+"@"+jaar))
                    break
                elif len(welk) == 3 and welk.upper()[0] in afsluitlijst and welk.upper()[2] in afsluitlijst:
                    doei()
                try:
                    welk = int(welk)-1
                    viban = rekeningenlijst[welk][0]
                    vjaar = rekeningenlijst[welk][1]
                    naarmap = os.path.join(basismap,viban+"@"+vjaar)
                    with open(os.path.join(basismap,naarmap,"header"),"w") as w:
                        print(header, file = w, end = "")
                    os.chdir(os.path.join(basismap,iban+"@"+jaar))
                except(Exception) as error:
                    #print(error)
                    os.chdir(os.path.join(basismap,iban+"@"+jaar))
            elif keuze2 == "0":
                if Taal == "EN":
                    input(versieEN)
                    input(info1EN)
                    print(info2EN)
                    input(toplijn)
                    print()
                elif Taal == "IT":
                    input(versieIT)
                    input(info1IT)
                    print(info2IT)
                    input(toplijn)
                    print()
                else:
                    input(versie)
                    input(info1)
                    print(info2)
                    input(toplijn)
                    print()
            elif keuze2 == "1" or keuze2 == "":
                for i in lijst:                                         # hier worden de mutaties van alle categorieën alsnog op datum gesorteerd (jwmn)
                    try:
                        with open(i,"r") as r:
                            inhoudvancategoriei = ast.literal_eval(r.read())
                        inhoudvancategorie = [inhoudvancategoriei[0]]   # het eerste item is altijd het budget
                        for j in sorted(inhoudvancategoriei[1:]):
                            inhoudvancategorie.append(j)                # alle mutaties worden op volgorde van 0:datum en 1:prijs (enz.) toegevoegd
                        with open(i,"w") as w:
                            print(inhoudvancategorie, file = w, end = "")
                    except(Exception) as error:
                        #print(error)
                        pass
                catbeheer = "Y"
                while catbeheer == "Y":
                    if Taal == "EN":
                        print("Choose a %scategory%s" % (LichtCyaan,ResetAll))
                    elif Taal == "IT":
                        print("Scegli una %scategoria%s" % (LichtCyaan,ResetAll))
                    else:
                        print("Kies een %scategorie%s" % (LichtCyaan,ResetAll))
                    alt()
                    kategorie = input("  : ")
                    if kategorie.upper() in afsluitlijst:
                        break
                    elif len(kategorie) == 2 and kategorie.upper()[0] in afsluitlijst and kategorie.upper()[1] in afsluitlijst:
                        catbeheer = "Q"
                        break
                    elif len(kategorie) == 3 and kategorie.upper()[0] in afsluitlijst and kategorie.upper()[2] in afsluitlijst:
                        doei()
                    else:
                        if kategorie.upper() in lijst:
                            try:
                                with open(kategorie.upper(),"r") as c:
                                    kat = ast.literal_eval(c.read())
                                    budget = kat[0]
                                col = catcol[kategorie.upper()]
                                if Taal == "EN":
                                    kategorienaam = alternatievenamenlijst[kategorie.upper()].replace("saldo & inkomen","funds & income").replace("vaste lasten","fixed costs").replace("boodschappen","groceries").replace("reis & verblijf","travel & stay").replace("leningen","loans").replace("overig","other")
                                    wat = input("Choose\n  1 Modify %scategory name%s (now %s)\n  2 Modify %smonth budget%s (now %s)\n  3 %sRemove category%s %s %sand everything in it%s\n  : " % (LichtCyaan,ResetAll,col+kategorienaam+ResetAll,LichtCyaan,ResetAll,col+Valuta+fornum(budget)+ResetAll,colslecht,ResetAll,col+kategorienaam+ResetAll,colslecht, ResetAll))
                                elif Taal == "IT":
                                    kategorienaam = alternatievenamenlijst[kategorie.upper()].replace("saldo & inkomen","saldo & reddito").replace("vaste lasten","costi fissi").replace("boodschappen","spese").replace("reis & verblijf","viaggioalloggio").replace("leningen","prestiti").replace("overig","altro")
                                    wat = input("Scegli\n  1 Modificare %snome di categoria%s (ora %s)\n  2 Modificare %sbudget mensile%s (ora %s)\n  3 %sEliminare categoria%s %s %scon tutto dentro%s\n  : " % (LichtCyaan,ResetAll,col+kategorienaam+ResetAll,LichtCyaan,ResetAll,col+Valuta+fornum(budget)+ResetAll,colslecht,ResetAll,col+kategorienaam+ResetAll,colslecht, ResetAll))
                                else:
                                    wat = input("Kies\n  1 %sCategorienaam%s wijzigen (nu %s)\n  2 %sMaandbudget%s wijzigen (nu %s)\n  3 %sCategorie%s %s %sverwijderen en alles wat daarin staat%s\n  : " % (LichtCyaan,ResetAll,col+alternatievenamenlijst[kategorie.upper()]+ResetAll,LichtCyaan,ResetAll,col+Valuta+fornum(budget)+ResetAll,colslecht,ResetAll,col+alternatievenamenlijst[kategorie.upper()]+ResetAll,colslecht,ResetAll))
                                if wat.upper() in afsluitlijst:
                                    break
                                elif len(wat) == 2 and wat.upper()[0] in afsluitlijst and wat.upper()[1] in afsluitlijst:
                                    catbeheer = "Q"
                                    break
                                elif len(wat) == 3 and wat.upper()[0] in afsluitlijst and wat.upper()[2] in afsluitlijst:
                                    doei()
                                elif wat == "1":
                                    if Taal == "EN":
                                        hoedan = input("Enter the new %scategory name%s (max 15)\n  : %s" % (LichtCyaan,ResetAll,col))
                                    elif Taal == "IT":
                                        hoedan = input("Dai il nuovo %snome della categoria%s (mass. 15)\n  : %s" % (LichtCyaan,ResetAll,col))
                                    else:
                                        hoedan = input("Geef de nieuwe %scategorienaam%s (max 15)\n  : %s" % (LichtCyaan,ResetAll,col))
                                    print(ResetAll, end = "")
                                    if hoedan.upper() in afsluitlijst:
                                        break
                                    elif len(hoedan) == 2 and hoedan.upper()[0] in afsluitlijst and hoedan.upper()[1] in afsluitlijst:
                                        catbeheer = "Q"
                                        break
                                    elif len(hoedan) == 3 and hoedan.upper()[0] in afsluitlijst and hoedan.upper()[2] in afsluitlijst:
                                        doei()
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
                                    if Taal == "EN":
                                        print(colbal+forr19("BALANCE ="),Valuta,fornum(round(balans,2))+ResetAll)
                                    elif Taal == "IT":
                                        print(colbal+forr19("BILANCIO ="),Valuta,fornum(round(balans,2))+ResetAll)
                                    else:
                                        print(colbal+forr19("BALANS ="),Valuta,fornum(round(balans,2))+ResetAll)
                                    if Taal == "EN":
                                        hoeveeldan = input("Enter the new %smonth budget%s for %s: %s\n  : %s" % (LichtCyaan,ResetAll,col+kategorie.upper(),alternatievenamenlijst[kategorie.upper()]+ResetAll,col))
                                    elif Taal == "IT":
                                        hoeveeldan = input("Dai il nuovo %sbudget mensile%s per %s: %s\n  : %s" % (LichtCyaan,ResetAll,col+kategorie.upper(),alternatievenamenlijst[kategorie.upper()]+ResetAll,col))
                                    else:
                                        hoeveeldan = input("Geef het nieuwe %smaandbudget%s voor %s: %s\n  : %s" % (LichtCyaan,ResetAll,col+kategorie.upper(),alternatievenamenlijst[kategorie.upper()]+ResetAll,col))
                                    print(ResetAll, end = "")
                                    if hoeveeldan.upper() in afsluitlijst:
                                        break
                                    elif len(hoeveeldan) == 2 and hoeveeldan.upper()[0] in afsluitlijst and hoeveeldan.upper()[1] in afsluitlijst:
                                        catbeheer = "Q"
                                        break
                                    elif len(hoeveeldan) == 3 and hoeveeldan.upper()[0] in afsluitlijst and hoeveeldan.upper()[2] in afsluitlijst:
                                        doei()
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
                                    if Taal == "EN":
                                        print(colbal+forr19("BALANCE ="),Valuta,fornum(round(balans,2))+ResetAll)
                                    elif Taal == "IT":
                                        print(colbal+forr19("BILANCIO ="),Valuta,fornum(round(balans,2))+ResetAll)
                                    else:
                                        print(colbal+forr19("BALANS ="),Valuta,fornum(round(balans,2))+ResetAll)
                                elif wat == "3":
                                    if kategorie.upper() in ["A","O"]:
                                        if Taal == "EN":
                                            print("%sYou can not remove this category%s\n  : " % (colslecht,ResetAll))
                                        elif Taal == "IT":
                                            print("%sNon si puó rimuovere questa categoria%s\n  : " % (colslecht,ResetAll))
                                        else:
                                            print("%sJe kunt deze categorie niet verwijderen%s\n  : " % (colslecht,ResetAll))
                                    else:
                                        if Taal == "EN":
                                            oknok = input("%sOK%s or %sNot OK%s\n%s  1 OK%s\n%s >2 Not OK%s\n  : " % (colgoed,ResetAll,colslecht,ResetAll,colgoed,ResetAll,colslecht,ResetAll))
                                        elif Taal == "IT":
                                            oknok = input("%sOK%s o %sNon OK%s\n%s  1 OK%s\n%s >2 Non OK%s\n  : " % (colgoed,ResetAll,colslecht,ResetAll,colgoed,ResetAll,colslecht,ResetAll))
                                        else:
                                            oknok = input("%sOK%s of %sNiet OK%s\n%s  1 OK%s\n%s >2 Niet OK%s\n  : " % (colgoed,ResetAll,colslecht,ResetAll,colgoed,ResetAll,colslecht,ResetAll))
                                        if oknok == "1":
                                            os.remove(kategorie.upper())
                                            del alternatievenamenlijst[kategorie.upper()]
                                            with open("alternatievenamen","w") as f:
                                                print(alternatievenamenlijst, file = f, end = "")
                                        elif len(oknok) == 2 and oknok.upper()[0] in afsluitlijst and oknok.upper()[1] in afsluitlijst:
                                            catbeheer = "Q"
                                            break
                                        elif len(oknok) == 3 and oknok.upper()[0] in afsluitlijst and oknok.upper()[2] in afsluitlijst:
                                            doei()
                            except(Exception) as error:
                                #print(error)
                                pass
                if catbeheer == "Q":
                    break
        print()
        print(toplijn)
        print()
