import tkinter as tk


def ctrl_click(event):
    pass


def initialisation_tk():
    """prepare tous les widgets necessaires à l'appli"""
    Root = tk.Tk()
    Canv = tk.Canvas(Root)
    Label = tk.Label(Root, text="test")
    MenuBar = tk.Menu(Root)
    MenuFichier = tk.Menu(MenuBar, tearoff=0)
    return(Root, Canv, Label, MenuBar, MenuFichier)


def configuration_tk(Root, Menubar, MenuFichier):
    """modifie les widgets"""
    Root.config(menu=MenuBar)
    MenuBar.add_cascade(label="Fichier", menu=MenuFichier)


def placement_tk(Label, Canv):
    """place les widgets sur le canv"""
    Label.pack(side="bottom", fill=tk.X)
    Canv.pack()


def Canv_call(Canv):
    pass


if __name__ == "__main__":

    (Root, Canv, Label, MenuBar, MenuFichier) = initialisation_tk()
    configuration_tk(Root, MenuBar, MenuFichier)
    placement_tk(Label, Canv)
    Canv_call(Canv)
    Root.mainloop()
