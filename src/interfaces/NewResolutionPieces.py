import json
import random
import time
from src.solveur import resoudre_defi

class NewResolutionPieces:

    fichier_plateau = "data/plateau1.json"
    fichier_pieces = "data/pieces_nouvelles_created.json"

    def __init__(self, fichier_defi, controller):
        """
        Initialise la résolution d'un défi avec possibilité de regénérer un nouveau jeu si nécessaire.

        :param fichier_defi: Chemin vers le fichier JSON contenant les monstres à trouver.
        :param fichier_pieces: Chemin vers le fichier JSON contenant les pièces disponibles.
        :param controller: Instance du contrôleur de l'application (Tkinter).
        """
        self.fichier_defi = fichier_defi
        self.pieces_data = self.charger_json(self.fichier_pieces)
        self.controller = controller  # Contrôleur Tkinter pour gérer les interfaces
        self.tentative = 0

        print(f"🔍 NewResolution chargée avec {fichier_defi}")

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
        self.fichier_plateau = "data/plateau_nouveau.json"
        with open("data/plateau_nouveau.json", "w") as f:
            json.dump(plateau_data, f, indent=4)

        print("🔄 Nouveau jeu généré automatiquement.")

        return self.resoudre()

    def resoudre(self):
        """
        Tente de résoudre le défi en utilisant les pièces disponibles.
        Si la résolution échoue, génère un nouveau jeu et réessaie jusqu'à obtenir une solution valide.
        """
        while True:
            self.tentative = self.tentative + 1
            print(f"🔄 Tentative de résolution {self.tentative} en cours...")

            # Charger les fichiers JSON
            defi_data = self.charger_json(self.fichier_defi)
            plateau_data = self.charger_json(self.fichier_plateau)

            if not defi_data:
                print("⚠️ Impossible de résoudre le défi en raison d'erreurs de chargement des fichiers.")
                return

            # Extraire les monstres et les pièces
            monstres = defi_data.get("monstres", [])
            pieces = self.pieces_data.get("pieces", [])
            plateau = plateau_data.get("plateau", [])

            if not monstres or not pieces:
                print("⚠️ Erreur : Données de défi ou de pièces manquantes.")
                return

            # Appel du solveur
            resultat = resoudre_defi({"monstres": monstres}, {"pieces": pieces}, {"plateau": plateau} )

            # Vérification du résultat
            if not resultat or any(not isinstance(val, list) or len(val) != 2 for val in resultat.values()):
                print(f"❌ Aucun placement valide trouvé lors de la tentative {self.tentative}. Génération d'un nouveau jeu...")

                self.nouveau_jeu()
                return  # Arrêter la boucle et laisser `self.nouveau_jeu()` relancer `resoudre()`

            # Affichage des résultats une fois une solution trouvée
            print("\n✅ Le jeu est résolvable ! Voici les pièces utilisées et leurs rotations :")
            print("----------------------------------------------------")
            for sous_grille, (piece, rotation) in resultat.items():
                print(f"🟢 Sous-grille {sous_grille} -> Pièce {piece}, Rotation {rotation}°")
            print("----------------------------------------------------")

            # Sortir de la boucle car on a trouvé une solution valide
            return True