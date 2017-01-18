import tkinter as tk


def ouvrir_fichier(file):
    """ ouvre un fichier
    si reussi retourne le file descriptor
    si echoue affiche les erreurs d ouverture"""
    try:
        file_open = open(file, "r")
        print("reussi\n")
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
    for line in file_open:
        linecollapse = line.split()
# on test s'il y a un espace dans le nom de la couleur si oui on l'enleve
        if len(linecollapse) == 5:
            linecollapse[3] = linecollapse[3]+linecollapse[4]

        linecollapse[3] = linecollapse[3].lower()
        test = False
        for color in dico:  # on regarde si la couleur est pas deja mis
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
    tab_color = color_alpha(dico_color)
    nbr_color = len(tab_color)
    print(nbr_color)
    nbr_colonne = 18
    nb_ligne = 1+(nbr_color)/nbr_colonne

    root = tk.Tk()
    ftop1 = tk.Toplevel(root)
    var = tk.StringVar()
    canv = tk.Canvas(ftop1)
    fram = tk.Frame(ftop1)
    lab = tk.Label(ftop1, text=var)

    lab.pack(side="top")
    canv.pack()
    fram.pack(side="bottom")

    boutton = {}
    for mesg in ("Ok", "Annuler"):
        boutton[mesg] = tk.Button(fram, text=mesg)
        boutton[mesg].pack(side="left")

    square_color = {}
    canv_ligne = {}
    indice_ligne = -1
    i = 0
    for color in dico_color:
        if i == 0:
            indice_ligne += 1
            canv_ligne[indice_ligne] = tk.Canvas(canv, height=20)
            canv_ligne[indice_ligne].pack(side="top")
        bg_color = '#{0:02x}{1:02x}{2:02x}'.format(dico_color[color][0],
                                                   dico_color[color][1],
                                                   dico_color[color][2])
        square_color[color] = canv_ligne[indice_ligne].create_rectangle(
                                    i*20+5, 5, i*20+25, 25,
                                    fill=bg_color, tags=("couleur", color))
        i += 1
        i = i % nbr_colonne

    root.mainloop()
