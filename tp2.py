import tkinter as tk


def initialisation_tk():
    Root = tk.Tk()
    Canv = tk.Canvas(Root)
    Label = tk.Label(Root, text="test")
    MenuBar = tk.Menu(Root)
    MenuFichier = tk.Menu(MenuBar, tearoff=0)
    return(Root, Canv, Label, MenuBar, MenuFichier)


def configuration_tk(Root, Menubar, MenuFichier):
    Root.config(menu=MenuBar)
    MenuBar.add_cascade(label="Fichier", menu=MenuFichier)


def placement_tk(Label, Canv):
    Label.pack(side="bottom", fill=tk.X)
    Canv.pack()


if __name__ == "__main__":

    (Root, Canv, Label, MenuBar, MenuFichier) = initialisation_tk()
    configuration_tk(Root, MenuBar, MenuFichier)
    placement_tk(Label, Canv)
    Root.mainloop()
