"""
Auteur      :Martin
Date        :17.11.2023
Version     :1.0
Description :partie graphique de loutil de management des scors dans le cadre du MA dbpy
"""
# modules
from tkinter import *
from tkinter import messagebox
from tkinter import ttk as ttk
import datetime
import database as data
import sys
import os
import io as io
import bcrypt

# constants
# définnition des langues
translate = {}

# fonction pour trouver un fichier de langue à partir du nom de la langue
def FindLangs(lang = "all"):
    listLangs = []
    files = os.listdir("./langs")
    # lister toutes les langues si la variable langue prends l'argument "all"
    if lang == "all":
        for i in files:
            listLangs.append(i[:-5])
        return listLangs
    # rechercher le fichier
    else:
        langfile = ""
        for i in files:
            if i[:-5] == lang:
                langfile = i
        if langfile == "":
            return 0
        else:
            return langfile

# fonction permettant de créer un dictionnaire pour traduire les textes
def DefLang(lang):
    global translate
    if lang != "en":
        file = io.open("./langs/" + FindLangs(lang), "r", encoding="utf-8")
        lines = file.readlines()
        for i in lines:
            separator = i.find(":")
            firstWord = i[:separator]
            secondWord = i[separator + 1:].strip()
            translate[firstWord] = secondWord
        file.close()

# définition des thèmes
listThemes = {"dark":{"bg":"#222222", "bg2":"#114411", "btn":"#003300", "fg":"#ffffff", "actbtn":"#006600", "actfg":"#ffffff", "fgbtn":"#ffffff", "bgTable": "#151515", "bgEntry":"#404040"},
              "white":{"bg":"#ffffff", "bg2":"#00cc00", "btn":"#00aa00", "fg":"#000000", "actbtn":"#44cc44", "actfg":"#ffffff", "fgbtn":"#000000", "bgTable": "#ffffff", "bgEntry":"#ffffff"},
              "normal":{"bg":"#8bc9c2", "bg2":"#ffffff", "btn":"#ffffff", "fg":"#000000", "actbtn":"#44cc44", "actfg":"#ffffff", "fgbtn":"#000000", "bgTable": "#ffffff", "bgEntry":"#ffffff"}}

themeName = "dark"
lang = "fr"
theme = []
dicoEntries={"ID": None, "Pseudo": None, "Game": None, "nb_total": None, "nb_ok": None, "start date": None, "start time": None}

# fonction pour ecrir le texte sur la sortie stderr
def Error(text = "Error"):
    sys.stderr.write("Error: "+ str(datetime.datetime.now()) + ", " + str(text) + "\n")

# fonction pour mettre la syntax du text en mode avertissement
def Warning(text = "warning"):
    return "\033[33m" + "Warning: "+ str(datetime.datetime.now()) + ", " + text + "\033[0m"

# fonction d'application de la configuration
def AplyConf():
    print("reading the settings ...")
    global themeName, lang
    conf = open(file="config", mode="r+")
    lang = conf.readline()[0:-1]
    themeName = conf.readline()[0:-1]
    DefLang(lang)
    conf.close()

def FalseUserMessage():
    messagebox.showinfo(Lang("warning"), Lang("you didn'a have privileges"))
    print(Warning("False user for this action"))

# fonction de définition de la langue
def Lang(text = "no text"):
    if lang == "en":
        return text
    else:
        try:
            return translate[text]
        except:
            print(Warning("translate of " + str(text) + " not found"))
            return text

# variables
isFiltred = False
logicTable = []
data.userType = "customer"
textChangeUser = ["login", "logout"]
listLines = []

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
    if data.userType == "admin":
        if messagebox.askquestion("error", Lang("Are you sure you want to erase the results?")) == "yes":
            data.delete()
            Load()
    else:
        FalseUserMessage()

def Delete(line):
    if data.userType == "admin":
        id = logicTable[line][0]
        if messagebox.askquestion("warning", Lang("Are you sure you want delete the line ") + str(id) + " ?"):
            data.delete(id)
            Load()

    else:
        FalseUserMessage()

# fenêtre pour changer le mot de passe d'un tuilisateur
def ChangePasswdWindow():
    if data.GetUserType(data.user) == "admin":
        cpw = Tk()
        cpw.title(Lang("change password"))
        cpw.geometry("400x400")
        cpw.configure(bg=theme["bg"])

        # création des frames
        upFrame = Frame(cpw, bg=theme["bg"])
        downFrame = Frame(cpw, bg=theme["bg"])
        labelFrame = Frame(upFrame, bg=theme["bg"])
        entryFrame = Frame(upFrame, bg=theme["bg"])
        upFrame.pack()
        downFrame.pack()
        labelFrame.pack(side=LEFT)
        entryFrame.pack(side=RIGHT)

        # création des labels
        for i in ["Pseudo", "Password", "confirm password"]:
            Label(labelFrame, text=Lang(i), fg=theme["fg"], bg=theme["bg"]).pack()

        # création des entrées
        pseudoEntry = Entry(entryFrame, fg=theme["fg"], bg=theme["bg"])
        passwdEntry = Entry(entryFrame, fg=theme["fg"], bg=theme["bg"], show="*")
        passwdConfEntry = Entry(entryFrame, fg=theme["fg"], bg=theme["bg"], show="*")
        pseudoEntry.pack()
        passwdEntry.pack()
        passwdConfEntry.pack()

        # text d'erreur
        labelErr = Label(cpw, fg="red", bg=theme["bg"], text="")

        # création de la fonction d'entrée
        def Enter():
            if len(passwdEntry.get()) < 8:
                labelErr.configure(text=Lang("incorrect password confirmation"))
                Error("incorrect password confirmation")
            else:
                if passwdEntry.get() == passwdConfEntry.get():
                    data.ChangeUserPasswd(pseudoEntry.get(), passwdEntry.get())
                    labelErr.configure(text="")
                else :
                    labelErr.configure(text=Lang("password confirmation failed"))
                    Error("password confirmation failed")

        # bouton d'entrée
        Button(cpw, text=Lang("enter"), bg=theme["btn"], fg=theme["fgbtn"], command=Enter).pack()

        cpw.mainloop()
    else:
        FalseUserMessage()

# fonction pour changer d'utilisateur
def ChangeUser():
    password = "mot de passe"
    # connection en superutilisateur
    if data.userType == "customer":
        # structure de la fenêtre
        connectWindow = Tk()
        connectWindow.title("connection")
        connectWindow.geometry("400x400")
        connectWindow.configure(bg=theme["bg"])
        Label(connectWindow, text=Lang("Pseudo"), fg=theme["fg"], bg=theme["bg"]).pack()
        entryPseudo = Entry(connectWindow, width=20, fg=theme["fg"], bg=theme["bgEntry"])
        entryPseudo.pack()
        Label(connectWindow, text=Lang("password"), fg=theme["fg"], bg=theme["bg"]).pack()
        EntryPassword = Entry(connectWindow, show="*", width=20, fg=theme["fg"], bg=theme["bgEntry"])
        EntryPassword.pack()
        labelError = Label(connectWindow, fg="red", text="", bg=theme["bg"])
        labelError.pack()
        # vérification des paramêtres
        def enterCommand():
            nonlocal labelError, connectWindow
            data.GetUserType("user")
            pseudo = entryPseudo.get()
            password = EntryPassword.get()
            # tester la connection
            if data.ConnectUser(pseudo, password):
                print("connected to " + data.user)
                Load()
                connectWindow.destroy()
            else:
                Error("incorrect password or user")
                labelError["text"] = "incorrect password"

        # définition du bouton d'entrée
        enterButton = Button(connectWindow, text="enter", command=enterCommand, bg=theme["btn"], fg=theme["fgbtn"])
        enterButton.pack()
        connectWindow.mainloop()
    # déconnection du superutilisateur
    else:
        data.disconnect()
        data.DBConnect("customer", "")
        data.userType = "customer"
    Load()

# fenêtre d'ajout d'utilisateurs
def AddUserWindow():
    if data.userType == "admin":
        # création de la fenêtre
        addUserWindow = Tk()
        addUserWindow.title(Lang("add user"))
        addUserWindow.configure(bg=theme["bg"])
        addUserWindow.geometry("300x200")

        # création des frames
        upFrame = Frame(addUserWindow, bg=theme["bg"])
        downFrame = Frame(addUserWindow, bg=theme["bg"])
        labelFrame = Frame(upFrame, bg=theme["bg"])
        entryFrame = Frame(upFrame, bg=theme["bg"])
        upFrame.pack()
        downFrame.pack()
        labelFrame.pack(side=LEFT)
        entryFrame.pack(side=RIGHT)

        # création des labels
        Label(labelFrame, text=Lang("Pseudo"), bg=theme["bg"], fg=theme["fg"]).pack()
        Label(labelFrame, text=Lang("Type"), bg=theme["bg"], fg=theme["fg"]).pack()
        Label(labelFrame, text=Lang("password"), bg=theme["bg"], fg=theme["fg"]).pack()
        Label(labelFrame, text=Lang("confirm password"), bg=theme["bg"], fg=theme["fg"]).pack()
        labelErr = Label(downFrame, text="", fg="red", bg=theme["bg"])
        labelErr.pack()

        # création des entrées
        pseudoEntry = Entry(entryFrame, bg=theme["bg"], fg=theme["fg"])
        passwordEntry = Entry(entryFrame, show="*", bg=theme["bg"], fg=theme["fg"])
        confirmPasswordEntry = Entry(entryFrame, show="*", bg=theme["bg"], fg=theme["fg"])
        userTypeEntry = ttk.Combobox(entryFrame, values=["customer", "admin"])

        # positionnement des entrées
        pseudoEntry.pack()
        userTypeEntry.pack()
        userTypeEntry.pack()
        passwordEntry.pack()
        confirmPasswordEntry.pack()

        def Confirm():
            errText = ""
            newUser = pseudoEntry.get()
            newPasswd = passwordEntry.get()
            newPasswdConfirm = confirmPasswordEntry.get()
            newUserType = userTypeEntry.get()
            # vérifier que le pseudo ne contienne pas de caractères spéciaux
            if not newUser.isalpha():
                errText = Lang("the name can't have specials caracters")
                Error("the pseudo can't contain specials caracters")
            else:
                # vérifier que le mot de passe soit plus long que 8 caractères
                if len(newPasswd) < 8:
                    errText = Lang("your password must contain 8 characters or more")
                    Error("your password must contain 8 characters or more")
                else:
                    # vérifier que l'utilisateur n'existe pas déjà
                    if data.GetUserType(newUser) != "false user":
                        errText = Lang("this user already exists")
                        Error("false entry, this user already exists")
                    else:
                        if newPasswdConfirm != newPasswd:
                            errText = Lang("incorrect password confirmation")
                            Error("incorrect password confirmation")
                        else:
                            if not newUserType in ["admin", "customer"]:
                                errText = Lang("invalide type")
                                Error("invalide type")
                            else:
                                if newUserType == "customer":
                                    salt = bcrypt.gensalt()
                                    binPasswd = newPasswd.encode("utf-8")
                                    binhashPasswd = bcrypt.hashpw(binPasswd, salt)
                                    hashPasswd = binhashPasswd.decode("utf-8")
                                    data.Adduser(newUser, newUserType, hashPasswd)
                                else:
                                    data.Adduser(newUser, newUserType, newPasswd)
                                labelErr.configure(text="")
            labelErr.configure(text=errText)




        # bouton de confirmation
        confirmButton = Button(downFrame, text=Lang("Enter"), bg=theme["btn"], fg=theme["fgbtn"], command=Confirm)
        confirmButton.pack()

        addUserWindow.mainloop()

    else:
        FalseUserMessage()

# fenêtre d'ajout de ligne
def InsertDataWindow():
    # créer la fenêtre si l'utilisateur est en su
    if data.userType == "admin":
        # structure de la fenêtre
        labelTable = ["Pseudo", "Game", "nb_total", "nb_ok", "start date", "time"]
        insertDataWindow = Tk()
        insertDataWindow.geometry("300x200")
        insertDataWindow.title(Lang("insert"))
        insertDataWindow.configure(bg=theme["bg"])

        # frames de la fenêtre
        frameUp = Frame(insertDataWindow, bg=theme["bg"])
        frameUp.pack()
        frameDown = Frame(insertDataWindow, bg=theme["bg"])
        frameDown.pack()
        textFrame = Frame(frameUp, bg=theme["bg"])
        textFrame.pack(side=LEFT)
        entryFrame = Frame(frameUp, bg=theme["bg"])
        entryFrame.pack(side=RIGHT)

        # créer tous les labels
        for i in labelTable:
            Label(textFrame, text=Lang(i), fg=theme["fg"], bg=theme["bg"]).pack()
        # création des entrées
        Pseudoentry = Entry(entryFrame, fg=theme["fg"], bg=theme["bgEntry"])
        GameEntry = ttk.Combobox(entryFrame, values=["geo01", "info02", "info05"])
        nb_totalEntry = Entry(entryFrame, fg=theme["fg"], bg=theme["bgEntry"])
        nb_okEntry = Entry(entryFrame, fg=theme["fg"], bg=theme["bgEntry"])
        startFrame = Frame(entryFrame, bg=theme["bg"])
        dateFrame = Frame(startFrame, bg=theme["bg"])
        timeFrame = Frame(startFrame, bg=theme["bg"])
        dayEntry = Entry(dateFrame, fg=theme["fg"], bg=theme["bgEntry"], width=2)
        mothEntry = Entry(dateFrame, fg=theme["fg"], bg=theme["bgEntry"], width=2)
        yearEntry = Entry(dateFrame, fg=theme["fg"], bg=theme["bgEntry"], width=4)
        clockEntry = Entry(timeFrame, fg=theme["fg"], bg=theme["bgEntry"], width=2)
        minutesEntry = Entry(timeFrame, fg=theme["fg"], bg=theme["bgEntry"], width=2)
        secondsEntry = Entry(timeFrame, fg=theme["fg"], bg=theme["bgEntry"], width=2)

        # placer les éléments
        Pseudoentry.pack()
        GameEntry.pack()
        GameEntry.pack()
        GameEntry.pack()
        GameEntry.pack()
        nb_totalEntry.pack()
        nb_okEntry.pack()
        startFrame.pack(side=TOP)
        dateFrame.pack(side=BOTTOM)
        timeFrame.pack()
        dayEntry.pack(side=LEFT)
        Label(dateFrame, text=".", fg=theme["fg"], bg=theme["bg"]).pack(side=LEFT)
        mothEntry.pack(side=LEFT)
        Label(dateFrame, text=".", fg=theme["fg"], bg=theme["bg"]).pack(side=LEFT)
        yearEntry.pack(side=LEFT)
        clockEntry.pack(side=LEFT)
        Label(timeFrame, text=":", fg=theme["fg"], bg=theme["bg"]).pack(side=LEFT)
        minutesEntry.pack(side=LEFT)
        Label(timeFrame, text=":", fg=theme["fg"], bg=theme["bg"]).pack(side=LEFT)
        secondsEntry.pack(side=LEFT)
        errorMsg = Label(frameDown, text="", fg="#ff0000", bg=theme["bg"])
        errorMsg.pack()
        def EnterChoice():
            # vérification des données
            nb_err = 0
            # vérifier les nombres entiers
            for i in [dayEntry, mothEntry, yearEntry, nb_totalEntry, nb_okEntry, secondsEntry, minutesEntry, clockEntry]:
                if not i.get().isdigit():
                    nb_err += 1
                    Error(str(i) + " si not integer")

            # vérifier que nb_ok soit plus petit que nb_total
            if nb_err == 0:
                if int(nb_okEntry.get()) > int(nb_totalEntry.get()):
                    nb_err += 1
                    Error("nb_ok is biger than nb_total")
            # vérifier que les date soit possible et les définir
            try:
                dateValue = datetime.date(day=int(dayEntry.get()), month=int(mothEntry.get()), year=int(yearEntry.get()))
            except:
                nb_err += 1
                Error("the date is not valable")
            try:
                timeValue = datetime.time(hour=int(clockEntry.get()), minute=int(minutesEntry.get()), second=int(secondsEntry.get()))
            except:
                nb_err += 1
                Error("the time is not valable")
            # entrer les valeures dans la base de donnée
            if nb_err == 0:
                data.SaveScore(Pseudoentry.get(), GameEntry.get(), nb_okEntry.get(), nb_totalEntry.get(), dateValue, timeValue)
                print("score saved")
            else:
                Error("the program was executed with " + str(nb_err) + " errors")
                errorMsg.configure(text=Lang("syntax error"))
            Load()
        enterButton = Button(frameDown, text=Lang("Enter"), bg=theme["btn"], fg=theme["fgbtn"], command=EnterChoice)
        enterButton.pack()

    # informer l'utilisateur qu'il n'a pas les droits
    else:
        FalseUserMessage()

# graphical
# création de la base de la fenêtre
window = Tk()
window.title("proj_dbpy")
window.geometry(str(window.winfo_screenwidth()) + "x" + str(window.winfo_screenheight()))
menu = Menu(window)
trashIcon = PhotoImage(file="./img/trash_icon16.png")

# fonction pour charger l'interface graphique
def Display():
    global window, logicTable, menu, listLines
    print("open the window ...")
    # détruire l'ancienne fenêtre
    try:
        for i in window.winfo_children():
            i.destroy()
    except:
        pass
    window.title("proj_dbpy             user:" + data.user)
    window.configure(bg=theme["bg"])
    # création des frames principales
    frameTop = Frame(window, bg="blue").pack(side=TOP)
    frameMidle = Frame(window, bg="green").pack(side=BOTTOM)

    filterFrame = Frame(frameTop, bg=theme["bgTable"])
    filterFrame.pack(anchor="w")

    # création du menu de filtrage
    listWidth = [7, 20, 20, 30, 30, 30, 35, 35, 14]
    for i in range(7):
        Label(filterFrame, width=listWidth[i], text=[Lang("ID"), Lang("Pseudo"), Lang("Game"), Lang("nb_total"), Lang("nb_ok"), Lang("start date"), Lang("start time"), Lang("progress")][i], bg=theme["bg2"], fg=theme["fg"]).grid(row=1, column=i)
    count = 0
    for i in ["ID", "Pseudo", "Game", "nb_total", "nb_ok", "start date", "start time"]:
        dicoEntries[i] = Entry(filterFrame, width=listWidth[count], bg=theme["bgEntry"], fg=theme["fg"])
        dicoEntries[i].grid(row=2, column=count)
        count += 1
    Button(filterFrame, width=14, text=Lang("filter"), bg=theme["btn"], fg=theme["fgbtn"], command=filter).grid(row=2, column=7)

    # menu
    menu = Menu(window)
    menu.delete(0, "end")

    menu1 = Menu(menu)
    menu1.add_command(label=Lang("reset"), command=Reset)
    menu1.add_command(label=Lang("insert"), command=InsertDataWindow)
    menu1.add_command(label=Lang("refresh"), command=Load)
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
        if data.userType == "customer":
            menuSettings.add_command(label="login", command=ChangeUser)
        else:
            menuSettings.add_command(label="logout", command=ChangeUser)
            menuSettings.add_command(label=Lang("add user"), command=AddUserWindow)
            menuSettings.add_command(label=Lang("change password"), command=ChangePasswdWindow)
    menuSettings = Menu(menu, postcommand=updateMenusetting)
    menu.add_cascade(menu=menuSettings, label=Lang("settings"))

    # table
    TGCanvas = Canvas(frameMidle, width=1700, height=1000, bg=theme["bg"], bd=0, relief="ridge", highlightthickness=0)
    TGCanvas.pack(side=LEFT, anchor="n", pady=30)

    def on_configure(event):
        TGCanvas.configure(scrollregion=TGCanvas.bbox('all'))

    # scrollbar
    scrollbar = Scrollbar(frameMidle, command=TGCanvas.yview)
    scrollbar.pack(anchor="e", fill=Y, expand=True)
    TGCanvas.configure(yscrollcommand=scrollbar.set)
    TGCanvas.bind('<Configure>', on_configure)

    # fonction de création de la bare de progression
    def ProgressBar(field, Value = 0):
        # définition de la couleur
        R = int(255 - 255 * (Value / 100))
        G = int(255 * (Value / 100))
        if R < 16:
            strR = "0" + str(hex(R))[2:]
        else:
            strR = str(hex(R))[2:]
        if G < 16:
            strG = "0" + str(hex(G))[2:]
        else:
            strG = str(hex(G))[2:]
        ProgressColor = "#" + strR + strG + "00"
        # création de la bare
        Frame(field, bg=ProgressColor, width=Value, height=15).grid(row=line + 1, column=8, sticky="w")

    # affichage des données
    frameTable = Frame(TGCanvas, bg=theme["bgTable"], height=1200)
    count = 0
    # aficher les titres
    for Text in ["", Lang("ID"), Lang("Pseudo"), Lang("Game"), Lang("nb_total"), Lang("nb_ok"), Lang("start date"), Lang("time"), Lang("progress")]:
        Label(frameTable, text=Text, borderwidth=1, bg=theme["bg2"], width=listWidth[count], fg=theme["fg"]).grid(row=0,column=count)
        count += 1
    # selectionner la table si elle n'est pas filtrée
    if not isFiltred:
        logicTable = data.GetTable("parties")
    # afficher le tableau principal
    for line in range(len(logicTable)):
        # afficher les boutons de suppressions
        Button(frameTable, image=trashIcon, command=lambda xline=line: Delete(xline), bg="red").grid(row=line + 1, column=0)
        # afficher les données
        for column in range(7):
            Label(frameTable, text=str(logicTable[line][column]), width=listWidth[column], borderwidth=1, bg=theme["bgTable"],
                   fg=theme["fg"]).grid(row=line + 1, column=column + 1)
        # afficher la bare de progression
        if int(logicTable[line][3]) != 0:
            ProgressValue = int(int(logicTable[line][3]) / int(logicTable[line][4]) * 100)
            ProgressBar(frameTable, ProgressValue)
    frameTable.pack()
    TGCanvas.create_window((0, 0), window=frameTable)
    window.config(menu=menu)

Load()
window.mainloop()
