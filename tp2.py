import tkinter as tk

global droite


def couleur_surligne(event):
    """ callback modifier le contour
    d'un rectangle au survol de la souris """
    Canv = event.widget
    droite = Canv.find_withtag("current")[0]
    Canv.itemconfig(droite, fill="red")
    Canv.itemconfig(droite, width=1.5)


def couleur_desurligne(event):
    """ callback remetant a l'etat initial si
    la souris sort d'un rectangle"""
    Canv = event.widget
    droite = Canv.find_withtag("current")[0]
    Canv.tag_bind(droite, "<Button-1>", update_label)
    Canv.itemconfig(droite, fill="black")
    Canv.itemconfig(droite, width=1)


def update_label(event):
    Canv = event.widget
    droite = Canv.find_withtag("current")[0]
    Vstr.set(droite)


def ctrl_click(event, points):
    global droite
    Canv = event.widget
    X = event.x
    Y = event.y
    if len(points) == 0:
        droite = Canv.create_line(X, Y, X, Y)
        Canv.tag_bind(droite, "<Enter>", couleur_surligne)
        Canv.tag_bind(droite, "<Leave>", couleur_desurligne)
    else:
        Canv.coords(droite, *points, X, Y)
    points.append(X)
    points.append(Y)


def release_key(event, points):
    while len(points) > 0:
        points.remove(points[0])
    print("test")


def initialisation_tk():
    """prepare tous les widgets necessaires à l'appli"""
    Root = tk.Tk()
    Canv = tk.Canvas(Root)
    Vstr = tk.StringVar()
    Label = tk.Label(Root, textvariable=Vstr)
    Vstr.set("test")
    MenuBar = tk.Menu(Root)
    MenuFichier = tk.Menu(MenuBar, tearoff=0)
    return(Root, Canv, Label, MenuBar, MenuFichier, Vstr)


def configuration_tk(Root, Menubar, MenuFichier):
    """modifie les widgets"""
    Root.config(menu=MenuBar)
    MenuBar.add_cascade(label="Fichier", menu=MenuFichier)


def placement_tk(Label, Canv):
    """place les widgets sur le canv"""
    Label.pack(side="bottom", fill=tk.X)
    Canv.pack()


def Canv_call(Canv):
    points = []
    Canv.bind("<Control-B1-Motion>",
              lambda event: ctrl_click(event, points))
    Canv.bind("<ButtonRelease-1>", lambda event: release_key(event, points))
    Canv.bind("<KeyRelease-Control_L>", release_key)  # marche pas
    Canv.bind("<KeyRelease-Control_R>", release_key)  # marche pas


if __name__ == "__main__":
    (Root, Canv, Label, MenuBar, MenuFichier, Vstr) = initialisation_tk()
    configuration_tk(Root, MenuBar, MenuFichier)
    placement_tk(Label, Canv)
    Canv_call(Canv)
    Root.mainloop()
