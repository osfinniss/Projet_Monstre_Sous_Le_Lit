import json
import random

def generer_defi():
    # Générer un défi aléatoire
    monstres = [random.randint(0, 7) for _ in range(4)]  # 4 valeurs aléatoires de monstres
    
    # Sauvegarder temporairement le défi
    fichier_defi = "data/defi_temp.json"
    with open(fichier_defi, "w") as f:
        json.dump({"monstres": monstres}, f, indent=4)
    
    print(f"Défi enregistré: {monstres}")
    exit()  # Quitter immédiatement après l'enregistrement du fichier

if __name__ == "__main__":
    print("Générer un défi")
    generer_defi()
