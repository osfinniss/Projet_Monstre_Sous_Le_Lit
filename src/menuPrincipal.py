import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk

def lancer_menu_principal():
    global root, window_width, window_height, screen_width, screen_height, x_position, y_position
    
    # Création de la fenêtre principale
    root = tk.Tk()
    root.title("Monstre sous le lit")
    root.configure(bg="#004A9A")  # Couleur de fond en RGB(0, 74, 154)
    
    # Récupération de la taille de l'écran
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Définition de la taille de la fenêtre (moitié de l'écran)
    window_width = screen_width // 2
    window_height = screen_height // 2
    
    # Calcul de la position pour centrer la fenêtre
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    
    # Application de la taille et de la position
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    
    afficher_menu_principal()
    
    # Gestion de la fermeture de la fenêtre
    root.protocol("WM_DELETE_WINDOW", root.quit)
    
    # Lancement de l'application
    root.mainloop()

# Fonction pour afficher le menu des défis
def afficher_menu_defis():
    global window_width, window_height
    
    # Modifier la taille de la fenêtre
    new_height = (screen_height // 5) * 4
    root.geometry(f"{window_width}x{new_height}+{x_position}+{(screen_height - new_height) // 2}")

    frames = []

    # D D D D
    # D B
    # D D C T
    # D D Y Y

    # D : 0
    # B : 1
    # C : 2
    # T : 3
    # Y : 4

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
    
    # Suppression des widgets existants
    for widget in root.winfo_children():
        widget.destroy()
    
    def on_click(frame, defi):
        for i in range(4):
            frames[i].config(bg="#003366")
        frame.config(bg="#0055AA")  # Change la couleur de fond pour montrer la sélection
    
    # Création des zones de défis
    for i in range(4):
        frame = tk.Frame(root, bg="#003366", height=new_height // 6, width=window_width)
        frame.pack_propagate(False)
        frame.pack(fill="x", pady=5)
        frames.append(frame)
        
        label = tk.Label(frame, text=f"Défi n°{i+1}", bg="#003366", fg="white", font=("Arial", 14, "bold"), anchor="w")
        label.pack(side="left", padx=20)
        
        image_frame = tk.Frame(frame, bg="#003366")
        image_frame.pack(side="right", padx=20)
        
        for monster in challenges_monsters[i]:
            # Charger l'image avec PIL
            image = Image.open(images_path[monster])

            # Redimensionner l'image à 100x100 pixels
            image_resized = image.resize((100, 100), Image.Resampling.LANCZOS)

            # Convertir l'image redimensionnée en format compatible avec Tkinter
            monster_image = ImageTk.PhotoImage(image_resized)

            # Afficher l'image dans un label
            monster_image_label = tk.Label(image_frame, image=monster_image, width=100, height=100, background="#003366")
            monster_image_label.image = monster_image  # Préserver la référence pour éviter le garbage collection
            monster_image_label.pack(side="left", padx=5)
 
        
        btn_overlay = tk.Button(frame, text="", bg="#003366", activebackground="#002244", bd=0, highlightthickness=0, command=lambda f=frame, i=i+1: on_click(f, i))
        btn_overlay.pack(fill="both", expand=True, padx=5, pady=5)
    
    # Zone pour ajouter un défi
    btn_add_challenge = tk.Button(root, text="+", font=("Arial", 20, "bold"), bg="#003366", fg="white", width=window_width, command=afficher_creation_defi)
    btn_add_challenge.pack(pady=10)
    
    # Bouton retour
    btn_retour = tk.Button(root, text="Retour", font=("Arial", 14, "bold"), bg="darkred", fg="white", command=afficher_menu_principal)
    btn_retour.pack(pady=10)

# Fonction pour afficher le menu principal
def afficher_menu_principal():
    global window_width, window_height
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    
    for widget in root.winfo_children():
        widget.destroy()
    
    # Chargement et affichage de l'image
    image_path = "data/title.png"
    try:
        logo = PhotoImage(file=image_path)
        logo_label = tk.Label(root, image=logo, bg="#004A9A", borderwidth=0, highlightthickness=0)
        logo_label.image = logo  # Préserver la référence
        logo_label.pack(pady=10)
    except Exception as e:
        print("Impossible de charger l'image:", e)
    
    # Création du cadre des boutons
    button_frame = tk.Frame(root, bg="#004A9A")
    button_frame.pack(expand=True)
    
    # Style des boutons
    def create_game_button(text, command):
        return tk.Button(button_frame, text=text, command=command, font=("Arial", 14, "bold"), bg="purple", fg="white", relief="raised", bd=5, padx=20, pady=10)
    
    btn_resoudre = create_game_button("Résoudre un défi", afficher_menu_defis)
    btn_generer = create_game_button("Générer un défi", lambda: print("Générer un défi"))
    btn_quitter = create_game_button("Quitter", root.quit)
    
    # Placement des boutons
    btn_resoudre.pack(pady=10)
    btn_generer.pack(pady=10)
    btn_quitter.pack(pady=10)


def afficher_creation_defi():
    global window_width, window_height

    # Modifier la taille de la fenêtre (par exemple, pour une taille fixe ou ajustée à l'écran)
    new_height = (screen_height // 5) * 4
    root.geometry(f"{window_width}x{new_height}+{x_position}+{(screen_height - new_height) // 2}")

    frames = []

    # Suppression des widgets existants
    for widget in root.winfo_children():
        widget.destroy()

    # Fonction pour incrémenter et décrémenter le compteur
    def update_counter(label, value, operation):
        if operation == "increment" and value < 10:
            value += 1
        elif operation == "decrement" and value > 0:
            value -= 1
        label.config(text=str(value))
        return value

    # Liste pour stocker les valeurs des compteurs
    counter_values = [0] * 8
    labels = []

    # Créer un cadre principal qui contiendra les deux lignes
    main_frame = tk.Frame(root, bg="#003366")
    main_frame.pack(fill="both", expand=True)

    # Créer la première ligne de 4 zones
    line_1 = tk.Frame(main_frame, bg="#003366")
    line_1.pack(fill="x", pady=5)
    
    # Créer les 4 zones pour la première ligne
    for i in range(4):
        frame = tk.Frame(line_1, bg="#003366", height=new_height // 6, width=window_width // 4)
        frame.pack_propagate(False)
        frame.pack(side="left", padx=5)
        frames.append(frame)

        # Image (représentée par un texte ici)
        image_label = tk.Label(frame, text=f"I-{i+1}", bg="#003366", fg="white", font=("Arial", 14, "bold"))
        image_label.pack(side="top", padx=20)

        # Zone de compteur
        counter_label = tk.Label(frame, text="0", bg="#003366", fg="white", font=("Arial", 14, "bold"))
        counter_label.pack(side="top", padx=10)
        labels.append(counter_label)

        # Boutons pour incrémenter et décrémenter
        def increment(i=i):
            counter_values[i] = update_counter(counter_label, counter_values[i], "increment")

        def decrement(i=i):
            counter_values[i] = update_counter(counter_label, counter_values[i], "decrement")

        btn_increment = tk.Button(frame, text="+", font=("Arial", 14), command=increment)
        btn_increment.pack(side="left", padx=5)

        btn_decrement = tk.Button(frame, text="-", font=("Arial", 14), command=decrement)
        btn_decrement.pack(side="left", padx=5)

    # Créer la deuxième ligne de 4 zones
    line_2 = tk.Frame(main_frame, bg="#003366")
    line_2.pack(fill="x", pady=5)

    # Créer les 4 zones pour la deuxième ligne
    for i in range(4, 8):
        frame = tk.Frame(line_2, bg="#003366", height=new_height // 6, width=window_width // 4)
        frame.pack_propagate(False)
        frame.pack(side="left", padx=5)
        frames.append(frame)

        # Image (représentée par un texte ici)
        image_label = tk.Label(frame, text=f"I-{i+1}", bg="#003366", fg="white", font=("Arial", 14, "bold"))
        image_label.pack(side="top", padx=20)

        # Zone de compteur
        counter_label = tk.Label(frame, text="0", bg="#003366", fg="white", font=("Arial", 14, "bold"))
        counter_label.pack(side="top", padx=10)
        labels.append(counter_label)

        # Boutons pour incrémenter et décrémenter
        def increment(i=i):
            counter_values[i] = update_counter(counter_label, counter_values[i], "increment")

        def decrement(i=i):
            counter_values[i] = update_counter(counter_label, counter_values[i], "decrement")

        btn_increment = tk.Button(frame, text="+", font=("Arial", 14), command=increment)
        btn_increment.pack(side="left", padx=5)

        btn_decrement = tk.Button(frame, text="-", font=("Arial", 14), command=decrement)
        btn_decrement.pack(side="left", padx=5)

    # Bouton Retour pour revenir au menu des défis
    btn_retour = tk.Button(root, text="Retour", font=("Arial", 14, "bold"), bg="darkred", fg="white", command=afficher_menu_defis)
    btn_retour.pack(side="left", padx=10, pady=20)

    # Bouton Valider pour finaliser la création du défi
    def valider_defi():
        # Exemple d'action à faire lors de la validation (peut être ajusté)
        print("Défi validé avec les valeurs suivantes :", counter_values)
        # Tu peux ici ajouter un traitement pour valider et enregistrer le défi

    btn_valider = tk.Button(root, text="Valider", font=("Arial", 14, "bold"), bg="green", fg="white", command=valider_defi)
    btn_valider.pack(side="right", padx=10, pady=20)
