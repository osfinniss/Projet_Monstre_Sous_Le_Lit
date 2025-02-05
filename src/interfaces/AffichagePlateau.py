import tkinter as tk
import json
from PIL import Image, ImageTk
from src.interfaces.MenuPrincipal import MenuPrincipal

class AffichagePlateau(tk.Frame):
    images_path = [
        "data/images/monsters/bat.png",
        "data/images/monsters/champi.png",
        "data/images/monsters/chien.png",
        "data/images/monsters/diable.png",
        "data/images/monsters/dino.png",
        "data/images/monsters/slime.png",
        "data/images/monsters/troll.png",
        "data/images/monsters/yeti.png"
    ]

    blank_image_path = "data/images/blank.png"
    
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller
        self.config(bg="#004A9A")
        
        self.plateau = self.load_plateau("data/plateau_aleatoire.json")
        
        self.grid_container = tk.Frame(self, bg="#004A9A")
        self.grid_container.pack()
        
        self.frames = [tk.Frame(self.grid_container, borderwidth=2, relief="solid", bg="#004A9A") for _ in range(4)]
        
        for i, frame in enumerate(self.frames):
            frame.grid(row=i // 2, column=i % 2, padx=5, pady=5)
            self.create_grid(frame, i)
        
        self.btn_retour = tk.Button(self, text="Retour", font=("Arial", 14, "bold"), bg="darkred", fg="white",
                                    command=self.retour_menu_principal)
        self.btn_retour.pack(pady=10)
    
    def load_plateau(self, json_path):
        try:
            with open(json_path, "r") as file:
                data = json.load(file)
            return data["plateau"]
        except Exception as e:
            print(f"Erreur lors du chargement du fichier JSON : {e}")
            return []
    
    def create_grid(self, parent, index):
        cell_size = 100
        try:
            grille_data = self.plateau[index]["cases"]
        except IndexError:
            grille_data = [[-1] * 3 for _ in range(3)]
        
        for row in range(3):
            for col in range(3):
                value = grille_data[row][col]
                if value >= 0:
                    image_path = self.images_path[value]
                else:
                    image_path = self.blank_image_path
                
                image = Image.open(image_path)
                image = image.resize((cell_size, cell_size), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                cell = tk.Label(parent, image=photo, borderwidth=1, relief="solid", width=cell_size, height=cell_size, background="#004A9A")
                cell.image = photo
                cell.grid(row=row, column=col)
    
    def retour_menu_principal(self):
        self.controller.changer_interface(MenuPrincipal)
