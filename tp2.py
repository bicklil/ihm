import tkinter as tk
import tkinter.filedialog as tk_filedialog
import tkinter.messagebox as tk_msgbox


def couleur_surligne(event):
    """ callback modifiant le trait
    au survol de la souris """
    Canv = event.widget
    droite = Canv.find_withtag("current")[0]
    Vstr.set(droite)
    Canv.itemconfig(droite, fill="red")
    Canv.itemconfig(droite, width=1.5)


def couleur_desurligne(event):
    """ callback remmetant a l'etat initial
    la couleur de la droite si
    la souris s'ecarte du trait"""
    Canv = event.widget
    droite = Canv.find_withtag("current")[0]
    Vstr.set("NULL")
    Canv.itemconfig(droite, fill="black")
    Canv.itemconfig(droite, width=1)


def update_label(event):
    """modifie le label au survol du trait"""
    Canv = event.widget
    droite = Canv.find_withtag("current")[0]


def clean_canv(Canv):
    """fonction qui permet de liberer le canvas"""
    for line in Canv.find_all():
        Canv.delete(line)


def libere_sauv(MenuBar):
    """fonction qui degrise le bouton sauver"""
    MenuBar.menu.entryconfig("Sauver", state="normal")


def bouge_droite(event, points):
    """ bouge la courbe si on a bougé la souris avec
    le click gauche enclenché sur la courbe"""
    if len(points) == 0 and xint.get() != 0:
        Canv = event.widget
        ligne = Canv.find_withtag("current")[0]
        x1 = Canv.coords(ligne)[xint.get()]
        y1 = Canv.coords(ligne)[xint.get()+1]
        X = - x1 + event.x
        Y = - y1 + event.y
        Canv.move(ligne, X, Y)


def click(event):
    """recupere l'indice dans les coordonnées
    de la droite cliqué et la stock dans un intvar()"""
    canv = event.widget
    ligne = Canv.find_withtag("current")[0]
    points = canv.coords(ligne)
    for i in range(0, len(points), 2):
        if points[i]-13 <= event.x <= points[i]+13:
            if points[i+1]-13 <= event.y <= points[i+1]+13:
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


def bouge_text(event, tagarr, tagdep):
    """ il faut tag de depart et tag d'arrive
    on compare pour savoir si on fait +20 ou -20
    """
    text = event.widget
    posdep = text.index(tagdep)
    posarr = text.index(tagarr)
    if text.compare(posdep, ">", posarr):
        posf = str(float(posarr)-20)
        text.mark_set("tempo", posf)
        print(posf)
    else:
        posf = str(float(posarr)+20)
        text.mark_set("tempo", posf)
        print(posf)

    text.see("tempo")
    text.mark_unset("tempo")


def ouvrir_aide(Root):
    """ouvre l'aide apres appuie sur le bouton aide"""
    Fenaide = tk.Toplevel(Root)
    Fenaide.resizable(width=tk.FALSE, height=tk.FALSE)
    text = tk.Text(Fenaide, height=20, width=50)
    text.config(cursor="arrow")
    fichier = open("aide.txt", "r")
    for ligne in fichier:
        text.insert(tk.END, ligne)

    text.tag_config("lien", foreground="blue", underline=1)
    text.mark_set("debut", 1.0)
    text.mark_set("chap1", 24.0)
    text.tag_add("chap1", 2.2, 2.9)
    text.tag_add("lien", 2.2, 2.9)
    text.tag_add("debut", 24.0, 24.4)
    text.tag_add("lien", 24.0, 24.4)
    text.tag_bind("debut", "<ButtonRelease-1>",
                  lambda event: bouge_text(event, "debut", "chap1"), add="+")
    text.tag_bind("chap1", "<ButtonRelease-1>",
                  lambda event: bouge_text(event, "chap1", "debut"), add="+")
    text["state"] = tk.DISABLED
    text.pack()


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
    Root.resizable(width=tk.FALSE, height=tk.FALSE)

    Frame.config(borderwidth=1, relief=tk.RAISED)
    Canv.config(bg="white", height=500, width=800)
    BoutonAide.config(text="Aide",
                      borderwidth=0, command=lambda: ouvrir_aide(Root))
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
