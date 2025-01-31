import tkinter as tk
from tkinter import PhotoImage



def lancer_menu_defis():
    # Création de la fenêtre principale
    root = tk.Tk()
    root.title("Sélectionner le défi")
    root.configure(bg="#004A9A")

    # Récupération de la taille de l'écran
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Définition de la taille de la fenêtre (moitié de l'écran)
    window_width = screen_width // 2
    window_height = (screen_height // 5) * 4

    # Calcul de la position pour centrer la fenêtre
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2

    # Application de la taille et de la position
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    # Chargement et affichage de l'image (remplace "logo.png" par ton image)
    image_path = "data/title.png"
    try:
        logo = PhotoImage(file=image_path)
        logo_label = tk.Label(root, image=logo, borderwidth=0, highlightthickness=0)
        logo_label.pack(pady=10)
    except Exception as e:
        print("Impossible de charger l'image:", e)

    # Fonctionnalités des boutons
    def resoudre_defi():
        print("Résoudre un défi")

    def generer_defi():
        print("Générer un défi")

    def quitter():
        root.quit()

    # Création d'un cadre pour centrer les boutons
    button_frame = tk.Frame(root)
    button_frame.pack(expand=True)
    button_frame.configure(bg="#004A9A")


    # Style des boutons
    def create_game_button(text, command):
        return tk.Button(button_frame, text=text, command=command, font=("Arial", 14, "bold"), bg="purple", fg="white", relief="raised", bd=5, padx=20, pady=10)

    btn_resoudre = create_game_button("Résoudre un défi", resoudre_defi)
    btn_generer = create_game_button("Générer un défi", generer_defi)
    btn_quitter = create_game_button("Quitter", quitter)

    # Placement des boutons au centre
    btn_resoudre.pack(pady=10)
    btn_generer.pack(pady=10)
    btn_quitter.pack(pady=10)

    # Gestion de la fermeture de la fenêtre
    root.protocol("WM_DELETE_WINDOW", quitter)

    # Lancement de l'application
    root.mainloop()
