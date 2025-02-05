from pycsp3 import *
import json

pieces_path = "data/pieces.json"

#Renvoie la version de la pièce sur laquelle on a appliqué la rotation indiquée en paramètre
#On suppose qu'une sous-grille est de taille 3*3
def rotation(piece_originale,rotation):
    piece_tournee =[]

    #Si la rotation est de 0°, on renvoie une pièce identique à la pièce originale
    if rotation==0:
        for i in range(len(piece_originale)):
            piece_tournee.append(piece_originale[i])
    #Si la rotation est de 90°
    elif rotation==90:
        for i in range(len(piece_originale)):
            piece_tournee.append(3 * (piece_originale[i]%3) + 2 - (piece_originale[i]//3))
    #Si la rotation est de 180°
    elif rotation==180:
        for i in range(len(piece_originale)):
            piece_tournee.append(8-piece_originale[i])
    #Sinon, la rotation est de 270°
    else:
        for i in range(len(piece_originale)):
            piece_tournee.append(3 * (2 - (piece_originale[i] % 3)) + (piece_originale[i] // 3))
    return piece_tournee

def resoudre_defi(fichier_defis, fichier_pieces=pieces_path):
    """Résout un défi à partir d'un fichier JSON ou d'une structure JSON en mémoire"""

    clear()
    
    if isinstance(fichier_defis, str):  # Si on passe un chemin de fichier
        with open(fichier_defis, "r") as f:
            defi = json.load(f)["monstres"]
    elif isinstance(fichier_defis, dict):  # Si on passe un objet JSON déjà chargé
        defi = fichier_defis["monstres"]
    else:
        raise ValueError("Données invalides : fournir un chemin de fichier ou un objet JSON.")

    
    for i in range(len(defi)):
        print("defi[",i,"] vaut ", defi[i])
    
    #On représente la grille par 4 sous-grilles avec 9 cases
    #Chaque entier représentera un monstre, -1 représentera une case vide
    #Monstres:
    #0=bat
    #1=champi
    #2=chien
    #3=diable
    #4=dino
    #5=slime
    #6=troll
    #7=yeti

    grille = [
        [-1,1,4,7,-1,0,2,-1,-1],
        [1,5,-1,-1,7,0,2,3,-1],
        [1,4,3,7,0,-1,3,5,6],
        [-1,-1,-1,5,1,6,7,3,0]
    ]

    #Chaque pièce est représentée par les indices des cases qu'elles recouvrent dans une sous-grille

    # Récupérer les pièces
    if isinstance(fichier_pieces, str):  # Si on passe un chemin de fichier
        with open(fichier_pieces, "r") as f:
            pieces = json.load(f)["pieces"]
    elif isinstance(fichier_pieces, dict):  # Si on passe un objet JSON déjà chargé
        pieces = fichier_pieces["pieces"]
    else:
        raise ValueError("Données invalides : fournir un chemin de fichier ou un objet JSON.")

    # Pièces de test, qui ne nécessitent pas de rotation pour le défi 1
    # pieces = [
    #     [0, 1, 2, 3, 5, 6, 8],
    #     [0, 1, 3, 4, 5, 6, 8],
    #     [0, 1, 3, 4, 5, 7, 8],
    #     [0, 2, 3, 4, 5, 6, 8]
    # ]

    # Nombre de cases visibles
    nb_cases_visibles = sum(len(grille[i]) for i in range(len(grille))) - sum(len(pieces[i]) for i in range(len(pieces)))

    # Variables de décision :
    cases_visibles = VarArray(size=nb_cases_visibles, dom=range(-1, 8))
        # cases_visibles contient les valeurs de toutes les cases visibles en fonction du placement des pièces,
        # Toutes les cases non vides dans cases_visibles doivent former une permutation de defi pour résoudre le problème
    x = VarArray(size=[len(grille), len(pieces)], dom={0, 1})  # x[i][j] = 1 si la pièce j est placée sur la sous-grille i, sinon 0
    r = VarArray(size=[len(pieces)], dom={0,90,180,270})  # r[i] = la valeur de la rotation adoptée pour la pièce i (0,90,180,270)

    # Contrainte : chaque pièce doit être placée exactement une fois
    for j in range(len(pieces)):
        satisfy(Sum([x[i][j] for i in range(len(grille))]) == 1)

    # Contrainte : chaque grille doit avoir exactement une pièce
    for i in range(len(grille)):
        satisfy(Sum([x[i][j] for j in range(len(pieces))]) == 1)

    # Contrainte : cases_visibles doit contenir chaque monstre autant de fois qu'il est présent dans defi
    satisfy(Count(cases_visibles,value = monstre) == defi.count(monstre) for monstre in range(8))

    # # Contrainte des cases visibles sans rotation
    # # Contrainte : cases_visibles contient les cases qui sont visibles (non couvertes) en fonction du placement des pièces
    # cases_visibles_index = 0
    # for i in range(len(grille)):
    #     for j in range(len(pieces)):
    #         indices_cases_visibles = [k for k in range(len(grille[i])) if pieces[j].count(k)==0]
    #         for k in range(len(indices_cases_visibles)):
    #             satisfy(If(x[i][j]==1,Then = cases_visibles[cases_visibles_index] == grille[i][indices_cases_visibles[k]]))
    #             cases_visibles_index+=1

    # Contrainte des cases visibles avec rotation
    # Contrainte : cases_visibles contient les cases qui sont visibles (non couvertes) en fonction du placement des pièces
    cases_visibles_index = 0
    for i in range(len(grille)):
        for j in range(len(pieces)):
            for k in [0,90,180,270]:
                piece_tournee=rotation(pieces[j],k)
                indices_cases_visibles = [l for l in range(len(grille[i])) if piece_tournee.count(l)==0]
                for l in range(len(indices_cases_visibles)):
                    satisfy(If(both(x[i][j]==1,r[j]==k),Then = cases_visibles[cases_visibles_index] == grille[i][indices_cases_visibles[l]]))
                    cases_visibles_index+=1
                cases_visibles_index-=len(indices_cases_visibles)
        #On suppose que toutes les pièces couvrent le même nombre de cases
        cases_visibles_index+=(len(grille[i])-len(pieces[0]))

    # Résolution
    if solve():

        pieces_rotation = {
            1: [],
            2: [],
            3: [],
            4: []
        }

        # Affichage des résultats
        for i in range(len(grille)):
            for j in range(len(pieces)):
                # print("x[",i,"][",j,"]=",x[i][j].value)
                if x[i][j].value==1:
                    print(f"Sous-grille ",i+1,": Pièce utilisée -> ",j+1,", Rotation utilisée -> ",r[j].value,"°")
                    pieces_rotation[i+1] = [j+1, r[j].value]
    else:
        print("Pas de solution trouvée.")
    
    return pieces_rotation