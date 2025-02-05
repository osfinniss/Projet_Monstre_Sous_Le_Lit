import json
from src.solveur import resoudre_defi

class NewResolution:
    def __init__(self, fichier_defi, fichier_pieces):
        """
        Initialise la résolution d'un défi.

        :param fichier_defi: Chemin vers le fichier JSON contenant les monstres à trouver.
        :param fichier_pieces: Chemin vers le fichier JSON contenant les pièces disponibles.
        """
        self.fichier_defi = fichier_defi
        self.fichier_pieces = fichier_pieces
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

    def resoudre(self):
        """
        Tente de résoudre le défi en utilisant les pièces disponibles.
        Affiche les résultats sous un format lisible.
        """
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

        print("🔄 Tentative de résolution en cours...")

        # Appel du solveur
        resultat = resoudre_defi({"monstres": monstres}, {"pieces": pieces})


        # Vérification du résultat
        if not resultat or any(not isinstance(val, list) or len(val) != 2 for val in resultat.values()):
            print("❌ Aucun placement valide trouvé ou erreur dans les résultats.")
            return

        # Affichage des résultats de manière organisée
        print("\n✅ Le jeu est résolvable ! Voici les pièces utilisées et leurs rotations :")
        print("----------------------------------------------------")
        for sous_grille, (piece, rotation) in resultat.items():
            print(f"🟢 Sous-grille {sous_grille} -> Pièce {piece}, Rotation {rotation}°")
        print("----------------------------------------------------")

