


def ouvrir_fichier(file):
	try:
		file_open = open(file,"r")
		print("reussi\n")
		return file_open
	except OSError as e:
		print("errno: ",e.errno)
		print("filename: ",e.filename)
		print("strerror: ",e.strerror)
		
def parser_rgb(file_open):
    
    next(file_open)
    dico = {}
    for line in file_open :
        linecollapse = line.split()
        
        if len(linecollapse) == 5:
            linecollapse[3] = linecollapse[3]+linecollapse[4]
            
        linecollapse[3] = linecollapse[3].lower()
        test = False
        for color in dico:
            if color == linecollapse[3] :
                test = True
                break
                
        if test == False:
            dico[linecollapse[3]] = (int(linecollapse[0]),int(linecollapse[1]),int(linecollapse[2]))
    
    return dico
	
def color_alpha(dico):
    tab_color = []
    for color in dico:
        color = color[0].upper() + color[1:]
        i=1
        while color[-i].isdigit():
            i+=1
            
        if i!=1: #on a une fin avec un chiffre
            i-=1
            color = color[:-i]+" "+color[-i:]
            
        tab_color.append(color)
    tab_color.sort()
    return tab_color




rgbtxt = ouvrir_fichier("/etc/X11/rgb.txt")
dico = parser_rgb(rgbtxt)
print(color_alpha(dico))
		
