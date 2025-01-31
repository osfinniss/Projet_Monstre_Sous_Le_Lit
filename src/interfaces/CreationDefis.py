import tkinter as tk

class CreationDefis(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller
        self.config(bg="#003366")

        # Modifier la taille de la fenêtre
        new_height = (controller.screen_height // 5) * 4
        controller.geometry(f"{controller.window_width}x{new_height}+{controller.x_position}+{(controller.screen_height - new_height) // 2}")

        self.frames = []
        self.counter_values = [0] * 8
        self.labels = []

        # Créer un cadre principal qui contiendra les deux lignes
        main_frame = tk.Frame(self, bg="#003366")
        main_frame.pack(fill="both", expand=True)

        # Créer la première ligne de 4 zones
        self.create_line(main_frame, 0, 4)

        # Créer la deuxième ligne de 4 zones
        self.create_line(main_frame, 4, 8)

        # Bouton Retour
        btn_retour = tk.Button(self, text="Retour", font=("Arial", 14, "bold"), bg="darkred", fg="white",
                               command=self.retour_menu_defis)
        btn_retour.pack(side="left", padx=10, pady=20)

        # Bouton Valider
        btn_valider = tk.Button(self, text="Valider", font=("Arial", 14, "bold"), bg="green", fg="white",
                                command=self.valider_defi)
        btn_valider.pack(side="right", padx=10, pady=20)

    def create_line(self, parent, start, end):
        """Crée une ligne avec plusieurs compteurs"""
        line_frame = tk.Frame(parent, bg="#003366")
        line_frame.pack(fill="x", pady=5)

        for i in range(start, end):
            frame = tk.Frame(line_frame, bg="#003366", height=self.controller.window_height // 6,
                             width=self.controller.window_width // 4)
            frame.pack_propagate(False)
            frame.pack(side="left", padx=5)
            self.frames.append(frame)

            # Image (représentée par un texte ici)
            image_label = tk.Label(frame, text=f"I-{i+1}", bg="#003366", fg="white", font=("Arial", 14, "bold"))
            image_label.pack(side="top", padx=20)

            # Zone de compteur
            counter_label = tk.Label(frame, text="0", bg="#003366", fg="white", font=("Arial", 14, "bold"))
            counter_label.pack(side="top", padx=10)
            self.labels.append(counter_label)

            # Boutons pour incrémenter et décrémenter
            btn_increment = tk.Button(frame, text="+", font=("Arial", 14), command=lambda i=i: self.update_counter(i, "increment"))
            btn_increment.pack(side="left", padx=5)

            btn_decrement = tk.Button(frame, text="-", font=("Arial", 14), command=lambda i=i: self.update_counter(i, "decrement"))
            btn_decrement.pack(side="left", padx=5)

    def update_counter(self, index, operation):
        """Incrémente ou décrémente le compteur"""
        if operation == "increment" and self.counter_values[index] < 10:
            self.counter_values[index] += 1
        elif operation == "decrement" and self.counter_values[index] > 0:
            self.counter_values[index] -= 1

        self.labels[index].config(text=str(self.counter_values[index]))

    def retour_menu_defis(self):
        """Retourne à l'interface de sélection de défis"""
        from src.interfaces.SelectionDefis import SelectionDefis  # Import différé pour éviter la boucle d'import
        self.controller.changer_interface(SelectionDefis)

    def valider_defi(self):
        """Valide le défi créé"""
        print("Défi validé avec les valeurs suivantes :", self.counter_values)
