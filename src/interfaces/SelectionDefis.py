import tkinter as tk
import json
from PIL import Image, ImageTk

class SelectionDefis(tk.Frame):

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

    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller

        self.config(bg="#004A9A")

        # Modifier la taille de la fenêtre
        screen_width = self.controller.winfo_screenwidth()
        screen_height = self.controller.winfo_screenheight()
        new_height = (screen_height // 5) * 4
        self.controller.geometry(f"{screen_width // 2}x{new_height}+{(screen_width - (screen_width // 2)) // 2}+{(screen_height - new_height) // 2}")

        frames = []
        challenges_monsters = []

        for i in range(4):
            challenge_path = f"data/defis/defi{i+1}.json"
            with open(challenge_path, "r") as f:
                challenges_monsters.append(json.load(f)["monstres"])
      
        # Création des zones de défis
        for i in range(4):
            frame = tk.Frame(self, bg="#003366", height=new_height // 6, width=screen_width // 2)
            frame.pack_propagate(False)
            frame.pack(fill="x", pady=5)
            frames.append(frame)
            
            label = tk.Label(frame, text=f"Défi n°{i+1}", bg="#003366", fg="white", font=("Arial", 14, "bold"), anchor="w")
            label.pack(side="left", padx=20)
            
            image_frame = tk.Frame(frame, bg="#003366")
            image_frame.pack(side="right", padx=20)
            
            for monster in challenges_monsters[i]:
                image = Image.open(self.images_path[monster])
                image_resized = image.resize((100, 100), Image.Resampling.LANCZOS)
                monster_image = ImageTk.PhotoImage(image_resized)

                monster_image_label = tk.Label(image_frame, image=monster_image, width=100, height=100, background="#003366")
                monster_image_label.image = monster_image
                monster_image_label.pack(side="left", padx=5)
            
            btn_overlay = tk.Button(frame, text="", bg="#003366", activebackground="#002244", bd=0, highlightthickness=0, command=lambda f=frame, i=i+1: self.go_to_resolution_defi(i))
            btn_overlay.pack(fill="both", expand=True, padx=5, pady=5)

        # Zone pour ajouter un défi
        btn_add_challenge = tk.Button(self, text="+", font=("Arial", 20, "bold"), bg="#003366", fg="white", width=screen_width // 2, command=self.go_to_creation_defi)
        btn_add_challenge.pack(pady=10)

        # Bouton retour
        btn_retour = tk.Button(self, text="Retour", font=("Arial", 14, "bold"), bg="darkred", fg="white", command=self.retour_menu_principal)
        btn_retour.pack(pady=10)



    def retour_menu_principal(self):
        from src.interfaces.MenuPrincipal import MenuPrincipal
        self.controller.changer_interface(MenuPrincipal, resize=True)

    def go_to_creation_defi(self):
        from src.interfaces.CreationDefis import CreationDefis
        self.controller.changer_interface(CreationDefis, resize=True)

    def go_to_resolution_defi(self, num_defi):
        from src.interfaces.Resolution import Resolution
        self.controller.changer_interface(Resolution, num_defi=num_defi)

