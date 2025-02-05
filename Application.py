import tkinter as tk
from src.interfaces.MenuPrincipal import MenuPrincipal
from src.interfaces.SelectionDefis import SelectionDefis
from src.interfaces.SelectionDefisValides import SelectionDefisValides
from src.interfaces.Resolution import Resolution
from src.interfaces.CreationDefis import CreationDefis
from src.interfaces.CreationPieces import CreationPieces
from src.interfaces.OptionsGeneration import OptionsGeneration

DEFAULT_NUM_DEFI = -1
DEFAULT_COUNTER_VALUES = None
DEFAULT_FICHIER_PIECES = "data/pieces.json"
DEFAULT_DEFI_GENERATED = False

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
        self.window_height = (self.screen_height // 5) * 4

        # Positionnement au centre
        self.x_position = (self.screen_width - self.window_width) // 2
        self.y_position = (self.screen_height - self.window_height) // 2
        self.geometry(f"{self.window_width}x{self.window_height}+{self.x_position}+{self.y_position}")

        # Afficher le menu principal
        self.changer_interface(MenuPrincipal)

    def changer_interface(self, nouvelle_interface, 
                          resize=True, 
                          num_defi=DEFAULT_NUM_DEFI, 
                          counter_values=DEFAULT_COUNTER_VALUES, 
                          fichier_pieces=DEFAULT_FICHIER_PIECES,
                          defi_generated=DEFAULT_DEFI_GENERATED):
        
        """Change l'interface et redimensionne si nécessaire."""
        for widget in self.winfo_children():
            widget.destroy()

        if nouvelle_interface in (CreationPieces, OptionsGeneration):
            self.interface = nouvelle_interface(self, counter_values)
            self.interface.grid(row=0, column=0, sticky="nsew")

        elif nouvelle_interface == Resolution :
            self.interface = nouvelle_interface(self, num_defi, counter_values, fichier_pieces, defi_generated)
            self.interface.grid(row=0, column=0, sticky="nsew")
        else:
            self.interface = nouvelle_interface(self)
            self.interface.pack(expand=True, fill="both")


if __name__ == "__main__":
    app = Application()
    app.mainloop()