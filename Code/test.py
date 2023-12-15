import tkinter as tk

def on_button_click(button_number):
    print(f"Bouton {button_number} cliqué!")

root = tk.Tk()

# Nombre de boutons
num_buttons = 5

# Création des boutons avec une boucle for
for i in range(num_buttons):
    button = tk.Button(root, text=f"Bouton {i+1}", command=lambda num=i+1: on_button_click(num))
    button.grid(row=i, column=0)

root.mainloop()