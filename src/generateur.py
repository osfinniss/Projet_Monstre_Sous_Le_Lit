# generateur.py
import json
import random

def generer_defi(id_defi):
    """Génère un défi avec un identifiant spécifique"""
    tailles_possibles = [3, 4, 5]
    taille = random.choice(tailles_possibles)
    
    # Génération aléatoire de monstres
    nb_monstres = random.randint(1, 3)
    monstres_visibles = []
    positions_utilisees = set()
    
    while len(monstres_visibles) < nb_monstres:
        x = random.randint(0, taille-1)
        y = random.randint(0, taille-1)
        if (x, y) not in positions_utilisees:
            monstres_visibles.append([x, y])
            positions_utilisees.add((x, y))
    
    # Génération de pièces aléatoires
    formes_possibles = [
        [[1, 1], [1, 0]],  # L
        [[1, 1], [1, 1]],  # Carré
        [[1, 1, 1]],       # Ligne
        [[1, 1, 1], [0, 1, 0]]  # T
    ]
    
    nb_pieces = random.randint(1, 3)
    pieces = []
    for _ in range(nb_pieces):
        forme = random.choice(formes_possibles)
        pieces.append({
            "forme": forme,
            "rotation": random.randint(0, 3)
        })
    
    return {
        "plateau": {
            "taille": taille,
            "monstres_visibles": monstres_visibles
        },
        "pieces": pieces
    }

def generer_defis(nb_defis=5):
    """Génère plusieurs défis et les sauvegarde dans le fichier JSON"""
    defis = {}
    for i in range(nb_defis):
        defis[f"defi{i+1}"] = generer_defi(i+1)
    
    with open("data/defis.json", "w") as f:
        json.dump(defis, f, indent=4)
    print(f"{nb_defis} défis générés avec succès.")