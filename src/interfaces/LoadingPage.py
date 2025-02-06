import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import random
import json

class LoadingPage(tk.Frame):
    def __init__(self, controller, counter_values, fichier_pieces, pieces_created):
        super().__init__(controller)
        self.controller = controller
        self.counter_values = counter_values
        self.fichier_pieces = fichier_pieces
        self.pieces_created = pieces_created
        self.config(bg="#004A9A")

        if isinstance(fichier_pieces, str):  # Si on passe un chemin de fichier
            with open(fichier_pieces, "r") as f:
                self.pieces = json.load(f)["pieces"]
        elif isinstance(fichier_pieces, dict):  # Si on passe un objet JSON déjà chargé
            self.pieces = fichier_pieces["pieces"]
        else:
            raise ValueError("Données invalides : fournir un chemin de fichier ou un objet JSON.")


        # Définir la taille de la fenêtre
        new_dimension = (controller.screen_height // 5) * 3
        window_width = new_dimension
        window_height = new_dimension

        # Calculer les positions X et Y pour centrer la fenêtre
        x_position = (controller.screen_width - window_width) // 2
        y_position = (controller.screen_height - window_height) // 2

        # Appliquer la géométrie avec la taille et la position
        controller.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        controller.title("Chargement")
        self.config(bg="#004A9A")

        # Charger le GIF de chargement
        self.gif_path = "data/images/loading.gif"  # Assurez-vous que le chemin du GIF est correct
        self.loading_gif = Image.open(self.gif_path)
        image_resized = self.loading_gif.resize((200, 200), Image.Resampling.LANCZOS)

        # Utiliser ImageSequence pour récupérer les frames du GIF
        self.frames = []
        for frame in ImageSequence.Iterator(self.loading_gif):
            self.frames.append(ImageTk.PhotoImage(frame.copy()))  # Convertir chaque frame en PhotoImage
        
        # Créer un Label pour afficher le GIF
        self.label = tk.Label(self, image=self.frames[0], bg="#004A9A")  # Afficher la première image
        self.label.pack(expand=True)


        label_explications = tk.Label(self, text="Génération de la solution en cours...", font=("Arial", 14, "bold"), bg="#003366", fg="white")
        label_explications.pack(side="top", padx=5, pady=20)

        # Lancer l'animation
        self.animate_gif(0)  # Commencer avec la première frame


        if self.pieces_created:
            print(f"nouveau plateau généré avec les pieces : {self.pieces}")
        else:
            self.nouveau_jeu()


    def animate_gif(self, frame_index):
        """Anime le GIF en passant d'une frame à l'autre."""
        next_frame = (frame_index + 1) % len(self.frames)  # Boucler sur les frames
        self.label.config(image=self.frames[next_frame])  # Mettre à jour l'image du label
        self.after(100, self.animate_gif, next_frame)  # Appeler à nouveau la fonction après 100ms

    


    def nouveau_jeu(self):
        def generer_plateau_aleatoire():
            """Génère un plateau avec au moins les monstres spécifiés."""
            fichier_monstres = "data/new_defi.json"
            try:
                with open(fichier_monstres, "r", encoding="utf-8") as f:
                    monstres = json.load(f).get("monstres", [])
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"Erreur lors du chargement des monstres: {e}")
            monstres = []
            
            plateau = []
            for i in range(4):
                cases = [[random.choice([-1] + list(range(8))) for _ in range(3)] for _ in range(3)]
                for monstre in monstres:
                    x, y = random.randint(0, 2), random.randint(0, 2)
                    cases[x][y] = monstre
                    plateau.append({"grille_id": i + 1, "cases": cases})
            
            return {"plateau": plateau}
        

        # Générer un nouveau plateau
        self.plateau_data = generer_plateau_aleatoire()
        with open("data/plateau_nouveau.json", "w") as f:
            json.dump(self.plateau_data, f, indent=4)
        
        if self.pieces_created:
            print("######### RESOLUTION ##############")

            from src.interfaces.NewResolution import NewResolution
            resolution = NewResolution("data/new_defi.json","data/pieces_nouvelles_created.json",self.controller)
        else:
            # Générer de nouvelles pièces
            pieces_data = {"pieces": [sorted(random.sample(range(9), 6)) for _ in range(4)]}
            with open("data/pieces_nouvelles.json", "w") as f:
                json.dump(pieces_data, f, indent=4)
        
            print("######### RESOLUTION ##############")

            from src.interfaces.NewResolution import NewResolution
            resolution = NewResolution("data/new_defi.json","data/pieces_nouvelles.json",self.controller)

        resolution.resoudre()