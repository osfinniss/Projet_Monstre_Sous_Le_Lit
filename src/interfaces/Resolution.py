import tkinter as tk
import json
from PIL import Image, ImageTk
from src.solveur import resoudre_defi, rotation


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

    plateau_path="data/plateau1.json"

    pieces_path="data/pieces.json"

    def __init__(self, controller, num_defi, counter_values, fichier_pieces, defi_generated):
        super().__init__(controller)
        self.controller = controller
        self.num_defi = num_defi
        self.counter_values = counter_values
        self.is_generated = defi_generated
        self.fichier_pieces = fichier_pieces
        self.config(bg="#004A9A")

        if isinstance(fichier_pieces, str):  # Si on passe un chemin de fichier
            with open(fichier_pieces, "r") as f:
                self.pieces = json.load(f)["pieces"]
        elif isinstance(fichier_pieces, dict):  # Si on passe un objet JSON déjà chargé
            self.pieces = fichier_pieces["pieces"]
        else:
            raise ValueError("Données invalides : fournir un chemin de fichier ou un objet JSON.")

        if self.is_generated:
            with open("data/defis_valides.json", "r") as f:
                defi = json.load(f)[self.num_defi-1]
            self.rotation_pieces = resoudre_defi(defi)

        elif num_defi < 0:
            self.rotation_pieces = resoudre_defi(convertir_monstres(counter_values), fichier_pieces)
        else:
            self.rotation_pieces = resoudre_defi(f"data/defis/defi{self.num_defi}.json", fichier_pieces)

        # Vérifier si toutes les sous-grilles ont une rotation
        self.is_resolvable = all(value != [] for value in self.rotation_pieces.values())

        # Charger le plateau depuis le fichier JSON
        self.plateau = self.load_plateau(self.plateau_path)

        # Définir la largeur et la hauteur de la fenêtre
        cell_size = 100  # Taille d'une cellule
        grid_size = 3 * cell_size  # Une grille fait 3 colonnes x 100 px = 300 px
        if self.is_resolvable:
            total_width = 2 * ((2 * grid_size) + 60)  # Ajustement : 60 px de marge
        else:
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
        if self.is_resolvable:
            self.view_container = tk.Frame(self, bg="#004A9A")
            self.view_container.grid(row=0, column=0, padx=10, pady=10)  # Placer à la première colonne

        self.grid_container = tk.Frame(self, bg="#004A9A")
        self.grid_container.grid(row=0, column=1, padx=10, pady=10)  # Placer à la deuxième colonne

        # Créer 4 frames pour les 4 grilles
        self.frames = [tk.Frame(self.grid_container, borderwidth=2, relief="solid", bg="#004A9A") for _ in range(4)]

        if self.is_resolvable:
            self.frames_view = [tk.Frame(self.view_container, borderwidth=2, relief="solid", bg="#004A9A") for _ in range(4)]

            # Positionner les frames en grille 2x2
            for i, frame in enumerate(self.frames_view):
                frame.grid(row=i // 2, column=i % 2, padx=5, pady=5)
                self.create_grid(frame, i, True)

        # Positionner les frames en grille 2x2
        for i, frame in enumerate(self.frames):
            frame.grid(row=i // 2, column=i % 2, padx=5, pady=5)
            self.create_grid(frame, i, False)

        # Ajouter un Label "(NON) RESOLVABLE" en dessous de la grille
        if self.is_resolvable:
            self.label_resolvable = tk.Label(self, text="RESOLVABLE", font=("Arial", 30, "bold"), bg="#004A9A", fg="white")
        else:
            self.label_resolvable = tk.Label(self, text="NON RESOLVABLE", font=("Arial", 30, "bold"), bg="#004A9A", fg="red")

        self.label_resolvable.grid(row=1, column=0, columnspan=2, pady=10)

        # Bouton retour
        self.btn_retour = tk.Button(self, text="Retour", font=("Arial", 14, "bold"), bg="darkred", fg="white",
                                    command=self.retour_menu_defis)
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

    def create_grid(self, parent, index, is_preview):
        """Crée une grille 3x3 pour afficher les images."""
        cell_width = 100
        cell_height = 100

        try:
            grille_data = self.plateau[index]["cases"]
        except IndexError:
            grille_data = [[-1] * 3 for _ in range(3)]  # Grille vide si erreur

        if self.is_resolvable and not is_preview:
            # Obtenir les informations de pièce et de rotation pour cette grille
            piece_info = self.rotation_pieces.get(index + 1, [])  # index+1 pour correspondre à la grille 1,2,3,4

            piece_num, rotation_angle = piece_info

            piece_tournee = rotation(self.pieces[piece_num-1], rotation_angle)
            for row in range(3):
                for col in range(3):
                    cell_index = row * 3 + col

                    if cell_index in piece_tournee:  # Si la cellule est couverte par la pièce
                        grey_image = Image.open("data/images/grey.png")
                        grey_image = grey_image.resize((cell_width, cell_height), Image.LANCZOS)
                        grey_photo = ImageTk.PhotoImage(grey_image)  # Convertir l'image en PhotoImage
                        cell = tk.Label(parent, image=grey_photo, borderwidth=0, relief="solid", width=cell_width, height=cell_height, background="#004A9A")
                        cell.image = grey_photo  # Assigner l'image à la variable image du Label
                        cell.grid(row=row, column=col)   
                    else:
                        # Obtenir l'image de base de la cellule
                        value = grille_data[row][col]
                        image_path = ""
                        if value >= 0:
                            image_path = self.images_path[value]
                        else:
                            image_path = self.blank_image_path
                        base_image = Image.open(image_path)
                        base_image = base_image.resize((cell_width, cell_height), Image.LANCZOS)
                        base_photo = ImageTk.PhotoImage(base_image)  # Convertir l'image en PhotoImage

                        cell = tk.Label(parent, image=base_photo, borderwidth=0, relief="solid", width=cell_width, height=cell_height, background="#004A9A")
                        cell.image = base_photo  # Assigner l'image à la variable image du Label
                        cell.grid(row=row, column=col)
        else:
            # Si pas de pièce à superposer, afficher la grille normale
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
                    photo = ImageTk.PhotoImage(image)  # Convertir l'image en PhotoImage

                    # Cellules sans pièces sont simplement l'image du monstre
                    cell = tk.Label(parent, image=photo, borderwidth=1, relief="solid", width=cell_width, height=cell_height, background="#004A9A")
                    cell.image = photo  # Assigner l'image à la variable image du Label
                    cell.grid(row=row, column=col)

    
    def retour_menu_defis(self):
        if self.is_generated:
            """Retourne à l'interface de sélection de défis"""
            from src.interfaces.SelectionDefisValides import SelectionDefisValides  # Import différé pour éviter la boucle d'import
            self.controller.changer_interface(SelectionDefisValides)
        else:
            """Retourne à l'interface de sélection de défis"""
            from src.interfaces.SelectionDefis import SelectionDefis  # Import différé pour éviter la boucle d'import
            self.controller.changer_interface(SelectionDefis)

def convertir_monstres(counter_values):
    """Convertit counter_values en une liste de monstres sous forme d'occurrences"""
    monstres = []
    for index, count in enumerate(counter_values):
        monstres.extend([index] * count)  # Ajoute `count` fois le monstre `index+1`
    return {"monstres": monstres}