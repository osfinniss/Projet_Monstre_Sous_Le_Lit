import json
import random
import time
from tkinter import messagebox
from src.solveur import resoudre_defi

class NewResolution:
    def __init__(self, fichier_defi, fichier_pieces, controller):
        """
        Initialise la résolution d'un défi avec possibilité de regénérer un nouveau jeu si nécessaire.

        :param fichier_defi: Chemin vers le fichier JSON contenant les monstres à trouver.
        :param fichier_pieces: Chemin vers le fichier JSON contenant les pièces disponibles.
        :param controller: Instance du contrôleur de l'application (Tkinter).
        """
        self.fichier_defi = fichier_defi
        self.fichier_pieces = fichier_pieces
        self.controller = controller  # Contrôleur Tkinter pour gérer les interfaces
        print(f"🔍 NewResolution chargée avec {fichier_defi} et {fichier_pieces}")

    def charger_json(self, fichier):
        """
        Charge un fichier JSON et retourne son contenu.

        :param fichier: Chemin du fichier JSON à charger.
        :return: Contenu du fichier JSON sous forme de dictionnaire ou None en cas d'erreur.
        """
        try:
            with open(fichier, "r") as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            print(f"❌ Erreur : Le fichier {fichier} n'existe pas.")
        except json.JSONDecodeError:
            print(f"❌ Erreur : Le fichier {fichier} est mal formaté.")
        return None

    def generer_plateau_aleatoire(self):
        """
        Génère un plateau aléatoire avec des monstres placés aléatoirement.

        :return: Dictionnaire représentant un plateau aléatoire.
        """
        return {
            "plateau": [
                {"grille_id": i + 1, "cases": [[random.choice([-1] + list(range(8))) for _ in range(3)] for _ in range(3)]}
                for i in range(4)
            ]
        }

    def nouveau_jeu(self):
        """
        Génère un nouveau plateau et de nouvelles pièces, les enregistre dans des fichiers JSON,
        puis relance automatiquement la résolution.
        """
        plateau_data = self.generer_plateau_aleatoire()
        with open("data/plateau_nouveau.json", "w") as f:
            json.dump(plateau_data, f, indent=4)
        
        pieces_data = {"pieces": [sorted(random.sample(range(9), 6)) for _ in range(4)]}
        with open("data/pieces_nouvelles.json", "w") as f:
            json.dump(pieces_data, f, indent=4)

        print("🔄 Nouveau jeu généré automatiquement.")

        # Afficher un message et cliquer automatiquement sur "OK" après 1 seconde
        self.controller.after(1000, lambda: self.resoudre())

    def resoudre(self):
        """
        Tente de résoudre le défi en utilisant les pièces disponibles.
        Si la résolution échoue, génère un nouveau jeu et réessaie jusqu'à obtenir une solution valide.
        """
        tentative = 1
        while True:
            print(f"🔄 Tentative de résolution {tentative} en cours...")

            # Charger les fichiers JSON
            defi_data = self.charger_json(self.fichier_defi)
            pieces_data = self.charger_json(self.fichier_pieces)

            if not defi_data or not pieces_data:
                print("⚠️ Impossible de résoudre le défi en raison d'erreurs de chargement des fichiers.")
                return

            # Extraire les monstres et les pièces
            monstres = defi_data.get("monstres", [])
            pieces = pieces_data.get("pieces", [])

            if not monstres or not pieces:
                print("⚠️ Erreur : Données de défi ou de pièces manquantes.")
                return

            # Appel du solveur
            resultat = resoudre_defi({"monstres": monstres}, {"pieces": pieces})

            # Vérification du résultat
            if not resultat or any(not isinstance(val, list) or len(val) != 2 for val in resultat.values()):
                print(f"❌ Aucun placement valide trouvé lors de la tentative {tentative}. Génération d'un nouveau jeu...")

                # Afficher le messagebox avec un clic automatique sur OK
                self.controller.after(500, lambda: messagebox.showinfo("Nouveau Jeu", "Un nouveau jeu a été généré car l'ancien n'était pas résolvable."))
                self.controller.after(1500, lambda: self.nouveau_jeu())  # Générer un nouveau jeu après 1,5s
                return  # Arrêter la boucle et laisser `self.nouveau_jeu()` relancer `resoudre()`

            # Affichage des résultats une fois une solution trouvée
            print("\n✅ Le jeu est résolvable ! Voici les pièces utilisées et leurs rotations :")
            print("----------------------------------------------------")
            for sous_grille, (piece, rotation) in resultat.items():
                print(f"🟢 Sous-grille {sous_grille} -> Pièce {piece}, Rotation {rotation}°")
            print("----------------------------------------------------")

            # Sortir de la boucle car on a trouvé une solution valide
            break