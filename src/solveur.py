from pycsp3 import *
import json

def resoudre_defi(fichier_defis):
    with open(fichier_defis, "r") as f:
        defi = json.load(f)["defi1"]
    
    plateau = defi["plateau"]
    pieces = defi["pieces"]
    
    x = VarArray(size=len(pieces), dom=range(plateau["taille"]))
    y = VarArray(size=len(pieces), dom=range(plateau["taille"]))
    rotation = VarArray(size=len(pieces), dom=range(4))
    
    satisfy(
        (x[i], y[i], rotation[i]) != (x[j], y[j], rotation[j]) for i in range(len(pieces)) for j in range(i+1, len(pieces))
    )
    
    if solve():
        print("Solution trouvée :")
        print("Positions :", values(x), values(y), values(rotation))
    else:
        print("Aucune solution trouvée.")