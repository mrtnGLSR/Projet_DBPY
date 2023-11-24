"""
Auteur      :Martin Glauser
Date        :10.11.2023
Version     :1.0
Description :fichier contennant toutes les fonctions touchant à la base de donnée
"""
# modules
import mysql.connector
from datetime import *
# constantes

# variables

# définition de la base de donnée
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  buffered=True,
  autocommit=True
)
cursor = mydb.cursor()
cursor.execute("USE proj_dbpy")
# TODO ajouter un utilisateur pour plus de sécurité

# fonctions

# fonction permettant de sauvegarder les scors
def SaveScore(pseudo, game, nb_ok, nb_total,startDay , time):
    sqlCommand = "INSERT INTO parties (Pseudo, game, nb_ok, nb_Total, start_date, total_time) Values('" + pseudo + "', '" + game + "', " + str(nb_ok) + ", " + str(nb_total) + ", '" + str(startDay) + "', '" + str(time) + "');"
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
def delete():
    cursor.execute("delete from parties;")