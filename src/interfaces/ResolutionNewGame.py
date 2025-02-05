import tkinter as tk
import json
from PIL import Image, ImageTk
from src.solveur import resoudre_defi
from src.interfaces.CreationDefis import CreationDefis

class ResolutionNewGame(tk.Frame):
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
    plateau_path = "data/plateau_nouveau.json"
    pieces_path = "data/pieces_nouvelles.json"

    def __init__(self, controller, counter_values, fichier_pieces=pieces_path):
        super().__init__(controller)
        self.controller = controller
        self.counter_values = counter_values
        self.config(bg="#004A9A")
        
        # Convertir les monstres en format compatible avec le solveur
        defi_monstres = convertir_monstres(counter_values)
        
        # Lancer la résolution
        self.rotation_pieces = resoudre_defi(defi_monstres, fichier_pieces)
        
        # Vérifier si une solution a été trouvée
        is_resolvable = all(value != [] for value in self.rotation_pieces.values())
        print("Solution trouvée!" if is_resolvable else "Aucune solution trouvée.")
        
        # Charger le plateau depuis le fichier JSON
        self.plateau = self.load_plateau(self.plateau_path)
        
        # Définir la taille de la fenêtre
        cell_size = 100
        grid_size = 3 * cell_size
        total_width = (2 * grid_size) + 60
        total_height = (2 * grid_size) + 200
        
        screen_width = self.controller.winfo_screenwidth()
        screen_height = self.controller.winfo_screenheight()
        x_position = (screen_width - total_width) // 2
        y_position = (screen_height - total_height) // 2
        self.controller.geometry(f"{total_width}x{total_height}+{x_position}+{y_position}")
        
        self.grid(row=0, column=0, sticky="nsew")
        
        # Conteneur des grilles
        self.grid_container = tk.Frame(self, bg="#004A9A")
        self.grid_container.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        
        self.frames = [tk.Frame(self.grid_container, borderwidth=2, relief="solid", bg="#004A9A") for _ in range(4)]
        
        for i, frame in enumerate(self.frames):
            frame.grid(row=i // 2, column=i % 2, padx=5, pady=5)
            self.create_grid(frame, i)
        
        # Label de résultat
        self.label_resolvable = tk.Label(
            self, 
            text="RESOLVABLE" if is_resolvable else "NON RESOLVABLE", 
            font=("Arial", 30, "bold"), 
            bg="#004A9A", 
            fg="white" if is_resolvable else "red"
        )
        self.label_resolvable.grid(row=1, column=0, columnspan=2, pady=10)
        
        # Bouton retour
        self.btn_retour = tk.Button(
            self, text="Retour", font=("Arial", 14, "bold"), bg="darkred", fg="white",
            command=self.retour_menu_defis
        )
        self.btn_retour.grid(row=2, column=0, columnspan=2, pady=10)

    def load_plateau(self, json_path):
        try:
            with open(json_path, "r") as file:
                data = json.load(file)
            return data["plateau"]
        except Exception as e:
            print(f"Erreur lors du chargement du fichier JSON : {e}")
            return []

    def create_grid(self, parent, index):
        cell_width, cell_height = 100, 100
        
        try:
            grille_data = self.plateau[index]["cases"]
        except IndexError:
            grille_data = [[-1] * 3 for _ in range(3)]
        
        for row in range(3):
            for col in range(3):
                value = grille_data[row][col]
                image_path = self.images_path[value] if value >= 0 else self.blank_image_path
                image = Image.open(image_path).resize((cell_width, cell_height), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                
                cell = tk.Label(parent, image=photo, borderwidth=1, relief="solid", width=cell_width, height=cell_height, background="#004A9A")
                cell.image = photo
                cell.grid(row=row, column=col)
    
    def retour_menu_defis(self):
        from src.interfaces.SelectionDefis import SelectionDefis
        self.controller.changer_interface(SelectionDefis)


def convertir_monstres(counter_values):
    return {"monstres": [index for index, count in enumerate(counter_values) for _ in range(count)]}
