"""
Auteur      :Martin
Date        :17.11.2023
Version     :1.0
Description :partie graphique de loutil de management des scors dans le cadre du MA dbpy
"""

# modules
from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk
import datetime
import database as data

# constants
# définnition des langues
listLangs = {"fr":{"dark":"sombre", "white":"claire", "data":"données", "settings":"paramètres", "reset":"réinitialiser", "english":"anglais", "french":"français", "theme":"thème", "text":"text", "language":"langue", "ID":"ID", "Pseudo":"Pseudo", "Game":"Jeux", "nb_ok":"nb_ok", "nb_total":"nb_total", "start date":"heure de commencement", "start time":"heure de départ", "Are you sure you want to erase the results?":"êtes vous sûre de vouloir éfacer les résultats ?", "normal":"normal", "ratio":"ratio"}}
# définition des thèmes
listThemes = {"dark":{"bg":"#222222", "bg2":"#114411", "btn":"#003300", "fg":"#ffffff", "actbtn":"#006600", "actfg":"#ffffff", "fgbtn":"#ffffff", "bgTable":"#151515"},
              "white":{"bg":"#ffffff", "bg2":"#00cc00", "btn":"##00aa00", "fg":"#000000", "actbtn":"#44cc44", "actfg":"#ffffff", "fgbtn":"#ffffff", "bgTable":"#ffffff"},
              "normal":{"bg":"#8bc9c2", "bg2":"#ffffff", "btn":"#ffffff", "fg":"#000000", "actbtn":"#44cc44", "actfg":"#ffffff", "fgbtn":"#ffffff", "bgTable":"#ffffff"}}

themeName = "dark"
lang = "fr"
theme = []

def Error(text = "no text"):
    return "\033[91m" + text + "\033[0m"

# fonction d'application de la configuration
def AplyConf():
    print("reading the settings ...")
    global themeName, lang
    conf = open(file="config", mode="r+")
    lang = conf.readline()[0:-1]
    themeName = conf.readline()[0:-1]
    conf.close()

# fonction de définition de la langue
def Lang(text = "no text"):
    if lang == "en":
        return text
    else:
        try:
            return listLangs[lang][text]
        except:
            print(Error("error in the translate of " + str(text)))
            return text

# variables

# functions

def Load():
    print("reload ...")
    global theme
    AplyConf()
    theme = listThemes[themeName]
    Display()

def SetConf(parameter, value):
    global lang, themeName
    if parameter == "theme":
        themeName = value
        print("set theme: " + value)
    elif parameter == "lang":
        lang = value
        print("set lang: " + value)
    conf = open(file="config", mode="w+")
    conf.write(lang + "\n" + themeName + "\n")
    conf.close()
    Load()

# fonction de réinitialisation de la table
def Reset():
    if messagebox.askquestion(Lang("Are you sure you want to erase the results?")):
        data.delete()
        Load()

# graphical
window = Tk()
def Display():
    global window
    print("open the window ...")
    try:
        for i in window.winfo_children():
            i.destroy()
    except:
        pass
    window.geometry(str(window.winfo_screenwidth()) + "x" + str(window.winfo_screenheight()))
    window.configure(bg=theme["bg"])

    # menu
    menu = Menu(window)
    menu1 = Menu(menu)
    menu1.add_command(label=Lang("reset"), command=Reset)
    menu.add_cascade(label=Lang("data"), menu=menu1)

    menuTheme = Menu(menu)
    menuTheme.add_command(label=Lang("dark"), command=lambda: SetConf("theme", "dark"))
    menuTheme.add_command(label=Lang("white"), command=lambda: SetConf("theme", "white"))
    menuTheme.add_command(label=Lang("normal"), command=lambda: SetConf("theme", "normal"))
    menu.add_cascade(label=Lang("theme"), menu=menuTheme)

    menuLang = Menu(menu)
    menuLang.add_command(label=Lang("french"), command=lambda: SetConf("lang", "fr"))
    menuLang.add_command(label=Lang("english"), command=lambda: SetConf("lang", "en"))
    menu.add_cascade(menu=menuLang, label=Lang("language"))

    # table
    TGCanvas = Canvas(window, width=1600, bg=theme["bg"])
    TGCanvas.pack(side=LEFT, fill=Y)

    def on_configure(event):
        TGCanvas.configure(scrollregion=TGCanvas.bbox('all'))

    scrollbar = Scrollbar(window, command=TGCanvas.yview)
    scrollbar.pack(side=LEFT, fill=Y)
    TGCanvas.configure(yscrollcommand=scrollbar.set)
    TGCanvas.bind('<Configure>', on_configure)

    frameTable = Frame(TGCanvas, bg=theme["bg2"])
    count = 0
    listWidth = [7, 20, 30, 20, 20, 35, 35]
    for Text in [Lang("ID"), Lang("Pseudo"), Lang("Game"), Lang("nb_total"), Lang("nb_ok"), Lang("start date"), Lang("start time")]:
        Button(frameTable, text=Text, borderwidth=1, bg=theme["bg2"], width=listWidth[count], fg=theme["fg"]).grid(row=0,column=count)
        count += 1
    logicTable = data.GetTable("parties")
    for line in range(len(logicTable)):
        for column in range(7):
            Button(frameTable, text=str(logicTable[line][column]), width=listWidth[column], borderwidth=1, bg=theme["bgTable"],
                   fg=theme["fg"]).grid(row=line + 1, column=column)
        ttk.Progressbar(frameTable, orient=HORIZONTAL, length=100, mode='indeterminate').grid(row=line + 1, column=8)
    frameTable.pack(side=LEFT)
    TGCanvas.create_window((0, 0), window=frameTable)

    window.config(menu=menu)

Load()
window.mainloop()
