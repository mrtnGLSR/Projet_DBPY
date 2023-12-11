"""
Auteur      :Martin
Date        :17.11.2023
Version     :1.0
Description :partie graphique de loutil de management des scors dans le cadre du MA dbpy
"""

# modules
from tkinter import *
from tkinter import messagebox
import datetime
import database as data

# constants
# définnition des langues
listLangs = {"fr":{"dark":"sombre", "white":"claire", "data":"données", "settings":"paramètres", "reset":"réinitialiser", "english":"anglais", "french":"français", "theme":"thème", "text":"text", "language":"langue", "ID":"ID", "Pseudo":"Pseudo", "Game":"Jeux", "nb_ok":"nb_ok", "nb_total":"nb_total", "start date":"heure de commencement", "start time":"heure de départ", "Are you sure you want to erase the results?":"êtes vous sûre de vouloir éfacer les résultats ?", "normal":"normal", "ratio":"ratio", "progress":"progression", "filter":"filtrer", "change user":"changer d'utilisateur"}}
# définition des thèmes
listThemes = {"dark":{"bg":"#222222", "bg2":"#114411", "btn":"#003300", "fg":"#ffffff", "actbtn":"#006600", "actfg":"#ffffff", "fgbtn":"#ffffff", "bgTable": "#151515", "bgEntry":"#666666"},
              "white":{"bg":"#ffffff", "bg2":"#00cc00", "btn":"#00aa00", "fg":"#000000", "actbtn":"#44cc44", "actfg":"#ffffff", "fgbtn":"#000000", "bgTable": "#ffffff", "bgEntry":"#ffffff"},
              "normal":{"bg":"#8bc9c2", "bg2":"#ffffff", "btn":"#ffffff", "fg":"#000000", "actbtn":"#44cc44", "actfg":"#ffffff", "fgbtn":"#000000", "bgTable": "#ffffff", "bgEntry":"#ffffff"}}

themeName = "dark"
lang = "fr"
theme = []
dicoEntries={"ID": None, "Pseudo": None, "Game": None, "nb_total": None, "nb_ok": None, "start date": None, "start time": None}


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
isFiltred = False
logicTable = []
user = "customer"
textChangeUser = ["login", "logout"]

# functions

# fonction pour charger la page
def Load():
    print("reload ...")
    global theme
    AplyConf()
    theme = listThemes[themeName]
    Display()

# fonction pour modifier les paramêtres
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

# fonction de filtrage
def filter():
    global isFiltred, logicTable
    count = 0
    table = data.GetTable("parties")
    isFiltred = False
    # boucle par colonne
    for i in ["ID", "Pseudo", "Game", "nb_total", "nb_ok", "start date", "start time"]:
        if dicoEntries[i].get() != "":
            isFiltred = True
            count2 = 0
            cTable = table.copy()
            # boucle par ligne
            for j in cTable:
                if str(j[count]) != dicoEntries[i].get():
                    table.pop(count2)
                else:
                    count2 += 1
        count += 1
    logicTable = table
    Load()

# fonction de réinitialisation de la table
def Reset():
    if messagebox.askquestion(Lang("Are you sure you want to erase the results?")):
        data.delete()
        Load()

# fonction pour changer d'utilisateur
def ChangeUser():
    global user
    password = "mot de passe"
    if user == "customer":
        connectWindow = Tk()
        connectWindow.title("connection")
        connectWindow.geometry("400x400")
        labelPassword = Label(connectWindow, text=Lang("password"))
        labelPassword.pack()
        EntryPassword = Entry(connectWindow, show="*", width=20)
        EntryPassword.pack()
        labelError = Label(connectWindow, fg="red", text="")
        labelError.pack()
        def enterCommand():
            global user
            nonlocal password, labelError, connectWindow
            password = EntryPassword.get()
            data.disconnect()
            if data.DBConnect("su", password):
                print("connected")
                user = "su"
                connectWindow.destroy()
            else:
                print(Error("incorrect password :" + password))
                data.DBConnect("customer", "")
                labelError["text"] = "incorrect password"
        enterButton = Button(connectWindow, text="enter", command=enterCommand)
        enterButton.pack()
        connectWindow.mainloop()
    else:
        data.disconnect()
        data.DBConnect("customer", "")
        user = "customer"
    Load()



# graphical
window = Tk()
window.title("proj_dbpy")
window.geometry(str(window.winfo_screenwidth()) + "x" + str(window.winfo_screenheight()))
menu = Menu(window)

# fonction pour charger l'interface graphique
def Display():
    global window, logicTable, menu
    print("open the window ...")
    try:
        for i in window.winfo_children():
            i.destroy()
    except:
        pass
    window.configure(bg=theme["bg"])

    frameTop = Frame(window, bg="blue").pack(side=TOP)
    frameMidle = Frame(window, bg="green").pack(side=BOTTOM)

    filterFrame = Frame(frameTop, bg=theme["bgTable"])
    filterFrame.pack(anchor="w")
    listWidth = [7, 20, 30, 20, 20, 35, 35, 14]
    for i in range(7):
        Label(filterFrame, width=listWidth[i], text=[Lang("ID"), Lang("Pseudo"), Lang("Game"), Lang("nb_total"), Lang("nb_ok"), Lang("start date"), Lang("start time"), Lang("progress")][i], bg=theme["bg2"], fg=theme["fg"]).grid(row=1, column=i)
    count = 0
    for i in ["ID", "Pseudo", "Game", "nb_total", "nb_ok", "start date", "start time"]:
        dicoEntries[i] = Entry(filterFrame, width=listWidth[count], bg=theme["bgEntry"])
        dicoEntries[i].grid(row=2, column=count)
        count += 1
    filterButton = Button(filterFrame, width=14, text=Lang("filter"), bg=theme["btn"], fg=theme["fgbtn"], command=filter).grid(row=2, column=7)

    # menu
    menu = Menu(window)
    menu.delete(0, "end")
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

    # fonction pour créer et rafraichire le menu setting (pour changer le texte login et logout)
    def updateMenusetting():
        menuSettings.delete(0, "end")
        if user == "customer":
            menuSettings.add_command(label="login", command=ChangeUser)
        else:
            menuSettings.add_command(label="logout", command=ChangeUser)
    menuSettings = Menu(menu, postcommand=updateMenusetting)
    menu.add_cascade(menu=menuSettings, label=Lang("settings"))

    # table
    TGCanvas = Canvas(frameMidle, width=1600, bg=theme["bg"], bd=0, relief="ridge", highlightthickness=0)
    TGCanvas.pack(side=LEFT ,anchor="n", pady=30)

    def on_configure(event):
        TGCanvas.configure(scrollregion=TGCanvas.bbox('all'))

    # scrollbar
    scrollbar = Scrollbar(frameMidle, command=TGCanvas.yview)
    scrollbar.pack(anchor="e", fill=Y, expand=True)
    TGCanvas.configure(yscrollcommand=scrollbar.set)
    TGCanvas.bind('<Configure>', on_configure)

    # fonction de création de la bare de progression
    def ProgressBar(field, Value = 0):
        ProgressColor = "#00ff00"
        if Value < 50:
            ProgressColor = "#ff0000"
        elif Value < 75:
            ProgressColor = "#ff9900"
        Frame(field, bg=ProgressColor, width=Value, height=15).grid(row=line + 1, column=7, sticky="w")

    # affichage des données
    frameTable = Frame(TGCanvas, bg=theme["bgTable"])
    count = 0
    for Text in [Lang("ID"), Lang("Pseudo"), Lang("Game"), Lang("nb_total"), Lang("nb_ok"), Lang("start date"), Lang("start time"), Lang("progress")]:
        Label(frameTable, text=Text, borderwidth=1, bg=theme["bg2"], width=listWidth[count], fg=theme["fg"]).grid(row=0,column=count)
        count += 1
    if not isFiltred:
        logicTable = data.GetTable("parties")
    for line in range(len(logicTable)):
        for column in range(7):
            Label(frameTable, text=str(logicTable[line][column]), width=listWidth[column], borderwidth=1, bg=theme["bgTable"],
                   fg=theme["fg"]).grid(row=line + 1, column=column)
        if int(logicTable[line][3]) != 0:
            ProgressValue = int(int(logicTable[line][3]) / int(logicTable[line][4]) * 100)
            ProgressBar(frameTable, ProgressValue)
    frameTable.pack()
    TGCanvas.create_window((0, 0), window=frameTable)
    window.config(menu=menu)

Load()
window.mainloop()
