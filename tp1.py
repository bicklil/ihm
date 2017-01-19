import tkinter as tk


def clic_couleur(event, color, var, lab):
    """ callback apres avoir click sur une couleur
    qui implique une mise a jour du texte"""
    var.set(color)
    lab["text"] = var.get()


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
    # on decompose toutes lse lignes sous le format r g b nom
    # puis on ajoute au dico
    for line in file_open:
        linecollapse = line.split()
        # on test s'il y a un espace dans le nom de la couleur
        while len(linecollapse) > 4:
            linecollapse[3] = linecollapse[3]+linecollapse[4]
            del linecollapse[4]

        linecollapse[3] = linecollapse[3].lower()
        test = False
        for color in dico:  # on regarde si la couleur est pas deja mise
            if color == linecollapse[3]:
                test = True
                break

        if not test:
            dico[linecollapse[3]] = (int(linecollapse[0]),
                                     int(linecollapse[1]),
                                     int(linecollapse[2]))

    return dico


def color_alpha(dico):
    """prends le dictionaire de couleur
    mets chaque element dans un tableau
    et on le trie"""
    tab_color = []
    for color in dico:
        color = color[0].upper() + color[1:]
        i = 1
        # on regarde si la couleur finit par un nombre
        while color[-i].isdigit():
            i += 1

        if i != 1:  # si on a une fin avec un chiffre on ajoute un espace
            i -= 1
            color = color[:-i]+" "+color[-i:]

        tab_color.append(color)
    tab_color.sort()
    return tab_color


if __name__ == "__main__":
    rgbtxt = ouvrir_fichier("/etc/X11/rgb.txt")
    dico_color = parser_rgb(rgbtxt)
    rgbtxt.close()

    # init de variable
    tab_color = color_alpha(dico_color)
    nb_color = len(tab_color)
    nb_colonne = 14
    nb_ligne = (nb_color)/nb_colonne
    nb_ligne_a_afficher = 10
    if nb_color % nb_colonne != 0:
        nb_ligne += 1

    # initialisation des principaux éléments
    root = tk.Tk()
    ftop1 = tk.Toplevel(root)
    var = tk.StringVar()
    var.set("NULL")
    canv = tk.Canvas(ftop1, width=10+nb_colonne * 20,
                     height=10+nb_ligne_a_afficher*20,
                     scrollregion=(0, 0, 10+nb_colonne*20, 10+nb_ligne*20))
    fram = tk.Frame(ftop1)
    lab = tk.Label(ftop1, text=var.get())
    scroll = tk.Scrollbar(ftop1)

    # placement de la premiere couche d'element
    lab.pack(side="top")
    scroll.pack(side="right", fill=tk.Y)
    # mise en place de la scrollbar
    scroll.config(command=canv.yview)
    canv.config(yscrollcommand=scroll.set)
    canv.pack()
    fram.pack(side="bottom")

    boutton = {}  # mise en place des boutons
    for mesg in ("Ok", "Annuler"):
        boutton[mesg] = tk.Button(fram, text=mesg)
        boutton[mesg].pack(side="left")

    # mise en place des couleurs dans des rectangles
    # chaque rectangle a comme tag le nom de la couleur et le tag "couleur"
    square_color = {}
    canv_ligne = {}
    indice_ligne = -1
    i = 0
    for color in dico_color:
        if i == 0:
            indice_ligne += 1
        bg_color = '#{0:02x}{1:02x}{2:02x}'.format(dico_color[color][0],
                                                   dico_color[color][1],
                                                   dico_color[color][2])
        square_color[color] = canv.create_rectangle(
                                    i*20+5, 5+20*indice_ligne,
                                    i*20+25, 25+20*indice_ligne,
                                    fill=bg_color, tags=("couleur", color))
        # ajout du tag bind pour le click sur une couleur
        canv.tag_bind(color, "<Button-1>",
                      lambda event, color=color:
                      clic_couleur(0, color, var, lab))
        i += 1
        i = i % nb_colonne

    root.mainloop()
