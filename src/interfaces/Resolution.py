import tkinter as tk
import json
from PIL import Image, ImageTk

class Resolution(tk.Frame):

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

    def __init__(self, controller, json_path="data/plateau1.json"):
        super().__init__(controller)
        self.controller = controller
        self.config(bg="#004A9A")

        # Charger le plateau depuis le fichier JSON
        self.plateau = self.load_plateau(json_path)

        # Définir la largeur et la hauteur de la fenêtre
        cell_size = 100  # Taille d'une cellule
        grid_size = 3 * cell_size  # Une grille fait 3 colonnes x 100 px = 300 px
        total_width = (2 * grid_size) + 60  # Ajustement : 60 px de marge
        total_height = (2 * grid_size) + 200  # Ajustement + place pour le label

        # Modifier la taille de la fenêtre et la centrer
        screen_width = self.controller.winfo_screenwidth()
        screen_height = self.controller.winfo_screenheight()
        x_position = (screen_width - total_width) // 2
        y_position = (screen_height - total_height) // 2
        self.controller.geometry(f"{total_width}x{total_height}+{x_position}+{y_position}")

        # Utiliser `grid()` pour placer `Resolution` correctement
        self.grid(row=0, column=0, sticky="nsew")

        # Créer un conteneur pour les grilles
        self.grid_container = tk.Frame(self, bg="#004A9A")
        self.grid_container.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Créer 4 frames pour les 4 grilles
        self.frames = [tk.Frame(self.grid_container, borderwidth=2, relief="solid", bg="#004A9A") for _ in range(4)]

        # Positionner les frames en grille 2x2
        for i, frame in enumerate(self.frames):
            frame.grid(row=i // 2, column=i % 2, padx=5, pady=5)
            self.create_grid(frame, i)

        # Ajouter un Label "RESOLVABLE" en dessous de la grille
        self.label_resolvable = tk.Label(self, text="RESOLVABLE", font=("Arial", 30, "bold"), bg="#004A9A", fg="white")
        self.label_resolvable.grid(row=1, column=0, columnspan=2, pady=10)
        
        # Bouton retour
        self.btn_retour = tk.Button(self, text="Retour", font=("Arial", 14, "bold"), bg="darkred", fg="white",
                                    command=self.retour_menu_principal)
        self.btn_retour.grid(row=2, column=0, columnspan=2, pady=10)

        # Forcer l'expansion des lignes/colonnes pour le bon positionnement
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=0)

    def load_plateau(self, json_path):
        """Charge le fichier JSON du plateau."""
        try:
            with open(json_path, "r") as file:
                data = json.load(file)
            return data["plateau"]
        except Exception as e:
            print(f"Erreur lors du chargement du fichier JSON : {e}")
            return []

    def create_grid(self, parent, index):
        """Crée une grille 3x3 pour afficher les images."""
        cell_width = 100
        cell_height = 100

        try:
            grille_data = self.plateau[index]["cases"]
        except IndexError:
            grille_data = [[-1] * 3 for _ in range(3)]  # Grille vide si erreur

        for row in range(3):
            for col in range(3):
                value = grille_data[row][col]
                image_path = ""
                if value >= 0:
                    image_path = self.images_path[value]
                else:
                    image_path = self.blank_image_path
                image = Image.open(image_path)
                image = image.resize((cell_width, cell_height), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                cell = tk.Label(parent, image=photo, borderwidth=1, relief="solid", width=cell_width, height=cell_height, background="#004A9A")
                cell.image = photo  # Référence pour éviter la suppression
                cell.grid(row=row, column=col)


    def retour_menu_principal(self):
        """Méthode pour revenir au menu principal"""
        from src.interfaces.MenuPrincipal import MenuPrincipal  # Import différé pour éviter la boucle
        self.controller.changer_interface(MenuPrincipal, resize=True)
