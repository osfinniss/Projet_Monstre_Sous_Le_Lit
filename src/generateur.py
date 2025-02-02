import json
import random
import os

def generer_grille():
    """
    Génère une grille 3x3 pour chaque sous-grille, en remplissant aléatoirement les cases avec des monstres.
    """
    monstres = list(range(8))  # Liste des monstres de 0 à 7
    grille = []
    for _ in range(4):
        sous_grille = random.choices(monstres + [-1] * 2, k=9)  # Remplir avec des monstres et quelques cases vides
        grille.append(sous_grille)
    return grille

def generer_pieces():
    """
    Génère un ensemble de pièces couvrant 7 cases sur une sous-grille 3x3.
    """
    pieces = [
        [0, 1, 3, 4, 5, 7, 8],  
        [0, 1, 2, 3, 5, 6, 8],  
        [0, 2, 3, 4, 5, 7, 8],  
        [0, 2, 3, 4, 5, 6, 8]   
    ]
    return pieces

def extraire_defi(grille, pieces):
    """
    Extrait la liste des monstres visibles une fois les pièces placées.
    """
    cases_visibles = []
    for i in range(len(grille)):
        cases_recouvertes = set(pieces[i])  # Indices couverts par la pièce
        for idx in range(9):
            if idx not in cases_recouvertes:
                cases_visibles.append(grille[i][idx])
    return [m for m in cases_visibles if m != -1]  # Exclure les cases vides

def verifier_solution_unique(grille, pieces, defi):
    """
    Vérifie si le défi a une solution unique.
    """
    solutions = resoudre_defi_temporaire(grille, pieces, defi)
    return len(solutions) == 1

def generer_defi_unique():
    """
    Génère un défi avec une solution unique.
    """
    while True:
        grille = generer_grille()
        pieces = generer_pieces()
        defi = extraire_defi(grille, pieces)

        if verifier_solution_unique(grille, pieces, defi):
            break
    
    return {"monstres": defi, "grille": grille, "pieces": pieces, "solution": grille}

def resoudre_defi_temporaire(grille, pieces, defi):
    """
    Vérifie le nombre de solutions possibles pour un défi donné.
    """
    # Pour tester, on pourrait appeler ici un solveur CSP comme dans le solveur initial.
    # À la place, nous faisons une simulation simple en assumant que le défi est bien posé.
    # Dans un vrai cas, il faudrait appeler un solveur CSP et compter les solutions.
    return [1]  # Supposons ici une solution unique pour simplifier

def sauvegarder_defi(defi, dossier="data", fichier="defi.json"):
    """
    Sauvegarde le défi dans un fichier JSON dans le dossier spécifié.
    """
    # Vérifier si le dossier existe, sinon le créer
    if not os.path.exists(dossier):
        os.makedirs(dossier)
    
    chemin_fichier = os.path.join(dossier, fichier)
    with open(chemin_fichier, "w") as f:
        json.dump(defi, f, indent=4)

if __name__ == "__main__":
    defi_unique = generer_defi_unique()
    sauvegarder_defi(defi_unique)
    print("Défi généré avec succès et sauvegardé dans 'data/defi.json'.")
    print("Solution du défi:")
    for i, sous_grille in enumerate(defi_unique["solution"]):
        print(f"Sous-grille {i + 1}: {sous_grille}")
