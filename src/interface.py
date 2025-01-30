# interface.py
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json

def charger_defis():
    with open("data/defis.json", "r") as f:
        return json.load(f)

class InterfaceJeu:
    def __init__(self, root):
        self.root = root
        self.root.title("Monstres sous le lit")
        self.defis = charger_defis()
        self.defi_actuel = None
        self.canvas_list = []
        self.grille_list = []
        
        # Création du sélecteur de défi
        frame_selection = tk.Frame(root)
        frame_selection.grid(row=0, column=0, columnspan=2, pady=10)
        
        tk.Label(frame_selection, text="Sélectionner un défi:").pack(side=tk.LEFT)
        self.combo_defis = ttk.Combobox(frame_selection, values=list(self.defis.keys()))
        self.combo_defis.pack(side=tk.LEFT, padx=5)
        self.combo_defis.bind('<<ComboboxSelected>>', self.charger_defi)
        
        # Zone de jeu
        self.frame_jeu = tk.Frame(root)
        self.frame_jeu.grid(row=1, column=0, columnspan=2)
        
        # Boutons
        self.frame_boutons = tk.Frame(root)
        self.frame_boutons.grid(row=2, column=0, columnspan=2)
        
        # Sélectionner le premier défi par défaut
        if self.defis:
            self.combo_defis.set(list(self.defis.keys())[0])
            self.charger_defi(None)

    def charger_defi(self, event):
        defi_id = self.combo_defis.get()
        self.defi_actuel = self.defis[defi_id]
        self.reinitialiser_interface()

    def reinitialiser_interface(self):
        # Nettoyer l'interface existante
        for widget in self.frame_jeu.winfo_children():
            widget.destroy()
        for widget in self.frame_boutons.winfo_children():
            widget.destroy()
            
        self.canvas_list = []
        self.grille_list = []
        taille = self.defi_actuel["plateau"]["taille"]
        
        # Créer les nouvelles grilles
        for k in range(4):
            canvas = tk.Canvas(self.frame_jeu, width=300, height=300)
            canvas.grid(row=k//2, column=k%2, padx=20, pady=20)
            self.canvas_list.append(canvas)
            grille = [[0 for _ in range(taille)] for _ in range(taille)]
            self.grille_list.append(grille)
            canvas.bind("<Button-1>", lambda event, index=k: self.placer_tuile(event, index))
            
        # Recréer les boutons
        tk.Button(self.frame_boutons, text="Rotation Gauche", command=self.rotation_gauche).grid(row=0, column=0, pady=20, padx=5)
        tk.Button(self.frame_boutons, text="Rotation Droite", command=self.rotation_droite).grid(row=0, column=1, pady=20, padx=5)
        tk.Button(self.frame_boutons, text="Vérifier", command=self.verifier_solution).grid(row=0, column=2, pady=20, padx=5)
        tk.Button(self.frame_boutons, text="Réinitialiser", command=lambda: self.charger_defi(None)).grid(row=0, column=3, pady=20, padx=5)
        
        # Dessiner les grilles
        for i in range(4):
            self.dessiner_grille(i)

    def placer_tuile(self, event, canvas_index):
        taille_case = 300 // self.defi_actuel["plateau"]["taille"]
        x, y = event.x // taille_case, event.y // taille_case
        if x < len(self.grille_list[canvas_index]) and y < len(self.grille_list[canvas_index]):
            self.grille_list[canvas_index][y][x] = 1 if self.grille_list[canvas_index][y][x] == 0 else 0
            self.dessiner_grille(canvas_index)

    def dessiner_grille(self, canvas_index):
        canvas = self.canvas_list[canvas_index]
        grille = self.grille_list[canvas_index]
        taille = self.defi_actuel["plateau"]["taille"]
        taille_case = 300 // taille
        
        canvas.delete("all")
        for i in range(taille):
            for j in range(taille):
                couleur = "blue" if grille[j][i] == 1 else "white"
                canvas.create_rectangle(
                    i * taille_case, j * taille_case,
                    (i+1) * taille_case, (j+1) * taille_case,
                    fill=couleur, outline="black"
                )
                
        # Dessiner les monstres
        monstres = self.defi_actuel["plateau"]["monstres_visibles"]
        for mx, my in monstres:
            canvas.create_oval(
                mx * taille_case + taille_case*0.4,
                my * taille_case + taille_case*0.4,
                mx * taille_case + taille_case*0.6,
                my * taille_case + taille_case*0.6,
                fill="red"
            )

    def rotation_gauche(self):
        for grille in self.grille_list:
            grille[:] = [list(reversed(col)) for col in zip(*grille)]
        for i in range(4):
            self.dessiner_grille(i)

    def rotation_droite(self):
        for grille in self.grille_list:
            grille[:] = [list(col) for col in zip(*reversed(grille))]
        for i in range(4):
            self.dessiner_grille(i)

    def verifier_solution(self):
        monstres = self.defi_actuel["plateau"]["monstres_visibles"]
        solution_correcte = all(self.grille_list[grid_idx][y][x] == 1 
                              for grid_idx in range(4)
                              for x, y in monstres)
        messagebox.showinfo("Résultat", 
                          "Solution correcte!" if solution_correcte else "Essayez encore!")

def lancer_interface():
    root = tk.Tk()
    app = InterfaceJeu(root)
    root.mainloop()