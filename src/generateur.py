import json
import random
import pandas as pd
import os
from solveur import resoudre_defi 

monstres = ["bat", "champi", "chien", "diable", "dino", "slime", "troll", "yeti"]

def generer_defis(nb_defis=3):
    defis_valides = []
    
    while len(defis_valides) < nb_defis:
        nb_monstres = random.randint(2, 8)
        defi = {"monstres": random.choices(range(8), k=nb_monstres)}
        
        resultat = resoudre_defi(defi)

        is_resolvable = all(value != [] for value in resultat.values())
        
        if is_resolvable and defi not in defis_valides:
            defis_valides.append(defi)

    return defis_valides

defis_valides = generer_defis(3)

os.makedirs("data", exist_ok=True)

fichier_sortie = "data/defis_valides.json"
with open(fichier_sortie, "w") as f:
    json.dump(defis_valides, f, indent=4)

print(f"Les défis valides ont été sauvegardés dans {fichier_sortie}")