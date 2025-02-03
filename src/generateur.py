import json
import random
import os
from pycsp3 import *

def rotation(piece_originale, rotation):
    piece_tournee = []
    if rotation == 0:
        return piece_originale[:]
    elif rotation == 90:
        return [3 * (piece % 3) + 2 - (piece // 3) for piece in piece_originale]
    elif rotation == 180:
        return [8 - piece for piece in piece_originale]
    else:
        return [3 * (2 - (piece % 3)) + (piece // 3) for piece in piece_originale]

def generer_defi():
    # Définition de la grille et des pièces
    grille = [
        [-1, 1, 4, 7, -1, 0, 2, -1, -1],
        [1, 5, -1, -1, 7, 0, 2, 3, -1],
        [1, 4, 3, 7, 0, -1, 3, 5, 6],
        [-1, -1, -1, 5, 1, 6, 7, 3, 0]
    ]
    
    pieces = [
        [0, 1, 3, 4, 5, 7, 8],
        [0, 1, 2, 3, 5, 6, 8],
        [0, 2, 3, 4, 5, 7, 8],
        [0, 2, 3, 4, 5, 6, 8]
    ]
    
    # Générer une configuration de placement aléatoire des pièces
    solution_unique = False
    while not solution_unique:
        placement_pieces = random.sample(range(4), 4)
        rotations = [random.choice([0, 90, 180, 270]) for _ in range(4)]
        
        # Déterminer les monstres visibles après placement
        cases_visibles = []
        for i in range(len(grille)):
            piece_placee = rotation(pieces[placement_pieces[i]], rotations[i])
            indices_cases_visibles = [k for k in range(len(grille[i])) if k not in piece_placee]
            cases_visibles.extend(grille[i][k] for k in indices_cases_visibles)
        
        # Générer le défi correspondant
        defi = {"monstres": [cases_visibles.count(i) for i in range(8)]}
        
        # Définir le chemin du fichier dans le dossier data/
        os.makedirs("data", exist_ok=True)
        defi_path = "data/defi_temp.json"
        
        # Sauvegarder le défi temporaire pour le solveur
        with open(defi_path, "w") as f:
            json.dump(defi, f)
        
        # Vérifier si le défi a une solution unique
        if resoudre_defi(defi_path) == 1:
            solution_unique = True
    
    return defi

def resoudre_defi(fichier_defis):
    from solveur import resoudre_defi as solveur_existant
    return solveur_existant(fichier_defis)

def main():
    # Génération d'un défi jouable
    defi_genere = generer_defi()
    print("Défi généré:", defi_genere)

if __name__ == "__main__":
    main()
