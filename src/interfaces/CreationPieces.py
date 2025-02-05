import tkinter as tk
from tkinter import ttk, messagebox

class CreationPieces(tk.Frame):

    def __init__(self, controller, num_defi, counter_values):
        super().__init__(controller)
        self.controller = controller
        self.num_defi = num_defi
        self.counter_values = counter_values
        self.config(bg="#004A9A")

        self.pieces = []

        # Modifier la taille de la fenêtre
        new_height = (controller.screen_height // 5) * 3
        controller.geometry(f"{controller.window_width}x{new_height}+{controller.x_position}+{(controller.screen_height - new_height) // 2}")

        self.grid(row=0, column=0, sticky="n")

        self.main_container = tk.Frame(self, bg="#004A9A")
        self.main_container.grid(row=0, column=0, padx=10, pady=10)

        # Créer un conteneur pour les grilles
        self.grid_container = tk.Frame(self.main_container, bg="#004A9A")
        self.grid_container.grid(row=0, column=0, padx=10, pady=10)

        # Définir les styles
        style = ttk.Style()
        style.configure("Toggle.TButton", background="lightblue", foreground="black")
        style.map("Toggle.TButton", background=[("active", "lightblue"), ("!selected", "lightblue")])
        style.configure("Pressed.TButton", background="#003366", foreground="white")
        style.map("Pressed.TButton", background=[("active", "#003366"), ("selected", "#003366")])

        self.boutons = self.create_switch_grid(self.grid_container)

        # Ajout des boutons en dessous de la grille
        tk.Button(self.main_container, text="Ajouter", font=("Arial", 14, "bold"), bg="blue", fg="white", 
                    command=self.valider_piece, width=20).grid(row=1, column=0, pady=10)
        tk.Button(self.main_container, text="Effacer dernière pièce", font=("Arial", 14, "bold"), bg="red", fg="white", 
                    command=self.effacer_derniere_piece, width=20).grid(row=1, column=1, pady=10)
        tk.Button(self.main_container, text="Retour", font=("Arial", 14, "bold"), bg="darkred", fg="white", 
                    command=self.retour_option_generation, width=20).grid(row=2, column=0, pady=10)
        tk.Button(self.main_container, text="Valider les 4 pièces", font=("Arial", 14, "bold"), bg="green", fg="white", 
                    command=self.valider_toutes_les_pieces, width=20).grid(row=2, column=1, pady=10)

        # Conteneur pour l'aperçu des pièces créées (une seule ligne d'aperçu)
        self.apercu_frame = tk.Frame(self.main_container, bg="#004A9A")
        self.apercu_frame.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    def create_switch_grid(self, root):
        frame = ttk.Frame(root, width=300, height=300)
        frame.grid(row=0, column=0, padx=10, pady=10)
        frame.grid_propagate(False)
        
        buttons = []
        for i in range(3):
            for j in range(3):
                frame.rowconfigure(i, weight=1)
                frame.columnconfigure(j, weight=1)
                var = tk.IntVar()
                btn = ttk.Checkbutton(frame, variable=var, style="Toggle.TButton")
                btn.config(command=lambda b=btn, v=var: toggle_button(b, v))
                btn.grid(row=i, column=j, sticky="nsew")
                buttons.append((btn, var))
        
        return buttons

    def ajouter_piece(self):
        if len(self.pieces) >= 4:
            messagebox.showerror("Limite atteinte", "Vous ne pouvez créer que 4 pièces.")
            return

        nouvelle_piece = []
        for i in range(9):
            bouton = self.boutons[i]
            if bouton[1].get():
                nouvelle_piece.append(i)

        # Vérification de la contrainte des 2 trous (2 boutons non activés)
        trous = 9 - len(nouvelle_piece)
        if trous != 2:
            messagebox.showerror("Erreur", "La pièce doit avoir exactement 2 trous.")
            return

        self.pieces.append(nouvelle_piece)
        self.aperçu_piece(nouvelle_piece)

    def effacer_derniere_piece(self):
        if self.pieces:
            # Supprimer la dernière pièce
            self.pieces.pop()
            
            # Effacer l'aperçu de la dernière pièce supprimée
            for widget in self.apercu_frame.winfo_children():
                widget.grid_forget()  # Utiliser grid_forget() au lieu de destroy
            
            # Redessiner l'aperçu de toutes les pièces restantes
            for index, piece in enumerate(self.pieces):
                self.aperçu_piece(piece)
        else:
            messagebox.showerror("Erreur", "Aucune pièce à supprimer.")


    def aperçu_piece(self, nouvelle_piece):
        # Créer un aperçu simple de la pièce (représentation graphique des boutons activés)
        row_num = len(self.pieces) - 1

        # Créer un conteneur pour chaque aperçu de pièce
        frame = tk.Frame(self.apercu_frame, bg="#004A9A")
        frame.grid(row=0, column=row_num, padx=10, pady=10)

        for i in range(9):
            row_grid, col_grid = divmod(i, 3)
            if i in nouvelle_piece:
                color = "lightblue"
            else:
                color = "#004A9A"
            # Ajouter un label pour chaque case de la grille avec espacement entre les aperçus
            tk.Label(frame, width=4, height=2, bg=color).grid(row=row_grid, column=col_grid, padx=1, pady=1)

    def valider_piece(self):
        if len(self.pieces) >= 4:
            messagebox.showerror("Limite atteinte", "Vous ne pouvez créer que 4 pièces.")
            return

        nouvelle_piece = []
        for i in range(9):
            bouton = self.boutons[i]
            if bouton[1].get():
                nouvelle_piece.append(i)

        trous = 9 - len(nouvelle_piece)
        if trous != 2:
            messagebox.showerror("Erreur", "La pièce doit avoir exactement 2 trous.")
            return

        self.pieces.append(nouvelle_piece)
        self.aperçu_piece(nouvelle_piece)
        print(f"Pièce validée: {nouvelle_piece}")

    def valider_toutes_les_pieces(self):
        if len(self.pieces) != 4:
            messagebox.showerror("Erreur", "Vous devez créer exactement 4 pièces avant de valider.")
            return
        
        json_pieces = {"pieces": self.pieces}

        from src.interfaces.Resolution import Resolution
        self.controller.changer_interface(Resolution, num_defi=self.num_defi, counter_values=self.counter_values, fichier_pieces=json_pieces)

    def retour_option_generation(self):
        from src.interfaces.OptionsGeneration import OptionsGeneration
        self.controller.changer_interface(OptionsGeneration, self.num_defi, self.counter_values)
    
def toggle_button(button, var):
    if var.get():
        button.configure(style="Pressed.TButton")
    else:
        button.configure(style="Toggle.TButton")
