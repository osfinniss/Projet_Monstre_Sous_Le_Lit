import json
import random
import pandas as pd
import os
from solveur import resoudre_defi  # Import du solveur

# Liste des monstres (indices de 0 à 7)
monstres = ["bat", "champi", "chien", "diable", "dino", "slime", "troll", "yeti"]

# Fonction pour générer des défis valides
def generer_defis(nb_defis=30):
    defis_valides = []
    
    while len(defis_valides) < nb_defis:
        # Générer un défi aléatoire
        defi = {"monstres": random.choices(range(8), k=4)}
        
        # Vérifier si le solveur peut le résoudre
        solution = resoudre_defi(defi)
        
        if solution:  # Si le solveur trouve une solution
            defis_valides.append(defi)

    return defis_valides

# Générer des défis résolubles
defis_valides = generer_defis(30)

# Vérifier si le dossier data existe, sinon le créer
os.makedirs("data", exist_ok=True)

# Sauvegarde dans un fichier JSON
fichier_sortie = "data/defis_valides.json"
with open(fichier_sortie, "w") as f:
    json.dump(defis_valides, f, indent=4)

print(f"Les défis valides ont été sauvegardés dans {fichier_sortie}")