import tkinter as tk


if __name__ == "__main__":
    Root = tk.Tk()

    MenuBar = tk.Menu(Root)
    Root.config(menu=MenuBar)

    MenuFichier = tk.Menu(MenuBar, tearoff=0)
    MenuBar.add_cascade(label="Fichier", menu=MenuFichier)
    MenuAide = tk.Menu(MenuBar, tearoff=0)
    MenuBar.add_cascade(label="Aide", menu=MenuAide)

    Root.mainloop()
