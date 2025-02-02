import json
import random
from pycsp3 import *

def generer_defi():
    # Générer un défi aléatoire
    monstres = [random.randint(0, 7) for _ in range(4)]  # 4 valeurs aléatoires de monstres
    
    # Sauvegarder temporairement le défi
    fichier_defi = "data/defi_temp.json"
    with open(fichier_defi, "w") as f:
        json.dump({"monstres": monstres}, f, indent=4)
    
    print(f"Défi enregistré: {monstres}")
    
    # Tester le défi généré
    resoudre_defi(fichier_defi)

def rotation(piece_originale, rotation):
    piece_tournee = []
    if rotation == 0:
        piece_tournee = piece_originale[:]
    elif rotation == 90:
        piece_tournee = [3 * (piece_originale[i] % 3) + 2 - (piece_originale[i] // 3) for i in range(len(piece_originale))]
    elif rotation == 180:
        piece_tournee = [8 - piece_originale[i] for i in range(len(piece_originale))]
    else:
        piece_tournee = [3 * (2 - (piece_originale[i] % 3)) + (piece_originale[i] // 3) for i in range(len(piece_originale))]
    return piece_tournee

def resoudre_defi(fichier_defis):
    with open(fichier_defis, "r") as f:
        defi = json.load(f)["monstres"]
    
    grille = [
        [-1,1,4,7,-1,0,2,-1,-1],
        [1,5,-1,-1,7,0,2,3,-1],
        [1,4,3,7,0,-1,3,5,6],
        [-1,-1,-1,5,1,6,7,3,0]
    ]
    
    pieces = [
        [0, 1, 3, 4, 5, 7, 8],
        [0, 1, 2, 3, 5, 6, 8],
        [0, 2, 3, 4, 5, 7, 8],
        [0, 2, 3, 4, 5, 6, 8]
    ]
    
    nb_cases_visibles = sum(len(grille[i]) for i in range(len(grille))) - sum(len(pieces[i]) for i in range(len(pieces)))
    cases_visibles = VarArray(size=nb_cases_visibles, dom=range(-1, 8))
    x = VarArray(size=[len(grille), len(pieces)], dom={0, 1})
    r = VarArray(size=[len(pieces)], dom={0, 90, 180, 270})
    
    for j in range(len(pieces)):
        satisfy(Sum([x[i][j] for i in range(len(grille))]) == 1)
    
    for i in range(len(grille)):
        satisfy(Sum([x[i][j] for j in range(len(pieces))]) == 1)
    
    satisfy(Count(cases_visibles, value=monstre) == defi.count(monstre) for monstre in range(8))
    
    cases_visibles_index = 0
    for i in range(len(grille)):
        for j in range(len(pieces)):
            for k in {0, 90, 180, 270}:
                piece_tournee = rotation(pieces[j], k)
                indices_cases_visibles = [l for l in range(len(grille[i])) if piece_tournee.count(l) == 0]
                for l in range(len(indices_cases_visibles)):
                    satisfy(If(both(x[i][j] == 1, r[j] == k), Then=cases_visibles[cases_visibles_index] == grille[i][indices_cases_visibles[l]]))
                    cases_visibles_index += 1
                cases_visibles_index -= len(indices_cases_visibles)
        cases_visibles_index += (len(grille[i]) - len(pieces[0]))
    
    if solve():
        for i in range(len(grille)):
            for j in range(len(pieces)):
                if x[i][j].value == 1:
                    print(f"Sous-grille {i+1}: Pièce {j+1}, Rotation {r[j].value}°")
    else:
        print("Pas de solution trouvée.")

if __name__ == "__main__":
    print("Générer un défi")
    generer_defi()

