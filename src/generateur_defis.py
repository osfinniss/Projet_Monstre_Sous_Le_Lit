import tkinter as tk
from tkinter import messagebox
import json
import random
import os
import concurrent.futures
from src.solveur import resoudre_defi

def solve_candidate(defi):
    # On peut, par exemple, ajouter un paramètre verbose=False dans resoudre_defi
    resultat = resoudre_defi(defi)  # ou resoudre_defi(defi, verbose=False) si vous avez adapté la fonction
    # On considère le défi valide si toutes les clés ont une solution non vide
    if all(resultat[k] != [] for k in resultat):
        return defi
    return None

class GenerateurDefis(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller
        self.config(bg="#004A9A")

        # Titre
        self.label_titre = tk.Label(self, text="Générer des défis", font=("Arial", 20, "bold"), bg="#004A9A", fg="white")
        self.label_titre.pack(pady=20)

        # Nombre de défis à générer
        self.label_nb_defis = tk.Label(self, text="Nombre de défis à générer :", font=("Arial", 14), bg="#004A9A", fg="white")
        self.label_nb_defis.pack()
        self.nb_defis_var = tk.IntVar(value=3)
        self.entry_nb_defis = tk.Entry(self, textvariable=self.nb_defis_var, font=("Arial", 14))
        self.entry_nb_defis.pack(pady=5)

        # Nombre de monstres par défi
        self.label_nb_monstres = tk.Label(self, text="Nombre de monstres par défi :", font=("Arial", 14), bg="#004A9A", fg="white")
        self.label_nb_monstres.pack()
        self.nb_monstres_var = tk.IntVar(value=5)
        self.entry_nb_monstres = tk.Entry(self, textvariable=self.nb_monstres_var, font=("Arial", 14))
        self.entry_nb_monstres.pack(pady=5)

        # Bouton Générer
        self.btn_generer = tk.Button(self, text="Générer", font=("Arial", 14, "bold"), bg="purple", fg="white", relief="raised", bd=5, padx=20, pady=10, command=self.generer_defis)
        self.btn_generer.pack(pady=10)

        # Bouton Retour
        self.btn_retour = tk.Button(self, text="Retour", font=("Arial", 14, "bold"), bg="darkred", fg="white", command=self.retour_menu_principal)
        self.btn_retour.pack(pady=10)

    def generer_defis(self):
        nb_defis = self.nb_defis_var.get()
        nb_monstres = self.nb_monstres_var.get()

        if nb_defis <= 0 or nb_monstres <= 0:
            messagebox.showerror("Erreur", "Veuillez entrer des valeurs positives.")
            return

        defis_valides = []
        # On utilisera un set pour éviter de retester des défis identiques
        deja_testes = set()
        batch_size = 10  # nombre de candidats générés en batch

        # Utilisation d'un exécuteur en parallèle pour tester les candidats
        with concurrent.futures.ProcessPoolExecutor() as executor:
            while len(defis_valides) < nb_defis:
                candidats = []
                # Génération d'un batch de candidats
                for _ in range(batch_size):
                    # On génère le défi sous forme de tuple pour pouvoir le comparer facilement
                    monstres = tuple(random.choices(range(8), k=nb_monstres))
                    if monstres not in deja_testes:
                        deja_testes.add(monstres)
                        candidats.append({"monstres": list(monstres)})
                # On teste les candidats en parallèle
                futures = [executor.submit(solve_candidate, defi) for defi in candidats]
                for future in concurrent.futures.as_completed(futures):
                    defi_valide = future.result()
                    if defi_valide is not None:
                        defis_valides.append(defi_valide)
                        if len(defis_valides) >= nb_defis:
                            break

        os.makedirs("data", exist_ok=True)
        fichier_sortie = "data/defis_valides.json"
        with open(fichier_sortie, "w") as f:
            json.dump(defis_valides, f, indent=4)

        messagebox.showinfo("Succès", f"{nb_defis} défis valides ont été générés.")

        from src.interfaces.SelectionDefisValides import SelectionDefisValides
        self.controller.changer_interface(SelectionDefisValides, resize=True)

    def retour_menu_principal(self):
        from src.interfaces.MenuPrincipal import MenuPrincipal
        self.controller.changer_interface(MenuPrincipal, resize=True)
