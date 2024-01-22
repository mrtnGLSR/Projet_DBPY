"""
Auteur      :Martin Glauser
Date        :10.11.2023
Version     :1.0
Description :fichier contennant toutes les fonctions touchant à la base de donnée
"""
# modules
import mysql.connector
from datetime import *
import bcrypt
# constantes

# variables

cursor = None
mydb = None
user = "customer"
userType = "customer"

# connection à la base de données
def DBConnect(user, password):
    global mydb, cursor
    print(password)
    try:
        mydb = mysql.connector.connect(
          host="localhost",
          user=user,
          password=password,
          buffered=True,
          autocommit=True
        )
        cursor = mydb.cursor()
        cursor.execute("USE proj_dbpy")
        return True
    except:
        return False
DBConnect("customer", "")

# déconnection
def disconnect():
    global mysql, cursor
    cursor.close()
    mydb.close()

# fonctions

# fonction permettant de sauvegarder les scors
def SaveScore(pseudo, game, nb_ok, nb_total,startDay ,time):
    sqlCommand = "INSERT INTO parties (Pseudo, game, nb_ok, nb_Total, start_date, time) Values('" + pseudo + "', '" + game + "', " + str(nb_ok) + ", " + str(nb_total) + ", '" + str(startDay) + "', '" + str(time) + "');"
    print(sqlCommand)
    cursor.execute(sqlCommand)

# fonction permettant d'interroger la base de donnée pour en tirer un tableau
def GetTable(table, columns="all"):
    sqlCommand = ""
    # permet de selectionner toute la table
    if columns == "all":
        sqlCommand = "SELECT * from " + str(table) + ";"
    # verifie la validité des entrées
    elif type(columns) == list and len(columns) != 0:
        sqlCommand = "SELECT "
        count = 0
        for i in columns:
            count += 1
            sqlCommand += str(i)
            if count != len(columns):
                sqlCommand += ", "
        sqlCommand += " FROM " + table + ";"
    # message en cas d'erreur
    else:
        print("l'argument columns n'es pas valide")
    # execution de la commande
    cursor.execute(sqlCommand)
    return cursor.fetchall()

# fonction de réinitialisation de la db
def delete(line = "all"):
    print(line)
    if line == "all":
        cursor.execute("delete from parties;")
    else:
        cursor.execute("delete from parties WHERE id = " + str(line) + ";")

def GetUserType(user):
    userInfos = GetTable("users")
    userType = ""
    existsUser = False
    for i in userInfos:
        if i[1] == user:
            userType = i[2]
            existsUser = True
    if existsUser:
        return userType
    else:
        return "false user"
def Adduser(pseudo, type, passwd):
    print("create user " + pseudo + "...")
    sqlCommand = "insert into users (pseudo, userType"
    if type == "customer":
        sqlCommand += ", passwd) VALUES (\""
    else:
        sqlCommand += ") VALUES (\""
    sqlCommand += pseudo + "\", \"" + type + "\""
    if type == "customer":
        sqlCommand += ", \"" + passwd + "\""
    sqlCommand += ");"
    cursor.execute(sqlCommand)
    if type == "admin":
        cursor.execute("CREATE USER \'" + pseudo + "\'@\'localhost\' IDENTIFIED BY \'" + passwd + "\';")
        cursor.execute("GRANT ALL ON proj_dbpy.* TO '" + pseudo + "'@'localhost';")
def ConnectUser(tmpUser, passwd):
    global user, userType
    varToReturn = False
    if GetUserType(tmpUser) == "admin":
        disconnect()
        if DBConnect(tmpUser, passwd):
            user = tmpUser
            varToReturn = True
        else:
            DBConnect("customer", "")
            user = "customer"
            varToReturn = False
    else:
        users = GetTable("users")
        for i in users:
            if i[1] == tmpUser:
                if bcrypt.checkpw(passwd.encode("utf-8"), i[3].encode("utf-8")):
                    DBConnect("customer", "")
                    user = tmpUser
                    varToReturn = True
                else:
                    DBConnect("customer", "")
                    user = "customer"
                    varToReturn = False
    userType = GetUserType(user)
    return varToReturn
def ChangeUserPasswd(tmpUser, passwd):
    if GetUserType(tmpUser) == "customer":
        salt = bcrypt.gensalt()
        binPasswd = passwd.encode("utf-8")
        binhashPasswd = bcrypt.hashpw(binPasswd, salt)
        hashPasswd = binhashPasswd.decode("utf-8")
        sqlCommand = "UPDATE users SET passwd = \"" + hashPasswd + "\" WHERE Pseudo LIKE '" + tmpUser + "';"
        cursor.execute(sqlCommand)
        print("password changed")
    elif GetUserType(tmpUser) == "admin":
        sqlCommand = "ALTER USER \"" + tmpUser + "\"@'localhost' IDENTIFIED BY \"" + passwd + "\";"
        cursor.execute(sqlCommand)
        print("password changed")


