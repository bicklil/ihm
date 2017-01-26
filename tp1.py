import tkinter as tk
import getopt
import sys


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


def resize_fen(event, NbLigne, NbLigne_affiche, NbColonne, ecart, Canv):
    TopLevel1 = event.widget
    largeur = event.width
    hauteur = event.height
    if hauteur > 149:
        TopLevel1.unbind("<Configure>")
        Canv["height"] = hauteur - 50
        Canv["width"] = largeur
        larg_rect = (largeur-16-(ecart*(NbColonne+1)))/NbColonne
        haut_rect = (hauteur-50-(ecart*(NbLigne_affiche+1)))/NbLigne_affiche
        Canv["scrollregion"] = (0, 0, 0, Ecart+NbLigne * (haut_rect+Ecart))
        indice_ligne = -1
        i = 0
        for rect in Canv.find_all():
            if i == 0:
                indice_ligne += 1
            x1 = i*larg_rect + Ecart + i*Ecart
            y1 = Ecart+haut_rect*indice_ligne + Ecart * indice_ligne
            x2 = (i+1)*larg_rect + (i+1)*Ecart
            y2 = haut_rect*(indice_ligne+1) + Ecart * (indice_ligne+1)
            Canv.coords(rect, x1, y1, x2, y2)
            i += 1
            i = i % NbColonne
        TopLevel1.update()
        TopLevel1.bind("<Configure>",
                       lambda event: resize_fen(event, NbLigne,
                                                NbLigne_affiche,
                                                NbColonne, Ecart, Canv))


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


def usage():
    """texte a afficher avec l'option -h ou --help dans le terminal"""
    print("executable affichant les couleurs associées au rgb.txt")
    print("\n-h ,--help : affiche l'aide")
    print("-d ,--default : garde les valeurs par defaut")
    print("--colonne= : modifie le nombre de colonne de carre a l'ecran")
    print("--ecart= : modifie l'ecart entre les carrés")
    print("--ligne= : modifie le nombre de ligne a afficher")
    print("--cote= : modifie la longeur des cotés des carrés")


def recuperation_arg():
    """recupere les arguments sur la ligne de commande"""
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hd", ["help", "colonne=",
                                                        "ecart=", "default",
                                                        "ligne=", "cote="])
    except getopt.GetoptError as err:
        print(err)
        print("essayez avec -h pour plus d'informations")
        sys.exit(2)
    # valeur par defaut
    Ecart = 2
    colonne = 18
    Ligne = 10
    CoteCarre = 20
    for opt, arg in opts:
        if opt in ("-d", "--default"):
            return (Ecart, colonne, Ligne, CoteCarre)
        elif opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt == "--ecart":
            print(arg)
            if arg.isdigit():
                Ecart = int(arg)
            else:
                print("ecart doit etre un int")
                sys.exit(3)
        elif opt == "--colonne":
            if arg.isdigit():
                colonne = int(arg)
            else:
                print("colonne doit etre un int")
                sys.exit(3)
        elif opt == "--ligne":
            if arg.isdigit():
                Ligne = int(arg)
            else:
                print("ligne doit etre un int")
                sys.exit(3)
        elif opt == "--cote":
            if arg.isdigit():
                CoteCarre = int(arg)
            else:
                print("cote doit etre un int")
                sys.exit(3)
        else:
            assert False, "unhandled option"

    return (Ecart, colonne, Ligne, CoteCarre)


def init_variable():
    """recupere toutes les données necessaire au fonctionnement du prog"""
    (Ecart, NbColonne, NbLigne_a_afficher, CoteCarre) = recuperation_arg()
    RgbTxt = ouvrir_fichier("/etc/X11/rgb.txt")
    DicoColor = parser_rgb(RgbTxt)
    RgbTxt.close()

    TabColor = color_alpha(DicoColor)
    NbColor = len(TabColor)
    NbLigne = (NbColor)/NbColonne

    return (DicoColor, NbColonne, NbLigne,
            NbLigne_a_afficher, CoteCarre, Ecart)


def tk_init(Ecart, NbColonne, NbLigne, NbLigne_a_afficher, CoteCarre):
    """cree toute les instances de widget necessaire"""
    Root = tk.Tk()
    TopLevel1 = tk.Toplevel(Root)
    TopLevel1.minsize(width=Ecart+NbColonne * (10+Ecart)+16,
                      height=Ecart+NbLigne_a_afficher * (10+Ecart)+28)
    TopLevel1.maxsize(width=Ecart+NbColonne * (30+Ecart)+16,
                      height=Ecart+NbLigne_a_afficher * (30+Ecart)+28)
    Var = tk.StringVar()
    Var.set("NULL")
    Canv = tk.Canvas(TopLevel1, width=Ecart+NbColonne * (CoteCarre+Ecart),
                     height=Ecart+NbLigne_a_afficher * (CoteCarre+Ecart),
                     scrollregion=(0, 0, 0,
                     Ecart+NbLigne * (CoteCarre+Ecart)))
    Fram = tk.Frame(TopLevel1)
    Lab = tk.Label(TopLevel1, text=Var.get())
    Scroll = tk.Scrollbar(TopLevel1)
    Boutton = {}
    for Mesg in ("Ok", "Annuler"):
        Boutton[Mesg] = tk.Button(Fram, text=Mesg)

    return (TopLevel1, Canv, Fram, Lab, Scroll, Var, Root, Boutton)


def tk_placement_topLevel(Lab, Scroll, Canv, Fram, Boutton):
    """place les widget sur la TopLevel"""
    Lab.pack(side="top")
    Scroll.pack(side="right", fill=tk.Y)
    Canv.pack(side="top")
    Fram.pack(side="top", expand=True)
    Boutton["Ok"].pack(side="left")
    Boutton["Annuler"].pack(side="left")


def config_widget(Scroll, Canv, Boutton, Lab, TopLevel1, Var):
    """ lie la scrollbar et le canvas
    lie les boutons a leur fonction respective
    lie la molette au scroll"""
    Scroll.config(command=Canv.yview)
    Canv.config(yscrollcommand=Scroll.set)
    Tl_width = TopLevel1.winfo_width()
    Tl_height = TopLevel1.winfo_height()
    size = [Tl_width, Tl_height]
    Boutton["Ok"].config(command=lambda: click_ok(Lab, Var, TopLevel1))
    Boutton["Annuler"].config(command=lambda: click_annuler(TopLevel1))
    Canv.bind("<Button-4>", mouse_wheel)
    Canv.bind("<Button-5>", mouse_wheel)


def creation_carre(DicoColor, CoteCarre, Ecart, Lab,
                   NbColonne, NbLigne_a_afficher, TopLevel1):
    """mise en place des couleurs dans des rectangles
    chaque rectangle a comme tag le nom de la couleur et le tag "couleur"
    association des events avec les tags"""
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

        # ajout des fonctions surlignagne du carre au survol de la souris
        Canv.tag_bind(Color, "<Enter>", couleur_surligne)
        Canv.tag_bind(Color, "<Leave>", couleur_desurligne)
        i += 1
        i = i % NbColonne
    TopLevel1.update()
    TopLevel1.bind("<Configure>", lambda event: resize_fen(event, NbLigne,
                                                           NbLigne_a_afficher,
                                                           NbColonne, Ecart,
                                                           Canv))


if __name__ == "__main__":
    (DicoColor, NbColonne, NbLigne,
     NbLigne_a_afficher, CoteCarre, Ecart) = init_variable()

    (TopLevel1, Canv, Fram,
     Lab, Scroll, Var, Root, Boutton) = tk_init(Ecart, NbColonne, NbLigne,
                                                NbLigne_a_afficher, CoteCarre)

    tk_placement_topLevel(Lab, Scroll, Canv, Fram, Boutton)
    config_widget(Scroll, Canv, Boutton, Lab, TopLevel1, Var)

    creation_carre(DicoColor, CoteCarre, Ecart, Lab,
                   NbColonne, NbLigne_a_afficher, TopLevel1)

    TopLevel1.grab_set()
    TopLevel1.focus_set()

    Root.mainloop()
