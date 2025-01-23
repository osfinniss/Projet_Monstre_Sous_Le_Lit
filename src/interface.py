import tkinter as tk
from tkinter import messagebox
import json

def charger_defi():
    with open("data/defis.json", "r") as f:
        return json.load(f)["defi1"]

def lancer_interface():
    defi = charger_defi()
    taille = defi["plateau"]["taille"]
    monstres = defi["plateau"]["monstres_visibles"]

    root = tk.Tk()
    root.title("Monstres sous le lit")
    canvas = tk.Canvas(root, width=500, height=500)
    canvas.pack()

    grille = [[0 for _ in range(taille)] for _ in range(taille)]

    def placer_tuile(event):
        x, y = event.x // 100, event.y // 100
        grille[y][x] = 1 if grille[y][x] == 0 else 0
        dessiner_grille()

    def dessiner_grille():
        canvas.delete("all")
        for i in range(taille):
            for j in range(taille):
                couleur = "blue" if grille[j][i] == 1 else "white"
                canvas.create_rectangle(i * 100, j * 100, (i+1) * 100, (j+1) * 100, fill=couleur, outline="black")
        for mx, my in monstres:
            canvas.create_oval(mx * 100 + 40, my * 100 + 40, mx * 100 + 60, my * 100 + 60, fill="red")

    def verifier_solution():
        solution_correcte = all(grille[y][x] == 1 for x, y in monstres)
        messagebox.showinfo("Résultat", "Solution correcte!" if solution_correcte else "Essayez encore!")

    canvas.bind("<Button-1>", placer_tuile)
    dessiner_grille()

    tk.Button(root, text="Vérifier", command=verifier_solution).pack()
    tk.Button(root, text="Réinitialiser", command=lancer_interface).pack()
    root.mainloop()
