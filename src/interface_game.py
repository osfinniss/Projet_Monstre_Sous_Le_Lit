import tkinter as tk
from PIL import Image, ImageTk

class Interface:
    def __init__(self, root):
        self.root = root
        self.root.title("Interface avec 4 grilles 3x3")
        
        # Créer 4 frames pour les 4 grilles
        self.frames = [tk.Frame(root, borderwidth=2, relief="solid") for _ in range(4)]
        
        # Positionner les frames dans une grille 2x2
        for i, frame in enumerate(self.frames):
            frame.grid(row=i//2, column=i%2, padx=10, pady=10)
            self.create_grid(frame, i)
    
    def create_grid(self, parent, index):
        # Taille de chaque cellule de la grille
        cell_width = 100
        cell_height = 100
        
        # Dictionnaire des positions et chemins des images pour les grilles
        images_positions = {
            0: {
                (1, 0): "data/monsters/yeti.png",
                (2, 0): "data/monsters/chien.png",
                (0, 1): "data/monsters/champi.png",
                (0, 2): "data/monsters/dino.png",
                (1, 2): "data/monsters/bat.png",
                (0, 0): "data/monsters/blanc.png",
                (1, 1): "data/monsters/blanc.png",
                (2, 1): "data/monsters/blanc.png",
                (2, 2): "data/monsters/blanc.png"

            },

            1: {
                (0, 0): "data/monsters/champi.png",
                (2, 0): "data/monsters/chien.png",
                (0, 1): "data/monsters/slime.png",
                (1, 1): "data/monsters/yeti.png",
                (2, 1): "data/monsters/diable.png",
                (1, 2): "data/monsters/bat.png",
                (0, 2): "data/monsters/blanc.png",
                (2, 2): "data/monsters/blanc.png",
                (1, 0): "data/monsters/blanc.png"

            },
            2: {
                (0, 0): "data/monsters/champi.png",
                (0, 1): "data/monsters/dino.png",
                (0, 2): "data/monsters/diable.png",
                (1, 0): "data/monsters/yeti.png",
                (2, 0): "data/monsters/diable.png",
                (1, 1): "data/monsters/bat.png",
                (2, 1): "data/monsters/slime.png",
                (2, 2): "data/monsters/troll.png",
                (1, 2): "data/monsters/blanc.png"

            },
            3: {
                (1, 0): "data/monsters/slime.png",
                (1, 1): "data/monsters/champi.png",
                (1, 2): "data/monsters/troll.png",
                (2, 0): "data/monsters/yeti.png",
                (2, 1): "data/monsters/diable.png",
                (2, 2): "data/monsters/bat.png",
                (0, 0): "data/monsters/blanc.png",
                (0, 1): "data/monsters/blanc.png",
                (0, 2): "data/monsters/blanc.png"
               
            }
       
        }
        
        # Créer une grille 3x3 dans le parent donné
        for row in range(3):
            for col in range(3):
                if index in images_positions and (row, col) in images_positions[index]:
                    # Charger et redimensionner l'image à la taille de la cellule
                    image_path = images_positions[index][(row, col)]
                    image = Image.open(image_path)
                    image = image.resize((cell_width, cell_height), Image.LANCZOS)
                    photo = ImageTk.PhotoImage(image)
                    cell = tk.Label(parent, image=photo, borderwidth=1, relief="solid", width=cell_width, height=cell_height)
                    cell.image = photo  # Garder une référence de l'image pour éviter qu'elle soit garbage collected
                else:
                    cell = tk.Label(parent, text=f"({row},{col})", borderwidth=1, relief="solid", width=10, height=3)
                cell.grid(row=row, column=col, padx=5, pady=5)