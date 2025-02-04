import tkinter as tk

class OptionsGeneration(tk.Frame):

    def __init__(self, controller, num_defi, counter_values):
        super().__init__(controller)
        self.controller = controller
        self.num_defi = num_defi
        self.counter_values = counter_values
        self.config(bg="#004A9A")

        # if num_defi < 0:
        #     self.rotation_pieces = resoudre_defi(convertir_monstres(counter_values))
        # else:
        #     self.rotation_pieces = resoudre_defi(f"data/defis/defi{self.num_defi}.json")


        # Modifier la taille de la fenêtre
        new_height = (controller.screen_height // 5) * 2
        controller.geometry(f"{controller.window_width}x{new_height}+{controller.x_position}+{(controller.screen_height - new_height) // 2}")


        # Créer un cadre principal qui contiendra les boutons
        main_frame = tk.Frame(self, bg="#003366")
        main_frame.pack(fill="both", expand=True, pady=50)

        # Bouton Générer uniquement un nouveau plateau
        btn_plateau = tk.Button(main_frame, text="Générer uniquement un nouveau plateau", font=("Arial", 14, "bold"), bg="blue", fg="white",
                               command=self.resoudre_avec_generations(True, False), width=50)
        btn_plateau.pack(side="top", padx=5, pady=20)

        # Bouton Générer uniquement de nouvelles pièces
        btn_pieces = tk.Button(main_frame, text="Générer uniquement de nouvelles pièces", font=("Arial", 14, "bold"), bg="blue", fg="white",
                               command=self.resoudre_avec_generations(False, True), width=50)
        btn_pieces.pack(side="top", padx=5, pady=20)

        # Bouton Générer un nouveau plateau et de nouvelles pièces
        btn_plateau_et_pieces = tk.Button(main_frame, text="Générer un nouveau plateau et de nouvelles pièces", font=("Arial", 14, "bold"), bg="blue", fg="white",
                               command=self.resoudre_avec_generations(True, True), width=50)
        btn_plateau_et_pieces.pack(side="top", padx=5, pady=20)


        # Bouton Retour
        btn_retour = tk.Button(self, text="Retour", font=("Arial", 14, "bold"), bg="darkred", fg="white",
                               command=self.retour_menu_defis, width=20)
        btn_retour.pack(side="bottom", padx=5, pady=20)


    def resoudre_avec_generations(self, nouveauPlateau, nouvellesPieces):
        from src.interfaces.CreationPieces import CreationPieces  # Import différé pour éviter la boucle d'import
        self.controller.changer_interface(CreationPieces, num_defi=-1, counter_values=self.counter_values)

    def retour_menu_defis(self):
        """Retourne à l'interface de sélection de défis"""
        from src.interfaces.SelectionDefis import SelectionDefis  # Import différé pour éviter la boucle d'import
        self.controller.changer_interface(SelectionDefis)
