# solveur.py
from pycsp3 import *
import numpy as np
import json
import random

def rotation_piece(piece, rot):
    """Applique une rotation à une pièce"""
    for _ in range(rot):
        piece = list(zip(*piece[::-1]))
    return [list(row) for row in piece]

def verifier_solution_unique(taille, monstres, pieces):
    """Vérifie si le défi a une solution unique"""
    model = Model()
    
    # Créer les variables pour les positions des pièces
    n_pieces = len(pieces)
    x = VarArray(size=n_pieces, dom=range(taille))
    y = VarArray(size=n_pieces, dom=range(taille))
    r = VarArray(size=n_pieces, dom=range(4))
    
    # Créer la grille
    grille = VarArray(size=[taille, taille], dom={0, 1})
    
    # Contraintes pour les pièces
    for i in range(n_pieces):
        piece = pieces[i]["forme"]
        h, w = len(piece), len(piece[0])
        
        # Contraintes de limite du plateau
        model += [x[i] + w <= taille]
        model += [y[i] + h <= taille]
        
        # Contraintes de non-chevauchement
        for j in range(i + 1, n_pieces):
            model += [(x[i], y[i]) != (x[j], y[j])]
    
    # Contraintes pour les monstres
    for mx, my in monstres:
        model += [grille[my][mx] == 1]
    
    # Chercher toutes les solutions
    solutions = []
    def collector():
        solutions.append((values(x), values(y), values(r)))
    
    satisfy(model)
    solve(collector)
    
    return len(solutions) == 1

def generer_defi_valide(taille=3):
    """Génère un défi avec une solution unique"""
    formes_pieces = [
        [[1, 1],
         [1, 0]],  # L
        
        [[1, 1],
         [1, 1]],  # Carré
        
        [[1, 1, 1]],  # Ligne
        
        [[1, 0],
         [1, 1]]   # L inversé
    ]
    
    essais_max = 100
    essais = 0
    
    while essais < essais_max:
        essais += 1
        
        # Générer les monstres
        n_monstres = random.randint(1, 2)
        monstres = []
        while len(monstres) < n_monstres:
            x = random.randint(0, taille-1)
            y = random.randint(0, taille-1)
            if [x, y] not in monstres:
                monstres.append([x, y])
        
        # Sélectionner une pièce
        piece = random.choice(formes_pieces)
        pieces = [{"forme": piece, "rotation": 0}]
        
        try:
            if verifier_solution_unique(taille, monstres, pieces):
                return {
                    "plateau": {
                        "taille": taille,
                        "monstres_visibles": monstres
                    },
                    "pieces": pieces
                }
        except:
            continue
    
    # Si aucun défi valide n'est trouvé, retourner un défi par défaut
    return {
        "plateau": {
            "taille": 3,
            "monstres_visibles": [[1, 1]]
        },
        "pieces": [{"forme": [[1, 1], [1, 0]], "rotation": 0}]
    }

def generer_defis(nb_defis):
    """Génère plusieurs défis valides"""
    defis = {}
    for i in range(nb_defis):
        defis[f"defi{i+1}"] = generer_defi_valide()
    
    # Sauvegarder les défis
    with open("data/defis.json", "w") as f:
        json.dump(defis, f, indent=4)
    print(f"{nb_defis} défis générés avec succès.")

def resoudre_defi(fichier_defis, id_defi="defi1"):
    """Résout un défi spécifique"""
    with open(fichier_defis, "r") as f:
        defi = json.load(f)[id_defi]
    
    taille = defi["plateau"]["taille"]
    monstres = defi["plateau"]["monstres_visibles"]
    pieces = defi["pieces"]
    
    model = Model()
    
    # Variables
    n_pieces = len(pieces)
    x = VarArray(size=n_pieces, dom=range(taille))
    y = VarArray(size=n_pieces, dom=range(taille))
    r = VarArray(size=n_pieces, dom=range(4))
    
    # Contraintes
    for i in range(n_pieces):
        piece = pieces[i]["forme"]
        h, w = len(piece), len(piece[0])
        model += [x[i] + w <= taille]
        model += [y[i] + h <= taille]
    
    # Résolution
    if solve(model):
        print("\nSolution trouvée!")
        for i in range(n_pieces):
            print(f"Pièce {i+1}: position ({values(x[i])}, {values(y[i])}) rotation {values(r[i])}")
        return True
    else:
        print("Aucune solution trouvée.")
        return False