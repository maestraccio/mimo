#!/usr/bin/python3
import pathlib, os, ast, calendar, textwrap
from time import sleep
from datetime import datetime, date, timedelta

bouw = "3.43"
plaats = "Pedara"
hardedatum = "20240225"

w=70
versie = """
Versie: %s
Auteur: Maestraccio
Contact: maestraccio (at) musician (dot) org
%s %s

+-----""" % (bouw,plaats,hardedatum)
versieEN = """
Version: %s
Writer: Maestraccio
Contact: maestraccio (at) musician (dot) org
%s %s

+-----""" % (bouw,plaats,hardedatum)
versieIT = """
Versione: %s
Scrittore: Maestraccio
Recapiti: maestraccio (at) musician (dot) org
%s %s

+-----""" % (bouw,plaats,hardedatum)
menu = {
        "0": "Beheer rekeningopties",
            "0,0": "Print versie en info",
            "0,1": "Categoriebeheer",
                "0,1,1": "Categorienaam wijzigen",
                "0,1,2": "Maandbudget wijzigen",
                "0,1,3": "Categorie verwijderen",
            "0,2": "Rekeninginstellingen aanpassen",
                "0,2,1": "Beschrijving",
                "0,2,2": "Rekeninghouder",
                "0,2,3": "Plaats",
                "0,2,4": "Taal",
                "0,2,5": "Valuta",
                "0,2,6": "Nulregels",
                "0,2,7": "Markering Laag >< Hoog",
                "0,2,8": "Kleur",
                "0,2,9": "Datumformaat",
                "0,2,10": "Print maandoverzicht naar bestand",
                "0,2,11": "Toon totaalsaldo op startscherm",
                "0,2,12": "Exporteer alles naar csv-bestand",
            "0,3": "Toon of verberg rekening",
            "0,4": "Wissel van rekening",
            "0,5": "Nieuwe rekening toevoegen",
            "0,6": "Verwijder rekening",
            "0,7": "Instellingen overzetten",
        "1": "Mutaties bekijken",
        "2": "Mutatie toevoegen",
            "2,1": "Nieuw",
            "2,2": "Kopie naar vandaag",
            "2,3": "Kopie naar andere rekening",
        "3": "Mutatie wijzigen",
            "3,1": "Wijzig datum",
            "3,2": "Wijzig bedrag",
            "3,3": "Wijzig wederpartij",
            "3,4": "Wijzig betreft",
            "3,5": "Wijzig categorie",
        "4": "Mutatie verwijderen",
        "5": "Spaarpotten",
            "5,1": "Bekijk spaarpotten",
            "5,2": "Wijzig spaarpot",
                "5,2,1": "Naam",
                "5,2,2": "Waarde",
            "5,3": "Voeg nieuwe spaarpot toe",
            "5,4": "Verwijder spaarpot"
        }
menuEN = {
        "0": "Manage account options",
            "0,0": "Print version and info",
            "0,1": "Category management",
                "0,1,1": "Modify category name",
                "0,1,2": "Modify month budget",
                "0,1,3": "Remove category",
            "0,2": "Alter account settings",
                "0,2,1": "Description",
                "0,2,2": "Account holder",
                "0,2,3": "City",
                "0,2,4": "Language",
                "0,2,5": "Currency",
                "0,2,6": "Zero lines",
                "0,2,7": "Marking Lower >< Upper",
                "0,2,8": "Colour",
                "0,2,9": "Date formatting",
                "0,2,10": "Print month overview to file",
                "0,2,11": "Show total amount on start screen",
                "0,2,12": "Export all to csv file",
            "0,3": "Show or hide account",
            "0,4": "Switch account",
            "0,5": "Add new account",
            "0,6": "Delete account",
            "0,7": "Transfer account settings",
        "1": "View mutations",
        "2": "Add mutation",
            "2,1": "New",
            "2,2": "Copy to today",
            "2,3": "Copy to another account",
        "3": "Modify mutation",
            "3,1": "Change date",
            "3,2": "Change amount",
            "3,3": "Change other party",
            "3,4": "Change about",
            "3,5": "Change category",
        "4": "Remove mutation",
        "5": "Piggy banks",
            "5,1": "View piggy banks",
            "5,2": "Modify piggy bank",
                "5,2,1": "Name",
                "5,2,2": "Value",
            "5,3": "Add new piggy bank",
            "5,4": "Remove piggy bank"
        }
menuIT = {
        "0": "Gestire opzioni del conto",
            "0,0": "Print versione ed info",
            "0,1": "Gestione categorie",
                "0,1,1": "Modificare nome di categoria",
                "0,1,2": "Modificare budget mensile",
                "0,1,3": "Eliminare categoria",
            "0,2": "Modificare impostazioni del conto",
                "0,2,1": "Descrizione",
                "0,2,2": "Intestatario",
                "0,2,3": "Città",
                "0,2,4": "Lingua",
                "0,2,5": "Valuta",
                "0,2,6": "Linee a zero",
                "0,2,7": "Indicazione Inferiore >< Superiore",
                "0,2,8": "Colore",
                "0,2,9": "Formato data",
                "0,2,10": "Stampa riepilogo mensile in file",
                "0,2,11": "Mostra totale sullo schermo iniziale",
                "0,2,12": "Esporta tutto in file csv",
            "0,3": "Mostrare o nascondere conto",
            "0,4": "Passare ad un altro conto",
            "0,5": "Aggiungere un nuovo conto",
            "0,6": "Eliminare conto",
            "0,7": "Trasferire impostazioni",
        "1": "Vedere mutazioni",
        "2": "Aggiungere mutazione",
            "2,1": "Nuova",
            "2,2": "Copia colla data di oggi",
            "2,3": "Copia su un altro conto",
        "3": "Modificare mutazione",
            "3,1": "Modifica data",
            "3,2": "Modifica somma",
            "3,3": "Modifica controparte",
            "3,4": "Modifica riguarda",
            "3,5": "Modifica categoria",
        "4": "Rimuovere mutazione",
        "5": "Salvadanai",
            "5,1": "Vedere salvadanai",
            "5,2": "Modificare salvadanaio",
                "5,2,1": "Nome",
                "5,2,2": "Valore",
            "5,3": "Aggiungere salvadanaio",
            "5,4": "Rimuovere salvadanaio"
        }



info1 = """
Iedere rekeningmapnaam bestaat uit een rekeningnummer en een jaartal.
In opzet bevat een map één kalenderjaar, hoewel het mogelijk is om
onbeperkt door te schrijven; dit is door de gebruiker vrij te bepalen.
In de hoofdmap bevindt zich het programma, de rekeningmappen en het
bestand "lastselected" met naam van de laatstgebruikte rekeningmap.
In de rekeningmap worden standaard de volgende bestanden aangemaakt:
  - "alternatievenamen": de Nederlandse categorienamen
  - "header": rekeninggegevens en rekeninggebonden weergaveopties

Voor huishoudelijke rekeningen:
6 categorieën (uitbreid- en aanpasbaar):
A: saldo & inkomen: in principe positieve bedragen, budget negatief
B: vaste lasten   : verwachte en terugkerende uitgaven
C: boodschappen   : dagelijkse variabele uitgaven
D: reis & verblijf: reiskosten, brandstof, overnachtingen, enz.
E: leningen       : bedragen die worden voorgeschoten en terugbetaald
O: overig         : overige mutaties
Het aanpasbare startsaldo "0.0" staat in "A" op datum "11111111".

Voor zakelijke rekeningen:
10 categorieën (uitbreid- en aanpasbaar):
0: vaste act/pass. 
1: vlotte act/pass 
2: tussenrekening  
3: voorraden       
4: kosten          
5: kostenplaatsen  
6: fabricagerek.   
7: inkoopwaarde    
8: omzet           
9: privé           
Het aanpasbare startsaldo "0.0" staat in "1" op datum "11111111".

Andere categorieën kunnen worden toegevoegd door een nieuwe mutatie 
toe te voegen of te wijzigen en toe te wijzen aan de nieuwe categorie.

"header" bevat 12 items waarvan alleen de eerste drie worden getoond:
 1: %s 
 2: %s 
 3: %s 
 4: %s 
 5: %s 
 6: %s 
 7: %s 
 8: %s 
 9: %s 
10: %s 
11: %s 
12: %s 

+-----""" % (menu["0,2,1"],menu["0,2,2"],menu["0,2,3"],menu["0,2,4"],menu["0,2,5"],menu["0,2,6"],menu["0,2,7"],menu["0,2,8"],menu["0,2,9"],menu["0,2,10"],menu["0,2,11"],menu["0,2,12"])
info1EN = """
Every account folder name is formed by an account number and a year.
It is intended for details of one calendar year, although the user can
decide otherwise and continue adding details to the same folder. The
main folder contains the program file, the account folders, and the
file "lastselected" with the name of the last selected account folder.
In the account folder the following files are created by default:
  - "alternatievenamen": the Dutch category names
  - "header": account details and account related interface options

For household accounts:
6 categories (expandable, adjustable, translated from Dutch names):
A: funds & income : intentionally positive amounts, budget negative
B: fixed costs    : expected and repeated expenses
C: groceries      : daily variable expenses
D: travel & stay  : traveling costs, fuel, hotel stays, etc.
E: loans          : expenses to be returned and vice versa
O: other          : other mutations
The customizable starting balance "0.0" is in "A" on date "11111111".

For business accounts:
10 categories (expandable, adjustable, translated from Dutch names):
0: fixd ass/equity
1: cash (equiv.) 
2: intermediary  
3: inventory     
4: expenses      
5: cost centers  
6: manufact.acc. 
7: cost of goods 
8: sales         
9: private       
The customizable starting balance "0.0" is in "1" on date "11111111".

Other categories can be added by adding a new mutation or making a
copy and assigning it to a new to be made category.

"header" contains 12 items of which only the first three are shown:
 1: %s 
 2: %s 
 3: %s 
 4: %s 
 5: %s 
 6: %s 
 7: %s 
 8: %s 
 9: %s 
10: %s 
11: %s 
12: %s 

+-----""" % (menuEN["0,2,1"],menuEN["0,2,2"],menuEN["0,2,3"],menuEN["0,2,4"],menuEN["0,2,5"],menuEN["0,2,6"],menuEN["0,2,7"],menuEN["0,2,8"],menuEN["0,2,9"],menuEN["0,2,10"],menuEN["0,2,11"],menuEN["0,2,12"])
info1IT = """
Ogni nome della cartella del conto consiste in un numero di conto ed
un anno. Nella configurazione, una cartella contiene un anno di
calendario, anche se è possibile scrittura illimitata; questo può
essere liberamente determinato dall'utente. La cartella principale
contiene il programma, le cartelle dell'account ed il file
"lastselected" con il nome dell'ultima cartella di account utilizzata.
In questa cartella del conto vengono creati i seguenti file per
impostazione predefinita:
  - "alternatievenamen": i nomi delle categorie in Olandese
  - "header": dettagli del conto ed opzioni dell'interfaccia relative
    al conto

Per conti domestici:
6 categorie (espandibili e regolabili, nomi olandesi del file):
A: saldo & reddito: importi intenzionalmente positivi, budget negativo
B: costi fissi: spese previste e ripetute
C: spese: spese variabili giornaliere/alimentari
D: viaggioalloggio: spese di viaggio, carburante, soggiorni, ecc.
E: prestiti: spese da restituire e viceversa
O: altro: atre mutazioni
Il personalizzabile saldo iniziale "0.0" è in "A" su data "11111111".

Per conti aziendali:
10 categorie (espandibili e regolabili, nomi olandesi del file):
0: attiv. fisse
1: dispon. liquide
2: conti intermedi
3: magazzino
4: costi
5: centri di costo
6: contiproduzione
7: costi vendute
8: ricavi
9: privato
Il personalizzabile saldo iniziale "0.0" è in "1" su data "11111111".

È possibile aggiungere altre categorie aggiungendo una nuova muta-
zione o effettuando a copiarla ed assegnarla ad una nuova categoria
da fare.

"header" contiene 11 elementi di cui vengono mostrati solo i primi
tre:
 1: %s 
 2: %s 
 3: %s 
 4: %s 
 5: %s 
 6: %s 
 7: %s 
 8: %s 
 9: %s 
10: %s 
11: %s 
12: %s 

+-----""" % (menuIT["0,2,1"],menuIT["0,2,2"],menuIT["0,2,3"],menuIT["0,2,4"],menuIT["0,2,5"],menuIT["0,2,6"],menuIT["0,2,7"],menuIT["0,2,8"],menuIT["0,2,9"],menuIT["0,2,10"],menuIT["0,2,11"],menuIT["0,2,12"])
info2 = """
PROGRAMMASTRUCTUUR en snelkeuzes:

De laatstgebruikte rekening wordt opnieuw geopend met ""+"Enter"

Interactieve hulp: H

0 %s
    0 %s
    1 %s
        1 %s
        2 %s
        3 %s
    2 %s
        1 %s
        2 %s
        3 %s
        4 %s
        5 %s
        6 %s
        7 %s
        8 %s
        9 %s
       10 %s
       11 %s
       12 %s
    3 %s
    4 %s
    5 %s
    6 %s
    7 %s
1 %s
    Datumselectie -> Categorieselectie -> Subselectie -> Toon + ID
2 %s
    1 %s
    2 %s
    3 %s
3 %s
    1 %s
    2 %s
    3 %s
    4 %s
    5 %s
4 %s
5 %s
    1 %s
    2 %s
        1 %s
        2 %s
    3 %s
    4 %s

Keuzes moeten worden bevestigd met "Enter".
Probeer ook eens snelkeuzes "M", "MI", "MO" en " ".
"Terug" of "Verlaten" met "Q" (of "X").
"Terug naar hoofdmenu" met "QQ", "Nu afsluiten" met "QQQ".
""" % (menu["0"],menu["0,0"],menu["0,1"],menu["0,1,1"],menu["0,1,2"],menu["0,1,3"],menu["0,2"],menu["0,2,1"],menu["0,2,2"],menu["0,2,3"],menu["0,2,4"],menu["0,2,5"],menu["0,2,6"],menu["0,2,7"],menu["0,2,8"],menu["0,2,9"],menu["0,2,10"],menu["0,2,11"],menu["0,2,12"],menu["0,3"],menu["0,4"],menu["0,5"],menu["0,6"],menu["0,7"],menu["1"],menu["2"],menu["2,1"],menu["2,2"],menu["2,3"],menu["3"],menu["3,1"],menu["3,2"],menu["3,3"],menu["3,4"],menu["3,5"],menu["4"],menu["5"],menu["5,1"],menu["5,2"],menu["5,2,1"],menu["5,2,2"],menu["5,3"],menu["5,4"])
info2EN = """
PROGRAM STRUCTURE and quick choices:

The last used account is reopened with ""+"Enter"

Interactive help: H

0 %s
    0 %s
    1 %s
        1 %s
        2 %s
        3 %s
    2 %s
        1 %s
        2 %s
        3 %s
        4 %s
        5 %s
        6 %s
        7 %s
        8 %s
        9 %s
       10 %s
       11 %s
       12 %s
    3 %s
    4 %s
    5 %s
    6 %s
    7 %s
1 %s
    Date selection -> Category selection -> Subselection -> Show + ID
2 %s
    1 %s
    2 %s
    3 %s
3 %s
    1 %s
    2 %s
    3 %s
    4 %s
    5 %s
4 %s
5 %s
    1 %s
    2 %s
        1 %s
        2 %s
    3 %s
    4 %s

Choices must be confirmed with "Enter".
Try also quick choices "M", "MI", "MO" and " ".
"Back" or "Abort" with "Q" (or "X").
"Back to main menu" with "QQ", "Exit now" with "QQQ".
""" % (menuEN["0"],menuEN["0,0"],menuEN["0,1"],menuEN["0,1,1"],menuEN["0,1,2"],menuEN["0,1,3"],menuEN["0,2"],menuEN["0,2,1"],menuEN["0,2,2"],menuEN["0,2,3"],menuEN["0,2,4"],menuEN["0,2,5"],menuEN["0,2,6"],menuEN["0,2,7"],menuEN["0,2,8"],menuEN["0,2,9"],menuEN["0,2,10"],menuEN["0,2,11"],menuEN["0,2,12"],menuEN["0,3"],menuEN["0,4"],menuEN["0,5"],menuEN["0,6"],menuEN["0,7"],menuEN["1"],menuEN["2"],menuEN["2,1"],menuEN["2,2"],menuEN["2,3"],menuEN["3"],menuEN["3,1"],menuEN["3,2"],menuEN["3,3"],menuEN["3,4"],menuEN["3,5"],menuEN["4"],menuEN["5"],menuEN["5,1"],menuEN["5,2"],menuEN["5,2,1"],menuEN["5,2,2"],menuEN["5,3"],menuEN["5,4"])
info2IT = """
STRUTTURA DEL PROGRAMMA e selezioni rapidi:

L'ultimo usato conto si riapre con ""+"Enter"

Assistenza interattiva: H

0 %s
    0 %s
    1 %s
        1 %s
        2 %s
        3 %s
    2 %s
        1 %s
        2 %s
        3 %s
        4 %s
        5 %s
        6 %s
        7 %s
        8 %s
        9 %s
       10 %s
       11 %s
       12 %s
    3 %s
    4 %s
    5 %s
    6 %s
    7 %s
1 %s
    Selezione data > Selezione categoria > Sottoselezione > Mostra+ID
2 %s
    1 %s
    2 %s
    3 %s
3 %s
    1 %s
    2 %s
    3 %s
    4 %s
    5 %s
4 %s
5 %s
    1 %s
    2 %s
        1 %s
        2 %s
    3 %s
    4 %s

Le scelte devono essere confermate con "Invio".
Prova anche selezioni rapidi "M", "MI", "MO" e " ".
Selezione rapida "M" per "Tutto questo mese".
"Indietro" o "Annulla" con "Q" (o "X").
"Tornare al menu principale" con "QQ", "Uscire ora" con "QQQ".
""" % (menuIT["0"],menuIT["0,0"],menuIT["0,1"],menuIT["0,1,1"],menuIT["0,1,2"],menuIT["0,1,3"],menuIT["0,2"],menuIT["0,2,1"],menuIT["0,2,2"],menuIT["0,2,3"],menuIT["0,2,4"],menuIT["0,2,5"],menuIT["0,2,6"],menuIT["0,2,7"],menuIT["0,2,8"],menuIT["0,2,9"],menuIT["0,2,10"],menuIT["0,2,11"],menuIT["0,2,12"],menuIT["0,3"],menuIT["0,4"],menuIT["0,5"],menuIT["0,6"],menuIT["0,7"],menuIT["1"],menuIT["2"],menuIT["2,1"],menuIT["2,2"],menuIT["2,3"],menuIT["3"],menuIT["3,1"],menuIT["3,2"],menuIT["3,3"],menuIT["3,4"],menuIT["3,5"],menuIT["4"],menuIT["5"],menuIT["5,1"],menuIT["5,2"],menuIT["5,2,1"],menuIT["5,2,2"],menuIT["5,3"],menuIT["5,4"])

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
for4 = "{:4}".format
forc5 = "{:^5}".format
forr7 = "{:>7}".format
for8 = "{:8}".format
forr8 = "{:>8}".format
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
lijst = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O"]
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
        catcol = {"0":Rood,"1":Groen,"2":Geel,"3":Blauw,"4":Magenta,"5":Cyaan,"6":LichtGrijs,"7":DonkerGrijs,"8":LichtRood,"9":LichtGroen,"A":Rood,"B":Groen,"C":Geel,"D":Blauw,"E":Magenta,"F":Cyaan,"G":LichtGrijs,"H":DonkerGrijs,"I":LichtRood,"J":LichtGroen,"K":LichtGeel,"L":LichtBlauw,"M":LichtMagenta,"N":LichtCyaan,"O":Wit}
    elif header["Kleur"] == "Mono":
        kleuren = {"ResetAll":"\033[0m","Omkeren":"\033[7m","Rood":ResetAll,"Groen":ResetAll,"Geel":ResetAll,"Blauw":ResetAll,"Magenta":ResetAll,"Cyaan":ResetAll,"LichtGrijs":ResetAll,"DonkerGrijs":ResetAll,"LichtRood":ResetAll,"LichtGroen":ResetAll,"LichtGeel":ResetAll,"LichtBlauw":ResetAll,"LichtMagenta":ResetAll,"LichtCyaan":ResetAll,"Wit":ResetAll,"colgoed":LichtGroen,"colslecht":LichtRood,"colonbepaald":Blauw}
        catcol = {"0":Rood,"1":Groen,"2":Geel,"3":Blauw,"4":Magenta,"5":Cyaan,"6":LichtGrijs,"7":DonkerGrijs,"8":LichtRood,"9":LichtGroen,"A":Rood,"B":Groen,"C":Geel,"D":Blauw,"E":Magenta,"F":Cyaan,"G":LichtGrijs,"H":DonkerGrijs,"I":LichtRood,"J":LichtGroen,"K":LichtGeel,"L":LichtBlauw,"M":LichtMagenta,"N":LichtCyaan,"O":Wit}
    elif header["Kleur"] == "Regenboog":
        kleuren = {"ResetAll":"\033[0m","Omkeren":"\033[7m","Rood":"\033[31m","Groen":"\033[32m","Geel":"\033[33m","Blauw":"\033[34m","Magenta":"\033[35m","Cyaan":"\033[36m","LichtGrijs":"\033[37m","DonkerGrijs":"\033[90m","LichtRood":"\033[91m","LichtGroen":"\033[92m","LichtGeel":"\033[93m","LichtBlauw":"\033[94m","LichtMagenta":"\033[95m","LichtCyaan":"\033[96m","Wit":"\033[97m","colgoed":LichtGroen,"colslecht":LichtRood,"colonbepaald":Blauw}
        catcol = {"0":AchtergrondRood+LichtGroen,"1":AchtergrondGeel+LichtBlauw,"2":AchtergrondLichtGeel+Blauw,"3":AchtergrondGroen+LichtRood,"4":AchtergrondBlauw+LichtGeel,"5":AchtergrondMagenta+LichtCyaan,"6":AchtergrondRood+LichtGroen,"7":AchtergrondGeel+LichtBlauw,"8":AchtergrondLichtGeel+Blauw,"9":AchtergrondGroen+LichtRood,"A":AchtergrondRood+LichtGroen,"B":AchtergrondGeel+LichtBlauw,"C":AchtergrondLichtGeel+Blauw,"D":AchtergrondGroen+LichtRood,"E":AchtergrondBlauw+LichtGeel,"F":AchtergrondMagenta+LichtCyaan,"G":AchtergrondRood+LichtGroen,"H":AchtergrondGeel+LichtBlauw,"I":AchtergrondLichtGeel+Blauw,"J":AchtergrondGroen+LichtRood,"K":AchtergrondBlauw+LichtGeel,"L":AchtergrondMagenta+LichtCyaan,"M":AchtergrondLichtGroen+Rood,"N":AchtergrondLichtRood+Groen,"O":AchtergrondMagenta+LichtCyaan}
    else:
        kleuren = {"ResetAll":"\033[0m","Omkeren":"\033[7m","Rood":ResetAll,"Groen":ResetAll,"Geel":ResetAll,"Blauw":ResetAll,"Magenta":ResetAll,"Cyaan":ResetAll,"LichtGrijs":ResetAll,"DonkerGrijs":ResetAll,"LichtRood":ResetAll,"LichtGroen":ResetAll,"LichtGeel":ResetAll,"LichtBlauw":ResetAll,"LichtMagenta":ResetAll,"LichtCyaan":ResetAll,"Wit":ResetAll,"colgoed":LichtGroen,"colslecht":LichtRood,"colonbepaald":Blauw}
        catcol = {"0":"\033[31m","1":"\033[32m","2":"\033[33m","3":"\033[34m","4":"\033[35m","5":"\033[36m","6":"\033[37m","7":"\033[90m","8":"\033[91m","9":"\033[92m","A":"\033[31m","B":"\033[32m","C":"\033[33m","D":"\033[34m","E":"\033[35m","F":"\033[36m","G":"\033[37m","H":"\033[90m","I":"\033[91m","J":"\033[92m","K":"\033[93m","L":"\033[94m","M":"\033[95m","N":"\033[96m","O":"\033[97m"}
    return kleuren,catcol


def toontotaal():
    with open("header","r") as h:
        header = ast.literal_eval(h.read())
    return header["Toon"]

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
    valutalijst = []
    nimo = 0.0
    for d in os.listdir():
        if "@" in d:
            with open(os.path.join(d,"header"),"r") as h:
                header = ast.literal_eval(h.read())
            beschrijving = header["Beschrijving"]
            Toon = header["Toon"]
            Valuta = header["Valuta"]
            moni = 0.0                                # hier telt hij alle bedragen die hij kan vinden bij elkaar op
            for i in lijst:
                try:
                    with open(os.path.join(d,i),"r") as f:
                        inhoudvancategorie = ast.literal_eval(f.read())
                        for j in inhoudvancategorie[1:]:
                            moni += j[1]
                except(Exception) as error:
                    #print(error)
                    pass
            if Toon == "Nee":
                moni = 0
            valutalijst.append(Valuta)
            nimo += moni
            e = d+"@"+Valuta+"@"+fornum(moni)+"@"+beschrijving
            rekeningenlijst.append(e.split("@"))
    rekeningenlijst = sorted(rekeningenlijst)
    reking = 1
    for i in rekeningenlijst:
        mo = i[2]+i[3]
        if i[3] == fornum(0):
            mo = " "*9
        print("  "+colslecht+for3(str(reking))+ResetAll+colgoed+for20(i[0])+colonbepaald+i[1]+ResetAll+" "+LichtGeel+mo+ResetAll+" "+colslecht+i[4]+ResetAll)
        reking += 1
    valutalijst = sorted(valutalijst)
    if valutalijst[0] == valutalijst[-1]:             # Toon totaal alleen als alle valuta gelijk zijn
        if nimo <= -10000 or nimo >= 10000:
            nimo = "± "+str(round(nimo/1000))+"~K"
            print("  "+for3("")+for20("")+for4("")+" "+Geel+Valuta+forr8(nimo))
        else:
            print("  "+for3("")+for20("")+for4("")+" "+Geel+Valuta+fornum(nimo))
    if "lastselected" not in os.listdir():
        with open("lastselected","w") as l:
            print(rekeningenlijst[0][0]+"@"+rekeningenlijst[0][1], end = "", file = l)
    with open("lastselected","r") as l:
        last = l.read()
    return rekeningenlijst,last

def rek():
    os.chdir(basismap)
    rek = "N"
    while rek == "N":
        rekening = input("%s  : %s" % (colslecht,colgoed))
        print(ResetAll, end = "")
        if rekening.upper() in afsluitlijst:
            doei()
        elif len(rekening) == 2 and rekening.upper()[0] in afsluitlijst and rekening.upper()[1] in afsluitlijst:
            break
        elif len(rekening) == 3 and rekening.upper()[0] in afsluitlijst and rekening.upper()[2] in afsluitlijst:
            doei()
        elif rekening == "":
            lastlist = rekeningenlijst[1].split("@")
            iban = lastlist[0]
            jaar = lastlist[1]
        else:
            try:
                indrek = int(rekening)-1
                iban = rekeningenlijst[0][indrek][0]
                jaar = rekeningenlijst[0][indrek][1]
            except(Exception) as error:
                #print(error)
                indrek = 0
            iban = rekeningenlijst[0][indrek][0]
            jaar = rekeningenlijst[0][indrek][1]
        with open("lastselected","w") as l:
            print(iban+"@"+jaar, end = "", file = l)
        werkmap = os.path.join(basismap,iban+"@"+jaar)
        os.chdir(werkmap)
        with open("header","r") as f:
            header = ast.literal_eval(f.read())
        with open("alternatievenamen","r") as g:
            alternatievenamenlijst = ast.literal_eval(g.read())
        return iban,jaar,header,alternatievenamenlijst,werkmap

def printheaderall():
    for k,v in header.items():
        if Taal == "EN":
            if k == "Markering L><H":
                v = header["Valuta"]+fornum(v[0])+ResetAll+" >< "+colgoed+header["Valuta"]+fornum(v[1])
            print(colslecht+for15(k.replace("Beschrijving","Description").replace("Rekeninghouder","Account holder").replace("Plaats","City").replace("Taal","Language").replace("Valuta","Currency").replace("Nulregels","Zero lines").replace("Markering L><H","Marking L><U").replace("Kleur","Colour").replace("Datumformaat","Date formatting").replace("Print","Print").replace("Toon","Show").replace("CSV","CSV")),colonbepaald+":",colgoed+v+ResetAll)
        elif Taal == "IT":
            if k == "Markering L><H":
                v = header["Valuta"]+fornum(v[0])+ResetAll+" >< "+colgoed+header["Valuta"]+fornum(v[1])
            if k == "Datumformaat":
                v = v.replace("DDMMYYYY","GGMMAAAA").replace("DD-MM-YY","GG-MM-YY").replace("DD/MM/YY","GG/MM/AA").replace("DDmmm\'YY","GGmmm\'AA").replace("DD-mmmYY","GG-mmmAA").replace("YYYYMMDD","AAAAMMGG")
            print(colslecht+for15(k.replace("Beschrijving","Descrizione").replace("Rekeninghouder","Intestatario").replace("Plaats","Città").replace("Taal","Lingua").replace("Valuta","Valuta").replace("Nulregels","Linee a zero").replace("Markering L><H","Indicaz. I><S").replace("Kleur","Colore").replace("Datumformaat","Formato data").replace("Print","Stampa").replace("Toon","Mostra").replace("CSV","CSV")),colonbepaald+":",colgoed+v+ResetAll)
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
            print(colslecht+for15(k.replace("Beschrijving","Description").replace("Rekeninghouder","Account holder").replace("Plaats","City").replace("Taal","Language").replace("Valuta","Currency").replace("Nulregels","Zero lines").replace("Markering L><H","Marking L><U").replace("Kleur","Colour").replace("Datumformaat","Date formatting").replace("Print","Print").replace("Toon","Show").replace("CSV","CSV")),colonbepaald+":",colgoed+v+ResetAll)
        elif Taal == "IT":
            if k == "Markering L><H":
                v = header["Valuta"]+fornum(v[0])+" >< "+header["Valuta"]+fornum(v[1])
            if k == "Datumformaat":
                v = v.replace("DDMMYYYY","GGMMAAAA").replace("DD-MM-YY","GG-MM-YY").replace("DD/MM/YY","GG/MM/AA").replace("DDmmm\'YY","GGmmm\'AA").replace("DD-mmmYY","GG-mmmAA").replace("YYYYMMDD","AAAAMMGG")
            print(colslecht+for15(k.replace("Beschrijving","Descrizione").replace("Rekeninghouder","Intestatario").replace("Plaats","Città").replace("Taal","Lingua").replace("Valuta","Valuta").replace("Nulregels","Linee a zero").replace("Markering L><H","Indicaz. I><S").replace("Kleur","Colore").replace("Datumformaat","Formato data").replace("Print","Stampa").replace("Toon","Mostra").replace("CSV","CSV")),colonbepaald+":",colgoed+v+ResetAll)
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
    with open("alternatievenamen","r") as f:
        alternatievenamen = ast.literal_eval(f.read())
        for k,v in sorted(alternatievenamen.items()):
            try:
                with open(k,"r") as g:
                    lengte = ast.literal_eval(g.read())
                    tot = 0
                    for i in lengte[1:]:
                        if i[0] > int(strnu[:6]+"00"):
                            tot = tot + i[1]
                    budget = lengte[0]
                    col = catcol[k]
                    if Taal == "EN":
                        v = v.replace("vaste act/pass.","fixd ass/equity").replace("vlotte act/pass","cash (equiv.)").replace("tussenrekening","intermediary").replace("voorraden","inventory").replace("kostenplaatsen","cost centers").replace("kosten","expenses").replace("fabricagerek.","manufact.acc.").replace("inkoopwaarde","cost of goods").replace("omzet","sales").replace("privé","private").replace("saldo & inkomen","funds & income").replace("vaste lasten","fixed costs").replace("boodschappen","groceries").replace("reis & verblijf","travel & stay").replace("leningen","loans").replace("overig","other")
                    elif Taal == "IT":
                        v = v.replace("vaste act/pass.","attiv. fisse").replace("vlotte act/pass","dispon. liquide").replace("tussenrekening","conti intermedi").replace("voorraden","magazzino").replace("kostenplaatsen","centri di costo").replace("kosten","costi").replace("fabricagerek.","contiproduzione").replace("inkoopwaarde","costi vendute").replace("omzet","ricavi").replace("privé","privato").replace("saldo & inkomen","saldo & reddito").replace("vaste lasten","costi fissi").replace("boodschappen","spese").replace("reis & verblijf","viaggioalloggio").replace("leningen","prestiti").replace("overig","altro")
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
            huza = input("Is this a household or a business account?\n >1 household\n  2 business\n  : ")
        elif Taal == "IT":
            huza = input("Si tratta di un conto domestico o aziendale?\n >1 domestico\n  2 aziendale\n  : ")
        else:
            huza = input("Betreft dit een huishoudelijke of een zakelijke rekening?\n >1 huishoudelijk\n  2 zakelijk\n  : ")
        print(ResetAll, end = "")
        if huza.upper() in afsluitlijst:
            break
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
        nieuwheader = {'Beschrijving':'','Rekeninghouder':'','Plaats':'','Taal':Taal,'Valuta':'€', 'Nulregels':'Nee','Markering L><H': [-100,100],'Kleur':'Categorie','Datumformaat':'YYYYMMDD','Print':'Nee','Toon':'Ja','CSV':'Nee'}
        with open("header","w") as f:
            print(nieuwheader, file = f, end = "")
        nieuwalternatievenamenlijst = {'0':'vaste act/pass.','1':'vlotte act/pass','2':'tussenrekening','3':'voorraden','4':'kosten','5':'kostenplaatsen','6':'fabricagerek.','7':'inkoopwaarde','8':'omzet','9':'privé','A':'saldo & inkomen','B':'vaste lasten','C':'boodschappen','D':'reis & verblijf','E':'leningen','O':'overig'}
        with open("alternatievenamen","w") as g:
            print(nieuwalternatievenamenlijst, file = g, end = "")
        if huza == "2":
            for k in lijst:
                if k in ["0","1","2","3","4","5","6","7","8","9"]:
                    with open(k,"w") as h:
                        print([0.0], file = h, end = "")
            with open("1","w") as w:
                if Taal == "EN":
                    print([0.0, [11111111, 0.0, "Balance", "StartingBalance"]], file = w, end = "")
                elif Taal == "IT":
                    print([0.0, [11111111, 0.0, "Saldo", "SaldoIniziale"]], file = w, end = "")
                else:
                    print([0.0, [11111111, 0.0, "Saldo", "Startsaldo"]], file = w, end = "")
        else:
            for k in lijst:
                if k in ["A","B","C","D","E","O"]:
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
    if header["CSV"] == "Ja":
        exportcsv()
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
try:
    rekeningenlijst = rknngnlst()
except:
    rekeningenlijst = []
if len(rekeningenlijst) == 0:
    nieuwetaal = input("Kies uw taal | Choose your language | Scegli la tua lingua\n >1 NL\n  2 EN\n  3 IT\n  : %s" % (colgoed))
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
        huza = input("Is this a household or a business account?\n >1 household\n  2 business\n  : ")
    elif Taal == "IT":
        huza = input("Si tratta di un conto domestico o aziendale?\n >1 domestico\n  2 aziendale\n  : ")
    else:
        huza = input("Betreft dit een huishoudelijke of een zakelijke rekening?\n >1 huishoudelijk\n  2 zakelijk\n  : ")
    print(ResetAll, end = "")
    if huza.upper() in afsluitlijst:
        doei()
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
    nieuwheader = {'Beschrijving':'','Rekeninghouder':'','Plaats':'','Taal':Taal,'Valuta':'€','Nulregels':'Nee','Markering L><H':[-100,100],'Kleur':'Categorie','Datumformaat':'YYYYMMDD','Print':'Nee','Toon':'Ja','CSV':'Nee'}
    with open("header","w") as f:
        print(nieuwheader, file = f, end = "")
    nieuwalternatievenamenlijst = {'0':'vaste act/pass.','1':'vlotte act/pass','2':'tussenrekening','3':'voorraden','4':'kosten','5':'kostenplaatsen','6':'fabricagerek.','7':'inkoopwaarde','8':'omzet','9':'privé','A':'saldo & inkomen','B':'vaste lasten','C':'boodschappen','D':'reis & verblijf','E':'leningen','O':'overig'}
    with open("alternatievenamen","w") as g:
        print(nieuwalternatievenamenlijst, file = g, end = "")
    if huza == "2":
        for k in lijst:
            if k in ["0","1","2","3","4","5","6","7","8","9"]:
                with open(k,"w") as h:
                    print([0.0], file = h, end = "")
        with open("1","w") as w:
            if Taal == "EN":
                print([0.0, [11111111, 0.0, "Balance", "StartingBalance"]], file = w, end = "")
            elif Taal == "IT":
                print([0.0, [11111111, 0.0, "Saldo", "SaldoIniziale"]], file = w, end = "")
            else:
                print([0.0, [11111111, 0.0, "Saldo", "Startsaldo"]], file = w, end = "")
    else:
        for k in lijst:
            if k in ["A","B","C","D","E","O"]:
                with open(k,"w") as h:
                    print([0.0], file = h, end = "")
        with open("A","w") as w:
            if Taal == "EN":
                print([0.0, [11111111, 0.0, "Balance", "StartingBalance"]], file = w, end = "")
            elif Taal == "IT":
                print([0.0, [11111111, 0.0, "Saldo", "SaldoIniziale"]], file = w, end = "")
            else:
                print([0.0, [11111111, 0.0, "Saldo", "Startsaldo"]], file = w, end = "")
    rekeningenlijst = [[nieuwiban,nieuwjaar]]
try:
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
        Toon = toontotaal()
        kleur = updatekleur()
        Kleuren = kleur[0]
        globals().update(Kleuren)
        catcol = kleur[1]
except:
    exit()
##### Hier worden de standaarwaarden overschreven met de aangepaste waarden in header

try:
    with open("header","r") as h:
        header = ast.literal_eval(h.read())
    for k,v in header.items():
        k = v
    globals().update(header)
except(Exception) as error:
    #print(error)
    nieuwheader = {'Beschrijving':'','Rekeninghouder':'','Plaats':'','Taal':Taal,'Valuta':'€','Nulregels':'Nee','Markering L><H':[-100,100],'Kleur':'Categorie','Datumformaat':'YYYYMMDD','Print':'Nee','Toon':'Ja','CSV':'Nee'}
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

def exportcsv():
    alternatievenamendict = {}
    with open("alternatievenamen","r") as a:
        alternatieven = ast.literal_eval(a.read())
        for i,j in alternatieven.items():
            alternatievenamendict[i] = j
    with open("export.csv","w+") as e:
        for i in lijst:
            try:
                with open(i,"r") as z:
                    Z = ast.literal_eval(z.read())
                    print(i+": "+alternatievenamendict[i]+","+str(Z[0]), file = e)
                    for j in Z[1:]:
                        for k in j:
                            print(str(k), file = e, end = ",")
                        print(file = e)
                    print(file = e)
            except:
                pass


def aid():
    if Taal == "EN":
        print(info2EN)
    elif Taal == "IT":
        print(info2IT)
    else:
        print(info2)
    if Taal == "EN":
        warp = textwrap.wrap("Choose - for example - \"2 1\" for help with adding a new mutation. Separate the menu options with a space \" \", hyphen \"-\", or comma \",\".", width = w)
    elif Taal == "IT":
        warp = textwrap.wrap("Scegli - ad esempio - \"2 1\" per ottenere assistenza nell'aggiunta di una nuova mutazione. Separa le opzioni del menu con uno spazio \" \", un trattino \"-\" o una virgola \",\".", width = w)
    else:
        warp = textwrap.wrap("Kies - bijvoorbeeld - \"2 1\" voor hulp bij het toevoegen van een nieuwe mutatie. Scheid de menu-opties met een spatie \" \", koppelteken \"-\"of komma \",\".", width = w)
    for i in warp:
        print(i)
    loop = True
    while loop == True:
        warp = ""
        op = ""
        wat = input().replace(" ",",").replace("-",",").split(",")
        while '' in wat:
            wat.remove('')
        if len(wat) == 0 or wat[0].upper() in afsluitlijst:
            break
        if wat == ['0']:
            if Taal == "EN":
                op = menuEN["0"]
                warp = textwrap.wrap("View and change environmental variables, mainly for this specific account.", width = w)
            elif Taal == "IT":
                op = menuIT["0"]
                warp = textwrap.wrap("Visualizzare e modificare le variabili ambientali, principalmente per questo account specifico.", width = w)
            else:
                op = menu["0"]
                warp = textwrap.wrap("Bekijk en verander omgevingsvariabelen, voornamelijk voor dit specifieke account.", width = w)
        elif wat == ['0','0']:
            if Taal == "EN":
                op = menuEN["0"]+" - "+menuEN["0,0"]
                warp = textwrap.wrap("Information about the program version and this Help menu. Choose - for example - \"2 1\" for help with adding a new mutation. Separate the menu options with a space \" \", hyphen \"-\", or comma \",\".", width = w)
            elif Taal == "IT":
                op = menuIT["0"]+" - "+menuIT["0,0"]
                warp = textwrap.wrap("Informazioni sulla versione del programma e su questo menu di aiuto. Scegli - ad esempio - \"2 1\" per ottenere assistenza nell'aggiunta di una nuova mutazione. Separa le opzioni del menu con uno spazio \" \", un trattino \"-\" o una virgola \",\".", width = w)
            else:
                op = menu["0"]+" - "+menu["0,0"]
                warp = textwrap.wrap("Informatie over de programmaversie en dit Helpmenu. Kies - bijvoorbeeld - \"2 1\" voor hulp bij het toevoegen van een nieuwe mutatie. Scheid de menu-opties met een spatie \" \", koppelteken \"-\"of komma \",\".", width = w)
        elif wat == ['0','1']:
            if Taal == "EN":
                op = menuEN["0"]+" - "+menuEN["0,1"]
                warp = textwrap.wrap("Change the name of, or an available budget for a category, or delete it. A NEW category is created by adding a new mutation to a new category; it is created at that time.", width = w)
            elif Taal == "IT":
                op = menuIT["0"]+" - "+menuIT["0,1"]
                warp = textwrap.wrap("Modifica il nome, o un budget disponibile per una categoria, o rimuovila. Una NUOVA categoria viene creata aggiungendo una nuova mutazione a una nuova categoria; questa viene creata in quel momento.", width = w)
            else:
                op = menu["0"]+" - "+menu["0,1"]
                warp = textwrap.wrap("Wijzig de naam van, of een beschikbaar budget voor een categorie, of verwijder die. Een NIEUWE categorie maakt men aan door een nieuwe mutatie toe te voegen aan een nieuwe categorie; die wordt op dat moment aangemaakt.", width = w)
        elif wat == ['0','1','1']:
            if Taal == "EN":
                op = menuEN["0"]+" - "+menuEN["0,1"]+" - "+menuEN["0,1,1"]
                warp = textwrap.wrap("Change the name of the category.", width = w)
            elif Taal == "IT":
                op = menuIT["0"]+" - "+menuIT["0,1"]+" - "+menuIT["0,1,1"]
                warp = textwrap.wrap("Cambia il nome della categoria.", width = w)
            else:
                op = menu["0"]+" - "+menu["0,1"]+" - "+menu["0,1,1"]
                warp = textwrap.wrap("Wijzig de naam van de categorie", width = w)
        elif wat == ['0','1','2']:
            if Taal == "EN":
                op = menuEN["0"]+" - "+menuEN["0,1"]+" - "+menuEN["0,1,2"]
                warp = textwrap.wrap("Adjust the budget for this category. It will be automatically calculated whether the budgets are balanced; make sure the balance is always 0.", width = w)
            elif Taal == "IT":
                op = menuIT["0"]+" - "+menuIT["0,1"]+" - "+menuIT["0,1,2"]
                warp = textwrap.wrap("Modifica il budget per questa categoria. Verrà calcolato automaticamente se i budget sono equilibrati; assicurati che il bilancio sia sempre 0.", width = w)
            else:
                op = menu["0"]+" - "+menu["0,1"]+" - "+menu["0,1,2"]
                warp = textwrap.wrap("Pas het budget voor deze categorie aan. Er wordt automatisch berekend of de budgetten sluitend zijn; zorg ervoor dat de balans altijd 0 is.", width = w)
        elif wat == ['0','1','3']:
            if Taal == "EN":
                op = menuEN["0"]+" - "+menuEN["0,1"]+" - "+menuEN["0,1,3"]
                warp = textwrap.wrap("Completely delete a category, including all transactions in that category. NOTE: the bank balance will be increased or decreased by the total amount of this category. So, make sure that any transactions in this category are first distributed among one or more other categories!", width = w)
            elif Taal == "IT":
                op = menuIT["0"]+" - "+menuIT["0,1"]+" - "+menuIT["0,1,3"]
                warp = textwrap.wrap("Elimina completamente una categoria, inclusi tutti le transazioni in quella categoria. NOTA: il saldo bancario verrà aumentato o diminuito dell'importo totale di questa categoria. Assicurati quindi che tutte le eventuali transazioni in questa categoria siano state prima distribuite tra una o più altre categorie!", width = w)
            else:
                op = menu["0"]+" - "+menu["0,1"]+" - "+menu["0,1,3"]
                warp = textwrap.wrap("Verwijder een categorie compleet, inclusief alle transacties in die categorie. LET OP: het banksaldo wordt verhoogd of verlaagd met het totaalbedrag van deze categorie. Zorg er dus eerst voor dat alle eventuele transacties in deze categorie zijn verdeeld over één of meer andere categorie(-ën)!", width = w)
        elif wat == ['0','2']:
            if Taal == "EN":
                op = menuEN["0"]+" - "+menuEN["0,2"]
                warp = textwrap.wrap("Adjust various display settings of this account, and create export files with useful overviews or reusable data.", width = w)
            elif Taal == "IT":
                op = menuIT["0"]+" - "+menuIT["0,2"]
                warp = textwrap.wrap("Modifica le diverse impostazioni di visualizzazione di questo account e crea file di esportazione con panorami utili o dati riutilizzabili.", width = w)
            else:
                op = menu["0"]+" - "+menu["0,2"]
                warp = textwrap.wrap("Pas verschillende weergave-instellingen van dit account aan, en stel exportbestanden met handige overzichten of herbruikbare gegevens in.", width = w)
        elif wat == ['0','2','1']:
            if Taal == "EN":
                op = menuEN["0"]+" - "+menuEN["0,2"]+" - "+menuEN["0,2,1"]
                warp = textwrap.wrap("Here you can adjust the account name.", width = w)
            elif Taal == "IT":
                op = menuIT["0"]+" - "+menuIT["0,2"]+" - "+menuIT["0,2,1"]
                warp = textwrap.wrap("Qui puoi modificare il nome del conto.", width = w)
            else:
                op = menu["0"]+" - "+menu["0,2"]+" - "+menu["0,2,1"]
                warp = textwrap.wrap("Hier kunt u de rekeningnaam aanpassen.", width = w)
        elif wat == ['0','2','2']:
            if Taal == "EN":
                op = menuEN["0"]+" - "+menuEN["0,2"]+" - "+menuEN["0,2,2"]
                warp = textwrap.wrap("Here you can adjust the account holder name.", width = w)
            elif Taal == "IT":
                op = menuIT["0"]+" - "+menuIT["0,2"]+" - "+menuIT["0,2,2"]
                warp = textwrap.wrap("Qui puoi modificare il nome del intestario del conto.", width = w)
            else:
                op = menu["0"]+" - "+menu["0,2"]+" - "+menu["0,2,2"]
                warp = textwrap.wrap("Hier kunt u de rekeninghoudernaam aanpassen.", width = w)
        elif wat == ['0','2','3']:
            if Taal == "EN":
                op = menuEN["0"]+" - "+menuEN["0,2"]+" - "+menuEN["0,2,3"]
                warp = textwrap.wrap("Here you can adjust the place of business.", width = w)
            elif Taal == "IT":
                op = menuIT["0"]+" - "+menuIT["0,2"]+" - "+menuIT["0,2,3"]
                warp = textwrap.wrap("Qui puoi modificare la sede legale.", width = w)
            else:
                op = menu["0"]+" - "+menu["0,2"]+" - "+menu["0,2,3"]
                warp = textwrap.wrap("Hier kunt u de vestigingsplaats aanpassen.", width = w)
        elif wat == ['0','2','4']:
            if Taal == "EN":
                op = menuEN["0"]+" - "+menuEN["0,2"]+" - "+menuEN["0,2,4"]
                warp = textwrap.wrap("You can adjust the language of the program per account. Currently, you can choose from \"NL\" (Dutch, default), \"EN\" (English), or \"IT\" (Italian).", width = w)
            elif Taal == "IT":
                op = menuIT["0"]+" - "+menuIT["0,2"]+" - "+menuIT["0,2,4"]
                warp = textwrap.wrap("È possibile modificare la lingua del programma per account. Attualmente è possibile scegliere tra \"NL\" (olandese, predefinito), \"EN\" (inglese) o \"IT\" (italiano).", width = w)
            else:
                op = menu["0"]+" - "+menu["0,2"]+" - "+menu["0,2,4"]
                warp = textwrap.wrap("U kunt de taal van het programma per rekening aanpassen. Op dit moment kunt u kiezen uit \"NL\" (Nederlands, standaard), \"EN\" (Engels) of \"IT\" (Italiaans).", width = w)
        elif wat == ['0','2','5']:
            if Taal == "EN":
                op = menuEN["0"]+" - "+menuEN["0,2"]+" - "+menuEN["0,2,5"]
                warp = textwrap.wrap("Here you can enter any currency symbol. Choose a currency symbol - it can also be a letter or another symbol - that occupies exactly one position. The Euro symbol \"€\" is used by default, commonly used other currency symbols are for example \"$\" and \"¥\".", width = w)
            elif Taal == "IT":
                op = menuIT["0"]+" - "+menuIT["0,2"]+" - "+menuIT["0,2,5"]
                warp = textwrap.wrap("ValutaQui puoi inserire qualsiasi simbolo di valuta. Scegli un simbolo di valuta - che può essere anche una lettera o un altro simbolo - che occupi una sola posizionea. Di default viene utilizzato il simbolo dell'euro \"€\", altri simboli di valuta comunemente utilizzati sono ad esempio \"$\" e \"¥\".", width = w)
            else:
                op = menu["0"]+" - "+menu["0,2"]+" - "+menu["0,2,5"]
                warp = textwrap.wrap("Hier kunt u ieder valutateken invoeren. Kies een valutateken - dat kan ook een letter of een ander symbool zijn - dat precies één positie inneemt. Standaard wordt het Euroteken \"€\" gebruikt, veelgebruikte andere valutatekens zijn bijvoorbeeld \"$\" en \"¥\"", width = w)
        elif wat == ['0','2','6']:
            if Taal == "EN":
                op = menuEN["0"]+" - "+menuEN["0,2"]+" - "+menuEN["0,2,6"]
                warp = textwrap.wrap("Choose here whether you want to see empty categories in the totals.", width = w)
            elif Taal == "IT":
                op = menuIT["0"]+" - "+menuIT["0,2"]+" - "+menuIT["0,2,6"]
                warp = textwrap.wrap("Scegli qui se vuoi vedere anche le categorie vuote nei totali.", width = w)
            else:
                op = menu["0"]+" - "+menu["0,2"]+" - "+menu["0,2,6"]
                warp = textwrap.wrap("Kies hier of u in de totalen ook lege categorieën wilt zien.", width = w)
        elif wat == ['0','2','7']:
            if Taal == "EN":
                op = menuEN["0"]+" - "+menuEN["0,2"]+" - "+menuEN["0,2,7"]
                warp = textwrap.wrap("The currency symbol can be highlighted if a mutation is higher or lower than a certain amount. By default, these are set to \"lower than -100\" and \"higher than 100\".", width = w)
            elif Taal == "IT":
                op = menuIT["0"]+" - "+menuIT["0,2"]+" - "+menuIT["0,2,7"]
                warp = textwrap.wrap("Il simbolo di valuta può essere evidenziato se una variazione è superiore o inferiore a un determinato importo. Di default, questi sono impostati su \"inferiore a -100\" e \"superiore a 100\".", width = w)
            else:
                op = menu["0"]+" - "+menu["0,2"]+" - "+menu["0,2,7"]
                warp = textwrap.wrap("Het valutateken kan worden geaccentueerd als een mutatie hoger of lager is dan een hier bepaald bedrag. Standaard staan deze op \"lager dan -100\" en \"hoger dan 100\".", width = w)
        elif wat == ['0','2','8']:
            if Taal == "EN":
                op = menuEN["0"]+" - "+menuEN["0,2"]+" - "+menuEN["0,2,8"]
                warp = textwrap.wrap("The account and the environment can be displayed in different color palettes. Try them out!", width = w)
            elif Taal == "IT":
                op = menuIT["0"]+" - "+menuIT["0,2"]+" - "+menuIT["0,2,8"]
                warp = textwrap.wrap("Il conto e l'ambiente possono essere visualizzati in diverse tavolozze di colori. Provali!", width = w)
            else:
                op = menu["0"]+" - "+menu["0,2"]+" - "+menu["0,2,8"]
                warp = textwrap.wrap("De rekening en de omgeving kunnen in verschillende kleurenpaletten worden weergegeven. Probeer ze uit!", width = w)
        elif wat == ['0','2','9']:
            if Taal == "EN":
                op = menuEN["0"]+" - "+menuEN["0,2"]+" - "+menuEN["0,2,9"]
                warp = textwrap.wrap("Here you can choose the date formatting. Default \"YYYYMMDD\": %s" % nu, width = w)
            elif Taal == "IT":
                op = menuIT["0"]+" - "+menuIT["0,2"]+" - "+menuIT["0,2,9"]
                warp = textwrap.wrap("Qui puoi scegliere il formato di visualizzazione della data. Predefinito \"AAAAMMGG\": %s" % nu, width = w)
            else:
                op = menu["0"]+" - "+menu["0,2"]+" - "+menu["0,2,9"]
                warp = textwrap.wrap("Hier kunt u de datumweergave kiezen. Standaard \"JJJJMMDD\": %s" % nu, width = w)
        elif wat == ['0','2','10']:
            if Taal == "EN":
                op = menuEN["0"]+" - "+menuen["0,2"]+" - "+menuEN["0,2,10"]
                warp = textwrap.wrap("A monthly overview (one month) can be exported to a file in the account folder. The account folder is located in the directory where the program is running and always contains a \"@\". By default, this is turned off. When you enable this, every monthly overview will be automatically exported; if it already exists, it will be overwritten.", width = w)
            elif Taal == "IT":
                op = menuIT["0"]+" - "+menuIT["0,2"]+" - "+menuIT["0,2,10"]
                warp = textwrap.wrap("Una visualizzazione mensile (un mese) può essere esportata in un file nella cartella del conto. La cartella del conto si trova nella cartella in cui il programma è in esecuzione e contiene sempre un \"@\". Di default, questa opzione è disattivata. Quando si attiva questo, ogni riepilogo mensile verrà sempre esportato automaticamente; se esiste già, verrà sovrascritto.", width = w)
            else:
                op = menu["0"]+" - "+menu["0,2"]+" - "+menu["0,2,10"]
                warp = textwrap.wrap("Een maandoverzicht (één maand) kan naar een bestand in de rekeningmap worden geëxporteerd. De rekeningmap bevindt zich in de map waar het programma draait, en bevat altijd een \"@\". Standaard staat dit uit. Wanneer u dit aanzet wordt ieder maandoverzicht steeds automatisch geëxporteerd; als het al bestaat wordt het overschreven.", width = w)
        elif wat == ['0','2','11']:
            if Taal == "EN":
                op = menuEN["0"]+" - "+menuEN["0,2"]+" - "+menuEN["0,2,11"]
                warp = textwrap.wrap("The account balance can be displayed on the start screen. Also, the total of all different accounts where this is activated will be shown. By default, this is enabled. PLEASE NOTE: The total balance of multiple accounts may be incorrect if different currencies are used!", width = w)
            elif Taal == "IT":
                op = menuIT["0"]+" - "+menuIT["0,2"]+" - "+menuIT["0,2,11"]
                warp = textwrap.wrap("Il saldo del conto può essere visualizzato nella schermata iniziale. Inoltre, verrà mostrato il totale di tutti i diversi conti in cui questa opzione è attiva. Di default, questa opzione è attiva. ATTENZIONE: Il saldo totale di più conti può essere impreciso se vengono utilizzate valute diverse!", width = w)
            else:
                op = menu["0"]+" - "+menu["0,2"]+" - "+menu["0,2,11"]
                warp = textwrap.wrap("Het rekeningsaldo kan op het startscherm worden getoond. Tevens wordt het totaal getoond van alle verschillende rekeningen waarbij dit is geactiveerd. Standaard staat dit aan. LET OP: Het totaalsaldo van meerdere rekeningen kan onjuist zijn als er verschillende valuta worden gebruikt!", width = w)
        elif wat == ['0','2','12']:
            if Taal == "EN":
                op = menuEN["0"]+" - "+menuEN["0,2"]+" - "+menuEN["0,2,12"]
                warp = textwrap.wrap("The entire account can be exported in one CSV file: export.csv, which is placed in the account folder. The account folder is located in the directory where the program runs, and always contains an \"@\". By default, this is disabled. When you enable this, each CSV file is automatically exported when the program is closed; if it already exists, it will be overwritten.", width = w)
            elif Taal == "IT":
                op = menuIT["0"]+" - "+menuIT["0,2"]+" - "+menuIT["0,2,12"]
                warp = textwrap.wrap("L'intero conto può essere esportato in un unico file CSV: export.csv, che verrà posizionato nella cartella del conto. La cartella del conto si trova nella directory in cui il programma è in esecuzione e contiene sempre una \"@\". Di default, questa opzione è disattivata. Quando la si attiva, ogni file CSV viene esportato automaticamente alla chiusura del programma; se esiste già, verrà sovrascritto.", width = w)
            else:
                op = menu["0"]+" - "+menu["0,2"]+" - "+menu["0,2,12"]
                warp = textwrap.wrap("De hele rekening kan worden geëxporteerd in één csv-bestand: export.csv, dat in de rekeningmap wordt geplaatst. De rekeningmap bevindt zich in de map waar het programma draait, en bevat altijd een \"@\". Standaard staat dit uit. Wanneer u dit aanzet wordt ieder csv-bestand bij het afsluiten van het programma automatisch geëxporteerd; als het al bestaat wordt het overschreven.", width = w)
        elif wat == ['0','3']:
            if Taal == "EN":
                op = menuEN["0"]+" - "+menuEN["0,3"]
                warp = textwrap.wrap("\"Showing an account\" roughly means \"making it available\". One can only edit an account, add transactions, etc., if the account is \"visible\". \"Hidden\" accounts can be archived accounts, draft accounts, and so on. Choose here which accounts should be shown or hidden.", width = w)
            elif Taal == "IT":
                op = menuIT["0"]+" - "+menuIT["0,3"]
                warp = textwrap.wrap("\"Mostrare\" un conto significa approssimativamente \"rendere disponibile\". Si può modificare un conto, aggiungere transazioni, ecc., solo se il conto è \"visibile\". I conti \"nascosti\" possono essere conti archiviati, conti di progetto, ecc. Scegli qui quali conti devono essere mostrati o nascosti.", width = w)
            else:
                op = menu["0"]+" - "+menu["0,3"]
                warp = textwrap.wrap("Een rekening \"tonen\" betekent ongeveer \"beschikbaar maken\". Men kan alleen een rekening bewerken, er mutaties aan toevoegen, enzovoorts, als de rekening \"zichtbaar\" is. \"Verborgen\" rekeningen kunnen gearchiveerde rekeningen zijn, conceptrekeningen, enzovoorts. Kies hier welke rekeningen getoond of verborgen moeten worden.", width = w)
        elif wat == ['0','4']:
            if Taal == "EN":
                op = menuEN["0"]+" - "+menuEN["0,4"]
                warp = textwrap.wrap("You don't have to exit the program to switch accounts. Choose another one here. PLEASE NOTE: if you cancel this prematurely, you will still exit the program!", width = w)
            elif Taal == "IT":
                op = menuIT["0"]+" - "+menuIT["0,4"]
                warp = textwrap.wrap("Non è necessario uscire dal programma per cambiare conto. Scegliene un altro qui. ATTENZIONE: se interrompi prematuramente, uscirai comunque dal programma!", width = w)
            else:
                op = menu["0"]+" - "+menu["0,4"]
                warp = textwrap.wrap("U hoeft het programma niet te verlaten om van rekening te wisselen. Kies hier een andere. LET OP: als u dit voortijdig afbreekt verlaat u het programma alsnog!", width = w)
        elif wat == ['0','5']:
            if Taal == "EN":
                op = menuEN["0"]+" - "+menuEN["0,5"]
                warp = textwrap.wrap("Add a new account here.", width = w)
            elif Taal == "IT":
                op = menuIT["0"]+" - "+menuIT["0,5"]
                warp = textwrap.wrap("Aggiungi qui un nuovo conto.", width = w)
            else:
                op = menu["0"]+" - "+menu["0,5"]
                warp = textwrap.wrap("Voeg hier een nieuwe rekening toe.", width = w)
        elif wat == ['0','6']:
            if Taal == "EN":
                op = menuEN["0"]+" - "+menuEN["0,6"]
                warp = textwrap.wrap("First consider whether the account should be \"hidden\" (\"archived\"), but here an account can be completely deleted.", width = w)
            elif Taal == "IT":
                op = menuIT["0"]+" - "+menuIT["0,6"]
                warp = textwrap.wrap("Prima considera se il conto deve essere \"nascosto\" (\"archiviato\"), ma qui un conto può essere completamente eliminato.", width = w)
            else:
                op = menu["0"]+" - "+menu["0,6"]
                warp = textwrap.wrap("Overweeg eerst of de rekening \"verborgen\" (\"gearchiveerd\") moet worden, maar hier kan een rekening volledig worden verwijderd.", width = w)
        elif wat == ['0','7']:
            if Taal == "EN":
                op = menuEN["0"]+" - "+menuEN["0,7"]
                warp = textwrap.wrap("Here you can transfer the current settings of this account to another one. The existing settings of the other account will be overwritten.", width = w)
            elif Taal == "IT":
                op = menuIT["0"]+" - "+menuIT["0,7"]
                warp = textwrap.wrap("Qui puoi trasferire le impostazioni attuali di questo conto su un altro. Le impostazioni esistenti dell'altro conto saranno sovrascritte.", width = w)
            else:
                op = menu["0"]+" - "+menu["0,7"]
                warp = textwrap.wrap("Hier kunt u de huidige instellingen van deze rekening overzetten naar een andere. De bestaande instellingen van de andere rekening worden daarmee overschreven.", width = w)
        elif wat == ['1']:
            if Taal == "EN":
                op = menuEN["1"]
                warp = textwrap.wrap("Transactions can be filtered based on various criteria, such as time period, category, amount, and so on. The results are displayed in a clear table where the transactions are assigned a unique ID. This ID can be used for various operations, such as copying, modifying, or deleting.", width = w)
            elif Taal == "IT":
                op = menuIT["1"]
                warp = textwrap.wrap("Le mutazioni possono essere filtrate in base a vari criteri, come periodo di tempo, categoria, importo, e così via. I risultati vengono mostrati in una tabella chiara, in cui le mutazioni ricevono un ID univoco. Questo ID può essere utilizzato per varie operazioni, come copiare, modificare o eliminare.", width = w)
            else:
                op = menu["1"]
                warp = textwrap.wrap("Mutaties kunnen op verschillende criteria worden gefilterd, zoals tijdvak, categorie, bedrag, enzovoorts. Het resultaat wordt in een overzichtelijke tabel getoond waarbij de mutaties een uniek ID krijgen. Dit ID kan worden gebruikt voor verschillende bewerkingen, zoals kopiëren, wijzigen of verwijderen.", width = w)
        elif wat == ['2']:
            if Taal == "EN":
                op = menuEN["2"]
                warp = textwrap.wrap("Here you can add or copy new transactions.", width = w)
            elif Taal == "IT":
                op = menuIT["2"]
                warp = textwrap.wrap("Qui è possibile aggiungere o copiare nuove mutazioni.", width = w)
            else:
                op = menu["2"]
                warp = textwrap.wrap("Hier kunt u nieuwe mutaties toevoegen of kopiëren.", width = w)
        elif wat == ['2','1']:
            if Taal == "EN":
                op = menuEN["2"]+" - "+menuEN["2,1"]
                warp = textwrap.wrap("Adding a new, blank transaction. It is possible to fill in \"Date\", \"Amount\", \"Other party\", and \"About\" on one line, comma-separated in CSV style, and then assign it to a category, or line by line. Leaving the date empty will use today's date, leaving the amount empty will input a transaction of 0.00 in the specified currency.", width = w)
            elif Taal == "IT":
                op = menuIT["2"]+" - "+menuIT["2,1"]
                warp = textwrap.wrap("Aggiungere una nuova transazione vuota. È possibile inserire su una riga, separati da virgola in stile CSV, in successione \"Data\", \"Somma\", \"Controparte\" e \"Riguarda\", e quindi assegnarli a una categoria, o riga per riga. Lasciare vuota la data imposterà la data odierna, lasciare vuoto l'importo creerà una transazione di 0.00 nella valuta specificata.", width = w)
            else:
                op = menu["2"]+" - "+menu["2,1"]
                warp = textwrap.wrap("Een nieuwe, blanco mutatie toevoegen. Men kan op één regel, kommagescheiden in csv-stijl, achtereenvolgens \"Datum\",\"Bedrag\",\"Wederpartij\" en \"Betreft\" invullen en die vervolgens aan een categorie toekennen, of regel voor regel. Het leeg laten van de datum geeft de datum van vandaag, het bedrag leeg laten geeft een mutatie van 0.00 in de opgegeven valuta.", width = w)
        elif wat == ['2','2']:
            if Taal == "EN":
                op = menuEN["2"]+" - "+menuEN["2,2"]
                warp = textwrap.wrap("Make a copy of an existing mutation based on a previously generated ID. The date of the original will be replaced by today's date in the copy; this can be changed later if desired (3,1), just like any other element.", width = w)
            elif Taal == "IT":
                op = menuIT["2"]+" - "+menuIT["2,2"]
                warp = textwrap.wrap("Creare una copia di una mutazione esistente basata su un ID generato in precedenza. La data dell'originale viene sostituita dalla data odierna nella copia; questa può essere modificata in un secondo momento se necessario (3,1), come ogni altro elemento.", width = w)
            else:
                op = menu["2"]+" - "+menu["2,2"]
                warp = textwrap.wrap("Maak een kopie van een bestaande mutatie op basis van een eerder gegenereerd ID. De datum van het origineel wordt in de kopie vervangen door de datum van vandaag; die kan indien gewenst later gewijzigd worden (3,1), net als ieder ander element.", width = w)
        elif wat == ['2','3']:
            if Taal == "EN":
                op = menuEN["2"]+" - "+menuEN["2,3"]
                warp = textwrap.wrap("Make a copy to another account of an existing mutation based on a previously generated ID. The date of the original will be replaced by today's date in the copy; this can be changed later if desired (3,1: %s), just like any other element in the mutation." % menuEN["3,1"], width = w)
            elif Taal == "IT":
                op = menuIT["2"]+" - "+menuIT["2,3"]
                warp = textwrap.wrap("Creare una copia in un altro conto di una mutazione esistente basata su un ID generato in precedenza. La data dell'originale viene sostituita dalla data odierna nella copia; questa può essere modificata in un secondo momento se necessario (3,1: %s), come ogni altro elemento nella mutazione." % menuIT["3,1"], width = w)
            else:
                op = menu["2"]+" - "+menu["2,3"]
                warp = textwrap.wrap("Maak een kopie naar een andere rekening van een bestaande mutatie op basis van een eerder gegenereerd ID. De datum van het origineel wordt in de kopie vervangen door de datum van vandaag; die kan indien gewenst later gewijzigd worden (3,1: %s), net als ieder ander element in de mutatie." % (menu["3,1"]), width = w)
        elif wat == ['3']:
            if Taal == "EN":
                op = menuEN["3"]
                warp = textwrap.wrap("Make changes to an existing mutation, based on a previously generated ID.", width = w)
            elif Taal == "IT":
                op = menuIT["3"]
                warp = textwrap.wrap("Apportare modifiche a una mutazione esistente basata su un ID generato in precedenza.", width = w)
            else:
                op = menu["3"]
                warp = textwrap.wrap("Breng wijzigingen aan in een bestaande mutatie op basis van een eerder gegenereerd ID.", width = w)
        elif wat == ['3','1']:
            if Taal == "EN":
                op = menuEN["3"]+" - "+menuEN["3,1"]
                warp = textwrap.wrap("Change the date of an existing mutation. Enter the date as \"YYYYMMDD\". So today's date is %s. You can customize the date format in the overviews to your personal preference (0,2,9: %s)." % (nu,menuEN["0,2,9"]), width = w)
            elif Taal == "IT":
                op = menuIT["3"]+" - "+menuIT["3,1"]
                warp = textwrap.wrap("Cambia la data di una mutazione esistente. Inserisci la data come \"AAAAMMGG\". Quindi la data di oggi è %s. Puoi personalizzare il formato della data nelle viste secondo le tue preferenze personali (0,2,9: %s)." % (nu,menuIT["0,2,9"]), width = w)
            else:
                op = menu["3"]+" - "+menu["3,1"]
                warp = textwrap.wrap("Wijzig de datum van een bestaande mutatie. Voer de datum in als \"JJJJMMDD\". De datum van vandaag is aldus %s. De datumopmaak in de overzichten kunt u aanpassen naar uw persoonlijke voorkeur (0,2,9: %s)." % (nu,menu["0,2,9"]), width = w)
        elif wat == ['3','2']:
            if Taal == "EN":
                op = menuEN["3"]+" - "+menuEN["3,2"]
                warp = textwrap.wrap("Change the amount of an existing mutation. If you do not fill in anything here, the amount will be 0.00, according to the set currency (0,2,5: %s). Only a plus or minus sign (\"+\" or \"-\") inverts the existing amount." % (menuEN["0,2,5"]), width = w)
            elif Taal == "IT":
                op = menuIT["3"]+" - "+menuIT["3,2"]
                warp = textwrap.wrap("Modifica l'importo di una mutazione esistente. Se non inserisci nulla qui, l'importo sarà 0,00, secondo la valuta impostata (0,2,5: %s). Solo un segno più o meno (\"+\" o \"-\") inverte l'importo esistente." % (menuIT["0,2,5"]), width = w)
            else:
                op = menu["3"]+" - "+menu["3,2"]
                warp = textwrap.wrap("Wijzig het bedrag van een bestaande mutatie. Vult u hier niets in, dan is het bedrag op 0.00, volgens de ingestelde valuta (0,2,5: %s). Alleen een plus- of minteken (\"+\" of \"-\") inverteert het bestaande bedrag." % (menu["0,2,5"]), width = w)
        elif wat == ['3','3']:
            if Taal == "EN":
                op = menuEN["3"]+" - "+menuEN["3,3"]
                warp = textwrap.wrap("Change the name of the creditor or debtor. The maximum length is 15 characters, including spaces and punctuation marks.", width = w)
            elif Taal == "IT":
                op = menuIT["3"]+" - "+menuIT["3,3"]
                warp = textwrap.wrap("Modifica il nome del creditore o debitore. La lunghezza massima è di 15 caratteri, spazi e segni di punteggiatura inclusi.", width = w)
            else:
                op = menu["3"]+" - "+menu["3,3"]
                warp = textwrap.wrap("Wijzig de naam van de crediteur of debiteur. De maximale lengte is 15 karakters, inclusief spaties en leestekens.", width = w)
        elif wat == ['3','4']:
            if Taal == "EN":
                op = menuEN["3"]+" - "+menuEN["3,4"]
                warp = textwrap.wrap("Change the the description. The maximum length is 15 characters, including spaces and punctuation marks.", width = w)
            elif Taal == "IT":
                op = menuIT["3"]+" - "+menuIT["3,4"]
                warp = textwrap.wrap("Modifica la descrizione. La lunghezza massima è di 15 caratteri, spazi e segni di punteggiatura inclusi.", width = w)
            else:
                op = menu["3"]+" - "+menu["3,4"]
                warp = textwrap.wrap("Wijzig de omschrijving. De maximale lengte is 15 karakters, inclusief spaties en leestekens.", width = w)
        elif wat == ['3','5']:
            if Taal == "EN":
                op = menuEN["3"]+" - "+menuEN["3,5"]
                warp = textwrap.wrap("Assign the mutation to a different category. PLEASE NOTE: This will result in a different ID for the mutation!", width = w)
            elif Taal == "IT":
                op = menuIT["3"]+" - "+menuIT["3,5"]
                warp = textwrap.wrap("Assegna la mutazione a un'altra categoria. ATTENZIONE: ciò comporterà un cambio di ID per la mutazione!", width = w)
            else:
                op = menu["3"]+" - "+menu["3,5"]
                warp = textwrap.wrap("Wijs de mutatie aan een andere categorie toe. LET OP: de mutatie krijgt hierdoor een ander ID!", width = w)
        elif wat == ['4']:
            if Taal == "EN":
                op = menuEN["4"]
                warp = textwrap.wrap("Delete a mutation based on a previously generated ID. You must confirm this command again, after which the mutation will be permanently deleted. This action cannot be undone.", width = w)
            elif Taal == "IT":
                op = menuIT["4"]
                warp = textwrap.wrap("Elimina una mutazione in base a un ID generato in precedenza. Dovrai confermare nuovamente questo comando, dopodiché la mutazione verrà definitivamente eliminata. Questa azione non può essere annullata.", width = w)
            else:
                op = menu["4"]
                warp = textwrap.wrap("Verwijder een mutatie op basis van een eerder gegenereerd ID. U moet deze opdracht nogmaals bevestigen, daarna is de mutatie definitief verwijderd. Dit kan niet worden teruggedraaid.", width = w)
        elif wat == ['5']:
            try:
                with open("A","r") as a:
                    A = ast.literal_eval(a.read())
                with open("header","r") as h:
                    H = ast.literal_eval(h.read())
                if Taal == "EN":
                    op = menuEN["5"]
                    warp = textwrap.wrap("You can create savings pots (\"Piggy banks\") on a household account, where a portion of your total balance is reserved for a project of your own choice. A buffer is maintained on the account equal to the budget in category A (currently %s %s). You will receive a notification if you go below that buffer, and then you can no longer add an amount to your savings pot." % (H["Valuta"], int(A[0])*-1), width = w)
                elif Taal == "IT":
                    op = menuIT["5"]
                    warp = textwrap.wrap("Su un conto domestico puoi creare dei salvadanai, in cui una parte del tuo saldo totale viene riservata per un progetto da te scelto. Viene mantenuto un importo di riserva sul conto pari al budget nella categoria A (al momento %s %s). Riceverai un avviso se scendi al di sotto di tale importo e non sarai in grado di aggiungere ulteriori fondi al tuo salvadanaio."% (H["Valuta"], int(A[0])*-1), width = w)
                else:
                    op = menu["5"]
                    warp = textwrap.wrap("U kunt op een huishoudelijke rekening spaarpotten aanmaken, waarin een gedeelte van uw totaalsaldo wordt gereserveerd voor een door u zelf te bepalen project. Er wordt een buffer op de rekening aangehouden ter hoogte van het budget in categorie A (momenteel %s %s). U krijgt een waarschuwing als u onder die buffer komt, en u kunt dan geen bedrag meer aan uw spaarpot toevoegen." % (H["Valuta"], int(A[0])*-1), width = w)
            except:
                pass
        elif wat == ['5','1']:
            if Taal == "EN":
                op = menuEN["5"]+" - "+menuEN["5,1"]
                warp = textwrap.wrap("An overview of your piggy banks, with name and balance.", width = w)
            elif Taal == "IT":
                op = menuIT["5"]+" - "+menuIT["5,1"]
                warp = textwrap.wrap("Un elenco dei tuoi salvadanai, con nome e saldo.", width = w)
            else:
                op = menu["5"]+" - "+menu["5,1"]
                warp = textwrap.wrap("Een overzicht van uw spaarpotten, met naam en saldo.", width = w)
        elif wat == ['5','2']:
            if Taal == "EN":
                op = menuEN["5"]+" - "+menuEN["5,2"]
                warp = textwrap.wrap("Make changes to your piggy bank.", width = w)
            elif Taal == "IT":
                op = menuIT["5"]+" - "+menuIT["5,2"]
                warp = textwrap.wrap("Apporta modifiche al tuo salvadanaio.", width = w)
            else:
                op = menu["5"]+" - "+menu["5,2"]
                warp = textwrap.wrap("Breng veranderingen aan in uw spaarpot.", width = w)
        elif wat == ['5','2','1']:
            if Taal == "EN":
                op = menuEN["5"]+" - "+menuEN["5,2"]+" - "+menuEN["5,2,1"]
                warp = textwrap.wrap("Change the name of your piggy bank.", width = w)
            elif Taal == "IT":
                op = menuIT["5"]+" - "+menuIT["5,2"]+" - "+menuIT["5,2,1"]
                warp = textwrap.wrap("Modifica il nome del tuo salvadanaio.", width = w)
            else:
                op = menu["5"]+" - "+menu["5,2"]+" - "+menu["5,2,1"]
                warp = textwrap.wrap("Verander de naam van uw spaarpot.", width = w)
        elif wat == ['5','2','2']:
            if Taal == "EN":
                op = menuEN["5"]+" - "+menuEN["5,2"]+" - "+menuEN["5,2,2"]
                warp = textwrap.wrap("Change the amount in your piggy bank. If the total amount of all your piggy banks does not provide an adequate buffer (up to the budget in category A), then you cannot add amounts to your piggy banks. However, you can take money out of your piggy banks to replenish your buffer.", width = w)
            elif Taal == "IT":
                op = menuIT["5"]+" - "+menuIT["5,2"]+" - "+menuIT["5,2,2"]
                warp = textwrap.wrap("Modifica l'importo nel tuo salvadanaio. Se la somma di tutti i tuoi salvadanai non fornisce un'adeguata riserva (al livello di bilancio della categoria A), allora non potrai aggiungere fondi ai tuoi salvadanai. Tuttavia, potrai prelevare denaro dai tuoi salvadanai per integrare la tua riserva.", width = w)
            else:
                op = menu["5"]+" - "+menu["5,2"]+" - "+menu["5,2,2"]
                warp = textwrap.wrap("Verander het bedrag in uw spaarpot. Als het bedrag van als uw spaarpotten samen onvoldoende buffer laten (ter hoogte van het budget in categorie A), dan kunt u geen bedragen aan uw spaarpotten toevoegen. U kunt wel geld uit uw spaarpotten wegnemen om uw buffer aan te vullen.", width = w)
        elif wat == ['5','3']:
            if Taal == "EN":
                op = menuEN["5"]+" - "+menuEN["5,3"]
                warp = textwrap.wrap("Create a new piggy bank. If the total amount of all your piggy banks does not provide an adequate buffer (up to the budget in category A), then you cannot add amounts to your piggy banks.", width = w)
            elif Taal == "IT":
                op = menuIT["5"]+" - "+menuIT["5,3"]
                warp = textwrap.wrap("Crea un nuovo salvadanaio. Se la somma di tutti i tuoi salvadanai non fornisce un'adeguata riserva (al livello di bilancio della categoria A), allora non potrai aggiungere fondi ai tuoi salvadanai.", width = w)
            else:
                op = menu["5"]+" - "+menu["5,3"]
                warp = textwrap.wrap("Maak een nieuwe spaarpot. Als het bedrag van als uw spaarpotten samen onvoldoende buffer laten (ter hoogte van het budget in categorie A), dan kunt u geen bedragen aan uw spaarpotten toevoegen.", width = w)
        elif wat == ['5','4']:
            if Taal == "EN":
                op = menuEN["5"]+" - "+menuEN["5,4"]
                warp = textwrap.wrap("The balance in the piggy bank is released again.", width = w)
            elif Taal == "IT":
                op = menuIT["5"]+" - "+menuIT["5,4"]
                warp = textwrap.wrap("Il saldo nel salvadanaio viene nuovamente reso disponibile.", width = w)
            else:
                op = menu["5"]+" - "+menu["5,4"]
                warp = textwrap.wrap("Het saldo in de spaarpot wordt weer vrijgegeven.", width = w)
        print(coltekst+op+ResetAll)
        for i in warp:
            print(i)

if Taal == "EN":
    print("For help type \"H\"")
elif Taal == "IT":
    print("Per aiuto, scrivi \"H\"")
else:
    print("Voor hulp, typ \"H\"")

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
        #print(error)
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

    snelkeuze3 = "Y"
    snelkeuze2 = "Y"
    snelkeuze1 = "Y"
    snelkeuze0 = "Y"
    keuze1 = "Y"
    if Taal == "EN":
        keuze1 = input("Make a choice\n%s  0 Manage account options%s\n%s >1 View mutations%s\n%s  2 Add mutation%s\n%s  3 Modify mutation%s\n%s  4 Remove mutation%s\n%s  5 Piggy banks (only household)%s\n  : " % (LichtMagenta,ResetAll,LichtGeel,ResetAll,LichtGroen,ResetAll,LichtCyaan,ResetAll,LichtRood,ResetAll,col5,ResetAll))
    elif Taal == "IT":
        keuze1 = input("Scegli\n%s  0 Gestire opzioni del conto%s\n%s >1 Vedere mutazioni%s\n%s  2 Aggiungere mutazione%s\n%s  3 Modificare mutazione%s\n%s  4 Cancellare mutazione%s\n%s  5 Salvadanai (solo domestico)%s\n  : " % (LichtMagenta,ResetAll,LichtGeel,ResetAll,LichtGroen,ResetAll,LichtCyaan,ResetAll,LichtRood,ResetAll,col5,ResetAll))
    else:
        keuze1 = input("Maak een keuze\n%s  0 Beheer rekeningopties%s\n%s >1 Mutaties bekijken%s\n%s  2 Mutatie toevoegen%s\n%s  3 Mutatie wijzigen%s\n%s  4 Mutatie verwijderen%s\n%s  5 Spaarpotten (alleen huishoudelijk)%s\n  : " % (LichtMagenta,ResetAll,LichtGeel,ResetAll,LichtGroen,ResetAll,LichtCyaan,ResetAll,LichtRood,ResetAll,col5,ResetAll))
    if keuze1.upper() in afsluitlijst:
        doei()
    elif len(keuze1) == 2 and keuze1.upper()[0] in afsluitlijst and keuze1.upper()[1] in afsluitlijst:
        pass
    elif len(keuze1) == 3 and keuze1.upper()[0] in afsluitlijst and keuze1.upper()[2] in afsluitlijst:
        doei()
    if keuze1.upper() == "H":
        aid()
    if keuze1 == "": # BEKIJKEN
        keuze1 = "1"
    try:
        snelkeuze3 = keuze1[3]
        snelkeuze2 = keuze1[2]
        snelkeuze1 = keuze1[1]
        snelkeuze0 = keuze1[0]
    except:
        try:
            snelkeuze2 = keuze1[2]
            snelkeuze1 = keuze1[1]
            snelkeuze0 = keuze1[0]
        except:
            try:
                snelkeuze1 = keuze1[1]
                snelkeuze0 = keuze1[0]
            except(Exception) as error:
                snelkeuze0 = keuze1[0]
                #print(error)
    if snelkeuze0 == "1" or snelkeuze0.upper() in ["M"," "]: # BEKIJKEN
        print()
        bekijken = "Y"
        while bekijken == "Y":
            budgetcheck = "N"
            dagsaldo = "N"
            col1 = LichtGeel
            if snelkeuze0.upper() in ["M"," "]:
                keuze2 = "1"
            else:
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
                            einddatum = 99991231
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
                    if snelkeuze0.upper() in ["M"," "]:
                        maanden = "0"
                    else:
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

                if snelkeuze0.upper() in ["M"," "]:
                    keuze3 = ""
                else:
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
                if keuze1.upper() in ["M","MIMO","MOMI"]:
                    keuze4 = ""
                elif keuze1.upper() in ["MI","MO"]:
                    keuze4 = "1"
                elif keuze1.upper() == " ":
                    keuze4 = "2"
                else:
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
                    if Taal == "EN":
                        sel3 = "amount"
                    elif Taal == "IT":
                        sel3 = "somma"
                    else:
                        sel3 = "bedrag"
                    bedrag = "N"
                    while bedrag == "N":
                        if keuze1.upper() == "MI":
                            if Taal == "EN":
                                sel3 = ", Only \"Money In\""
                            elif Taal == "IT":
                                sel3 = ", Solo \"Money In\""
                            else:
                                sel3 = ", Alleen \"Money In\""
                            bedragv = "0 99999.99"
                        elif keuze1.upper() == "MO":
                            if Taal == "EN":
                                sel3 = ", Only \"Money Out\""
                            elif Taal == "IT":
                                sel3 = ", Solo \"Money Out\""
                            else:
                                sel3 = ", Alleen \"Money Out\""
                            bedragv = "-99999.99 0"
                        else:
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
                            bedrag = "Y"
                        else:
                            bedragv = " ".join(bedragv.split())
                            bereik = bedragv.split(" ")
                            if len(bereik) == 1:
                                try:
                                    bedragv1 = float(bereik[0])
                                    bedragv2 = bedragv1
                                    bedrag = "Y"
                                except(Exception) as error:
                                    #print(error)
                                    pass
                            else:
                                try:
                                    bedragv1 = float(bereik[0])
                                    bedragv2 = float(bereik[1])
                                    bedrag = "Y"
                                except(Exception) as error:
                                    #print(error)
                                    bedragv1 = -99999.99
                                    bedragv2 = 99999.99
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
                    if keuze1.upper() in ["MI","MO"]:
                        kop = sel3
                    ID = 0
                    for i in seldat:
                        if bedragv1 <= i[1] <= bedragv2:
                            vier = i[4]+str(ID)
                            i.remove(i[4])
                            i.append(vier)
                            sel.append(i)
                            ID += 1
                elif keuze4 == "2":
                    if Taal == "EN":
                        sel3 = "other party"
                    elif Taal == "IT":
                        sel3 = "controparte"
                    else:
                        sel3 = "wederpartij"
                    wederpartij = "N"
                    while wederpartij == "N":
                        if keuze1.upper() == " ":
                            sel3 = ""
                            if Taal == "EN":
                                wederpartijv = "No transactions, only totals"
                            elif Taal == "IT":
                                wederpartijv = "Nessuna transazione, solo totali"
                            else:
                                wederpartijv = "Geen transacties, alleen totalen"
                        else:
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
                    if Taal == "EN":
                        sel3 = "note"
                    if Taal == "IT":
                        sel3 = "annotazione"
                    else:
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
                        kop = ", Everything"
                    elif Taal == "IT":
                        kop = ", Tutto"
                    else:
                        kop = ", Alles"
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
                        if startdatum == 11111111 and einddatum == 99991231:
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
                            if i[1] <= -10000 or i[1] >= 10000:
                                print("|",for8(str(yymd)),"|",Valuta,forr8("± "+str(round(i[1]/1000))+"~K"),"|",for15(i[2]),"|",for18(i[3]),"|",for3(i[4]),"|", file = p)
                            else:
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
                                    if int(round(mndtot/budtot*100,0)) >= -100:
                                        print(forc5(int(round(mndtot/budtot*100,0)))+"% |"+forr25("-"*int(round(mndtot/budtot*-25,0)))+"|"+" "*25+"|", file = p)
                                    else:
                                        print(forc5(int(round(mndtot/budtot*100,0)))+"% |"+forr25("="*25)+"|"+" "*25+"|", file = p)
                                elif mndtot > 0:
                                    if int(round(mndtot/budtot*100,0)) <= 100:
                                        print(forc5(" ")+"|"+" "*25+"|"+forl25("+"*int(round(mndtot/budtot*25,0)))+"|"+forc5(int(round(mndtot/budtot*100,0)))+"%", file = p)
                                    else:
                                        print(forc5(" ")+"|"+" "*25+"|"+forl25("#"*25)+"|"+forc5(int(round(mndtot/budtot*100,0)))+"%", file = p)
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
                if startdatum == 11111111 and einddatum == 99991231:
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
                    if i[1] <= -10000 or i[1] >= 10000 and len(str(i[4])) <= 3:
                        print("|",for8(str(yymd)),"|",colc+Valuta+ResetAll,colc+forr8("± "+str(round(i[1]/1000))+"~K")+ResetAll,"|",for15(i[2]),"|",for18(i[3]),"|",col+for3(i[4])+ResetAll,"|")
                    elif i[1] <= -10000 or i[1] >= 10000 and len(str(i[4])) > 3:
                        print("|",for8(str(yymd)),"|",colc+Valuta+ResetAll,colc+forr8("± "+str(round(i[1]/1000))+"~K")+ResetAll,"|",for15(i[2]),"|",for18(i[3]),"|"+col+for3(i[4])+ResetAll,"|")
                    elif len(str(i[4])) > 3:
                        print("|",for8(str(yymd)),"|",colc+Valuta+ResetAll,fornum(i[1]),"|",for15(i[2]),"|",for18(i[3]),"|"+col+for3(i[4])+ResetAll,"|")
                    else:
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
                                try:
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
                                except(Exception) as error:
                                    pass
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

    elif snelkeuze0 == "2": # TOEVOEGEN
        print()
        col2 = LichtGroen
        if snelkeuze1 != "Y":
            keuze2 = snelkeuze1
            snelkeuze1 = "Y"
        else:
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
                                alternatievenaam= alternatievenaam.replace("vaste act/pass.","fixd ass/equity").replace("vlotte act/pass","cash (equiv.)").replace("tussenrekening","intermediary").replace("voorraden","inventory").replace("kostenplaatsen","cost centers").replace("kosten","expenses").replace("fabricagerek.","manufact.acc.").replace("inkoopwaarde","cost of goods").replace("omzet","sales").replace("privé","private").replace("saldo & inkomen","funds & income").replace("vaste lasten","fixed costs").replace("boodschappen","groceries").replace("reis & verblijf","travel & stay").replace("leningen","loans").replace("overig","other")
                                print("%s %s%d%s\n%s %s%s %s%s\n%s %s%s%s\n%s %s%s%s\n%s %s%s%s" % (for15("Date: "),col2,i[0],ResetAll,for15("Amount: "),col2,Valuta,forn(i[1]),ResetAll,for15("Other party: "),col2,i[2],ResetAll,for15("About: "),col2,i[3],ResetAll,for15("Category: "),col,alternatievenaam,ResetAll))
                            elif Taal == "IT":
                                alternatievenaam = alternatievenaam.replace("vaste act/pass.","attiv. fisse").replace("vlotte act/pass","dispon. liquide").replace("tussenrekening","conti intermedi").replace("voorraden","magazzino").replace("kostenplaatsen","centri di costo").replace("kosten","costi").replace("fabricagerek.","contiproduzione").replace("inkoopwaarde","costi vendute").replace("omzet","ricavi").replace("privé","privato").replace("saldo & inkomen","saldo & reddito").replace("vaste lasten","costi fissi").replace("boodschappen","spese").replace("reis & verblijf","viaggioalloggio").replace("leningen","prestiti").replace("overig","altro")
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
                                alternatievenaam= alternatievenaam.replace("vaste act/pass.","fixd ass/equity").replace("vlotte act/pass","cash (equiv.)").replace("tussenrekening","intermediary").replace("voorraden","inventory").replace("kostenplaatsen","cost centers").replace("kosten","expenses").replace("fabricagerek.","manufact.acc.").replace("inkoopwaarde","cost of goods").replace("omzet","sales").replace("privé","private").replace("saldo & inkomen","funds & income").replace("vaste lasten","fixed costs").replace("boodschappen","groceries").replace("reis & verblijf","travel & stay").replace("leningen","loans").replace("overig","other")
                                print("%s %s%d%s\n%s %s%s %s%s\n%s %s%s%s\n%s %s%s%s\n%s %s%s%s" % (for15("Date: "),col2,i[0],ResetAll,for15("Amount: "),col2,Valuta,forn(i[1]),ResetAll,for15("Other party: "),col2,i[2],ResetAll,for15("About: "),col2,i[3],ResetAll,for15("Category: "),col,alternatievenaam,ResetAll))
                            elif Taal == "IT":
                                alternatievenaam = alternatievenaam.replace("vaste act/pass.","attiv. fisse").replace("vlotte act/pass","dispon. liquide").replace("tussenrekening","conti intermedi").replace("voorraden","magazzino").replace("kostenplaatsen","centri di costo").replace("kosten","costi").replace("fabricagerek.","contiproduzione").replace("inkoopwaarde","costi vendute").replace("omzet","ricavi").replace("privé","privato").replace("saldo & inkomen","saldo & reddito").replace("vaste lasten","costi fissi").replace("boodschappen","spese").replace("reis & verblijf","viaggioalloggio").replace("leningen","prestiti").replace("overig","altro")
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
                        if Taal == "EN":
                            alternatievenaam= alternatievenaam.replace("vaste act/pass.","fixd ass/equity").replace("vlotte act/pass","cash (equiv.)").replace("tussenrekening","intermediary").replace("voorraden","inventory").replace("kostenplaatsen","cost centers").replace("kosten","expenses").replace("fabricagerek.","manufact.acc.").replace("inkoopwaarde","cost of goods").replace("omzet","sales").replace("privé","private").replace("saldo & inkomen","funds & income").replace("vaste lasten","fixed costs").replace("boodschappen","groceries").replace("reis & verblijf","travel & stay").replace("leningen","loans").replace("overig","other")
                        elif Taal == "IT":
                            alternatievenaam = alternatievenaam.replace("vaste act/pass.","attiv. fisse").replace("vlotte act/pass","dispon. liquide").replace("tussenrekening","conti intermedi").replace("voorraden","magazzino").replace("kostenplaatsen","centri di costo").replace("kosten","costi").replace("fabricagerek.","contiproduzione").replace("inkoopwaarde","costi vendute").replace("omzet","ricavi").replace("privé","privato").replace("saldo & inkomen","saldo & reddito").replace("vaste lasten","costi fissi").replace("boodschappen","spese").replace("reis & verblijf","viaggioalloggio").replace("leningen","prestiti").replace("overig","altro")
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
                pass
        print()
        print(toplijn)
        print()
    elif snelkeuze0 == "3": # WIJZIGEN
        print()
        col3 = LichtCyaan
        try:
            int(sel[0][0])
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
                            if snelkeuze1 != "Y":
                                wat = snelkeuze1
                                snelkeuze1 = "Y"
                            else:
                                if Taal == "EN":
                                    alternatievenaam= alternatievenaam.replace("vaste act/pass.","fixd ass/equity").replace("vlotte act/pass","cash (equiv.)").replace("tussenrekening","intermediary").replace("voorraden","inventory").replace("kostenplaatsen","cost centers").replace("kosten","expenses").replace("fabricagerek.","manufact.acc.").replace("inkoopwaarde","cost of goods").replace("omzet","sales").replace("privé","private").replace("saldo & inkomen","funds & income").replace("vaste lasten","fixed costs").replace("boodschappen","groceries").replace("reis & verblijf","travel & stay").replace("leningen","loans").replace("overig","other")
                                    wat = input("What do you want to %schange%s\n  %s1%s %s %s\n  %s2%s %s %s %s\n  %s3%s %s %s\n  %s4%s %s %s\n  %s5%s %s %s%s%s\n  : " % (col3,ResetAll,col3,ResetAll,for15("Date: "),i[0],col3,ResetAll,for15("Amount: "),Valuta,i[1],col3,ResetAll,for15("Other party: "),i[2],col3,ResetAll,for15("About: "),i[3],col3,ResetAll,for15("Category: "),col,alternatievenaam,ResetAll))
                                elif Taal == "IT":
                                    alternatievenaam = alternatievenaam.replace("vaste act/pass.","attiv. fisse").replace("vlotte act/pass","dispon. liquide").replace("tussenrekening","conti intermedi").replace("voorraden","magazzino").replace("kostenplaatsen","centri di costo").replace("kosten","costi").replace("fabricagerek.","contiproduzione").replace("inkoopwaarde","costi vendute").replace("omzet","ricavi").replace("privé","privato").replace("saldo & inkomen","saldo & reddito").replace("vaste lasten","costi fissi").replace("boodschappen","spese").replace("reis & verblijf","viaggioalloggio").replace("leningen","prestiti").replace("overig","altro")
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
                                                alternatievenaam= alternatievenaam.replace("vaste act/pass.","fixd ass/equity").replace("vlotte act/pass","cash (equiv.)").replace("tussenrekening","intermediary").replace("voorraden","inventory").replace("kostenplaatsen","cost centers").replace("kosten","expenses").replace("fabricagerek.","manufact.acc.").replace("inkoopwaarde","cost of goods").replace("omzet","sales").replace("privé","private").replace("saldo & inkomen","funds & income").replace("vaste lasten","fixed costs").replace("boodschappen","groceries").replace("reis & verblijf","travel & stay").replace("leningen","loans").replace("overig","other")
                                                print("%s %s%d%s\n%s %s%s %s%s\n%s %s%s%s\n%s %s%s%s\n%s %s%s%s" % (for15("Date: "),col3,i[0],ResetAll,for15("Amount: "),col3,Valuta,forn(i[1]),ResetAll,for15("Other party: "),col3,i[2],ResetAll,for15("About: "),col3,i[3],ResetAll,for15("Category: "),col,alternatievenaam,ResetAll))
                                            elif Taal == "IT":
                                                alternatievenaam = alternatievenaam.replace("vaste act/pass.","attiv. fisse").replace("vlotte act/pass","dispon. liquide").replace("tussenrekening","conti intermedi").replace("voorraden","magazzino").replace("kostenplaatsen","centri di costo").replace("kosten","costi").replace("fabricagerek.","contiproduzione").replace("inkoopwaarde","costi vendute").replace("omzet","ricavi").replace("privé","privato").replace("saldo & inkomen","saldo & reddito").replace("vaste lasten","costi fissi").replace("boodschappen","spese").replace("reis & verblijf","viaggioalloggio").replace("leningen","prestiti").replace("overig","altro")
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
            #print(error)
            pass
        print()
        print(toplijn)
        print()
    elif snelkeuze0 == "4": # VERWIJDEREN
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
                                    alternatievenaam= alternatievenaam.replace("vaste act/pass.","fixd ass/equity").replace("vlotte act/pass","cash (equiv.)").replace("tussenrekening","intermediary").replace("voorraden","inventory").replace("kostenplaatsen","cost centers").replace("kosten","expenses").replace("fabricagerek.","manufact.acc.").replace("inkoopwaarde","cost of goods").replace("omzet","sales").replace("privé","private").replace("saldo & inkomen","funds & income").replace("vaste lasten","fixed costs").replace("boodschappen","groceries").replace("reis & verblijf","travel & stay").replace("leningen","loans").replace("overig","other")
                                    wat = input("  %s %s\n  %s %s %s\n  %s %s\n  %s %s\n  %s %s\nConfirm\n  : %s" % (for15("Date: "),col4+str(i[0])+ResetAll,for15("Amount: "),col4+Valuta,str(i[1])+ResetAll,for15("Other party: "),col4+i[2]+ResetAll,for15("About: "),col4+i[3]+ResetAll,for15("Category: "),col4+alternatievenaam,ResetAll))
                                elif Taal == "IT":
                                    alternatievenaam = alternatievenaam.replace("vaste act/pass.","attiv. fisse").replace("vlotte act/pass","dispon. liquide").replace("tussenrekening","conti intermedi").replace("voorraden","magazzino").replace("kostenplaatsen","centri di costo").replace("kosten","costi").replace("fabricagerek.","contiproduzione").replace("inkoopwaarde","costi vendute").replace("omzet","ricavi").replace("privé","privato").replace("saldo & inkomen","saldo & reddito").replace("vaste lasten","costi fissi").replace("boodschappen","spese").replace("reis & verblijf","viaggioalloggio").replace("leningen","prestiti").replace("overig","altro")
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

    elif snelkeuze0 == "5": # SPAARPOTTEN
        try:
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
                            print("    A buffer of %s on payday is recommended" % (col5+Valuta+fornum(Uitgaven*-1)+ResetAll))
                        elif Taal == "IT":
                            print("    Totale in salvadanai: %s" % (col5+Valuta+fornum(spaartotaal)+ResetAll))
                            print("    %s è riservato per spese mensili" % (col5+Valuta+fornum(Uitgaven*-1)+ResetAll))
                            print("    Rimane %s nonsalvadanato" % (col5+Valuta+fornum(moni-spaartotaal+Uitgaven)+ResetAll))
                            print("    Un buffer di %s su giorno di paga è raccomandato" % (col5+Valuta+fornum(Uitgaven*-1)+ResetAll))
                        else:
                            print("    Totaal in spaarpotten: %s" % (col5+Valuta+fornum(spaartotaal)+ResetAll))
                            print("    %s is gereserveerd voor maandelijkse uitgaven" % (col5+Valuta+fornum(Uitgaven*-1)+ResetAll))
                            print("    Er blijft %s ongespaarpot over" % (col5+Valuta+fornum(moni-spaartotaal+Uitgaven)+ResetAll))
                            print("    Een buffer van %s op betaaldag wordt aanbevolen" % (col5+Valuta+fornum(Uitgaven*-1)+ResetAll))
                        print()
                except(Exception) as error:
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
                if snelkeuze1 != "Y":
                    keuze2 = snelkeuze1
                    snelkeuze1 = "Y"
                else:
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
                                                    if nieuwevalue > beschikbaar and nieuwevalue != 0:
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
                            print()
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
                                break
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
        except:
            pass

    elif snelkeuze0 == "0": # BEHEER
        print()
        col5 = LichtMagenta
        beheer = "Y"
        while beheer == "Y":
            if snelkeuze1 != "Y":
                try:
                    wat = snelkeuze2
                    keuze2 = snelkeuze1
                    keuze1 = keuze1[:1]
                    snelkeuze1 = "Y"
                    tweedekeus = True
                except:
                    keuze2 = snelkeuze1
                    snelkeuze1 = "Y"
                    tweedekeus = False
            else:
                tweedekeus = False
                if Taal == "EN":
                    keuze2 = input("Make a choice\n  0 %sPrint version and info%s\n >1 %sCategory management%s\n  2 %sModify account settings%s\n  3 %sShow or hide account%s\n  4 %sSwitch account%s (!)\n  5 %sAdd new account%s\n  6 %sDelete account%s\n  7 %sTransfer account settings%s\n  : " % (LichtGeel,ResetAll,LichtCyaan,ResetAll,Blauw,ResetAll,Geel,ResetAll,LichtMagenta,ResetAll,LichtGroen,ResetAll,LichtRood,ResetAll,Magenta,ResetAll))
                elif Taal == "IT":
                    keuze2 = input("Fai una scelta\n  0 %sPrint versione ed info%s\n >1 %sGestire categorie%s\n  2 %sModificare impostazioni del conto%s\n  3 %sEsporre o nascondere conto%s\n  4 %sPassare ad un\'altro conto%s (!)\n  5 %sAggiungere un nuovo conto%s\n  6 %sEliminare un conto%s\n  7 %sTrasferire impostazioni%s\n  : " % (LichtGeel,ResetAll,LichtCyaan,ResetAll,Blauw,ResetAll,Geel,ResetAll,LichtMagenta,ResetAll,LichtGroen,ResetAll,LichtRood,ResetAll,Magenta,ResetAll))
                else:
                    keuze2 = input("Maak een keuze\n  0 %sPrint versie en info%s\n >1 %sCategoriebeheer%s\n  2 %sRekeninginstellingen aanpassen%s\n  3 %sToon of verberg rekening%s\n  4 %sWissel van rekening%s (!)\n  5 %sNieuwe rekening toevoegen%s\n  6 %sVerwijder rekening%s\n  7 %sInstellingen overzetten%s\n  : " % (LichtGeel,ResetAll,LichtCyaan,ResetAll,Blauw,ResetAll,Geel,ResetAll,LichtMagenta,ResetAll,LichtGroen,ResetAll,LichtRood,ResetAll,Magenta,ResetAll))
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
                    Toon = header["Toon"]
                    CSV = header["CSV"]
                    if Taal == "EN":
                        Nulregels = Nulregels.replace("Ja","Yes").replace("Nee","No")
                        Print = Print.replace("Ja","Yes").replace("Nee","No")
                        Toon = Toon.replace("Ja","Yes").replace("Nee","No")
                        Kleur = Kleur.replace("Alle","All").replace("Categorie","Category").replace("Mono","Mono").replace("Regenboog","Rainbow")
                    elif Taal == "IT":
                        Nulregels = Nulregels.replace("Ja","Sì").replace("Nee","No")
                        Print = Print.replace("Ja","Sì").replace("Nee","No")
                        Toon = Toon.replace("Ja","Sì").replace("Nee","No")
                        Kleur = Kleur.replace("Alle","Tutti").replace("Categorie","Categoria").replace("Mono","Mono").replace("Regenboog","Arcobaleno")
                    if tweedekeus == False:
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
                            wat = input("Choose what you want to %smodify%s\n  1 %s\n  2 %s\n  3 %s\n  4 %s\n  5 %s\n  6 %s\n  7 %s\n  8 %s\n  9 %s\n 10 %s\n 11 %s\n 12 %s\n  : " % (Blauw,ResetAll,colslecht+for15("Description")+ResetAll+colgoed+for15(hoe)+ResetAll, colslecht+for15("Account holder")+ResetAll+colgoed+for15(wie)+ResetAll, colslecht+for15("City")+ResetAll+colgoed+for15(waar)+ResetAll, colslecht+for15("Language")+ResetAll+colgoed+for15(Taal)+ResetAll, colslecht+for15("Currency")+ResetAll+colgoed+for15(Valuta)+ResetAll, colslecht+for15("Zero lines")+ResetAll+colgoed+for15(Nulregels)+ResetAll, colslecht+for15("Marking L><U")+ResetAll+colgoed+Valuta+fornum(MarkeringLH[0])+ResetAll+" >< "+colgoed+Valuta+fornum(MarkeringLH[1])+ResetAll, colslecht+for15("Colour")+ResetAll+colgoed+for15(Kleur)+ResetAll, colslecht+for15("Date formatting")+ResetAll+colgoed+for15(Datumformaat)+for15(yymd)+ResetAll, colslecht+for15("Print to file")+ResetAll+colgoed+for15(Print)+ResetAll, colslecht+for15("Show total")+ResetAll+colgoed+for15(Toon)+ResetAll, colslecht+for15("Export CSV")+ResetAll+colgoed+for15(CSV)+ResetAll))
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
                            wat = input("Scegli cosa vuoi %smodificare%s\n  1 %s\n  2 %s\n  3 %s\n  4 %s\n  5 %s\n  6 %s\n  7 %s\n  8 %s\n  9 %s\n 10 %s\n 11 %s\n 12 %s\n  : " % (Blauw,ResetAll,colslecht+for15("Descrizione")+ResetAll+colgoed+for15(hoe)+ResetAll, colslecht+for15("Intestatario")+ResetAll+colgoed+for15(wie)+ResetAll, colslecht+for15("Città")+ResetAll+colgoed+for15(waar)+ResetAll, colslecht+for15("Lingua")+ResetAll+colgoed+for15(Taal)+ResetAll, colslecht+for15("Valuta")+ResetAll+colgoed+for15(Valuta)+ResetAll, colslecht+for15("Linee a zero")+ResetAll+colgoed+for15(Nulregels)+ResetAll, colslecht+for15("Indicaz. I><S")+ResetAll+colgoed+Valuta+fornum(MarkeringLH[0])+ResetAll+" >< "+colgoed+Valuta+fornum(MarkeringLH[1])+ResetAll, colslecht+for15("Colore")+ResetAll+colgoed+for15(Kleur)+ResetAll, colslecht+for15("Formato data")+ResetAll+colgoed+for15(Datumformaat)+for15(yymd)+ResetAll, colslecht+for15("Stampa file")+ResetAll+colgoed+for15(Print)+ResetAll, colslecht+for15("Mostra totale")+ResetAll+colgoed+for15(Toon)+ResetAll, colslecht+for15("Esporta CSV")+ResetAll+colgoed+for15(CSV)+ResetAll))
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
                            wat = input("Kies wat je wilt %saanpassen%s\n  1 %s\n  2 %s\n  3 %s\n  4 %s\n  5 %s\n  6 %s\n  7 %s\n  8 %s\n  9 %s\n 10 %s\n 11 %s\n 12 %s\n  : " % (Blauw,ResetAll,colslecht+for15("Beschrijving")+ResetAll+colgoed+for15(hoe)+ResetAll, colslecht+for15("Rekeninghouder")+ResetAll+colgoed+for15(wie)+ResetAll, colslecht+for15("Plaats")+ResetAll+colgoed+for15(waar)+ResetAll, colslecht+for15("Taal")+ResetAll+colgoed+for15(Taal)+ResetAll, colslecht+for15("Valuta")+ResetAll+colgoed+for15(Valuta)+ResetAll, colslecht+for15("Nulregels")+ResetAll+colgoed+for15(Nulregels)+ResetAll, colslecht+for15("Markering L><H")+ResetAll+colgoed+Valuta+fornum(MarkeringLH[0])+ResetAll+" >< "+colgoed+Valuta+fornum(MarkeringLH[1])+ResetAll, colslecht+for15("Kleur")+ResetAll+colgoed+for15(Kleur)+ResetAll, colslecht+for15("Datumformaat")+ResetAll+colgoed+for15(Datumformaat)+for15(yymd)+ResetAll, colslecht+for15("Print naar file")+ResetAll+colgoed+for15(Print)+ResetAll, colslecht+for15("Toon totaal")+ResetAll+colgoed+for15(Toon)+ResetAll, colslecht+for15("Exporteer CSV")+ResetAll+colgoed+for15(CSV)+ResetAll))
                    else:
                        tweedekeus = False
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
                            nuljanee = input("Linee a zero\n  S Sì\n >N No\n  : %s" % (colgoed))
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
                            printjanee = input("Stampa riepilogo mensile in file\n  S Sì\n >N No\n  : %s" % (colgoed))
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
                    elif wat.upper() == "11":
                        if Taal == "EN":
                            printjanee = input("Show total amount on start screen\n >Y Yes\n  N No\n  : %s" % (colgoed))
                        elif Taal == "IT":
                            printjanee = input("Mostra totale sullo schermo iniziale\n >S Sì\n  N No\n  : %s" % (colgoed))
                        else:
                            printjanee = input("Toon totaalsaldo op startscherm\n >J Ja\n  N Nee\n  : %s" % (colgoed))
                        print(ResetAll, end = "")
                        if printjanee.upper() in afsluitlijst:
                            break
                        elif len(printjanee) == 2 and printjanee.upper()[0] in afsluitlijst and printjanee.upper()[1] in afsluitlijst:
                            headerloop = "Q"
                            break
                        elif len(printjanee) == 3 and printjanee.upper()[0] in afsluitlijst and printjanee.upper()[2] in afsluitlijst:
                            doei()
                        elif printjanee.upper() in neelijst:
                            header["Toon"] = "Nee"
                        else:
                            header["Toon"] = "Ja"
                    elif wat == "12":
                        if Taal == "EN":
                            printjanee = input("Export all to csv file\n  Y Yes\n >N No\n  : %s" % (colgoed))
                        elif Taal == "IT":
                            printjanee = input("Esporta tutto in file csv\n  S Sì\n >N No\n  : %s" % (colgoed))
                        else:
                            printjanee = input("Exporteer alles naar csv-bestand\n  J Ja\n >N Nee\n  : %s" % (colgoed))
                        print(ResetAll, end = "")
                        if printjanee.upper() in afsluitlijst:
                            break
                        elif len(printjanee) == 2 and printjanee.upper()[0] in afsluitlijst and printjanee.upper()[1] in afsluitlijst:
                            headerloop = "Q"
                            break
                        elif len(printjanee) == 3 and printjanee.upper()[0] in afsluitlijst and printjanee.upper()[2] in afsluitlijst:
                            doei()
                        elif printjanee.upper() in jalijst:
                            header["CSV"] = "Ja"
                        else:
                            header["CSV"] = "Nee"
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
                                    kategorienaam = alternatievenamenlijst[kategorie.upper()].replace("vaste act/pass.","fixd ass/equity").replace("vlotte act/pass","cash (equiv.)").replace("tussenrekening","intermediary").replace("voorraden","inventory").replace("kostenplaatsen","cost centers").replace("kosten","expenses").replace("fabricagerek.","manufact.acc.").replace("inkoopwaarde","cost of goods").replace("omzet","sales").replace("privé","private").replace("saldo & inkomen","funds & income").replace("vaste lasten","fixed costs").replace("boodschappen","groceries").replace("reis & verblijf","travel & stay").replace("leningen","loans").replace("overig","other")
                                    wat = input("Choose\n  1 Modify %scategory name%s (now %s)\n  2 Modify %smonth budget%s (now %s)\n  3 %sRemove category%s %s %sand everything in it%s\n  : " % (LichtCyaan,ResetAll,col+kategorienaam+ResetAll,LichtCyaan,ResetAll,col+Valuta+fornum(budget)+ResetAll,colslecht,ResetAll,col+kategorienaam+ResetAll,colslecht, ResetAll))
                                elif Taal == "IT":
                                    kategorienaam = alternatievenamenlijst[kategorie.upper()].replace("vaste act/pass.","attiv. fisse").replace("vlotte act/pass","dispon. liquide").replace("tussenrekening","conti intermedi").replace("voorraden","magazzino").replace("kostenplaatsen","centri di costo").replace("kosten","costi").replace("fabricagerek.","contiproduzione").replace("inkoopwaarde","costi vendute").replace("omzet","ricavi").replace("privé","privato").replace("saldo & inkomen","saldo & reddito").replace("vaste lasten","costi fissi").replace("boodschappen","spese").replace("reis & verblijf","viaggioalloggio").replace("leningen","prestiti").replace("overig","altro")
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
                                        try:
                                            with open(k,"r") as f:
                                                cat = ast.literal_eval(f.read())
                                                budlijst.append(cat[0])
                                                print(k,forc17(v),Valuta,fornum(cat[0]))
                                        except(Exception) as f:
                                            #print(f)
                                            pass
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
