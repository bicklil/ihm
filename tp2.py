import tkinter as tk


def couleur_surligne(event):
    """ callback modifier le trait
    au survol de la souris """
    Canv = event.widget
    droite = Canv.find_withtag("current")[0]
    Canv.itemconfig(droite, fill="red")
    Canv.itemconfig(droite, width=1.5)


def couleur_desurligne(event):
    """ callback remetant a l'etat initial si
    la souris s'ecarte du trait"""
    Canv = event.widget
    droite = Canv.find_withtag("current")[0]
    Canv.tag_bind(droite, "<Button-1>", update_label)
    Canv.itemconfig(droite, fill="black")
    Canv.itemconfig(droite, width=1)


def update_label(event):
    """modifie le label au click sur le trait"""
    Canv = event.widget
    droite = Canv.find_withtag("current")[0]
    Vstr.set(droite)


def ctrl_click(event, points):
    """ajoute un point a droite en cours de creation
    si on a pas de trait en cours on en cree un"""
    Canv = event.widget
    X = event.x
    Y = event.y
    if len(points) == 0:  # pas de trait en cours
        droite = Canv.create_line(X, Y, X, Y)
        Canv.tag_bind(droite, "<Enter>", couleur_surligne)
        Canv.tag_bind(droite, "<Leave>", couleur_desurligne)
    else:
        droite = Canv.find_all()[-1]  # recupere le trait en cours de tracé
        Canv.coords(droite, *points, X, Y)

    points.append(X)
    points.append(Y)
    Canv.tag_bind(droite, "<Enter>", couleur_surligne)
    Canv.tag_bind(droite, "<Leave>", couleur_desurligne)


def release_key(event, points):
    """reset le tableau des coordonnée
    car le tracé c'est terminé"""
    while len(points) > 0:
        points.remove(points[0])


def menu_nouveau():
    """Fonction associée au boutton nouveau du menu"""
    pass


def menu_ouvrir(Canv):
    """Fonction associée au boutton ouvrir du menu"""
    Fichier = open("sav", "r")
    for lines in Fichier:
        coords = lines.split()
        droite = Canv.create_line(*coords)
        Canv.tag_bind(droite, "<Enter>", couleur_surligne)
        Canv.tag_bind(droite, "<Leave>", couleur_desurligne)
    Fichier.close()


def menu_sauver(Canv):
    """Fonction associée au boutton sauver du menu"""
    Fichier = open("sav", "w")
    for droite in Canv.find_all():
        coordon = Canv.coords(droite)
        for point in coordon:
            Fichier.write(str(point)+" ")
        Fichier.write("\n")
    Fichier.close()


def menu_quitter():
    """Fonction associée au boutton quitter du menu"""
    pass


def ouvrir_commande():
    """ouvre l'aide apres appuie sur le bouton aide"""
    pass


def initialisation_tk():
    """prepare tous les widgets necessaires à l'appli"""
    Root = tk.Tk()
    Canv = tk.Canvas(Root)
    Vstr = tk.StringVar()
    Label = tk.Label(Root, textvariable=Vstr)
    Vstr.set("test")
    MenuBar = tk.Menubutton(Root, text="Fichier")
    BoutonAide = tk.Button(MenuBar)
    return(Root, Canv, Label, MenuBar, Vstr, BoutonAide)


def configuration_tk(Root, MenuBar, BoutonAide, Canv):
    """modifie les widgets"""
    BoutonAide.config(text="Aide", command=ouvrir_commande)
    MenuBar.menu = tk.Menu(MenuBar, tearoff=0)
    MenuBar["menu"] = MenuBar.menu
    MenuBar["anchor"] = "w"
    MenuBar.menu.add_command(label="Nouveau",
                             command=menu_nouveau)
    MenuBar.menu.add_command(label="Ouvrir",
                             command=lambda: menu_ouvrir(Canv))
    MenuBar.menu.add_command(label="Sauver", state=tk.DISABLED, 
                             command=lambda: menu_sauver(Canv))
    MenuBar.menu.add_command(label="Quitter",
                             command=menu_quitter)


def placement_tk(Label, Canv, BoutonAide):
    """place les widgets sur le canv"""
    MenuBar.pack(side="top", anchor="nw", fill=tk.X)
    BoutonAide.pack(side="top", anchor="ne")
    Label.pack(side="bottom", fill=tk.X)
    Canv.pack()


def Canv_call(Canv):
    """associe tous les callbacks au canvas de base"""
    points = []
    Canv.bind("<Control-B1-Motion>",
              lambda event: ctrl_click(event, points))
    Canv.bind("<ButtonRelease-1>", lambda event: release_key(event, points))
    Canv.bind("<KeyRelease-Control_L>", release_key)  # marche pas
    Canv.bind("<KeyRelease-Control_R>", release_key)  # marche pas


if __name__ == "__main__":
    (Root, Canv, Label, MenuBar, Vstr, BoutonAide) = initialisation_tk()

    configuration_tk(Root, MenuBar, BoutonAide, Canv)
    placement_tk(Label, Canv, BoutonAide)
    Canv_call(Canv)
    Root.mainloop()
