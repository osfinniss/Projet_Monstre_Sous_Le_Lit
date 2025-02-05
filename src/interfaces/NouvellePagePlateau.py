import tkinter as tk
from PIL import Image, ImageTk
import json
import random
from tkinter import messagebox

class NouvellePagePlateau(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller
        self.config(bg="#004A9A")

        button_frame = tk.Frame(self, bg="#003366")
        button_frame.pack(expand=True, pady=50)

        self.btn_afficher_plateau = tk.Button(button_frame, text="Afficher le plateau", command=self.afficher_plateau,
                                              font=("Arial", 14, "bold"), bg="green", fg="white", relief="raised", bd=5, padx=20, pady=10)
        self.btn_afficher_plateau.pack(pady=10)

        self.btn_nouveau_jeu = tk.Button(button_frame, text="Générer nouveau jeu", command=self.nouveau_jeu,
                                         font=("Arial", 14, "bold"), bg="cyan", fg="black", relief="raised", bd=5, padx=20, pady=10)
        self.btn_nouveau_jeu.pack(pady=10)

        self.btn_resoudre_nouveau_jeu = tk.Button(button_frame, text="Résoudre un nouveau jeu", command=self.new_resolution,
                                         font=("Arial", 14, "bold"), bg="cyan", fg="black", relief="raised", bd=5, padx=20, pady=10)
        self.btn_resoudre_nouveau_jeu.pack(pady=10)

    def new_resolution(self):
        from src.interfaces.NewResolution import NewResolution
        # resolution = NewResolution("data/new_defi.json", "data/pieces_nouvelles.json")
        resolution = NewResolution("data/new_defi.json", "data/pieces_nouvelles.json", self.controller)

        resolution.resoudre()

        
    def afficher_plateau(self):
        from src.interfaces.AffichagePlateau import AffichagePlateau
        self.controller.changer_interface(AffichagePlateau)

    def generer_plateau_aleatoire(self):
        return {
            "plateau": [
                {"grille_id": i + 1, "cases": [[random.choice([-1] + list(range(8))) for _ in range(3)] for _ in range(3)]}
                for i in range(4)
            ]
        }

    def nouveau_jeu(self):
        plateau_data = self.generer_plateau_aleatoire()
        with open("data/plateau_nouveau.json", "w") as f:
            json.dump(plateau_data, f, indent=4)
        
        pieces_data = {"pieces": [sorted(random.sample(range(9), 6)) for _ in range(4)]}
        with open("data/pieces_nouvelles.json", "w") as f:
            json.dump(pieces_data, f, indent=4)
        
        messagebox.showinfo("Nouveau Jeu", "Un nouveau jeu a été généré avec succès!")

