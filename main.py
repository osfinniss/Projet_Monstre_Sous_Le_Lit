from src.solveur import resoudre_defi
from src.generateur import generer_defi
from src.interface import lancer_interface

def main():
    print("Bienvenue dans le jeu Monstres sous le lit !")
    choix = input("Voulez-vous (1) résoudre un défi ou (2) générer un défi ? ")
    if choix == "1":
        resoudre_defi("data/defi1.json")
    elif choix == "2":
        generer_defi()
    else:
        print("Choix invalide.")

if __name__ == "__main__":
    main()
    #lancer_interface()

