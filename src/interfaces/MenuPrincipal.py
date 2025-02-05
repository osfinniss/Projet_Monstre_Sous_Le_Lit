import tkinter as tk
import json
import random
from tkinter import messagebox
from src.generateur_defis import GenerateurDefis

class MenuPrincipal(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller
        self.config(bg="#004A9A")

        # Redimensionner la fenêtre à sa taille d'origine
        controller.geometry(f"{controller.window_width}x{controller.window_height}+{controller.x_position}+{controller.y_position}")

        # Chargement du titre du jeu
        image_path = "data/images/title.png"
        try:
            self.logo = tk.PhotoImage(file=image_path)
            self.logo_label = tk.Label(self, image=self.logo, bg="#004A9A", borderwidth=0, highlightthickness=0)
            self.logo_label.pack(pady=10)
        except Exception as e:
            print("Impossible de charger l'image:", e)

        # Cadre pour les boutons
        button_frame = tk.Frame(self, bg="#004A9A")
        button_frame.pack(expand=True)

        # Création des boutons
        self.btn_resoudre = tk.Button(button_frame, text="Résoudre un défi", command=self.go_to_defis,
                                      font=("Arial", 14, "bold"), bg="purple", fg="white", relief="raised", bd=5, padx=20, pady=10)
        self.btn_generer = tk.Button(button_frame, text="Générer un défi", command=self.choisir_parametres_generateur,
                                     font=("Arial", 14, "bold"), bg="purple", fg="white", relief="raised", bd=5, padx=20, pady=10)
        self.btn_creer_plateau = tk.Button(button_frame, text="Générer un plateau", command=self.go_to_creation_plateau,
                                           font=("Arial", 14, "bold"), bg="blue", fg="white", relief="raised", bd=5, padx=20, pady=10)
        self.btn_afficher_plateau = tk.Button(button_frame, text="Afficher le plateau", command=self.afficher_plateau,
                                              font=("Arial", 14, "bold"), bg="green", fg="white", relief="raised", bd=5, padx=20, pady=10)
        self.btn_quitter = tk.Button(button_frame, text="Quitter", command=controller.quit,
                                     font=("Arial", 14, "bold"), bg="red", fg="white", relief="raised", bd=5, padx=20, pady=10)

        # Placement des boutons
        self.btn_resoudre.pack(pady=10)
        self.btn_generer.pack(pady=10)
        self.btn_creer_plateau.pack(pady=10)
        self.btn_afficher_plateau.pack(pady=10)
        self.btn_quitter.pack(pady=10)

    def go_to_defis(self):
        from src.interfaces.SelectionDefis import SelectionDefis
        self.controller.changer_interface(SelectionDefis, resize=True)
    
    def choisir_parametres_generateur(self):
        self.controller.changer_interface(GenerateurDefis)

    def go_to_creation_plateau(self):
        plateau_data = self.generer_plateau_aleatoire()
        with open("data/plateau_aleatoire.json", "w") as f:
            json.dump(plateau_data, f, indent=4)
        messagebox.showinfo("Succès", "Plateau généré et sauvegardé avec succès!")
    
    def generer_plateau_aleatoire(self):
        return {
            "plateau": [
                {"grille_id": i + 1, "cases": [[random.choice([-1] + list(range(8))) for _ in range(3)] for _ in range(3)]}
                for i in range(4)
            ]
        }
    
    def afficher_plateau(self):
        from src.interfaces.AffichagePlateau import AffichagePlateau
        self.controller.changer_interface(AffichagePlateau)