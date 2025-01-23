import json

def generer_defi():
    defi = {
        "plateau": {"taille": 5, "monstres_visibles": [(1,2), (3,4)]},
        "pieces": [{"forme": [[1, 1], [1, 0]], "rotation": 4}]
    }
    
    with open("data/defis.json", "w") as f:
        json.dump({"defi1": defi}, f, indent=4)
    print("Défi généré avec succès.")