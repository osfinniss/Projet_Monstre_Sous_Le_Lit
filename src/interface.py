import tkinter as tk
from tkinter import messagebox
import json

def charger_defi():
    with open("data/defis.json", "r") as f:
        return json.load(f)["defi1"]

def lancer_interface():
    defi = charger_defi()
    taille = 3  # Taille fixe pour les 4 grilles
    monstres = defi["plateau"]["monstres_visibles"]

    root = tk.Tk()
    root.title("Monstres sous le lit")

    canvas_list = []
    grille_list = []

    for k in range(4):
        canvas = tk.Canvas(root, width=300, height=300)
        canvas.grid(row=k//2, column=k%2, padx=20, pady=20)  # Ajout de marges
        canvas_list.append(canvas)
        grille = [[0 for _ in range(taille)] for _ in range(taille)]
        grille_list.append(grille)

    def placer_tuile(event, canvas_index):
        x, y = event.x // 100, event.y // 100
        grille = grille_list[canvas_index]
        grille[y][x] = 1 if grille[y][x] == 0 else 0
        dessiner_grille(canvas_index)

    def dessiner_grille(canvas_index):
        canvas = canvas_list[canvas_index]
        grille = grille_list[canvas_index]
        canvas.delete("all")
        for i in range(taille):
            for j in range(taille):
                couleur = "blue" if grille[j][i] == 1 else "white"
                canvas.create_rectangle(i * 100, j * 100, (i+1) * 100, (j+1) * 100, fill=couleur, outline="black")
        for mx, my in monstres:
            canvas.create_oval(mx * 100 + 40, my * 100 + 40, mx * 100 + 60, my * 100 + 60, fill="red")

    def verifier_solution():
        solution_correcte = all(grille[y][x] == 1 for grille in grille_list for x, y in monstres)
        messagebox.showinfo("Résultat", "Solution correcte!" if solution_correcte else "Essayez encore!")

    def rotation_gauche():
        for grille in grille_list:
            grille[:] = [list(reversed(col)) for col in zip(*grille)]
        for i in range(4):
            dessiner_grille(i)

    def rotation_droite():
        for grille in grille_list:
            grille[:] = [list(col) for col in zip(*reversed(grille))]
        for i in range(4):
            dessiner_grille(i)

    for i in range(4):
        canvas_list[i].bind("<Button-1>", lambda event, index=i: placer_tuile(event, index))
        dessiner_grille(i)

    tk.Button(root, text="Rotation Gauche", command=rotation_gauche).grid(row=2, column=0, pady=20)
    tk.Button(root, text="Rotation Droite", command=rotation_droite).grid(row=2, column=1, pady=20)
    tk.Button(root, text="Vérifier", command=verifier_solution).grid(row=3, column=0, pady=20)
    tk.Button(root, text="Réinitialiser", command=lancer_interface).grid(row=3, column=1, pady=20)

    root.mainloop()