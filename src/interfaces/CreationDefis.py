import tkinter as tk
from PIL import Image, ImageTk

class CreationDefis(tk.Frame):

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

    number_max_per_monsters = {
        0: 4,   # bat
        1: 4,   # champi
        2: 2,   # chien
        3: 4,   # diable
        4: 2,   # dino
        5: 3,   # slime
        6: 2,   # troll
        7: 4    # yeti
    }

    counter_labels = {}
        
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller
        self.config(bg="#003366")

        # Modifier la taille de la fenêtre
        new_height = (controller.screen_height // 5) * 3 + 50
        controller.geometry(f"{controller.window_width}x{new_height}+{controller.x_position}+{(controller.screen_height - new_height) // 2}")

        self.frames = []
        self.counter_values = [0] * 8
        self.labels = []

        # Créer un cadre principal qui contiendra les deux lignes
        main_frame = tk.Frame(self, bg="#003366")
        main_frame.pack(fill="both", expand=True)

        self.create_line(main_frame, 0, 4)
        self.create_line(main_frame, 4, 8)

        # Bouton Retour
        btn_retour = tk.Button(self, text="Retour", font=("Arial", 14, "bold"), bg="darkred", fg="white",
                               command=self.retour_menu_defis, width=20)
        btn_retour.pack(side="left", padx=5, pady=20)

        self.rules_label = tk.Label(self, text="Maximum number of monsters : 8", font=("Arial", 20, "bold"), bg="#003366", fg="white")
        self.rules_label.pack(side="left")

        # Bouton Valider
        btn_valider = tk.Button(self, text="Valider", font=("Arial", 14, "bold"), bg="green", fg="white",
                                command=self.valider_defi, width=20)
        btn_valider.pack(side="right", padx=5, pady=20)

        # Bouton Valider avec génération
        btn_valider_avec_generation = tk.Button(main_frame, text="Valider (nouveau plateau et pièces)", font=("Arial", 14, "bold"), bg="blue", fg="white",
                                command=self.valider_defi_avec_generations, width=50)
        btn_valider_avec_generation.pack(side="bottom", padx=5, pady=5)

    def create_line(self, parent, start, end):
        """Crée une ligne avec plusieurs compteurs"""
        line_frame = tk.Frame(parent, bg="#003366")
        line_frame.pack(fill="x", pady=5)

        for i in range(start, end):
            frame = tk.Frame(line_frame, bg="#003366", height=250,
                             width=self.controller.window_width // 4)
            frame.pack_propagate(False)
            frame.pack(side="left", padx=5, pady=10)
            self.frames.append(frame)

            # Image (représentée par un texte ici)
            image = Image.open(self.images_path[i])
            image_resized = image.resize((150, 150), Image.Resampling.LANCZOS)
            monster_image = ImageTk.PhotoImage(image_resized)

            monster_image_label = tk.Label(frame, image=monster_image, background="#003366")
            monster_image_label.image = monster_image
            monster_image_label.pack(side="top", padx=20)

            # Sous-frame pour les boutons et le compteur
            counter_frame = tk.Frame(frame, bg="#003366")
            counter_frame.pack(side="top", pady=10)

            # Style pour les boutons
            button_style = {
                'font': ("Arial", 20, "bold"),
                'bg': "#FF6347",  # Couleur rouge tomate
                'fg': "white",
                'width': 2,
                'height': 2,
                'relief': "solid",
                'bd': 2,
                'activebackground': "#FF4500",  # Effet de survol
                'activeforeground': "white",
                'highlightthickness': 0
            }

            # Bouton pour décrémenter
            btn_decrement = tk.Button(counter_frame, text="-", command=lambda i=i: self.update_counter(i, "decrement"), **button_style)
            btn_decrement.pack(side="left", padx=10)

            # Zone de compteur
            counter_label = tk.Label(counter_frame, text=f"0/{self.number_max_per_monsters[i]}", bg="#003366", fg="white", font=("Arial", 14, "bold"))
            counter_label.pack(side="left", padx=10)
            self.labels.append(counter_label)
            self.counter_labels[i] = counter_label

            # Bouton pour incrémenter
            btn_increment = tk.Button(counter_frame, text="+", command=lambda i=i: self.update_counter(i, "increment"), **button_style)
            btn_increment.pack(side="left", padx=10)
            
    def update_counter(self, index, operation):
        """Incrémente ou décrémente le compteur"""
        
        # Calculer la somme actuelle des compteurs
        total_count = sum(self.counter_values)
        
        if operation == "increment":
            # Vérifier si l'incrémentation est possible
            if total_count == 8:
                self.blink_label(self.rules_label)
            elif self.counter_values[index] == self.number_max_per_monsters[index]:
                self.blink_label(self.counter_labels[index])
            else:
                self.counter_values[index] += 1
        elif operation == "decrement":
            # Vérifier si la décrémentation est possible
            if self.counter_values[index] > 0:
                self.counter_values[index] -= 1

        # Mettre à jour l'affichage du compteur
        self.labels[index].config(text=f"{str(self.counter_values[index])}/{self.number_max_per_monsters[index]}")

    def blink_label(self, label):
        """Fait clignoter un label en changeant la couleur de fond quelques fois"""
        blink_count = 5  # Nombre de fois que le label clignote
        delay = 100  # Délai entre chaque changement de couleur (en ms)
        
        def toggle_color(count):
            if count > 0:
                current_color = label.cget("bg")
                new_color = "#FF6347" if current_color == "#003366" else "#003366"
                label.config(bg=new_color)
                # Répéter le clignotement
                label.after(delay, toggle_color, count-1)
            else:
                # Rétablir la couleur initiale après les clignotements
                label.config(bg="#003366")

        # Démarrer le clignotement
        toggle_color(blink_count)

    def retour_menu_defis(self):
        """Retourne à l'interface de sélection de défis"""
        from src.interfaces.SelectionDefis import SelectionDefis  # Import différé pour éviter la boucle d'import
        self.controller.changer_interface(SelectionDefis)

    def valider_defi(self):
        """Valide le défi créé"""
        from src.interfaces.Resolution import Resolution
        self.controller.changer_interface(Resolution, num_defi=-1, counter_values=self.counter_values, defi_generated=False)

    def valider_defi_avec_generations(self):
        """Valide le défi créé"""
        from src.interfaces.CreationPieces import CreationPieces
        self.controller.changer_interface(CreationPieces, num_defi=-1, counter_values=self.counter_values)
