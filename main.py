from src.solveur import resoudre_defi

def main():

    print("Bienvenue dans le jeu Monstres sous le lit !")
    choix = input("Voulez-vous (1) résoudre un défi ou (2) générer un défi ? ")
    if choix == "1":
        resoudre_defi("data/defis/defi2.json")

if __name__ == "__main__":    
    main()

