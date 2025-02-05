import tkinter as tk
from PIL import Image, ImageTk

class OptionsGeneration(tk.Frame):

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

    def __init__(self, controller, counter_values):
        super().__init__(controller)
        self.controller = controller
        self.counter_values = counter_values
        self.config(bg="#004A9A")

        # if num_defi < 0:
        #     self.rotation_pieces = resoudre_defi(convertir_monstres(counter_values))
        # else:
        #     self.rotation_pieces = resoudre_defi(f"data/defis/defi{self.num_defi}.json")


        # Modifier la taille de la fenêtre
        new_height = (controller.screen_height // 5) * 3
        new_width = (controller.screen_height // 5) * 4
        controller.geometry(f"{new_width}x{new_height}+{controller.x_position}+{(controller.screen_height - new_height) // 2}")


        # Créer un cadre principal qui contiendra les boutons
        self.main_frame = tk.Frame(self, bg="#003366")
        self.main_frame.pack(fill="both", expand=True, pady=50)

        self.image_frame = tk.Frame(self.main_frame, bg="#003366")
        self.image_frame.pack(side="top", expand=True, pady=50)

        for index in range(len(self.counter_values)):
            for _ in range(self.counter_values[index]):
                image = Image.open(self.images_path[index])
                image_resized = image.resize((100, 100), Image.Resampling.LANCZOS)
                monster_image = ImageTk.PhotoImage(image_resized)

                monster_image_label = tk.Label(self.image_frame, image=monster_image, width=100, height=100, background="#003366")
                monster_image_label.image = monster_image
                monster_image_label.pack(side="left", padx=5)

        label_explications = tk.Label(self.main_frame, text="Pour ce défi, générer :", font=("Arial", 14, "bold"), bg="#003366", fg="white")
        label_explications.pack(side="top", padx=5, pady=20)

        # Bouton Générer uniquement un nouveau plateau
        btn_plateau = tk.Button(self.main_frame, text="Nouveau plateau et pièces", font=("Arial", 14, "bold"), bg="blue", fg="white",
                               command=lambda: self.resoudre_avec_generations(False), width=50)
        btn_plateau.pack(side="top", padx=5, pady=20)

        # Bouton Générer uniquement de nouvelles pièces
        btn_pieces = tk.Button(self.main_frame, text="Nouveau plateau et pièces à créer soit-même", font=("Arial", 14, "bold"), bg="blue", fg="white",
                               command=lambda: self.resoudre_avec_generations(True), width=50)
        btn_pieces.pack(side="top", padx=5, pady=20)


        # Bouton Retour
        btn_retour = tk.Button(self, text="Retour", font=("Arial", 14, "bold"), bg="darkred", fg="white",
                               command=self.retour_menu_defis, width=20)
        btn_retour.pack(side="bottom", padx=5, pady=20)


    def resoudre_avec_generations(self, nouvellesPieces):
        if nouvellesPieces:
            from src.interfaces.CreationPieces import CreationPieces  # Import différé pour éviter la boucle d'import
            self.controller.changer_interface(CreationPieces, num_defi=-1, counter_values=self.counter_values)
        

    def retour_menu_defis(self):
        """Retourne à l'interface de sélection de défis"""
        from src.interfaces.SelectionDefis import SelectionDefis  # Import différé pour éviter la boucle d'import
        self.controller.changer_interface(SelectionDefis)
