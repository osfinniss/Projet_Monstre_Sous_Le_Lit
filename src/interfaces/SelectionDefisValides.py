import tkinter as tk
import json
from PIL import Image, ImageTk

class SelectionDefisValides(tk.Frame):
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

        # Frame pour le scrolling
        canvas = tk.Canvas(self)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="#003366")

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Charger les défis
        try:
            with open("data/defis_valides.json", "r") as f:
                challenges_monsters = json.load(f)
        except Exception as e:
            print("Erreur lors de la lecture du fichier des défis validés:", e)
            return
      
        for i, challenge in enumerate(challenges_monsters):
            frame = tk.Frame(scroll_frame, bg="#003366")
            frame.pack(fill="x", pady=5)
            
            label = tk.Label(frame, text=f"Défi n°{i+1}", bg="#003366", fg="white", font=("Arial", 14, "bold"), anchor="w")
            label.pack(side="left", padx=20)
            
            image_frame = tk.Frame(frame, bg="#003366")
            image_frame.pack(side="right", padx=20)
            
            for monster in challenge["monstres"]:
                image = Image.open(self.images_path[monster])
                image_resized = image.resize((100, 100), Image.Resampling.LANCZOS)
                monster_image = ImageTk.PhotoImage(image_resized)
                monster_image_label = tk.Label(image_frame, image=monster_image, width=100, height=100, background="#003366")
                monster_image_label.image = monster_image
                monster_image_label.pack(side="left", padx=5)
            
        btn_retour = tk.Button(self, text="Retour", font=("Arial", 14, "bold"), bg="darkred", fg="white", command=self.retour_menu_principal)
        btn_retour.pack(pady=10)

    def retour_menu_principal(self):
        from src.interfaces.MenuPrincipal import MenuPrincipal
        self.controller.changer_interface(MenuPrincipal, resize=True)
