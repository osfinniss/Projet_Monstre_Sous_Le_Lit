import tkinter as tk

class MenuPrincipal(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller
        self.config(bg="#004A9A")

        # Redimensionner la fenêtre à sa taille d'origine
        controller.geometry(f"{controller.window_width}x{controller.window_height}+{controller.x_position}+{controller.y_position}")


        # Chargement du titre du jeu
        image_path = "data/images/title.png"
        try:
            self.logo = tk.PhotoImage(file=image_path)
            self.logo_label = tk.Label(self, image=self.logo, bg="#004A9A", borderwidth=0, highlightthickness=0)
            self.logo_label.pack(pady=10)
        except Exception as e:
            print("Impossible de charger l'image:", e)

        # Cadre pour les boutons
        button_frame = tk.Frame(self, bg="#004A9A")
        button_frame.pack(expand=True)

        # Création des boutons
        self.btn_resoudre = tk.Button(button_frame, text="Résoudre un défi", command=self.go_to_defis,
                                      font=("Arial", 14, "bold"), bg="purple", fg="white", relief="raised", bd=5, padx=20, pady=10)
        self.btn_generer = tk.Button(button_frame, text="Générer un défi", command=self.generer_defi,
                                     font=("Arial", 14, "bold"), bg="purple", fg="white", relief="raised", bd=5, padx=20, pady=10)
        self.btn_quitter = tk.Button(button_frame, text="Quitter", command=controller.quit,
                                     font=("Arial", 14, "bold"), bg="red", fg="white", relief="raised", bd=5, padx=20, pady=10)

        # Placement des boutons
        self.btn_resoudre.pack(pady=10)
        self.btn_generer.pack(pady=10)
        self.btn_quitter.pack(pady=10)

    def go_to_defis(self):
        """Méthode appelée pour aller au menu de sélection des défis."""
        from src.interfaces.SelectionDefis import SelectionDefis  # Import différé pour éviter la boucle
        self.controller.changer_interface(SelectionDefis, resize=True)
    
    def generer_defi(self):
        print("Générer un défi")
