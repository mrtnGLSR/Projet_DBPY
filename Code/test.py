import tkinter as tk
from tkinter import ttk

# Création de la fenêtre principale
app = tk.Tk()
app.title("Exemple de Combobox")

# Création de la Combobox
comboExample = ttk.Combobox(app, values=["January", "February", "March", "April"])

# Changer la couleur de fond
comboExample.configure(background="lightblue")

# Placement de la Combobox dans la fenêtre
comboExample.pack(padx=10, pady=10)

# Exécution de la boucle principale
app.mainloop()