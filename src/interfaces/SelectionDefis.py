import tkinter as tk
from PIL import Image, ImageTk

class SelectionDefis(tk.Frame):
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

        images_path = [
            "data/monsters/diable.png",
            "data/monsters/bat.png",
            "data/monsters/champi.png",
            "data/monsters/troll.png",
            "data/monsters/yeti.png"
        ]

        challenges_monsters = [
            [0, 0, 0, 0],
            [0, 1],
            [0, 0, 2, 3],
            [0, 0, 4, 4]
        ]

        def on_click(frame, defi):
            for i in range(4):
                frames[i].config(bg="#003366")
            frame.config(bg="#0055AA")  # Change la couleur de fond pour montrer la sélection
        
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
                image = Image.open(images_path[monster])
                image_resized = image.resize((100, 100), Image.Resampling.LANCZOS)
                monster_image = ImageTk.PhotoImage(image_resized)

                monster_image_label = tk.Label(image_frame, image=monster_image, width=100, height=100, background="#003366")
                monster_image_label.image = monster_image
                monster_image_label.pack(side="left", padx=5)
            
            btn_overlay = tk.Button(frame, text="", bg="#003366", activebackground="#002244", bd=0, highlightthickness=0, command=lambda f=frame, i=i+1: on_click(f, i))
            btn_overlay.pack(fill="both", expand=True, padx=5, pady=5)

        # Zone pour ajouter un défi
        btn_add_challenge = tk.Button(self, text="+", font=("Arial", 20, "bold"), bg="#003366", fg="white", width=screen_width // 2, command=self.go_to_creation_defi)
        btn_add_challenge.pack(pady=10)

        # Bouton retour
        btn_retour = tk.Button(self, text="Retour", font=("Arial", 14, "bold"), bg="darkred", fg="white", command=self.retour_menu_principal)
        btn_retour.pack(pady=10)

    def retour_menu_principal(self):
        """Méthode pour revenir au menu principal"""
        from src.interfaces.MenuPrincipal import MenuPrincipal  # Import différé pour éviter la boucle
        self.controller.changer_interface(MenuPrincipal, resize=True)

    def go_to_creation_defi(self):
        """Méthode pour aller au menu de création de défi"""
        from src.interfaces.CreationDefis import CreationDefis  # Import différé pour éviter la boucle
        self.controller.changer_interface(CreationDefis, resize=True)

