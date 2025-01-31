import tkinter as tk
from src.interfaces.MenuPrincipal import MenuPrincipal

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configuration initiale de la fenêtre
        self.title("Monstre sous le lit")
        self.configure(bg="#004A9A")

        # Récupération de la taille de l'écran
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

        # Définition de la taille initiale (moitié de l'écran)
        self.window_width = self.screen_width // 2
        self.window_height = self.screen_height // 2

        # Positionnement au centre
        self.x_position = (self.screen_width - self.window_width) // 2
        self.y_position = (self.screen_height - self.window_height) // 2
        self.geometry(f"{self.window_width}x{self.window_height}+{self.x_position}+{self.y_position}")

        # Afficher le menu principal
        self.changer_interface(MenuPrincipal)

    def changer_interface(self, nouvelle_interface, resize=False):
        """Change l'interface et redimensionne si nécessaire."""
        for widget in self.winfo_children():
            widget.destroy()
        
        # Charger la nouvelle interface
        self.interface = nouvelle_interface(self)
        self.interface.pack(expand=True, fill="both")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
