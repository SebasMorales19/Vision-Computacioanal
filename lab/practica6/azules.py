from tkinter import *
from PIL import Image, ImageTk
import math
import sys
from sys import argv 


def otro_gris(imagen_original):
    #escala de grises
    #toma el valor maximo del rgb de cada pixel
    
    x, y = imagen_original.size
    imagen_gris = Image.new("RGB", (x,y))
    pixeles = []

    for a in range(y):
        for b in range(x):
            r, g, b = imagen_original.getpixel((b, a))
            rgb = (r, g, b)
                #se elige el valor mas grande
            maximo = max(rgb)
            data = (maximo, maximo, maximo)
            pixeles.append(data)
    imagen_gris.putdata(pixeles)
    imagen_gris.save("imagen_gris.png")
    return imagen_gris

def puntos(imagen_original):

    x, y = imagen_original.size
    prueba = imagen_original.load()
    nueva_imagen = imagen_original.copy()
    prueba_nueva = nueva_imagen.load() 
    minimo = int(argv[2])

    #x es el ancho
    #y es la altura
    for i in range(x):
        for j in range(y):	
            pix = []
            for q in [-1, 0, 1]:
                for w in [-1, 0, 1]:
                    if 0 <= i+q  < x and 0 <= j+w  < y: 
                        pix.append(prueba[i+q,j+w][1])
            pix.sort()
            mediana= len(pix)/2
            
            if len(pix)%2 == 0:
                med=(pix[int(mediana)]+pix[int(mediana-1)])/2
            else:
                med=pix[int(mediana)] 
            med = math.trunc(med)
            prueba_nueva[i,j] = (med,med,med)
    
    for i in range(x):
        for j in range(y):
            otro= prueba_nueva[i,j][1]-prueba[i,j][1]
            if otro < 0:
                otro = 0
            if otro > 255:
                otro = 255
            if otro > minimo:
                prueba[i,j]= (otro,otro,otro)
            else:
                prueba[i,j]=(0,0,0)
            print(otro)
    lista = []
    for i in range(x):
        for j in range(y):
            if imagen_original.getpixel((i,j))!=(255,0,0) and imagen_original.getpixel((i,j))!=(0,0,0):
                lista.append(( imagen_original, (255,0,0)))
    
    imagen_original.save('esquina.png')	
    return imagen_original



#def toma_pix(imagen_original):
 #   x, y = imagen_original.size
  #  prueba2 = imagen_original.load()
  #  nueva_imagen2 = Image.new("RGB", (x,y))
    
   # lista = []
   # for i in range(x):
    #    for j in range(y):
     #       if imagen_original.getpixel((i,j))!=(0,255,0) and imagen_original.getpixel((i,j))!=(0,0,0):
      #          lista.append(imagen_original, (0,255,0))
    #return lista, imagen_

#def pinta():
 #   points = toma_pix(imagen_original)
  #  coords = []
   # for lista in points:
    #    coords.append(max(lista))
    #algo = centros([coords])
    #print algo
    #grados = {}
    #for coord in coords:
     #   dx = algo[0][0] - coord[0]
      #  dy = algo[0][1] - coord[1]
       # rads = math.atan2(-dy,dx)
        #rads %= 2*math.pi
        #gr = math.degrees(rads)
        #grados.update({gr:coord})




def main():
    """funcion principal
    """
    try:
        imagen_inicial = sys.argv[1]
        #print imagen_inicial
        imagen_original = Image.open(imagen_inicial)
        imagen_original = imagen_original.convert('RGB')
    except:
        print("selecciona la imagen")
        return
    imagen_b = otro_gris(imagen_original)
    nueva = puntos(imagen_b)
    

if __name__ == "__main__":
    main()



