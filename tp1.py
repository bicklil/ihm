import tkinter as tk


def ouvrir_fichier(file):
# ouvre un fichier 
#si reussi retourne le file descriptor
#si echoue affiche les erreurs d ouverture 
	try:
		file_open = open(file,"r")
		print("reussi\n")
		return file_open
	except OSError as e:
		print("errno: ",e.errno)
		print("filename: ",e.filename)
		print("strerror: ",e.strerror)
#fermeture du bin crash		()
		
def parser_rgb(file_open):
# recupere a partir du file descriptor toutes les couleurs
#enleve les doublons 
#et renvoie un dictionnaire 
    
    next(file_open) # on saute la premiere ligne du rgb elle sert a rien
    dico = {}
    for line in file_open :
        linecollapse = line.split()
        
        if len(linecollapse) == 5: #on test s'il y a un espace dans le nom de la couleur si oui on l'enleve
            linecollapse[3] = linecollapse[3]+linecollapse[4]
            
        linecollapse[3] = linecollapse[3].lower()
        test = False
        for color in dico: # on regarde si la couleur est pas deja mis
            if color == linecollapse[3] :
                test = True     
                break
                
        if test == False:
            dico[linecollapse[3]] = (int(linecollapse[0]),int(linecollapse[1]),int(linecollapse[2]))
    
    return dico
	
def color_alpha(dico):
#prends le dictionaire de couleur
#mets chaque element dans un tableau
#et on le trie 
    tab_color = []
    for color in dico:
        color = color[0].upper() + color[1:]
        i=1
        while color[-i].isdigit(): # on regarde si la couleur finit par un nombre
            i+=1
            
        if i!=1: #si on a une fin avec un chiffre on ajoute un espace
            i-=1
            color = color[:-i]+" "+color[-i:]
            
        tab_color.append(color)
    tab_color.sort()
    return tab_color



if __name__ == "__main__":
    rgbtxt = ouvrir_fichier("/etc/X11/rgb.txt")
    dico = parser_rgb(rgbtxt)
    tab_couleur = color_alpha(dico)

    root = tk.Tk()
    ftop1 = tk.Toplevel(root)

    var = tk.StringVar()
    
    canv = tk.Canvas(ftop1)
    canv.pack()
    
    fram = tk.Frame(ftop1)
    fram.pack()
    
    boutton = {}
    for mesg in ("Ok","Annuler"):
        boutton[mesg]=tk.Button(fram,text=mesg)
        boutton[mesg].pack(side="left")
    
    
    root.mainloop()
