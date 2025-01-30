# main.py
from src.solveur import resoudre_defi
from src.generateur import generer_defis
from src.interface import lancer_interface

def main():
    print("Bienvenue dans le jeu Monstres sous le lit !")
    print("1. Résoudre des défis")
    print("2. Générer de nouveaux défis")
    print("3. Lancer l'interface graphique")
    
    choix = input("Votre choix (1-3) : ")
    
    if choix == "1":
        resoudre_defi("data/defis.json")
    elif choix == "2":
        nb_defis = int(input("Combien de défis voulez-vous générer ? "))
        generer_defis(nb_defis)
    elif choix == "3":
        lancer_interface()
    else:
        print("Choix invalide.")

if __name__ == "__main__":
    main()