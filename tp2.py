import tkinter as tk
import tkinter.filedialog as tk_filedialog
import tkinter.messagebox as tk_msgbox


def couleur_surligne(event):
    """ callback modifier le trait
    au survol de la souris """
    Canv = event.widget
    droite = Canv.find_withtag("current")[0]
    Vstr.set(droite)
    Canv.itemconfig(droite, fill="red")
    Canv.itemconfig(droite, width=1.5)


def couleur_desurligne(event):
    """ callback remetant a l'etat initial si
    la souris s'ecarte du trait"""
    Canv = event.widget
    droite = Canv.find_withtag("current")[0]
    Vstr.set("NULL")
    Canv.itemconfig(droite, fill="black")
    Canv.itemconfig(droite, width=1)


def update_label(event):
    """modifie le label au click sur le trait"""
    Canv = event.widget
    droite = Canv.find_withtag("current")[0]


def clean_canv(Canv):
    """fonction qui permet de liberer le canvas"""
    for line in Canv.find_all():
        Canv.delete(line)


def libere_sauv(MenuBar):
    """fonction qui degrisse le bouton sauver"""
    MenuBar.menu.entryconfig("Sauver", state="normal")


def bouge_droite(event, points):
    """ bouge la courbe si on a click sur la courbe"""
    if len(points) == 0 and xint.get() != 0:
        Canv = event.widget
        ligne = Canv.find_withtag("current")[0]
        x1 = Canv.coords(ligne)[xint.get()]
        y1 = Canv.coords(ligne)[xint.get()+1]
        X = - x1 + event.x
        Y = - y1 + event.y
        Canv.move(ligne, X, Y)


def click(event):
    canv = event.widget
    ligne = Canv.find_withtag("current")[0]
    points = canv.coords(ligne)
    for i in range(0, len(points), 2):
        if points[i]-10 <= event.x <= points[i]+10:
            if points[i+1]-10 <= event.y <= points[i+1]+10:
                xint.set(i)
                print(i)
                break


def ctrl_click(event, points, MenuBar):
    """ajoute un point a droite en cours de creation
    si on a pas de trait en cours on en cree un"""
    Canv = event.widget
    X = event.x
    Y = event.y
    if len(points) == 0:  # pas de trait en cours
        droite = Canv.create_line(X, Y, X, Y)
        points.append(X)
        points.append(Y)
        libere_sauv(MenuBar)
        Canv.tag_bind(droite, "<Enter>", couleur_surligne)
        Canv.tag_bind(droite, "<Leave>", couleur_desurligne)
        Canv.tag_bind(droite, "<Button-1>", click)
        Canv.tag_bind(droite, "<B1-Motion>",
                      lambda event: bouge_droite(event, points))
    else:
        points.append(X)
        points.append(Y)
        droite = Canv.find_all()[-1]  # recupere le trait en cours de tracé
        Canv.coords(droite, *points)


def release_key(event, points):
    """reset le tableau des coordonnée
    car le tracé c'est terminé"""
    if event.keysym == "Control_L" or event.keysym == "Control_R":
        xint.set(0)
    while len(points) > 0:
        points.remove(points[0])


def menu_nouveau(Canv, MenuBar):
    """Fonction associée au boutton nouveau du menu"""
    clean_canv(Canv)
    MenuBar.menu.entryconfig("Sauver", state=tk.DISABLED)


def menu_ouvrir(Canv, MenuBar, points):
    """Fonction associée au boutton ouvrir du menu"""
    nomFichier = tk_filedialog.askopenfilename(defaultextension=".jcl",
                                               filetypes=[("JCL", "*.jcl")],
                                               parent=Root,
                                               title="ouvrir une sauvegarde")
    if nomFichier:
        Vstr.set(nomFichier)
        Fichier = open(nomFichier, "r")
        clean_canv(Canv)
        for lines in Fichier:
            coords = lines.split()
            droite = Canv.create_line(*coords)
            Canv.tag_bind(droite, "<Enter>", couleur_surligne)
            Canv.tag_bind(droite, "<Leave>", couleur_desurligne)
            Canv.tag_bind(droite, "<Button-1>", click)
            Canv.tag_bind(droite, "<B1-Motion>",
                          lambda event: bouge_droite(event, points))
            libere_sauv(MenuBar)
        Fichier.close()


def menu_sauver(Canv):
    """Fonction associée au boutton sauver du menu"""
    nomFichier = tk_filedialog.asksaveasfilename(defaultextension=".jcl",
                                                 filetypes=[("JCL", "*.jcl")],
                                                 parent=Root,
                                                 title="creer une sauvegarde")
    if nomFichier:
        Fichier = open(nomFichier, "w")
        for droite in Canv.find_all():
            coordon = Canv.coords(droite)
            for point in coordon:
                Fichier.write(str(point)+" ")
            Fichier.write("\n")
        Fichier.close()


def menu_quitter(Root, canv):
    """Fonction associée au boutton quitter du menu"""
    if len(Canv.find_all()) > 0:
        Choix = tk_msgbox.askyesno("Quitter", "Voulez-vous vraiment quitter ?",
                                   icon=tk_msgbox.QUESTION, parent=Root)
        if Choix:
            Root.destroy()
    else:
        Root.destroy()


def ouvrir_aide():
    """ouvre l'aide apres appuie sur le bouton aide"""

    pass


def initialisation_tk():
    """prepare tous les widgets necessaires à l'appli"""
    Root = tk.Tk()
    Canv = tk.Canvas(Root)
    Vstr = tk.StringVar()
    xint = tk.IntVar()
    Label = tk.Label(Root, textvariable=Vstr, bg="sky blue")
    Vstr.set("test")
    xint.set(0)
    Frame = tk.Frame(Root)
    MenuBar = tk.Menubutton(Frame, text="Fichier")
    BoutonAide = tk.Button(Frame)
    return(Root, Canv, Label, MenuBar, Vstr, xint, BoutonAide, Frame)


def configuration_tk(Root, MenuBar, BoutonAide, Canv, Frame, points):
    """modifie les widgets"""
    Root.geometry('800x500')
    Frame.config(borderwidth=1, relief=tk.RAISED)
    Canv.config(bg="white")
    BoutonAide.config(text="Aide", borderwidth=0, command=ouvrir_aide)
    MenuBar.menu = tk.Menu(MenuBar, tearoff=0)
    MenuBar["menu"] = MenuBar.menu
    MenuBar["anchor"] = "w"
    MenuBar.menu.add_command(label="Nouveau",
                             command=lambda: menu_nouveau(Canv, MenuBar))
    MenuBar.menu.add_command(label="Ouvrir",
                             command=lambda: menu_ouvrir(Canv,
                                                         MenuBar, points))
    MenuBar.menu.add_command(label="Sauver", state=tk.DISABLED,
                             command=lambda: menu_sauver(Canv))
    MenuBar.menu.add_command(label="Quitter",
                             command=lambda: menu_quitter(Root, Canv))


def placement_tk(Label, Canv, BoutonAide, Frame):
    """place les widgets sur le canv"""
    Frame.pack(side="top", fill=tk.X)
    MenuBar.pack(side="left")
    BoutonAide.pack(side="right")
    Label.pack(side="bottom", fill=tk.X)
    Canv.pack(fill=tk.BOTH)


def Canv_call(Canv, MenuBar, points):
    """associe tous les callbacks au canvas de base"""
    Canv.bind("<Control-B1-Motion>",
              lambda event: ctrl_click(event, points, MenuBar))
    Canv.bind("<ButtonRelease-1>", lambda event: release_key(event, points))
    Canv.bind_all("<KeyRelease-Control_L>",
                  lambda event: release_key(event, points), add="+")
    Canv.bind_all("<KeyRelease-Control_R>",
                  lambda event: release_key(event, points), add="+")


if __name__ == "__main__":
    points = []
    (Root, Canv, Label, MenuBar,
     Vstr, xint, BoutonAide, Frame) = initialisation_tk()

    configuration_tk(Root, MenuBar, BoutonAide, Canv, Frame, points)
    placement_tk(Label, Canv, BoutonAide, Frame)
    Canv_call(Canv, MenuBar, points)
    Root.mainloop()
