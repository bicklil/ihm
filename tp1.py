import tkinter as tk


def mouse_wheel(event):
    """ callback permettant de modifier
    la position en y du canvas a l'aide de la molette"""
    if event.num == 5:
        pas = 1
    if event.num == 4:
        pas = -1
    event.widget.yview_scroll(pas, tk.UNITS)


def couleur_surligne(event):
    """ callback modifier le contour
    d'un rectangle au survol de la souris """
    Canv = event.widget
    Rect = Canv.find_withtag("current")[0]
    Canv.itemconfig(Rect, outline="red")
    Canv.itemconfig(Rect, width=1.5)


def couleur_desurligne(event):
    """ callback remetant a l'etat initial si
    la souris sort d'un rectangle"""
    Canv = event.widget
    Rect = Canv.find_withtag("current")[0]
    Canv.itemconfig(Rect, outline="black")
    Canv.itemconfig(Rect, width=1)


def click_ok(Lab, Var, TopLevel):
    """ callback sur le click du bouton ok
    permettant de sauvegarder la derniere couleur cliqué
    et de close la fenetre"""
    Var.set(Lab["text"])
    print(Var.get())
    TopLevel.destroy()


def click_annuler(TopLevel):
    """ callback du clique annuler qui ferme la fenetre"""
    TopLevel.destroy()


def clic_couleur(Color,  Lab):
    """ callback apres avoir click sur une couleur
    qui implique une mise a jour du texte"""
    Lab["text"] = Color


def ouvrir_fichier(file):
    """ ouvre un fichier
    si reussi retourne le file descriptor
    si echoue affiche les erreurs d ouverture"""
    try:
        file_open = open(file, "r")
        return file_open
    except OSError as e:
        print("errno: ", e.errno)
        print("filename: ", e.filename)
        print("strerror: ", e.strerror)
        exit()


def parser_rgb(file_open):
    """ recupere a partir du file descriptor toutes les couleurs
    enleve les doublons
    et renvoie un dictionnaire """
    next(file_open)  # on saute la premiere ligne du rgb elle sert a rien
    dico = {}
    # on decompose toutes les lignes sous le format r g b nom
    # puis on ajoute au dico
    for line in file_open:
        linecollapse = line.split()
        # on test si le tuple n'existe pas deja dans le dico
        test = True
        for rgb in dico.values():
            if rgb == (int(linecollapse[0]), int(linecollapse[1]),
                       int(linecollapse[2])):
                test = False
        # s' il existe pas on enleve les espaces du nom
        while len(linecollapse) > 4 and test:
            linecollapse[3] = linecollapse[3]+linecollapse[4]
            del linecollapse[4]
        if test:
            linecollapse[3] = linecollapse[3].lower()
            dico[linecollapse[3]] = (int(linecollapse[0]),
                                     int(linecollapse[1]),
                                     int(linecollapse[2]))
    return dico


def color_alpha(dico):
    """prends le dictionaire de couleur
    mets chaque element dans un tableau
    et on le trie"""
    TabColor = []
    for Color in dico:
        Color = Color[0].upper() + Color[1:]
        i = 1
        # on regarde si la couleur finit par un nombre
        while Color[-i].isdigit():
            i += 1

        if i != 1:  # si on a une fin avec un chiffre on ajoute un espace
            i -= 1
            Color = Color[:-i]+" "+Color[-i:]

        TabColor.append(Color)
    TabColor.sort()
    return TabColor


def bazarre():
    """ fonction a split en plusieur sous fonction"""
    RgbTxt = ouvrir_fichier("/etc/X11/rgb.txt")
    DicoColor = parser_rgb(RgbTxt)
    RgbTxt.close()

    # init de variable
    TabColor = color_alpha(DicoColor)
    NbColor = len(TabColor)
    NbColonne = 18
    NbLigne = (NbColor)/NbColonne
    NbLigne_a_afficher = 10
    CoteCarre = 20
    Ecart = 2
    if NbColor % NbColonne != 0:
        NbLigne += 1

    # initialisation des principaux éléments
    Root = tk.Tk()
    TopLevel1 = tk.Toplevel(Root)
    Var = tk.StringVar()
    Var.set("NULL")
    Canv = tk.Canvas(TopLevel1, width=Ecart+NbColonne * (CoteCarre+Ecart),
                     height=Ecart+NbLigne_a_afficher * (CoteCarre+Ecart),
                     scrollregion=(0, 0, 0,
                     Ecart+NbLigne * (CoteCarre+Ecart)))
    Fram = tk.Frame(TopLevel1)
    Lab = tk.Label(TopLevel1, text=Var.get())
    scroll = tk.Scrollbar(TopLevel1)

    # placement de la premiere couche d'element
    Lab.pack(side="top")
    scroll.pack(side="right", fill=tk.Y)
    # mise en place de la scrollbar
    scroll.config(command=Canv.yview)
    Canv.config(yscrollcommand=scroll.set)
    Canv.pack()
    Fram.pack(side="bottom")

    Boutton = {}  # mise en place des boutons
    for Mesg in ("Ok", "Annuler"):
        Boutton[Mesg] = tk.Button(Fram, text=Mesg)
        Boutton[Mesg].pack(side="left")

    Boutton["Ok"].config(command=lambda: click_ok(Lab, Var, TopLevel1))
    Boutton["Annuler"].config(command=lambda: click_annuler(TopLevel1))
    # mise en place des couleurs dans des rectangles
    # chaque rectangle a comme tag le nom de la couleur et le tag "couleur"
    SquareColor = {}
    indice_ligne = -1
    i = 0
    for Color in sorted(DicoColor.keys()):
        if i == 0:
            indice_ligne += 1
        bg_color = '#{0:02x}{1:02x}{2:02x}'.format(DicoColor[Color][0],
                                                   DicoColor[Color][1],
                                                   DicoColor[Color][2])
        # calcul des coordonnées des rectangles
        x1 = i*CoteCarre + Ecart + i*Ecart
        y1 = Ecart+CoteCarre*indice_ligne + Ecart * indice_ligne
        x2 = (i+1)*CoteCarre + (i+1)*Ecart
        y2 = CoteCarre*(indice_ligne+1) + Ecart * (indice_ligne+1)

        SquareColor[Color] = Canv.create_rectangle(
                                    x1, y1, x2, y2,
                                    fill=bg_color, tags=("couleur", Color))
        # ajout du tag bind pour le click sur une couleur
        Canv.tag_bind(Color, "<Button-1>",
                      lambda event, Color=Color:
                      clic_couleur(Color, Lab))
        Canv.tag_bind(Color, "<Enter>", couleur_surligne)
        Canv.tag_bind(Color, "<Leave>", couleur_desurligne)
        i += 1
        i = i % NbColonne

    Canv.bind("<Button-4>", mouse_wheel)
    Canv.bind("<Button-5>", mouse_wheel)
    TopLevel1.grab_set()
    TopLevel1.focus_set()
    Root.mainloop()


if __name__ == "__main__":
    bazarre()
